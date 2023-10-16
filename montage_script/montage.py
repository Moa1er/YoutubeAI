import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips # pip3 install moviepy
# NEED : sudo apt install ffmpeg
from montage_script.audio_montage import create_final_audio
from montage_script.video_montage import create_final_video
from montage_script.vad import get_audio_duration

def make_montage(assets_folder_path, vid_file_path, impr_audio_file_path, artefact_file_path):
    final_audio_path, audio_extract_original_video_path = create_final_audio(vid_file_path, impr_audio_file_path)
    print("final_audio_path: ", final_audio_path)
    print("audio_extract_original_video_path: ", audio_extract_original_video_path)

    print("get_audio_duration(final_audio_path): ", get_audio_duration(final_audio_path))
    print("get_audio_duration(vid_full_audio_path): ", get_audio_duration(audio_extract_original_video_path))

    final_vid_path = create_final_video(vid_file_path, get_audio_duration(final_audio_path), get_audio_duration(audio_extract_original_video_path))

    video_clip = VideoFileClip(final_vid_path)
    audio_clip = AudioFileClip(final_audio_path)

    print("audio_clip.duration: ", audio_clip.duration)
    print("video_clip.duration: ", video_clip.duration)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(artefact_file_path)

    # delete tmp files
    # prefix_files_to_rm = vid_file_path.split(".")[0].replace(assets_folder_path, "").replace("/", "")
    # remove_files_starting_with(assets_folder_path, prefix_files_to_rm)
    

def remove_files_starting_with(directory, prefix):    
    for filename in os.listdir(directory):
        if filename.startswith(prefix):
            filepath = os.path.join(directory, filename)
            os.remove(filepath)
