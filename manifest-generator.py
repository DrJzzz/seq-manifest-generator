import os
import sys
import re
import csv

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def main():
    # Validate command line arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    
    
    # Is path valid?
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    # Dir name
    dir_name = re.search(r'[^/]+(?=/$|$)', directory_path).group(0)
    print(f"Directory name: {dir_name}")
    
    # List all files in the directory, ignoring hidden files
    file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and not f.startswith('.')]
    file_names.sort(key=natural_sort_key)

    # Clean the names
    names = [f.split('.')[0] for f in file_names]
    cleaned_names = [f.split('_')[0] for f in names]
    cleaned_names.sort(key=natural_sort_key)
    
    
    abs_paths = [None] * len(file_names)

    for i in range(len(file_names)):
        abs_paths[i] = "$PWD/" + dir_name + "/" + file_names[i]

    print(f"Absolute paths: {abs_paths}")
        
    
    directions = [None] * len(file_names)
    
    names.sort(key=natural_sort_key)
    names = [name for name in names if name]
   
    for i in range(len(names)):
        if names[i][-1] == '1':
            directions[i] = "forward"
        elif names[i][-1] == '2':
            directions[i] = "reverse"
            
    
    # Create a CSV file
    csv_name = f"{dir_name}_manifest.csv"
    manifest_path = os.path.join(directory_path, csv_name)
    with open(manifest_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["sample-id", "absolute-filepath", "direction"])  # Column names
        for i in range(len(names)):
            csv_writer.writerow([cleaned_names[i], abs_paths[i], directions[i]])  # Use names, abs_paths, and directions

    print(f"Manifest created at: {manifest_path}")
            

if __name__ == "__main__":
    main()
