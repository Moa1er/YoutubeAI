import datetime
import random
from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
# from text_to_speech_api.eleven_labs_tts import *
from text_to_speech_api.google_tts import *
from montage_script.montage import *
from montage_script.video_processing.video_montage import get_vid_duration
from youtube_api.yt_upload import *
from montage_script.audio_processing.tools import *
import re
from thumbnail_creation.thumbnail import *
from web_scrapping.selenium.tiktok_scraper import *
from other_scripts.tools import *

NB_VOD_TO_COMP = "30"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/funny_stories/"
JOKE_FILE_PATH = "jokes.txt"
TREND_KEYWORD = "satisfying"
NB_VID_TO_RETURN = 10

def main():
    ########### VARIABLES TESTS
    # new_vid_title = "Will Bob's last request be fulfilled? #Shorts"
    # joke = "Bob returned from a Doctor's visit and told his wife Alma that the Doctor said he only had 24 hours to live.*  Wiping away her tears, he asked her to make love with him. Of course she agreed and they made passionate love.  Six hours later, Bob went to her again, and said, 'Honey, now I only have 18 hours left to live. Maybe we could make love again?' Alma agreed and again they made love.  Later, Bob was getting into bed when he realized he now had only eight hours of life left.  He touched Alma's shoulder and said, 'Honey Please? Just one more time before I die.' She agreed, then afterwards she rolled over and fell asleep.  Bob, however, heard the clock ticking in his head, and he tossed and turned until he was down to only four more hours.  He tapped his wife on the shoulder to wake her up. 'Honey, I only have four hours left! Could we...?'  His wife sat up abruptly, turned to him and said :  *'Listen Bob, I have to get up in the morning for your funeral & You don't have to get up !!!*"
    # joke = joke.replace("*", " ").replace("'", "").replace('"', '')
    # artefacts_file_name = joke[0:10].replace(" ", "_") + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    # joke_aud_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # background_vids_paths = [ASSETS_FOLDER + "tmp_Bob_return_2023-10-26_0.mp4"]
    # impression_cleaned = joke
    ###############################################33
    joke = read_firs_line_and_del(JOKE_FILE_PATH)
    print("joke: ", joke)
    
    # creation of the name for the resulting files
    artefacts_file_name = joke[0:10].replace(" ", "_") + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # creation of the path for the video file from tiktok
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"

    # gets video title and url + aweme_id from tiktok
    # also download third artefact "trend_keyword_date.mp4"
    vid_titles, vid_urls, aweme_ids = get_vid_treding(
        TREND_KEYWORD,
        NB_VOD_TO_COMP, 
        NB_VID_TO_RETURN,
    )
    print("Videos found: ", vid_titles)
    print("Vods URL: ", vid_urls)
    print("Vids id: ", aweme_ids)

    # gets impression text
    new_vid_title = get_title(joke)
    new_vid_title += " #Shorts"
    print("new_vid_title: " + new_vid_title)

    # gets second artefact "trend_keyword_tmps_date.mp3"
    joke_aud_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    joke = joke.replace("*", " ")
    text_to_speech(joke, joke_aud_file_path)
    # because the sofware doesn't like commas
    joke_cleaned = joke.replace(",", " ").replace(".", " ").replace("'", "").replace('"', '')
    # removal of '"' in the title bc it sucks and chat gpt gives it everytime
    new_vid_title = new_vid_title.replace('"', "")

    # downloads each videos for background until there is enough videos to cover the impression
    tot_time_vids = 0
    joke_duration = get_audio_duration_mp3(joke_aud_file_path)
    background_vids_paths = []
    for i in range(0, len(vid_urls)):
        if joke_duration < tot_time_vids:
            break
        vid_file_name = video_file_path.split(".")[0] + "_" + str(i) + ".mp4"
        download_vod(vid_urls[i], vid_file_name)
        tot_time_vids += get_vid_duration(vid_file_name)
        background_vids_paths.append(vid_file_name)

    # remoing of emoji bc cannot show them on the video
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    joke_cleaned = emoji_pattern.sub(r'', joke_cleaned)

    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    funny_story_montage(
        background_vids_paths, 
        joke_aud_file_path, 
        final_vid_file_path, 
        joke_cleaned
    )
    
    # gets tag + category_id + description for the video
    joined_comment = ""
    tags = get_vid_tags(new_vid_title, joke, joined_comment)
    print("tags: ", tags)
    description = get_description(new_vid_title, joined_comment, " ".join(tags))
    print("description: ", description)

    # uploads to youtube and adds to playlist
    # id playlist reaction : PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ
    # id playlist compilation : PLpoAErUqpB6dz70h9KPbB0dOCn0XCtBZH
    # id playlist funny stories : PLpoAErUqpB6fHPiCoS5CA-zkxkLTeu1hz
    add_vid_to_yt(
        "23", 
        description, 
        new_vid_title, 
        tags, 
        "unlisted", 
        final_vid_file_path, 
        "PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ"
    )

    # # uploads to tiktok
    # upload_tiktok_vid(new_vid_title, tags, final_vid_file_path)

if __name__ == '__main__':
    # try:
        main()
    # except Exception as e:
    #     send_telegram_message("PROGRAM CRASHED:")
    #     send_telegram_message(str(e))