import os
import subprocess
import sys
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips # pip3 install moviepy
# NEED : sudo apt install ffmpeg
from montage_script.vad import get_voice_time
from os import path


def make_montage(video_file_path, audio_file_path, artefact_file_path):

    # separation audio from video in tiktok downloaded clip
    video_path_attr = video_file_path.split(".") #[0] name, [1] extension
    video_audio_name = video_path_attr[0] + "_video_sound.mp3"
    convert_video_to_audio_ffmpeg(video_file_path, video_audio_name)

    time_to_cut = get_voice_time(video_audio_name)
    print("time_to_cut", time_to_cut)

    # video_clip = VideoFileClip(video_file_path)
    # audio_clip = AudioFileClip(audio_file_path)

    # final_clip = video_clip.set_audio(audio_clip)
    # final_clip.write_videofile(artefact_file_path)


def convert_video_to_audio_ffmpeg(video_file, video_audio_name):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, video_audio_name], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    
# from pydub import AudioSegment 
  
# song = AudioSegment.from_mp3("test.mp3")
# # pydub does things in milliseconds 
# ten_seconds = 10 * 1000
  
# first_10_seconds = song[:ten_seconds] 
  
# last_5_seconds = song[-5000:] 

# first_10_seconds.export("new.mp3", format="mp3") 