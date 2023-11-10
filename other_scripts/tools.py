import os 
import send2trash

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
            send2trash(filepath)

def save_info(
        artefacts_file_name,
        video_file_path,
        impression_file_path,
        trend_keyword,
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
        f.write("artefacts_file_name:\n")
        f.write(artefacts_file_name + "\n")
        f.write("video_file_path:\n")
        f.write(video_file_path + "\n")
        f.write("impression_file_path:\n")
        f.write(impression_file_path + "\n")
        f.write("trend_keyword:\n")
        f.write(trend_keyword + "\n")
        f.write("vid_title:\n")
        f.write(vid_title + "\n")
        f.write("vid_url:\n")
        f.write(vid_url + "\n")
        f.write("aweme_id:\n")
        f.write(aweme_id + "\n")
        f.write("impression:\n")
        f.write(impression + "\n")
        f.write("impression_cleaned:\n")
        f.write(impression_cleaned + "\n")
        f.write("new_vid_title:\n")
        f.write(new_vid_title + "\n")
        f.write("tags:\n")
        f.write(" ".join(tags) + "\n")
        f.write("category_id:\n")
        f.write(category_id + "\n")
        f.write("description:\n")
        f.write(description + "\n")
        f.write("comments:\n")
        f.write(joined_comments + "\n")

def load_info(info_file_path):
    with open(info_file_path, "r") as f:
        f.readline()
        artefacts_file_name = f.readline().replace("\n", "")
        f.readline()
        video_file_path = f.readline().replace("\n", "")
        f.readline()
        impression_file_path = f.readline().replace("\n", "")
        f.readline()
        trend_keyword = f.readline().replace("\n", "")
        f.readline()
        vid_title = f.readline().replace("\n", "")
        f.readline()
        vid_url = f.readline().replace("\n", "")
        f.readline()
        aweme_id = f.readline().replace("\n", "")
        f.readline()
        impression = f.readline().replace("\n", "")
        f.readline()
        impression_cleaned = f.readline().replace("\n", "")
        f.readline()
        new_vid_title = f.readline().replace("\n", "")
        f.readline()
        tags = f.readline().replace("\n", "").split(" ")
        f.readline()
        category_id = f.readline().replace("\n", "")
        f.readline()
        description = f.readline().replace("\n", "")
        f.readline()
        joined_comments = f.readline().replace("\n", "")
    return artefacts_file_name, video_file_path, impression_file_path, trend_keyword, vid_title, vid_url, aweme_id,impression, impression_cleaned, new_vid_title,tags, category_id, description, joined_comments