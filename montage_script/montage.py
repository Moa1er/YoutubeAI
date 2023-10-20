import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip # pip3 install moviepy
# NEED : sudo apt install ffmpeg


from montage_script.audio_processing.audio_montage import get_audio_from_video
from montage_script.audio_processing.tools import *
from montage_script.video_processing.subtitles import add_impression_txt
from montage_script.video_processing.video_montage import create_blurred_vid, get_vid_duration, cut_excess_video, merge_vid, mute_video_at_interval


def make_montage(original_vid_path, impr_audio_file_path, final_vid_file_path, impression_txt):
    # CREATES THE FIRST PART WITH THE IMPRESSION ON BLURRED BACKGROUND
    # produces "_blurred.mp4" and "_blurred_cutted.mp4"
    blurred_vid_path = create_blurred_vid(original_vid_path, get_audio_duration_mp3(impr_audio_file_path))
    #put text on the video
    impression_blurred_text_vid_path = add_impression_txt(blurred_vid_path, impr_audio_file_path, impression_txt)
    #produces "_blurred_with_sound.mp4"
    impression_blurred_text_sound_vid_path = montage_blurred_impression(impr_audio_file_path, impression_blurred_text_vid_path)
    
    # the video has some sound at the end of it and i don't know why so i mute the end (-0.3 bc we need it ok?)
    impression_blurred_text_sound_fixed_vid_path = mute_video_at_interval(impression_blurred_text_sound_vid_path, get_audio_duration_mp3(impr_audio_file_path), get_vid_duration(impression_blurred_text_sound_vid_path))

    # CREATE SECOND PART (RESYNCRONIZATION BC ORIGINAL IS FUCKED FOR SOME REASON)
    syncronized_vid_path = syncronize_original_vid(original_vid_path)
    syncronized_vid_path_cutted = syncronized_vid_path.split(".")[0] + "_cutted.mp4"
    # 0.4 is very random but it is very much working
    cut_excess_video(syncronized_vid_path, 0, get_vid_duration(syncronized_vid_path) - 0.4, syncronized_vid_path_cutted)

    # MERGES BOTH VIDEOS TOGETHER
    merge_vid([impression_blurred_text_sound_fixed_vid_path, syncronized_vid_path_cutted], final_vid_file_path)
    
    # REMOVES ALL TMP FILES
    remove_files_starting_with(original_vid_path.split(".")[0] + '_')


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

    final_clip_path = impr_audio_file_path.split(".")[0] + "_blurred_with_sound.mp4"
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_clip_path)

    return final_clip_path


def remove_files_starting_with(dir_and_prefix):
    dir_and_prefix = dir_and_prefix.split("/")
    for filename in os.listdir(dir_and_prefix[0]):
        if filename.startswith(dir_and_prefix[1]):
            filepath = os.path.join(dir_and_prefix[0], filename)
            os.remove(filepath)
