import datetime

from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
from text_to_speech_api.text_to_speech import *
from montage_script.montage import *
from youtube_api.yt_upload import *

NB_VOD_TO_COMP = "20"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/"

def main():
    # # TESTED
    # trend_keyword = get_trend_keyword()
    # print("Trend_keyword is: " + trend_keyword)

    # # TESTED
    # # gets video title and url + aweme_id from tiktok
    # vid_title, vid_url, aweme_id = get_vid_name_url_id(trend_keyword, NB_VOD_TO_COMP)
    # print("Video found: " + vid_title)
    # print("Vod URL: " + vid_url)
    # print("Vid id: " + aweme_id)

    # # TESTED
    # # gets comments from tiktok video
    # vid_comments = get_vod_comments(aweme_id, NB_COMMENTS_TO_GET)
    # print("Nb of comments: " + str(len(vid_comments)))
    
    # # creation of the name for the resulting files
    # artefacts_file_name = trend_keyword + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # print("artefacts_file_name: " + artefacts_file_name)
    
    # # TESTED
    # # gets first artefact "trend_keyword_tmp_date.mp4"
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    # download_vod(vid_url, video_file_path)

    # # TESTED
    # # gets impression text
    # impression, new_vid_title = get_impression_and_title(vid_title, ",".join(vid_comments))
    # new_vid_title += " #Shorts"
    # print("impression: " + impression)
    # print("new_vid_title: " + new_vid_title)

    # # TESTED
    # # gets second artefact "trend_keyword_tmp_date.mp3"
    # audio_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # text_to_speech(impression, audio_file_path)

    artefacts_file_name = "Transition_2023-10-16"
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    audio_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"

    # TESTED
    # gets third artefact "trend_keyword_date.mp4"
    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # final_vid_file_path = ASSETS_FOLDER + "final_" + artefacts_file_name + ".mp4"
    make_montage(ASSETS_FOLDER, video_file_path, audio_file_path, final_vid_file_path)

    # to remove
    # final_vid_file_path = ASSETS_FOLDER + "FYP_2023-10-16.mp4"
    # new_vid_title = "T-Rex Transformation: When Fear Turns You Prehistoric" #Shorts
    # impression = "Hilarious video of a girl getting scared and instantly transforming into a T-Rex, complete with cross-legged walk and tiny arms, creating a true Jurassic Park moment."

    # TESTED
    # uploads to youtube
    # upload_to_yt(final_vid_file_path, new_vid_title, impression, "22", "unlisted")

if __name__ == '__main__':
    main()