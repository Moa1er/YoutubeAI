from montage_script.vad import get_no_voice_clip, mp3_to_wav, get_audio_duration_mp3, get_audio_from_video
import subprocess
from pydub import AudioSegment

def create_final_audio(vid_file_path, impr_audio_file_path):
     # separation audio from video in tiktok downloaded clip
    video_path_attr = vid_file_path.split(".") #[0] name, [1] extension
    audio_extract_original_video_path_mp3 = video_path_attr[0] + "_video_sound.mp3"
    # extract audio from tiktok video
    get_audio_from_video(vid_file_path, audio_extract_original_video_path_mp3)

    ########################################################
    ## FROM NOW ON WORKING IN .WAV FILE FORMAT
    ########################################################
    #choosing the final audio file name already
    final_audio_path = video_path_attr[0] + "_final.wav"
    audio_extract_original_video_path_wav = audio_extract_original_video_path_mp3.split(".")[0] + ".wav"
    # gathering the file names of each audio files
    impression_audio_path = mp3_to_wav(impr_audio_file_path)
    # audio_no_voice_filename is the audio from the video that has no voice from a person in it
    audio_no_voice_path = get_no_voice_clip(audio_extract_original_video_path_mp3)
    # means there is no human voice in the video
    if(audio_no_voice_path == None):
        merge_parts_and_silent(impression_audio_path, audio_extract_original_video_path_wav, final_audio_path)
        return final_audio_path, audio_extract_original_video_path_wav

    # TODO 
    # impression_duration = get_audio_duration(impression_audio_path)
    # audio_no_voice_duration = get_audio_duration(audio_no_voice_path)
    # duration_both_part = impression_duration + audio_no_voice_duration
    # original_audio_duration = get_audio_duration(audio_extract_original_video_path_wav)

    # print("original_audio_duration: ", original_audio_duration)
    # print("duration_both_part: ", duration_both_part)
    # print("duration_both_part > original_audio_duration", duration_both_part > original_audio_duration)
    # if duration_both_part > original_audio_duration:
    #     # # we cannot cut the impression part so we will cut audio_no_voice_filename
    #     # cut_duration = duration_both_part - impression_duration
    #     # # overwrites old audio so filename doesn't change
    #     # cut_excess_audio(audio_no_voice_filename, cut_duration)
    #     merge_parts_and_silent(impression_audio_path, audio_no_voice_path, final_audio_path)
    # else:
    #     # get a blank audio segment for the middle between part 1 and 2
    #     silence_duration = original_audio_duration - duration_both_part
    #     merge_parts_and_silent(impression_audio_path, audio_no_voice_path, final_audio_path, silence_duration)

    return final_audio_path, audio_extract_original_video_path_wav



def cut_excess_audio(audio_filename, cut_duration):
    audio = AudioSegment.from_wav(audio_filename)
    print("cut_duration: ", cut_duration)
    # pydub does things in milliseconds 
    cut_duration_ms = cut_duration * 1000
    final_audio = audio[-cut_duration_ms:]
    final_audio.export(audio_filename, format="wav")

def merge_parts_and_silent(part1_filename, part2_filename, final_audio_filename, silence_duration=None):
    part1 = AudioSegment.from_wav(part1_filename)
    part2 = AudioSegment.from_wav(part2_filename)
    merged_audio = None
    if silence_duration == None:
        merged_audio = part1 + part2
    else:
        silent_seg = AudioSegment.silent(duration=silence_duration)
        merged_audio = part1 + silent_seg + part2
    merged_audio.export(final_audio_filename, format="wav")