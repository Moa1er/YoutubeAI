import datetime

from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
from text_to_speech_api.text_to_speech import *
from montage_script.montage import *
from montage_script.video_processing.video_montage import get_vid_duration, alternative_merge_vid
from youtube_api.yt_upload import *
from montage_script.audio_processing.tools import *
import re

NB_VOD_TO_COMP = "20"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/"

def main():

    # # VARIABLE FOR TESTS, TO REMOVE
    # impression = "Adorably quirky and colorful, this TikTok video is a burst of kawaii fashion and cuteness overload."
    # impression_cleaned = impression.replace(",", " ")
    # impression_cleaned = impression_cleaned.upper()
    # vid_comments = "scrolled, realized it was bryce hall, came back, realized it wasnt.@✮ it looks like bryce hall😭.Or else what 😭.Insta reels would eat this up ❤️😘.Cuteness overload ;-;.sorry for looking into your eyes without permission.caption..oh! 🥰.the caption??😭?.@no BRYCE HALL.@Caroline @Josie i thought this was bryce hall..cuteness overload !! >•<.@Bea it’s so preppy in here 🥰.@sαv⸆⸉ @mia🪷 bryce hall.guys its talking abt the audio not them.@¡¡ORAMO!! cuteness not loading🤭.@milo oh.@AAAA you.@aether @izzi THE CAPTION.DO WHAT.@drez 🙆‍♂️ caption??.@shane u.This is so preppy!!.Ur beautiful.this is me if u even care.@justplainolM00 Jacob.this might be me😔.@Bryce Hall IT LOOKS LIKE U 🥰🥰.@🫧 marletta tell them how cute they are or else.cuteness overload.@lanz this is reminiscent of esan.@MILEZ 😧 @AJ 💫🫧 @ghost 👻 dannie coded.thats something...it’s so preppy in here!!.@syd gulp 😰.@ellie🩵 cuteness overload🤭🤭.So kawaii core!![cute](*^o^*).@suhruthi oh lord.Real..@Alara 🪩 my spirit animal.cuteness won't load 😻.alr...Cuteness won’tload 😜🥰.@gillian? this is u lol.@Ry WHAT IS HAPPENING...post this on instagram reels.This is the sound I feel like a stingray would make if you hugged it.to cuter.i edge to ur videos.@ilana Kirby 😋"
    # new_vid_title = "Squish my cheeks and tell me how adorable I am…or else. #fypage #fyp"
    # artefacts_file_name = "ColorfulFashion_2023-10-19"
    # final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    # impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"

    # TESTED
    trend_keyword = get_trend_keyword()
    print("Trend_keyword is: " + trend_keyword)

    # creation of the name for the resulting files
    artefacts_file_name = trend_keyword + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # creation of the path for the video file from tiktok
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"

    # TESTED
    # gets video title and url + aweme_id from tiktok
    vid_title, vid_url, aweme_id = get_vid_treding(trend_keyword, NB_VOD_TO_COMP, video_file_path)
    print("Video found: " + vid_title)
    print("Vod URL: " + vid_url)
    print("Vid id: " + aweme_id)

    # TESTED
    # gets comments from tiktok video
    vid_comments = get_vod_comments(aweme_id, NB_COMMENTS_TO_GET)
    print("Nb of comments: " + str(len(vid_comments)))

    # TESTED
    # gets impression text
    impression, new_vid_title = get_impression_and_title(vid_title, ".".join(vid_comments), get_vid_duration(video_file_path))
    new_vid_title += " #Shorts"
    print("impression: " + impression)
    print("new_vid_title: " + new_vid_title)

    # TESTED
    # gets second artefact "trend_keyword_tmp_date.mp3"
    impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    text_to_speech(impression, impression_file_path)
    # because the sofware doesn't like commas
    impression_cleaned = impression.replace(",", " ").replace(".", " ")

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)
    
    # TESTED
    # gets third artefact "trend_keyword_date.mp4"
    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    make_montage(video_file_path, impression_file_path, final_vid_file_path, impression_cleaned)
    
    # gets tag + category_id + description for the video
    joined_comment = ".".join(vid_comments)
    tags = get_vid_tags(new_vid_title, impression, joined_comment)
    print("tags: ", tags)
    category_id = get_category_id(new_vid_title, impression, joined_comment)
    print("category_id: ", category_id)
    description = get_description(new_vid_title, joined_comment, " ".join(tags))
    print("description: ", description)

    # TESTED
    # uploads to youtube
    upload_to_yt(final_vid_file_path, new_vid_title, description, tags, category_id, "unlisted")

if __name__ == '__main__':
    main()