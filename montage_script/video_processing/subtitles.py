import subprocess
import math
from montage_script.audio_processing.tools import get_word_timestamp
import re
import random

def add_impression_txt(vid_path, aud_path, text, output_path):
    # get the timestamps of each word in the aud_impression_file
    word_timestamps = get_word_timestamp(aud_path)

    # get the nb of cut to make to the video
    nb_cut_vid_todo = math.floor(len(text.split()) / 6)
    if nb_cut_vid_todo != 0:
        impr_txt_divided = split_string(text, nb_cut_vid_todo)

    return run_text_command(
        vid_path, 
        create_command_filters(create_word_timings(impr_txt_divided, word_timestamps)),
        output_path
    )


def create_word_timings(text, word_timestamps):
    if(len(word_timestamps) < len(text[0][0].split())):
        print("len(word_timestamps): ",  len(word_timestamps))
        print("word_timestamps: ", word_timestamps)
        print("len(text[0][0].split()): ", len(text[0][0].split()))
        print("text: ", text)
    #format of text is :
    # [(("this is a long very long string"), 7), (("this is another long very long string haha"), 8)]
    word_timings = []
    idx_pos_text = 0
    for i in range(0, len(text)):
        word_timings.append(("",0,0))
        nb_cut_text = len(text[i][0].split()) / 3.5
        # format of text_to_display_part is :
        # ["this is a long very",  "long string"]
        text_to_display_part = split_string_evenly(text[i][0], nb_cut_text)
        #we make the text centered on the screen
        text_to_display_part = make_txt_centered(text_to_display_part)
        #we add line return to not have overlapping on the screen
        text_to_display_part = [s + "\n\n" for s in text_to_display_part]
        for j in range(0, len(text_to_display_part)):
            # we separate each word while making sure that we leaves the spaces
            # used to make the text centered
            ttd_words = split_str_one_space(text_to_display_part[j])
            for k in range(0, len(ttd_words)):
                if(idx_pos_text >= len(word_timestamps)):
                    print("ERROR WATCH THIS")
                    print("idx_pos_text: ", idx_pos_text)
                    print("len(word_timestamps): ", len(word_timestamps))
                    print("word_timestamps: ", word_timestamps)
                    print("text: ", text)
                    print("text_to_display_part: ", text_to_display_part)
                    print("ttd_words: ", ttd_words)
                    print("len(ttd_words): ", len(ttd_words))
                    print("k: ", k)
                    print("len(ttd_words[k]): ", len(ttd_words[k]))
                    print("ttd_words[k]: ", ttd_words[k])
                    idx_pos_text += 1
                    continue
                # the function "split_str_one_space" introduces some empty string
                # so if we find one we ignore it 
                if(ttd_words[k] == ''):
                    continue
                word_timings.append((ttd_words[k], *(word_timestamps[idx_pos_text])))
                idx_pos_text += 1
    return word_timings

def create_command_filters(word_timings):
    font_size = 40
    font_file = "fonts/CONSOLAB.TTF"
    w = "(w-text_w)/2"
    h = "(h-text_h)/2 + 200"
    filters = []
    text_to_display_tot = []
    for word, start_time, end_time in word_timings:
        if (word, start_time, end_time) == ("", 0, 0):
            text_to_display_tot = []
            continue
        text_to_display_tot.append(word)
        filter_string = f"drawtext=fontfile={font_file}:text='{(' '.join(text_to_display_tot))}':x={w}:y={h}:fontsize={font_size}:fontcolor=white:enable='between(t,{start_time},{end_time})':borderw=3:bordercolor=black"
        filters.append(filter_string)

    return filters


def run_text_command(video_path, filters, output_path):
    filter_complex = ','.join(filters)

    command = [
        "ffmpeg", 
        "-y", 
        "-loglevel", "quiet", 
        "-i", video_path, 
        "-vf", filter_complex, 
        "-c:a", "copy", 
        output_path
    ]
    subprocess.run(command)

    return output_path
    # old command just in case 
    #     command = [
    #         "ffmpeg",
    #         "-loglevel", "quiet",
    #         "-y",
    #         "-i", input_file_path,
    #         "-vf", f'drawtext=fontfile={font_file}:text={text}:fontcolor=white:fontsize=30:box=1:boxcolor=black@0.5:boxborderw=15:x={w}:y={h}',
    #         "-codec:a", "copy",
    #         "-max_muxing_queue_size", "9999",
    #         output_file_path
    #     ]


def make_txt_centered(list_text):
    idx_longest_str, longest_str = max(enumerate(list_text), key=lambda x: len(x[1]))
    size_longest_str = len(longest_str)

    new_list_text = []
    for i in range(0, len(list_text)):
        if idx_longest_str:
            new_list_text.append(list_text[i])
            continue
        size_str = len(list_text[i])
        size_diff = size_longest_str - size_str
        nb_of_space = 0
        if size_diff < 2:
            nb_of_space = 0
        else:
            nb_of_space = int(size_diff / 2)
        new_str = " " * nb_of_space + list_text[i]

        new_list_text.append(new_str)
    
    return new_list_text

def split_str_one_space(s):
    return re.split(r'(?<! ) (?! )', s)

def split_string_evenly(text, parts):
    words = text.split()
    avg_length = len(text) // parts
    substrings = []
    current_length = 0
    current_words = []
    
    for word in words:
        if current_length + len(word) > avg_length and current_words:
            substrings.append(' '.join(current_words))
            current_words = []
            current_length = 0
        
        current_length += len(word) + 1  # 1 for the space
        current_words.append(word)
        
    # Add the last remaining words if there are any
    if current_words:
        substrings.append(' '.join(current_words))

    return substrings

def split_string(text, x):
    words = text.split()
    avg = len(words) / x
    out = []
    last = 0.0
    
    while last < len(words):
        out.append(((' '.join(words[int(last):int(last + avg)])), len(words)))
        last += avg

    return out