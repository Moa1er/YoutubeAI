import datetime
import random
from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
from text_to_speech_api.text_to_speech import *
from montage_script.montage import *
from montage_script.video_processing.video_montage import get_vid_duration
from youtube_api.yt_upload import *
from montage_script.audio_processing.tools import *
import re
from thumbnail_creation.thumbnail import *
from selenium_script.tiktok_scraper import *
import time



NB_VOD_TO_COMP = "30"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/"
     
def main():
    # VARIABLE FOR TESTS, TO REMOVE
    impression = "I miss you so much, it hurts."
    impression_cleaned = impression.replace(",", " ")
    impression_cleaned = impression_cleaned
    vid_comments = "I've reached bed time tiktok..My boy was ready to start before the song was lol.Jim from Royal Family.So we’re all just awake right now?.Goooo bro.My Boy’s got moves 💙.@archie you Friday this.Best one so far..@yas x for jords.@kianna my dancing be like 😂.beautiful.Best video ever so much 🙏.@Lisa.Nukk best one.Awesome T!!!.Easy now.best one I've seen so far.pure magic.Cracked me up!! You are too funny..Ayyyy bro hit this bih 🔥.@S I E N N A 🤍 bgt here we come 😂.haha you're awesome.😂😂😂 love it.you are so cute,keep up the dancing.@Logan? @On top-_- marko.Nailed it.@SB♥️its hashee.Best one I seen so far 😭.wow amazing nice job sir.lesssssgooooooo.best thing ever!!!.U got that rizz m8.@A.1 gonna be your son lad.let's go through the front door and far away.Killed it brother!.nice moves!.dance better than me bro keep it up🤜.🔥🔥🔥 You got them moves!!! 😎.@izzy🫶🏼 what a guy.Hell yeah brother.he smooth with it tho😂.You are amazing!!.he looks like jacksepticeye.@Niall Murphy practising ya moves for tomorrow.Well played!!.Why he look like jim our of the royal family tv show 😂 looking good pal ✌🏼.@Bleona I’m stalking ur reposts r u ok ???.Good job! Keep dancing 😁.@lior 🤷 cute.@Rayna :) @Jaan Khan he kinda looks like behrend.Unspoken rizz"
    new_vid_title = "Can you keep up? 💃"
    artefacts_file_name = "bestvideo_2023-10-23"
    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    description = "Discover the heartwarming moments of #Shorts as talented creators @BellaGonterman, @SawyerMoss, @AdaleLouallen, and many others express who they miss the most. This trending video is a must-watch, filled with emotion and relatable moments that will make you reach for the tissues. Don't miss out on this touching and relatable content. #TrendAlert"
    tags = ['#CanYouKeepUp', '#Shorts', '#BedTimeTikTok', '#ImpressiveMoves', '#Captivating', '#Entertaining', '#DancingSkills', '#RoyalFamily', '#FridayVibes', '#BestOne', '#PureMagic', '#FunnyVideo', '#Awesome', '#EasyNow', '#CrackedMeUp', '#ViralDance', '#BestVideoEver', '#GetYourDanceOn', '#KeepDancing', '#SmoothMoves', '#Amazing', '#LooksLikeJacksepticeye', '#StalkingReposts', '#GoodJob', '#CuteDancer']
    tags = tag_too_long(tags)
    print((",").join(tags))
    category_id = "22"

    get_description(new_vid_title, vid_comments, (" ").join(tags))
    # ##############################################################
    # ## START SCRIPT
    # ##############################################################
    
    # chat gpt get trend but always the same so nope
    # trend_keyword = get_trend_keyword()

    # those keyword are extracted with chatgpt-4 + bing
    # list_trend_keywords = ['tiktok', 'love', 'like', 'follow', 'explore', '2023', 'meme', 'video', 'duet', 'repost', 'tiktokchallenge', 'new', 'tiktokfamous', 'tiktoktrend', 'viralvideos', 'viralpost', 'blackgirlfollowtrend', 'relatable', 'slowmo', 'behindthescenes', 'dadsoftiktok', 'momsoftiktok', 'family', 'reallifeathome', 'tiktokmademebuyit', 'mexico', 'challenge', 'youtube', 'youtuber', 'artistsoftiktok', 'foryoupage', 'fyp', 'foryou', 'viral', 'funny', 'memes', 'followme', 'cute', 'fun', 'music', 'happy', 'fashion', 'comedy', 'bestvideo', 'tiktok4fun', 'thisis4u', 'loveyoutiktok', 'cutebaby', 'cutegirl', 'pregnantlife', 'cuteness', 'cuteboy']
    # trend_keyword = random.choice(list_trend_keywords)
    # # print("Trend_keyword is: " + trend_keyword)

    # # creation of the name for the resulting files
    # artefacts_file_name = trend_keyword + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # # creation of the path for the video file from tiktok
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"

    # # gets video title and url + aweme_id from tiktok
    # # also download third artefact "trend_keyword_date.mp4"
    # vid_title, vid_url, aweme_id = get_vid_treding(
    #     trend_keyword, 
    #     NB_VOD_TO_COMP, 
    #     video_file_path
    # )
    # print("Video found: " + vid_title)
    # print("Vod URL: " + vid_url)
    # print("Vid id: " + aweme_id)

    # # gets the last frame of the video for the thumbnail
    # thumbnail_path = extract_last_frame(video_file_path)

    # # gets comments from tiktok video
    # vid_comments = get_vod_comments(aweme_id, NB_COMMENTS_TO_GET)
    # print("Nb of comments: " + str(len(vid_comments)))

    # # gets impression text
    # impression, new_vid_title = get_impression_and_title(
    #     vid_title, ".".join(vid_comments), 
    #     get_vid_duration(video_file_path)
    # )
    # new_vid_title += " #Shorts"
    # print("impression: " + impression)
    # print("new_vid_title: " + new_vid_title)

    # # gets second artefact "trend_keyword_tmp_date.mp3"
    # impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # text_to_speech(impression, impression_file_path)
    # # because the sofware doesn't like commas
    # impression_cleaned = impression.replace(",", " ").replace(".", " ")
    # # removal of '"' in the title bc it sucks and chat gpt gives it everytime
    # new_vid_title = new_vid_title.replace('"', "")

    # # remoing of emoji bc cannot show them on the video
    # emoji_pattern = re.compile("["
    #     u"\U0001F600-\U0001F64F"  # emoticons
    #     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #     u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    # "]+", flags=re.UNICODE)
    # impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)

    # final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # make_montage(
    #     video_file_path, 
    #     impression_file_path, 
    #     final_vid_file_path, 
    #     impression_cleaned
    # )
    
    # # gets tag + category_id + description for the video
    # joined_comment = ".".join(vid_comments)
    # tags = get_vid_tags(new_vid_title, impression, joined_comment)
    # print("tags: ", tags)
    # category_id = get_category_id(new_vid_title, impression, joined_comment)
    # print("category_id: ", category_id)
    # description = get_description(new_vid_title, joined_comment, " ".join(tags))
    # print("description: ", description)

    # # uploads to youtube and adds to playlist
    # # id playlist reaction : PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ
    # # id playlist compilation : PLpoAErUqpB6dz70h9KPbB0dOCn0XCtBZH
    # add_vid_to_yt(
    #     category_id, 
    #     description, 
    #     new_vid_title, 
    #     tags, 
    #     "unlisted", 
    #     final_vid_file_path, 
    #     "PLpoAErUqpB6cdPK-rxiFItyLQ0CN-v2sZ",
    #     thumbnail_path
    # )

    # # uploads to tiktok
    # upload_tiktok_vid(new_vid_title, tags, final_vid_file_path)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        send_telegram_message("PROGRAM CRASHED:")
        send_telegram_message(str(e))