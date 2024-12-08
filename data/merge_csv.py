import pandas as pd

# Initialize an empty DataFrame for merging
merged_df = pd.DataFrame()

# Loop through files from 1 to 8, skipping 5
for i in range(1, 9):
    if i == 5:
        continue
    # Construct the file path for the current CSV file
    csv_file_path = f"{i}_chunks.csv"
    
    try:
        # Read the current CSV file
        df = pd.read_csv(csv_file_path)
        
        # Add 'm_' prefix and file number to the 'id' column
        df['id'] = df['id'].apply(lambda x: f"m_{i}file_{x}")
        
        # Append the current dataframe to the merged dataframe
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    except FileNotFoundError:
        print(f"File {csv_file_path} not found. Skipping...")
    except Exception as e:
        print(f"Error processing file {csv_file_path}: {e}")

# Save the merged DataFrame to a new CSV file
merged_df.to_csv("merged_chunks.csv", index=False)
print("Merged CSV file saved as 'merged_chunks.csv'.")