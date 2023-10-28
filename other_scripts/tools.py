import os 

def read_firs_line_and_del(file_path):
    # Open the file and read all lines into a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Write the remaining lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines[1:])
    
    return lines[0].strip()


def remove_files_starting_with(dir, prefix):
    for filename in os.listdir(dir):
        if filename.startswith(prefix):
            filepath = os.path.join(dir, filename)
            os.remove(filepath)