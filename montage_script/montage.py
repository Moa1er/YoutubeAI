import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips # pip3 install moviepy

def make_montage(video_file_path, audio_file_path, artefact_file_path):
    video_clip = VideoFileClip(video_file_path)
    audio_clip = AudioFileClip(audio_file_path)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(artefact_file_path)