import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips # pip3 install moviepy
# NEED : sudo apt install ffmpeg
from montage_script.audio_montage import create_final_audio, get_audio_from_video
from montage_script.video_montage import create_blurred_vid, merge_vid, cut_excess_video, get_vid_duration, alternative_merge_vid
from montage_script.vad import get_audio_duration_mp3
from pydub import AudioSegment
import subprocess
import math

def make_montage(original_vid_path, impr_audio_file_path, final_vid_file_path, impression_txt):
    # CREATES THE FIRST PART WITH THE IMPRESSION ON BLURRED BACKGROUND
    blurred_vid_path = create_blurred_vid(original_vid_path, get_audio_duration_mp3(impr_audio_file_path))
    blurred_text_vid_path = add_impression_txt(blurred_vid_path, impression_txt)
    impression_blurred_text_vid_path = montage_blurred_impression(impr_audio_file_path, blurred_text_vid_path)
    
    # the end of the video is often fucked so we cut a bit of it
    impression_blurred_text_vid_cutted_path = impression_blurred_text_vid_path.split(".")[0] + "_cutted.mp4"
    cut_excess_video(impression_blurred_text_vid_path, 0, get_vid_duration(impression_blurred_text_vid_path) - 0.4, impression_blurred_text_vid_cutted_path)
    
    # CREATE SECOND PART (RESYNCRONIZATION BC ORIGINAL IS FUCKED FOR SOME REASON)
    syncronized_vid_path = syncronize_original_vid(original_vid_path)
    syncronized_vid_path_cutted = syncronized_vid_path.split(".")[0] + "_cutted.mp4"
    cut_excess_video(syncronized_vid_path, 0, get_vid_duration(syncronized_vid_path) - 0.4, syncronized_vid_path_cutted)

    # MERGES BOTH VIDEOS TOGETHER
    merge_vid([impression_blurred_text_vid_cutted_path, syncronized_vid_path_cutted], final_vid_file_path)
    
    # REMOVES ALL TMP FILES
    remove_files_starting_with(original_vid_path.split(".")[0] + '_')

def add_impression_txt(vid_path, impression_txt):
    # get the nb of cut to make to the video
    nb_cut_vid_todo = math.floor(len(impression_txt.split()) / 6)
    # print("len(impression_txt.split()): ", len(impression_txt.split()))
    # print("nb_cut_vid_todo: ", nb_cut_vid_todo)
    if nb_cut_vid_todo != 0:
        impr_txt_divided = split_string(impression_txt, nb_cut_vid_todo)

    vid_original_duration = get_vid_duration(vid_path)
    each_segment_duration = vid_original_duration / nb_cut_vid_todo
    # print("each_segment_duration: ", each_segment_duration)
    all_parts_path = []
    final_vid_path = vid_path.split(".")[0] + "_blurred_text_no_voice.mp4"
    # cut the video x nb of times
    if nb_cut_vid_todo > 1:
        for i in range(0, nb_cut_vid_todo):
            cut_start = i * each_segment_duration
            cut_end = (i + 1) * each_segment_duration
            # print("cut_start:" , cut_start)
            # print("cut_end: ", cut_end)
            part_name = vid_path.split(".")[0] + "_blurred_part_" + str(i) + ".mp4"
            cut_excess_video(vid_path, cut_start, cut_end, part_name)
            part_name_with_text = part_name.split(".")[0] + "_text.mp4"
            put_text_on_vid(impr_txt_divided[i], part_name, part_name_with_text)
            all_parts_path.append(part_name_with_text)
        
        alternative_merge_vid(all_parts_path, final_vid_path)
    else:
        put_text_on_vid(impr_txt_divided[0], vid_path, final_vid_path)
    
    return final_vid_path

    


    # final_file = vid_path.split(".")[0] + "_blurred_with_text.mp4"
    # put_text_on_vid(impression_txt, vid_path, final_file)



def put_text_on_vid(text, input_file_path, output_file_path, x="center"):
    if x == "center":
        w = "(w-text_w)/2"
        h = "(h-text_h)/2 + 120"
    elif x == "left":
        w = "10"
        h = "h - 30"
    else:
        w = "0"
        y = "0"
    
    nb_cut_text = len(text.split()) / 4
    # print("nb_cut_text: ", nb_cut_text)
    impr_txt_divided = split_string_evenly(text, nb_cut_text)
    impr_txt_divided = make_txt_centered(impr_txt_divided)
    text = "\n\n".join(impr_txt_divided)

    default_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font_file = "fonts/CONSOLAB.TTF"
    command = [
        "ffmpeg",
        "-loglevel", "quiet",
        "-y",
        "-i", input_file_path,
        "-vf", f'drawtext=fontfile={font_file}:text={text}:fontcolor=white:fontsize=30:box=1:boxcolor=black@0.5:boxborderw=15:x={w}:y={h}',
        "-codec:a", "copy",
        "-max_muxing_queue_size", "9999",
        output_file_path
    ]

    # print("command: ", command)

    result = subprocess.run(command)

    if result.returncode == 0:
        print("Command executed successfully!")
    else:
        print("Command failed!")

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

        # print("list_text[i]: ", list_text[i])
        # print("size_str: ", size_str)
        # print("size_longest_str: ", size_longest_str)

        # print("nb_of_space: ", nb_of_space)
        # print("new_str: ", new_str)

        new_list_text.append(new_str)
    
    return new_list_text

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
        out.append(' '.join(words[int(last):int(last + avg)]))
        last += avg

    return out

def text_bottom_left():
    os.system("""ffmpeg -i merola.mp4 -vf drawtext="fontfile=/path/to/font.ttf: \
    text={text}: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: \
    boxborderw=5: x=0: y=h-30" -codec:a copy output.mp4""")


def syncronize_original_vid(vid_path):
    # getting the audio
    audio_extract_original_video_path_mp3 = vid_path.split(".")[0] + "_video_sound.mp3"
    get_audio_from_video(vid_path, audio_extract_original_video_path_mp3)

    audio = AudioSegment.from_mp3(audio_extract_original_video_path_mp3)
    silence = AudioSegment.silent(duration=400)

    merged_audio = silence + audio

    new_audio_path = vid_path.split(".")[0] + "_new_audio.mp3"
    merged_audio.export(new_audio_path, format="wav")

    video_clip = VideoFileClip(vid_path)
    audio_clip = AudioFileClip(new_audio_path)

    final_clip = video_clip.set_audio(audio_clip)

    syncronized_vid_path = vid_path.split(".")[0] + "_syncronised.mp4"
    final_clip.write_videofile(syncronized_vid_path)

    return syncronized_vid_path


def montage_blurred_impression(impr_audio_file_path, blurred_vid_path):
    video_clip = VideoFileClip(blurred_vid_path)
    audio_clip = AudioFileClip(impr_audio_file_path)

    # print("audio_clip.duration: ", audio_clip.duration)
    # print("video_clip.duration: ", video_clip.duration)

    final_clip_path = impr_audio_file_path.split(".")[0] + "_blurred_final.mp4"
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_clip_path)

    return final_clip_path


def remove_files_starting_with(dir_and_prefix):
    dir_and_prefix = dir_and_prefix.split("/")
    for filename in os.listdir(dir_and_prefix[0]):
        if filename.startswith(dir_and_prefix[1]):
            filepath = os.path.join(dir_and_prefix[0], filename)
            os.remove(filepath)
