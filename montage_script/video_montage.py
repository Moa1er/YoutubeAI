import subprocess
from moviepy import editor
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def create_final_video(vid_file_path, target_vid_duration, actual_vid_duration):
    if target_vid_duration < actual_vid_duration:
        return vid_file_path
    
    # takes the video.mp4 and blurs it name is %usual_blabla%_blur_part.mp4
    blur_vid_filename = blur_video(vid_file_path)
    target_blurred_vid_duration = target_vid_duration - actual_vid_duration

    print("target_blurred_vid_duration: ", target_blurred_vid_duration)
    final_blurred_vid_filname = blur_vid_filename.split(".")[0] + "_cutted.mp4"
    if target_blurred_vid_duration < actual_vid_duration:
        cut_excess_video(blur_vid_filename, target_blurred_vid_duration, final_blurred_vid_filname)
    else:
        repeat_blurred_vid(blur_vid_filename, target_blurred_vid_duration, actual_vid_duration, final_blurred_vid_filname)
    final_video_filename = vid_file_path.split(".")[0] + "_final.mp4"
    merge_vid([final_blurred_vid_filname, vid_file_path], final_video_filename)
    return final_video_filename

def repeat_blurred_vid(vid_file_path, duration_wanted, duration_vid, output_filname):
    nb_repeat = int(duration_wanted // duration_vid)
    rest_duration = duration_wanted % duration_vid
    cutted_vid_filename = vid_file_path.split(".")[0] + "_cutted_tmp.mp4"
    if rest_duration != 0:
        cut_excess_video(vid_file_path, rest_duration, cutted_vid_filename)
    tmp_merged_vid_filename = vid_file_path.split(".")[0] + "_merged.mp4"
    merge_vid([vid_file_path] * nb_repeat, tmp_merged_vid_filename)
    if rest_duration != 0:
        merge_vid([tmp_merged_vid_filename, cutted_vid_filename], output_filname)
    

def merge_vid(video_clip_paths, output_path):
    # create VideoFileClip object for each video file
    clips = [editor.VideoFileClip(c) for c in video_clip_paths]
    final_clip = editor.concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_path)

def cut_excess_video(vid_file_path, cut_duration, output_filname):
    ffmpeg_extract_subclip(vid_file_path, 0, cut_duration, targetname=output_filname)

def blur_video(vid_file_path):
    blur_vid_filename = vid_file_path.split(".")[0] + "_blur_part.mp4"
    command = [
        "ffmpeg",
        "-y",
        "-i", vid_file_path,
        "-vf", "boxblur=10",
        "-c:a", "copy",
        blur_vid_filename
    ]

    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if result.returncode == 0:
        print("Command executed successfully!")
    else:
        print("Command failed!")

    return blur_vid_filename
