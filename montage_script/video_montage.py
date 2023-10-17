import subprocess
from moviepy import editor
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import json


def create_blurred_vid(vid_file_path, audio_duration):
    blurred_vid_path = blur_video(vid_file_path)
    print("blurred_vid_path: ", blurred_vid_path)
    output_path = blurred_vid_path.split(".")[0] + "_cutted.mp4"
    print("output_path: ", output_path)
    cut_excess_video(blurred_vid_path, 0, audio_duration, output_path)
    return output_path

def create_final_video(vid_file_path, target_vid_duration, actual_vid_duration):
    if target_vid_duration < actual_vid_duration:
        return vid_file_path
    
    # takes the video.mp4 and blurs it name is %usual_blabla%_blur_part.mp4
    blur_vid_filename = blur_video(vid_file_path)
    #to remove
    print("blur_vid_dur: ", get_vid_duration(blur_vid_filename))
    print("origin_vid_dur: ", get_vid_duration(vid_file_path))
    
    target_blurred_vid_duration = target_vid_duration - actual_vid_duration
    print("target_blurred_vid_duration: ", target_blurred_vid_duration)
    final_blurred_vid_filname = blur_vid_filename.split(".")[0] + "_cutted.mp4"
    
    if target_blurred_vid_duration < actual_vid_duration:
        print("cut_excess_video")
        cut_excess_video(blur_vid_filename, 0, target_blurred_vid_duration, final_blurred_vid_filname)
    #this for some reason extend the video a lot so let's get rid of that if possible
    else:
        print("repeat_blurred_vid")
        repeat_blurred_vid(blur_vid_filename, target_blurred_vid_duration, actual_vid_duration, final_blurred_vid_filname)
    
    final_video_filename = vid_file_path.split(".")[0] + "_final.mp4"
    merge_vid([final_blurred_vid_filname, vid_file_path], final_video_filename)

    # to remove
    print("final_blurred_vid_filname: ", get_vid_duration(final_blurred_vid_filname))
    print("vid_file_path: ", get_vid_duration(vid_file_path))

    return final_video_filename

def repeat_blurred_vid(vid_file_path, duration_wanted, duration_vid, output_filname):
    nb_repeat = int(duration_wanted // duration_vid)
    rest_duration = duration_wanted % duration_vid
    print("nb_repeat: ", nb_repeat)
    print("rest_duration: ", rest_duration)
    cutted_vid_filename = vid_file_path.split(".")[0] + "_cutted_tmp.mp4"
    if rest_duration != 0:
        cut_excess_video(vid_file_path, 0, rest_duration, cutted_vid_filename)
        #to remove
        print("cutted_vid_dur: ", get_vid_duration(cutted_vid_filename))

        tmp_merged_vid_filename = vid_file_path.split(".")[0] + "_merged.mp4"
        merge_vid([vid_file_path] * nb_repeat, tmp_merged_vid_filename)

        #to remove
        print("tmp_merged_vid_dur: ", get_vid_duration(tmp_merged_vid_filename))
        merge_vid([tmp_merged_vid_filename, cutted_vid_filename], output_filname)

        #to remove
        print("output_filname: ", get_vid_duration(output_filname))
    else:
        merge_vid([vid_file_path] * nb_repeat, output_filname)

    

def merge_vid(video_clip_paths, output_path):
    # create VideoFileClip object for each video file
    clips = [editor.VideoFileClip(c) for c in video_clip_paths]
    final_clip = editor.concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_path)

def cut_excess_video(vid_file_path, cut_start, cut_end, output_filname):
    # print("cut_duration: ", cut_duration)
    ffmpeg_extract_subclip(vid_file_path, cut_start, cut_end, targetname=output_filname)

    # clip = VideoFileClip(vid_file_path)
    # # getting only first 5 seconds
    # clip = clip.subclip(0, cut_duration)
    # clip.write_videofile(output_filname)
    
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

    command = ["ffprobe",
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