import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip # pip3 install moviepy
# NEED : sudo apt install ffmpeg


from montage_script.audio_processing.audio_montage import get_audio_from_video
from montage_script.audio_processing.tools import *
from montage_script.video_processing.subtitles import add_impression_txt, add_invisible_text
from montage_script.video_processing.video_montage import create_blurred_vid, get_vid_duration, cut_excess_video, merge_vid, mute_video_at_interval


def tiktok_react_montage(original_vid_path, impr_audio_file_path, final_vid_file_path, impression_txt):
    # CREATES THE FIRST PART WITH THE IMPRESSION ON BLURRED BACKGROUND
    # produces "_blurred.mp4" and "_blurred_cutted.mp4"
    blurred_vid_path = create_blurred_vid(original_vid_path, get_audio_duration_mp3(impr_audio_file_path))
    #put text on the video
    impression_blurred_text_vid_path =  original_vid_path.split(".")[0] + "_text_final.mp4"
    add_impression_txt(blurred_vid_path, impr_audio_file_path, impression_txt, impression_blurred_text_vid_path)
    #produces "_blurred_with_sound.mp4"
    impression_blurred_text_sound_vid_path = impression_blurred_text_vid_path.split(".")[0] + "_with_sound.mp4"
    montage_aud_vid(impr_audio_file_path, impression_blurred_text_vid_path, impression_blurred_text_sound_vid_path)
    
    # the video has some sound at the end of it and i don't know why so i mute the endz
    impression_blurred_text_sound_fixed_vid_path = mute_video_at_interval(impression_blurred_text_sound_vid_path, get_audio_duration_mp3(impr_audio_file_path), get_vid_duration(impression_blurred_text_sound_vid_path))

    # CREATE SECOND PART (RESYNCRONIZATION BC ORIGINAL IS FUCKED FOR SOME REASON)
    syncronized_vid_path = syncronize_original_vid(original_vid_path)
    syncronized_vid_path_cutted = syncronized_vid_path.split(".")[0] + "_cutted.mp4"

    # 0.4 is very random but it is very much working
    cut_excess_video(syncronized_vid_path, 0, get_vid_duration(syncronized_vid_path) - 0.4, syncronized_vid_path_cutted)

    # add noise to the video to hope to not be shadow banned for unoriginal content ?
    syncronized_vid_path_cutted_noisy = syncronized_vid_path_cutted.split(".")[0] + "_noisy.mp4"
    add_invisible_text(syncronized_vid_path_cutted, syncronized_vid_path_cutted_noisy)

    # MERGES BOTH VIDEOS TOGETHER
    merge_vid([impression_blurred_text_sound_fixed_vid_path, syncronized_vid_path_cutted_noisy], final_vid_file_path)


def funny_story_montage(vids_paths, impr_audio_file_path, final_vid_file_path, impression_txt):
    # #make final long video
    tmp_merged_file = vids_paths[0].split(".")[0] + "_allvid_merged.mp4"
    merge_vid(vids_paths, tmp_merged_file)
    #put text on the video
    tmp_merge_with_text_path = tmp_merged_file.split(".")[0] + "_with_text.mp4"
    add_impression_txt(tmp_merged_file, impr_audio_file_path, impression_txt, tmp_merge_with_text_path)
    # put sound of impression on video
    montage_aud_vid(impr_audio_file_path, tmp_merge_with_text_path, final_vid_file_path)

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


def montage_aud_vid(aud_path, vid_path, output_path):
    audio_clip = AudioFileClip(aud_path)
    video_clip = VideoFileClip(vid_path)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path)

    return output_path

