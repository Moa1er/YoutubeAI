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
    # trend_keyword = "cuteness"
    # impression = "I can't resist the adorable and shiny tongue of this cute bunny! 🐰💖"
    # impression_cleaned = impression.replace(",", " ").replace(".", " ").replace("'", "")
    # emoji_pattern = re.compile("["
    #     u"\U0001F600-\U0001F64F"  # emoticons
    #     u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #     u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #     u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    # "]+", flags=re.UNICODE)
    # impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)

    # print("impression_cleaned: ", impression_cleaned)
    # vid_comments = "i thought it was capybara.I’m not hearing anyone out.THE TOUNG ITS SO SHINY AND CUTE.NAH THEIR TOUNGES😭😭😭.🥺🥺🥰🥰.hear me out.beautiful dude nice beautiful.i miss jan.BUNNYYYYYY.Ok hear me out.🥺🥺.@anushabdirahmaan6 carab qurxana.HIS TOUNGE OMG.my mom just sent me this vid thanks mom.@cate we lapon.Give it yellow dragon fruit @ella.@Summer 🫶🏻🤍 it’s tounge is so cuteee.why do i find this funny.I WANT ONEEE.Ayo what we’re u doing w that water 🤨📸.🥺🥺.AWWWW STOP PLZ IM DYING OF CUTENESS.very cute 💝.I got one to.I want oneee.THE TOUNG I CANT IM IN LOVE.sow pretty 🥰.Omgg mbbb.🥰🥺.🥰🥰.hear me out.I really want one omg.no way somebody said „hear me out“💀.oh my i want one so bad.when your days been tough watch this 😍🥰❤️.Vil have den @Sofeaaaaa.и жаныммм суйкымдысынайй😭😭💔.CUTE ASF.@jerzel eatwell!!.me waiting for the cooking part💀.Bro that’s extremely cute🥰.And then 🦅.where's the cooking the rabbit part.The tung part was a little weird but we good🥰.BRO THE TOUNGE IS KINDA CUTE THO.It looks so cute especially when it was drinking water💖💗💓💞🙈"
    # joined_comments = vid_comments
    # new_vid_title = "Can you handle this tongue? 😍 #Shorts"
    # new_vid_title = new_vid_title.replace('"', "")
    # artefacts_file_name = trend_keyword + "_2023-10-28" 
    # final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    # impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # description = "Wow, this hairline is so unique and creative! 😮 #amazed"
    # tags = ['#ReadyToBeAmazed', '#DojaCat', '#UniqueHairstyle', '#EyeCatching', '#BritneySpearsVibes', '#Satire', '#Idol', '#WildHair', '#MosesPartingTheSea', '#MiddlePart', '#HairGrowth', '#AvatarVibes', '#HeadacheRelief', '#BlondHair', '#PurposeOfLife', '#HairlineGoals', '#LaughOutOfSurprise', '#InvisiblePart', '#DIYHaircut', '#TrustTheProcess']
    # category_id = "24"
    # thumbnail_path = ASSETS_FOLDER + "last_thumbnail.jpg"
    # joined_comment = "Doja cat?.She’s back.me when he leaves me on delivered.Youre my idol.OH MY GOSH?!.oooohhh woaaahhhhhh.it’s giving britney spears.so concrete 🎀🎀.this is actually satire.silly willy billy.Ur wildinnn😭.when moses parted the sea.Now THAT’S a middle part.The way it’s not even in center.like why?😭.avatar vibes ⬆️.Me tryna get rid of my headache.I watched this 4 times thinking there was gonna be some type of oil to make it grow faster and better.Me tryna get my middle part straight.now what are we achieving from this.But why?.avatar.how I look when my blond hair grows back.I don't know what the purpose of my stay on planet Earth is. 😃.WHY WHHHHHHYYYY!!???.@<3 @Ne… @Jael_13 @EMILIA 🧿 unmmm.so freaking cute i might even do it on myself🤭🤭.Just why? 😅.Cute hair line 💗.@piper my heart.I STARTED TO LAUGH SO HARD AT THIS.it's not in the middle.but why 😭.@Insanest Yuriko's lover @fishu tặng.@lillian ┆彡 my hair line in the future.@Lucy Bijou Schurr bro.who did this cover???.but WHY.No centered.Love your hair line girly pop…”.Erm..My boy got lined up🔥🔥.Is this what they call an invisible part 🥴.@user192680743 u the next time u cut ur own hair 😍🥰😍🥰😍.@ur mom do this.@ashka_m do this it will look good trust.@😘 @danielaxxz @😍 lowkey wanna do this.BRO NO ONE CAN SAY SHE DOES NOT HAVE A MIDDLE PART 😭.that part!.@ruth🎧 you"

    # ##############################################################
    # ## START SCRIPT
    # ##############################################################
    
    # chat gpt get trend but always the same so nope
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
    impression = get_impression(
        vid_title, ".".join(vid_comments)
    )
    new_vid_title = get_title(impression)
    new_vid_title += " #shorts"
    print("impression: " + impression)
    print("new_vid_title: " + new_vid_title)

    # gets second artefact "trend_keyword_tmp_date.mp3"
    impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    text_to_speech(impression, impression_file_path)
    # because the sofware doesn't like commas
    impression_cleaned = impression.replace(",", " ").replace(".", " ").replace("'", "")
    # removal of '"' in the title bc it sucks and chat gpt gives it everytime
    new_vid_title = new_vid_title.replace('"', "")

    # remoing of emoji bc cannot show them on the video
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    impression_cleaned = emoji_pattern.sub(r'', impression_cleaned)

    final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    tiktok_react_montage(
        video_file_path, 
        impression_file_path, 
        final_vid_file_path, 
        impression_cleaned
    )
    
    # gets tag + category_id + description for the video
    joined_comments = ".".join(vid_comments)
    tags = get_vid_tags(new_vid_title, impression, joined_comments)
    print("tags: ", tags)
    category_id = get_category_id(new_vid_title, impression, joined_comments)
    description = get_description(new_vid_title, joined_comments, " ".join(tags))

    # gets the last frame of the video for the thumbnail
    thumbnail_path = extract_last_frame(final_vid_file_path, ASSETS_FOLDER + trend_keyword + "_last_thumbnail.jpg")

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