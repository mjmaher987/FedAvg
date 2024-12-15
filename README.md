# FedAvg
Implement the FedAvg from Scratch

## Overview
This project implements a Federated Learning system based on the Federated Averaging (FedAvg) algorithm. It includes functionalities for training models locally on multiple clients, aggregating their updates on a central server, and evaluating the global model on a test dataset.

## Code Functionality

### Data Loading
**Function:** `load_data`  
- **Purpose:** Splits a dataset (CIFAR10 or MNIST) among a specified number of clients in either a uniform or non-uniform manner.  
- **Inputs:**
  - `dataset`: Dataset to load (`'CIFAR10'` or `'MNIST'`).
  - `num_clients`: Number of clients to split the data among.
  - `data_split`: Strategy for splitting data (`'uniform'` or `'non-uniform'`).
- **Outputs:** List of `torch.utils.data.Subset` objects for each client.

### Neural Network
**Class:** `SimpleCNN`  
- **Purpose:** Defines a simple convolutional neural network for image classification tasks.  
- **Architecture:**
  - Two convolutional layers with ReLU activation and max pooling.
  - Two fully connected layers for classification.
- **Inputs:**
  - `input_channels`: Number of input channels (default: 1).
  - `num_classes`: Number of output classes (default: 10).
- **Outputs:** Logits (un-normalized scores) for each class.

### Model Aggregation
**Function:** `FedAvg`  
- **Purpose:** Averages the state dictionaries of client models to create a global model.  
- **Inputs:**
  - `state_dicts`: List of state dictionaries from client models.
- **Outputs:** Averaged state dictionary for the global model.

### Local Training
**Function:** `train_client`  
- **Purpose:** Trains a client model locally on its subset of the dataset.  
- **Inputs:**
  - `client_model`: Model to be trained.
  - `train_loader`: DataLoader for the client's training data.
  - `criterion`: Loss function.
  - `optimizer`: Optimization algorithm.
  - `epochs`: Number of local training epochs (default: 5).
- **Outputs:** Updated state dictionary of the client model after training.

### Global Model Evaluation
**Function:** `evaluate_model`  
- **Purpose:** Evaluates the global model on a test dataset.  
- **Inputs:**
  - `model`: Model to evaluate.
  - `test_loader`: DataLoader for the test dataset.
- **Outputs:** Accuracy of the model on the test dataset (percentage).

### Federated Learning Algorithm
**Function:** `federated_learning`  
- **Purpose:** Implements the full Federated Learning pipeline.  
- **Steps:**
  1. Loads and splits data among clients.
  2. Initializes the global model.
  3. Trains local models on clients for multiple rounds.
  4. Aggregates client models using FedAvg.
  5. Evaluates the global model on the test dataset after each round.  
- **Inputs:**
  - `num_clients`: Number of clients participating.
  - `dataset`: Dataset to use (`'CIFAR10'` or `'MNIST'`).
  - `model_architecture`: Model class for client and global models (default: `SimpleCNN`).
  - `num_rounds`: Number of training rounds.
  - `local_epochs`: Number of epochs for local training.
  - `learning_rate`: Learning rate for optimizers.
  - `batch_size`: Batch size for training and testing.
  - `datasplit`: Strategy for splitting data (`'uniform'` or `'non-uniform'`).
- **Outputs:** Trained global model.

## Usage

### Running the Code
Run the script with command-line arguments to customize the Federated Learning setup:
```bash
python script.py --lr <learning_rate> --epoch <local_epochs> --num_clients <num_clients> --num_rounds <num_rounds> --batch_size <batch_size> --data_split <data_split>


## References

- **diagrams.net (formerly draw.io)**  
  Available at: [https://www.drawio.com/](https://www.drawio.com/) (Accessed: 2024-12-09)

- Sarkar, S., Agrawal, S., Baker, T., Maddikunta, P. K. R., & Gadekallu, T. R. (2022).  
  *Catalysis of neural activation functions: Adaptive feed-forward training for big data applications*.  
  Applied Intelligence, 52(12), 13364–13383. Springer.

- McMahan, B., Moore, E., Ramage, D., Hampson, S., & y Arcas, B. A. (2017).  
  *Communication-efficient learning of deep networks from decentralized data*.  
  In *Artificial Intelligence and Statistics* (pp. 1273–1282). PMLR.

