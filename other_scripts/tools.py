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

def save_info(
        vid_title,
        vid_url,
        aweme_id,
        impression, 
        impression_cleaned, 
        new_vid_title, 
        joined_comments,
        tags, 
        category_id, 
        description,
        file_output_path
    ):
    with open(file_output_path, "w") as f:
        f.write("vid_title: " + vid_title + "\n")
        f.write("vid_url: " + vid_url + "\n")
        f.write("aweme_id: " + aweme_id + "\n")
        f.write("impression: " + impression + "\n")
        f.write("impression_cleaned: " + impression_cleaned + "\n")
        f.write("new_vid_title: " + new_vid_title + "\n")
        f.write("tags: " + " ".join(tags) + "\n")
        f.write("category_id: " + category_id + "\n")
        f.write("description: " + description + "\n")
        f.write("comments: " + joined_comments + "\n")