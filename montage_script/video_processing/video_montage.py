import subprocess
from moviepy import editor
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import json


def create_blurred_vid(vid_file_path, audio_duration):
    # we blur the default vid
    blurred_vid_path = blur_video(vid_file_path)
    #we take the duration of this video
    blurred_vid_duration = get_vid_duration(blurred_vid_path)

    output_path = blurred_vid_path.split(".")[0] + "_cutted.mp4"
    if audio_duration > blurred_vid_duration:
        make_blurred_vid_longer(blurred_vid_path, blurred_vid_duration, audio_duration, output_path)
    else:
        # print("blurred_vid_path: ", blurred_vid_path)
        # print("output_path: ", output_path)
        # we add 1 seconde so that it doesn't cut too fast
        cut_excess_video(blurred_vid_path, 0, audio_duration, output_path)
    return output_path

def make_blurred_vid_longer(vid_path, vid_duration, aud_duration, output_path):
    nb_repeat = int(aud_duration // vid_duration)
    rest_duration = aud_duration % vid_duration
    cutted_vid_filename = vid_path.split(".")[0] + "_longer_tmp.mp4"
    if rest_duration != 0:
        # we add 1 seconde so that it doesn't cut too fast
        cut_excess_video(vid_path, 0, rest_duration, cutted_vid_filename)
    tmp_merged_vid_filename = vid_path.split(".")[0] + "_longer.mp4"
    merge_vid([vid_path] * nb_repeat, tmp_merged_vid_filename)
    if rest_duration != 0:
        merge_vid([tmp_merged_vid_filename, cutted_vid_filename], output_path)
    

def alternative_merge_vid(vid_clip_paths, output_path):
    # Construct ffmpeg command with dynamic input files
    inputs = []
    filters = []
    
    for idx, file in enumerate(vid_clip_paths):
        inputs.extend(["-i", file])
        filters.extend([f"[{idx}:v]", f"[{idx}:a]"])
    
    filter_complex = f"{' '.join(filters)} concat=n={len(vid_clip_paths)}:v=1:a=1 [v] [a]"
    
    command = ["ffmpeg"] + ["-loglevel"] + ["quiet"] + ["-y"] + inputs + ["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]", output_path]
    
    # Execute the command
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print("Videos merged successfully!")
    else:
        print("Failed to merge videos!")

def mute_video_at_interval(video_path, start_time, end_time):
    # print("start_time: ", start_time)
    # print("end_time: ", end_time)
    output_path = video_path.split(".")[0] + "_muted_end.mp4"

    # Load the video clip
    clip = VideoFileClip(video_path)
    
    # Split the clip into three parts
    clip1 = clip.subclip(0, start_time)
    clip2 = clip.subclip(start_time, end_time).volumex(0)  # Mute this part
    # clip3 = clip.subclip(end_time, clip.duration)
    
    # Concatenate the clips
    final_clip = concatenate_videoclips([clip1, clip2])
    
    # Write to the output file
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path

def cut_excess_video(vid_file_path, cut_start, cut_end, output_filname):
    # METHOD 1
    # print("cut_duration: ", cut_duration)
    ffmpeg_extract_subclip(vid_file_path, cut_start, cut_end, targetname=output_filname)

    # METHOD 2
    # clip = VideoFileClip(vid_file_path)
    # # getting only first 5 seconds
    # clip = clip.subclip(cut_start, cut_end)
    # clip.write_videofile(output_filname)
    
    # METHOD 3
    # command = [
    #     "ffmpeg",
    #     "-y",
    #     "-i", vid_file_path,
    #     "-ss", str(cut_start),
    #     "-t", str(cut_end),
    #     output_filname
    # ]

    # result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # if result.returncode == 0:
    #     print("Command executed successfully!")
    # else:
    #     print("Command failed!")

def blur_video(vid_file_path):
    blur_vid_filename = vid_file_path.split(".")[0] + "_blurred.mp4"
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",  "quiet",
        "-i", vid_file_path,
        "-vf", "boxblur=10",
        "-c:a", "copy",
        blur_vid_filename
    ]

    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    if result.returncode == 0:
        print("Command executed successfully!")
    else:
        print("Command failed!", result)

    return blur_vid_filename


# VIDEO DURATION FUNCTIONS 
# SO COMPLICATED FOR NOTHING
def probe(vid_file_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = [
        "ffprobe",
        "-loglevel",  "quiet",
        "-print_format", "json",
            "-show_format",
            "-show_streams",
            vid_file_path
    ]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def get_vid_duration(vid_file_path):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
    #return None


def merge_vid(video_clip_paths, output_path):
    # create VideoFileClip object for each video file
    clips = [editor.VideoFileClip(c) for c in video_clip_paths]
    # concatenate all video clips
    final_clip = editor.concatenate(clips) # other attribute: method="compose"
    # write the output video file
    final_clip.write_videofile(output_path)