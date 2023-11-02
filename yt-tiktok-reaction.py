import datetime
import random
from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
from text_to_speech_api.google_tts import *
from montage_script.montage import *
from montage_script.video_processing.video_montage import get_vid_duration
from youtube_api.yt_upload import *
from montage_script.audio_processing.tools import *
import re
from thumbnail_creation.thumbnail import *
from web_scrapping.selenium.tiktok_scraper import *
from other_scripts.tools import *
import time



NB_VOD_TO_COMP = "30"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/tiktok_react/"
NB_VID_TO_RETURN = 5
def main():
    # VARIABLE FOR TESTS, TO REMOVE
    # trend_keyword = "like"
    # impression = "WATCHING THIS VIDEO MAKES ME FEEL HOPEFUL FOR THE KIND OF LOVE I WANT TO EXPERIENCE ONE DAY."
    # impression_cleaned = impression.replace(",", " ").replace(".", " ").replace("'", "").upper()
    # emoji_pattern = re.compile("["
    #     u"\U0001F600-\U0001F64F"  # emoticons
    #     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #     u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    # "]+", flags=re.UNICODE)
    # impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)

    # # print("impression_cleaned: ", impression_cleaned)
    # vid_comments = "0 gang here 👇.Cute (Never experienced this in my life and I have a feeling I won’t.).thanks for reminding me that i'll never find a female..:POV me and my pillow doing all those positions thinking wait when am I gonna get a girl???.knowing ill never experience this is sad.i just want a hug.Litarally any.here.3 and 5.3.@Jason Jay what one should we try.@X_Dreamcorelol_X what do u like?.1.I Like 3 in my opinion.6.3.thank u for reminding me i get no girls.6.@QWILZY 🫠😍 meltinggggg x.@A_workman2100 all?.@mia pick which ones.I just searched luh calm fir.1 and 2 is elite (I'm single and crying).That would never happen to me😭.2.Hi ❤️❤️❤️Nlie ❤️❤️❤️❤️.3 and 6.3,4,6❤.tryna nvm😂💘💗.3.This will never happen to me ☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️💀💀☠️☠️.4.@will what one.@real which one??.7 my own side and own space 😳.5 fr gonna lead to smth crazy bro.i like number 6.@Noah Pillsbury 4 or 6😍.6😏.@Coopdawg pleaseeeeeee.2, & 6.4,6.7 gang here👇 im singel.@Lilly🤍🫶🏼 yes 😍❤️which oneeeee.someone says 5.1.is 0 an option.7.1.@Noa ꨄ yesss"
    # joined_comments = vid_comments
    # new_vid_title = "Will you find true love? #shorts"
    # new_vid_title = new_vid_title.replace('"', "")
    # artefacts_file_name = trend_keyword + "_2023-11-02" 
    # final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    # impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # description = "Wow, this hairline is so unique and creative! 😮 #amazed"
    # tags = ['#ReadyToBeAmazed', '#DojaCat', '#UniqueHairstyle', '#EyeCatching', '#BritneySpearsVibes', '#Satire', '#Idol', '#WildHair', '#MosesPartingTheSea', '#MiddlePart', '#HairGrowth', '#AvatarVibes', '#HeadacheRelief', '#BlondHair', '#PurposeOfLife', '#HairlineGoals', '#LaughOutOfSurprise', '#InvisiblePart', '#DIYHaircut', '#TrustTheProcess']
    # category_id = "24"
    # thumbnail_path = ASSETS_FOLDER + "last_thumbnail.jpg"

    
    # TO TEST IMPRESSION TEXT   
    # blurred_vid_path = "assets_produced/tiktok_react/tmp_like_2023-11-02.mp4"
    # impression_txt = impression_cleaned
    # impression_blurred_text_vid_path = "assets_produced/tiktok_react/like_2023-11-02_testing.mp4"
    # impr_audio_file_path = "assets_produced/tiktok_react/tmp_like_2023-11-02.mp3"
    # # text_to_speech(impression_txt, impr_audio_file_path)
    # add_impression_txt(blurred_vid_path, impr_audio_file_path, impression_txt, impression_blurred_text_vid_path)
    
    # ##############################################################
    # ## START SCRIPT
    # ##############################################################
    
    # # chat gpt get trend but always the same so nope
    # trend_keyword = get_trend_keyword()

    # those keyword are extracted with chatgpt-4 + bing
    list_trend_keywords = ['tiktok', 'love', 'like', 'follow', 'explore', '2023', 'meme', 'video', 'duet', 'repost', 'tiktokchallenge', 'new', 'tiktokfamous', 'tiktoktrend', 'viralvideos', 'viralpost', 'blackgirlfollowtrend', 'relatable', 'slowmo', 'behindthescenes', 'dadsoftiktok', 'momsoftiktok', 'family', 'reallifeathome', 'tiktokmademebuyit', 'mexico', 'challenge', 'youtube', 'youtuber', 'artistsoftiktok', 'foryoupage', 'fyp', 'foryou', 'viral', 'funny', 'memes', 'followme', 'cute', 'fun', 'happy', 'fashion', 'comedy', 'bestvideo', 'tiktok4fun', 'thisis4u', 'loveyoutiktok', 'cutebaby', 'cutegirl', 'pregnantlife', 'cuteness', 'cuteboy']
    trend_keyword = random.choice(list_trend_keywords)
    # print("Trend_keyword is: " + trend_keyword)

    # creation of the name for the resulting files
    artefacts_file_name = trend_keyword + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # creation of the path for the video file from tiktok
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"

    # gets video titles and urls + aweme_ids from tiktok of "NB_VID_TO_RETURN"
    # from tiktok
    vid_titles, vid_urls, aweme_ids = get_vid_treding(
        trend_keyword, 
        NB_VOD_TO_COMP,
        NB_VID_TO_RETURN,
    )

    # Gets the video that has no human voice and put it in "/%trend_keyword%/_date.mp4"
    vid_title, vid_url, aweme_id = choose_vid_no_human_voice(vid_titles, vid_urls, aweme_ids, video_file_path)
    print("Video found: " + vid_title)
    print("Vod URL: " + vid_url)
    print("Vid id: " + aweme_id)

    # gets comments from tiktok video
    vid_comments = get_vod_comments(aweme_id, NB_COMMENTS_TO_GET)
    print("Nb of comments: " + str(len(vid_comments)))

    # gets impression text
    # removes the "-" bc it fucks it the ui for the words later
    impression = get_impression(vid_title, ".".join(vid_comments))
    new_vid_title = get_title(impression)
    new_vid_title += " #shorts"
    print("impression: " + impression)
    print("new_vid_title: " + new_vid_title)

    # gets second artefact "trend_keyword_tmp_date.mp3"
    impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    text_to_speech(impression, impression_file_path)
    # removal of '"' in the title bc it sucks and chat gpt gives it everytime
    new_vid_title = new_vid_title.replace('"', "")
    # because the sofware doesn't like commas
    impression_cleaned = impression.replace(",", " ").replace(".", " ").replace("'", "").replace("-", " ").upper()

    # remoing of emoji bc cannot show them on the video
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)


        # gets tag + category_id + description for the video
    joined_comments = ".".join(vid_comments)
    tags = get_vid_tags(new_vid_title, impression, joined_comments)
    print("tags: ", tags)
    category_id = get_category_id(new_vid_title, impression, joined_comments)
    description = get_description(new_vid_title, joined_comments, " ".join(tags))

    # saves every info like the title, the impression, the tags, the category_id and the description
    # useful for debug but also when crashing
    # does this before the video montage bc this is usually what crashes
    save_info(
        vid_title,
        vid_url,
        aweme_id,
        impression, 
        impression_cleaned, 
        new_vid_title,
        joined_comments,
        tags,
        category_id, 
        description,
        ASSETS_FOLDER + artefacts_file_name + "_info.txt"
    )

    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    tiktok_react_montage(
        video_file_path, 
        impression_file_path, 
        final_vid_file_path, 
        impression_cleaned
    )

    # gets the last frame of the video for the thumbnail
    thumbnail_path = extract_last_frame(final_vid_file_path, ASSETS_FOLDER + "tmp_" + trend_keyword + "_last_thumbnail.jpg")

    # uploads to youtube and adds to playlist
    # id playlist reaction : PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ
    # id playlist compilation : PLpoAErUqpB6dz70h9KPbB0dOCn0XCtBZH
    add_vid_to_yt(
        category_id, 
        description, 
        new_vid_title, 
        tags, 
        "unlisted", 
        final_vid_file_path, 
        "PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ",
        thumbnail_path
    )

    # REMOVES ALL TMP FILES
    remove_files_starting_with(ASSETS_FOLDER, "tmp_" + artefacts_file_name)

    # uploads to tiktok
    upload_tiktok_vid(new_vid_title, tags, final_vid_file_path)

if __name__ == '__main__':
    # try:
        main()
    # except Exception as e:
    #     send_telegram_message("PROGRAM CRASHED:")
    #     send_telegram_message(str(e))