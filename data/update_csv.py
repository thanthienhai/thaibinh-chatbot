import pandas as pd

# Load the CSV file
file_path = "merged_chunks.csv"  # Replace with your file path
df = pd.read_csv(file_path)

# Add 'm_' prefix to the 'id' column
df['id'] = df['id'].apply(lambda x: f"m_{x}")

# Save the updated DataFrame back to CSV
output_file = "updated_chunks_with_m.csv"
df.to_csv(output_file, index=False)

print(f"Updated file with 'm_' prefix added to 'id' saved as '{output_file}'.")