import os
import pandas as pd

# Directory containing the .out files
input_directory = r"C:\Users\mjmah\OneDrive\Desktop\everything\Main\AfterAll\0-Canada\Term1\3-Special Topics\Project\outputs"

# Get a list of all .out files in the directory
out_files = [f for f in os.listdir(input_directory) if f.endswith(".out")]

# Iterate over each .out file
for file_name in out_files:
    file_path = os.path.join(input_directory, file_name)
    
    data = {}  # To store extracted parameters
    accuracies = []  # To store accuracy values
    time_spent = None  # To store time spent

    with open(file_path, "r") as file:
        lines = file.readlines()

    # Extract data
    for line in lines:
        line = line.strip()
        if line.startswith("Number of Clients"):
            data["Number of Clients"] = int(line.split(":")[1].strip())
        elif line.startswith("Number of Rounds"):
            data["Rounds"] = int(line.split(":")[1].strip())
        elif line.startswith("Learning Rate"):
            data["Learning Rate"] = float(line.split(":")[1].strip())
        elif line.startswith("Batch Size"):
            data["Batch Size"] = int(line.split(":")[1].strip())
        elif line.startswith("Dataset"):
            data["Dataset"] = line.split(":")[1].strip()
        elif line.startswith("Test Accuracy Global Model"):
            accuracies.append(float(line.split(":")[1].strip().strip('%')))
        elif line.startswith("Time taken"):
            time_spent = float(line.split(":")[1].strip().split()[0])  # Extract the time in seconds

    # Add accuracies to the data dictionary
    data["Accuracies"] = accuracies
    data["Time Spent (s)"] = time_spent
    
    # Create a DataFrame for rounds and accuracies, along with the extracted parameters
    df = pd.DataFrame({
        "Round": list(range(1, len(data["Accuracies"]) + 1)),
        "Accuracy": data["Accuracies"]
    })

    # Add the static parameters to each row in the DataFrame
    for key, value in data.items():
        if key != "Accuracies":
            df[key] = value

    # Generate the output CSV file name based on the input .out file
    csv_file_name = os.path.splitext(file_name)[0] + ".csv"
    output_csv_path = os.path.join(input_directory, csv_file_name)

    # Save the DataFrame to the corresponding CSV file
    df.to_csv(output_csv_path, index=False)

    print(f"Saved: {output_csv_path}")
