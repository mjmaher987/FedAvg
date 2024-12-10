# -*- coding: utf-8 -*-
"""Federated_Learning-10272024-1755.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uHQUwZMM_AT7RKt6F5KdhJYiMThjJ7dA

# Federated Learning (FedAvg)
- Mohammadjavad Maheronnaghsh

## Approach 1: From Scratch
"""

# Libraries
# !pip install torch torchvision

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import numpy as np
from torch.utils.data import DataLoader, random_split, Subset
from collections import OrderedDict
import copy
import argparse
import time



# Data
def load_data(dataset='CIFAR10', num_clients=10, data_split='uniform'):
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    if dataset == 'CIFAR10':
        trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    elif dataset == 'MNIST':
        trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)

    data_size = len(trainset)
    indices = np.arange(data_size)
    np.random.shuffle(indices)

    client_data = []
    if data_split == 'uniform':
        # Split dataset equally
        print('Uniform data split')
        split_size = data_size // num_clients
        for i in range(num_clients):
            client_indices = indices[i*split_size:(i+1)*split_size]
            client_data.append(Subset(trainset, client_indices))
    else:
        # Non-uniform distribution
        print('None-Uniform data split')
        split_sizes = np.random.dirichlet(np.ones(num_clients), size=1)[0]
        split_sizes = (split_sizes * data_size).astype(int)
        for i, split_size in enumerate(split_sizes):
            client_indices = indices[:split_size]
            client_data.append(Subset(trainset, client_indices))
            indices = indices[split_size:]

    return client_data

# Network
class SimpleCNN(nn.Module):
    def __init__(self, input_channels=1, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# FedAvg
def FedAvg(state_dicts):
    avg_state_dict = OrderedDict()
    for key in state_dicts[0].keys():
        avg_state_dict[key] = torch.stack([state_dict[key].float() for state_dict in state_dicts], 0).mean(0)
    return avg_state_dict

# Client Train
def train_client(client_model, train_loader, criterion, optimizer, epochs=5):
    # print(train_loader.shape)
    client_model.train()
    for epoch in range(epochs):
        for inputs, labels in train_loader:
            # print('R')
            inputs, labels = inputs.cuda(), labels.cuda()
            # print(f'inputs: {inputs.shape}')
            optimizer.zero_grad()
            outputs = client_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    return client_model.state_dict()

# Evaluation of the global model
def evaluate_model(model, test_loader):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.cuda(), labels.cuda()
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    return accuracy

# Federated Learning Algorithm
def federated_learning(num_clients, dataset='CIFAR10', model_architecture=SimpleCNN, num_rounds=10, 
                       local_epochs=5, learning_rate=0.01, batch_size=10, datasplit='uniform'): 
    # Load client data
    client_data = load_data(dataset=dataset, num_clients=num_clients, datasplit=datasplit)


    if dataset == 'CIFAR10':
        test_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=test_transform)
    elif dataset == 'MNIST':
        test_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
        testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=test_transform)

    print('------')
    print('------')
    print(f"Number of Clients: {num_clients}")
    print(f"Number of Rounds: {num_rounds}")
    print(f"Local Epochs: {local_epochs}")
    print(f"Learning Rate: {learning_rate}")
    print(f"Batch Size: {batch_size}")
    print(f"Dataset: {dataset}")
    print(f"Data Split: {datasplit}")
    print('------')
    print('------')


    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=False)

    # Initialize global model
    global_model = model_architecture(input_channels=3).cuda()
    print(global_model)
    global_state_dict = global_model.state_dict()

    criterion = nn.CrossEntropyLoss()

    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}/{num_rounds}")

        client_state_dicts = []
        for client_idx in range(num_clients):
            # Load client data and create model
            client_model = model_architecture(input_channels=3).cuda()
            client_model.load_state_dict(global_state_dict)

            train_loader = DataLoader(client_data[client_idx], batch_size=batch_size, shuffle=True)
            optimizer = optim.SGD(client_model.parameters(), lr=learning_rate)

            # Train the client model locally
            client_state_dict = train_client(client_model, train_loader, criterion, optimizer, epochs=local_epochs)
            client_state_dicts.append(copy.deepcopy(client_state_dict))

        # Aggregate client models on the server
        global_state_dict = FedAvg(client_state_dicts)
        global_model.load_state_dict(global_state_dict)

        test_accuracy = evaluate_model(global_model, test_loader)
        print(f"Test Accuracy Global Model: {test_accuracy:.2f}%")
        print('------')

    return global_model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lr', type=float, default=0.01, help='Learning rate')
    parser.add_argument('--epoch', type=int, default=5, help='Number of epochs')
    parser.add_argument('--num_clients', type=int, default=10, help='Number of clients')
    parser.add_argument('--num_rounds', type=int, default=1000, help='Number of rounds')
    parser.add_argument('--batch_size', type=int, default=10, help='Batch size')
    parser.add_argument('--data_split', type=str, default='uniform', help='Data split')
    args = parser.parse_args()

    num_clients = args.num_clients
    num_rounds = args.num_rounds
    local_epochs = args.epoch
    learning_rate = args.lr
    batch_size = args.batch_size
    dataset = 'CIFAR10'

    start_time = time.time()

    final_global_model = federated_learning(
        num_clients=num_clients, 
        dataset=dataset, 
        num_rounds=num_rounds,
        local_epochs=local_epochs,
        learning_rate=learning_rate,
        batch_size=batch_size,
        datasplit=args.data_split)
    
    # torch.save(final_global_model.state_dict(), 'fedavg_global_model.pth')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

"""Ideas:
- If a client has not found a good thing, do not share it! We can measure it by local model's performance, etc.
- If a local model is doing well, do not receive data, because it is doing good!
- Models send more data about their loss, accurac, worst group accuracy, etc.
- Check heterogenousity, fairness, etc.
- Implement all other models on different datasets.
"""
