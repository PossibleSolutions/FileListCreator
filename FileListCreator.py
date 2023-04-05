import os
from datetime import datetime

# Get the directory of the current Python file
dir_path = os.path.dirname(__file__)

# List of excluded file extensions
excluded_extensions = ['.cpg', '.dbf', '.prj', '.shx', 'qmd','.gdbindexes', '.gdbtable', '.gdbtablx', '.atx', '.spx', 'timestamps', '.sbn', '.sbx', '.xml', '.freelist']

# Create a dictionary to hold the file paths grouped by file type
file_dict = {}

# Walk through the directory and its subfolders
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # Check if the file extension is not in the excluded extensions list
        if not any(file.endswith(ext) for ext in excluded_extensions):
            file_path = os.path.join(root, file)
            mod_time = os.path.getmtime(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            file_type = os.path.splitext(file_path)[1].lower()
            if file_type not in file_dict:
                file_dict[file_type] = []
            file_dict[file_type].append((file_path, mod_time, file_size))

# Sort the file paths by modification time
for file_type, file_list in file_dict.items():
    file_dict[file_type] = sorted(file_list, key=lambda x: x[1], reverse=True)

# Create a new text file in the same directory with a timestamp in the name
now = datetime.now()
output_file_name = 'file_list_{}.txt'.format(now.strftime('%Y_%m_%d'))
output_file_path = os.path.join(dir_path, output_file_name)
output_file = open(output_file_path, 'w')

# Write the file paths, modification dates, and sizes to the text file, one per line
for file_type, file_list in file_dict.items():
    output_file.write('{}\n'.format(file_type))
    for file_path, mod_time, file_size in file_list:
        output_file.write('  {} ({}, {:.2f} MB)\n'.format(file_path, datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d'), file_size))
    output_file.write('\n')  # Add an empty line after the group of files


# Close the output file
output_file.close()

# Print a message to confirm that the file list has been written to the text file
print('File list written to {}'.format(output_file_path))