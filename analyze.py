import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory containing the .csv files
input_directory = r"..."

# Function to extract the batch size, clients, or learning rate from the filename
def extract_metric_from_filename(file_name):
    if "lr_" in file_name:
        # Extract learning rate from filenames like lr_0_0001.out
        return df['Learning Rate'].iloc[0]
        # return float(file_name.split('_')[1].replace('.csv', ''))
    elif "epoch_" in file_name:
        # Extract epoch number from filenames like epoch_50.out
        return int(file_name.split('_')[1].replace('.csv', ''))
    elif "batch_" in file_name:
        # Extract batch size from filenames like batch_128.out
        return int(file_name.split('batch_')[1].replace('.csv', ''))
    elif "clients_" in file_name:
        # Extract number of clients from filenames like clients_1000.out
        return int(file_name.split('_')[1].replace('.csv', ''))
    elif "round_" in file_name:
        return int(file_name.split('_')[1].replace('.csv', ''))
    else:
        return None

# Get a list of all .csv files in the directory
csv_files = [f for f in os.listdir(input_directory) if f.endswith(".csv")]

# Initialize dictionaries to store data for each metric
lr_data = []  # For learning rate effect
epoch_data = []  # For epoch effect
batch_data = []  # For batch size effect
clients_data = []  # For number of clients effect
rounds_data = []  # For number of rounds effect
time_data = []

# Iterate over each CSV file and extract data
for file_name in csv_files:
    file_path = os.path.join(input_directory, file_name)
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Extract the metric (learning rate, epoch, batch size, or clients)
    metric = extract_metric_from_filename(file_name)
    # print(metric)
    

    
    # Extract the relevant data (accuracy and time)
    if 'Accuracy' in df.columns and 'Time Spent (s)' in df.columns:
        # avg_accuracy = df['Accuracy'].mean()  # Average accuracy across rounds
        avg_accuracy = df['Accuracy'].iloc[-1]
        total_time = df['Time Spent (s)'].iloc[-1]  # Time spent (last entry in the file)
        
        # Categorize by metric
        if "lr_" in file_name:
            lr_data.append((metric, avg_accuracy, total_time))
        elif "epoch_" in file_name:
            epoch_data.append((metric, avg_accuracy, total_time))
            time_data.append((f'Epoch: {metric}', avg_accuracy, total_time))
        elif "batch_" in file_name:
            batch_data.append((metric, avg_accuracy, total_time))
            time_data.append((f'Batch Size: {metric}', avg_accuracy, total_time))
        elif "clients_" in file_name:
            clients_data.append((metric, avg_accuracy, total_time))
            time_data.append((f'Client: {metric}', avg_accuracy, total_time))
        elif "round_" in file_name:
            rounds_data.append((metric, avg_accuracy, total_time))
            time_data.append((f'Round: {metric}', avg_accuracy, total_time))

print(time_data)
time_df = pd.DataFrame(time_data, columns=["Parameter", "Value", "Training Time (s)"])

# Sort the data for better readability
time_df = time_df.sort_values(by=["Parameter", "Value"])
print(time_df)



# Convert the lists to DataFrames
lr_df = pd.DataFrame(lr_data, columns=["Learning Rate", "Accuracy", "Time Spent (s)"])
epoch_df = pd.DataFrame(epoch_data, columns=["Epoch", "Accuracy", "Time Spent (s)"])
batch_df = pd.DataFrame(batch_data, columns=["Batch Size", "Accuracy", "Time Spent (s)"])
clients_df = pd.DataFrame(clients_data, columns=["Number of Clients", "Accuracy", "Time Spent (s)"])
rounds_df = pd.DataFrame(rounds_data, columns=["Number of Rounds", "Accuracy", "Time Spent (s)"])

# Plot the results
import matplotlib.pyplot as plt
lr_df = lr_df.sort_values(by="Learning Rate")
epoch_df = epoch_df.sort_values(by="Epoch")
batch_df = batch_df.sort_values(by="Batch Size")
clients_df = clients_df.sort_values(by="Number of Clients")
rounds_df = rounds_df.sort_values(by="Number of Rounds")
# Create a figure and the first x-axis
# print(lr_df)
# print(epoch_df)
fig, ax1 = plt.subplots(figsize=(10, 10))

# Plot Learning Rate vs Accuracy on the first x-axis
ax1.plot(lr_df["Learning Rate"], lr_df["Accuracy"], label="Learning Rate", marker='o', alpha=0.7, color='blue')
ax1.set_xlabel("Learning Rate", fontsize=22, color='blue')
ax1.tick_params(axis='x', labelcolor='blue')
ax1.set_ylabel("Accuracy", fontsize=22)
# ax1.set_title("Effects of Various Parameters on Accuracy", fontsize=14)

# Create a second x-axis for Epoch
ax2 = ax1.twiny()  # Create a new x-axis
ax2.plot(epoch_df["Epoch"], epoch_df["Accuracy"], label="Epoch", marker='s', alpha=0.7, color='green')
ax2.set_xlabel("Epoch", fontsize=22, color='green')
ax2.tick_params(axis='x', labelcolor='green')

# Create a third x-axis for Batch Size
ax3 = ax1.twiny()  # Add another x-axis
ax3.spines['top'].set_position(('outward', 50))  # Move it outward to avoid overlap
ax3.plot(batch_df["Batch Size"], batch_df["Accuracy"], label="Batch Size", marker='^', alpha=0.7, color='black')
ax3.set_xlabel("Batch Size", fontsize=22, color='black')
ax3.tick_params(axis='x', labelcolor='black')

# Create a fourth x-axis for Number of Clients
ax4 = ax1.twiny()
ax4.spines['top'].set_position(('outward', 100))  # Move it outward to avoid overlap
ax4.plot(clients_df["Number of Clients"], clients_df["Accuracy"], label="Number of Clients", marker='x', alpha=0.7, color='purple')
ax4.set_xlabel("Number of Clients", fontsize=22, color='purple')
ax4.tick_params(axis='x', labelcolor='purple')

# Create a fifth x-axis for Number of Rounds
ax5 = ax1.twiny()
ax5.spines['top'].set_position(('outward', 150))  # Move it outward to avoid overlap
ax5.plot(rounds_df["Number of Rounds"], rounds_df["Accuracy"], label="Number of Rounds", marker='D', alpha=0.7, color='red')
ax5.set_xlabel("Number of Rounds", fontsize=22, color='red')
ax5.tick_params(axis='x', labelcolor='red')

# Add grid and legends
ax1.grid(True)
plt.tight_layout()
plt.show()

# plt.figure(figsize=(10, 6))
# # plt.subplot(2, 3, 1)
# plt.scatter(lr_df["Learning Rate"], lr_df["Accuracy"], marker='o', label='Accuracy')
# plt.xlabel("Learning Rate")
# plt.ylabel("Accuracy")
# plt.title("Effect of Learning Rate on Accuracy")
# plt.xscale('log')  # Log scale for better visualization
# plt.grid(True)
# plt.tight_layout()
# plt.show()



# # plt.subplot(2, 3, 2)
# plt.scatter(epoch_df["Epoch"], epoch_df["Accuracy"], marker='o', label='Accuracy')
# plt.xlabel("Epoch")
# plt.ylabel("Accuracy")
# plt.title("Effect of Epoch on Accuracy")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # print(batch_df)
# # plt.subplot(2, 3, 3)
# plt.scatter(batch_df["Batch Size"], batch_df["Accuracy"], label='Accuracy')
# plt.xlabel("Batch Size")
# plt.ylabel("Accuracy")
# plt.title("Effect of Batch Size on Accuracy")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # plt.subplot(2, 3, 4)
# plt.scatter(clients_df["Number of Clients"], clients_df["Accuracy"], label='Accuracy')
# plt.xlabel("Number of Clients")
# plt.ylabel("Accuracy")
# plt.title("Effect of # of Clients on Accuracy")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # plt.subplot(2, 3, 5)
# plt.scatter(rounds_df["Number of Rounds"], rounds_df["Accuracy"], label='Accuracy')
# plt.xlabel("Number of Rounds")
# plt.ylabel("Accuracy")
# plt.title("Effect of # of Rounds on Accuracy")
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# Save the results as CSV files for further analysis if needed
# lr_df.to_csv(os.path.join(input_directory, "learning_rate_analysis.csv"), index=False)
# epoch_df.to_csv(os.path.join(input_directory, "epoch_analysis.csv"), index=False)
# batch_df.to_csv(os.path.join(input_directory, "batch_size_analysis.csv"), index=False)
# clients_df.to_csv(os.path.join(input_directory, "clients_analysis.csv"), index=False)

print("Analysis complete. Results saved to CSV files.")
