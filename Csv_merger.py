import csv

def merge_csv_files(file1, file2, output_file):
    # Read the contents of the first CSV file
    with open(file1, 'r', encoding='utf-8') as file1_handle:
        reader1 = csv.reader(file1_handle)
        data1 = list(reader1)

    # Read the contents of the second CSV file
    with open(file2, 'r', encoding='utf-8') as file2_handle:
        reader2 = csv.reader(file2_handle)
        data2 = list(reader2)

    # Merge the data
    merged_data = data1 + data2

    # Write the merged data to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as output_handle:
        writer = csv.writer(output_handle)
        writer.writerows(merged_data)

    print(f"Merged data saved to {output_file}")

# Example usage
file1 = "merged6(6).csv"  # Replace with the path to your first CSV file
file2 = "cleaned-hastag-Demonetisation.csv"  # Replace with the path to your second CSV file
output_file = "merged7(7).csv"  # Replace with the desired path for the merged CSV file

merge_csv_files(file1, file2, output_file)
