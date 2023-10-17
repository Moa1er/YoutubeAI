import datetime

from chatgpt_api.chat_gpt import * 
from tiktok_api.get_tiktok_data import *
from text_to_speech_api.text_to_speech import *
from montage_script.montage import *
from montage_script.video_montage import get_vid_duration
from youtube_api.yt_upload import *

NB_VOD_TO_COMP = "20"
NB_COMMENTS_TO_GET = "100"
ASSETS_FOLDER = "assets_produced/"

def main():
    # # TESTED
    # trend_keyword = get_trend_keyword()
    # print("Trend_keyword is: " + trend_keyword)

    # # creation of the name for the resulting files
    # artefacts_file_name = trend_keyword + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
    # # creation of the path for the video file from tiktok
    # video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"

    # # TESTED
    # # gets video title and url + aweme_id from tiktok
    # vid_title, vid_url, aweme_id = get_vid_treding(trend_keyword, NB_VOD_TO_COMP, video_file_path)
    # print("Video found: " + vid_title)
    # print("Vod URL: " + vid_url)
    # print("Vid id: " + aweme_id)

    # # TESTED
    # # gets comments from tiktok video
    # vid_comments = get_vod_comments(aweme_id, NB_COMMENTS_TO_GET)
    # print("Nb of comments: " + str(len(vid_comments)))
    
    # to remove
    vid_title = "#transition "
    vid_comments = "How u fill a beach with coke,Why so clean,If imma be honest this one better than the salt transition vid,THAT WAS SMOOTH 🔥🔥🔥🔥🔥,y’all don’t know about them musically transitions 🥶,WHATATA,that’s crazyyyy,God this was smooth,ryangoslinglover369,why does my coffee taste salty,THIS IS THE BEST ONE YET,👈🏾 my honest reaction,this one wins undoubtedly 😏,HE COOKED🔥🔥🔥🔥🔥🔥🔥🔥AND I ORDERED 🔥🔥🔥🔥🔥,How are ppl so good at transitions 😭,Now I’m gonna see waves and think coffee bubbles,Y’all sleeping on the kung fu panda 3 transitions (maybe I think they cool because I was zooted),The best transition ever,Nice, but the salt transition better,OK THAT WAS CLEAN,Add a spinning skull and it’ll be perfect,and bro made this on an android 💀,At this point we can’t even say which one‘s the best - y’all ate 😮‍💨,DAMNNN🔥🔥🔥🔥,wow mezing,got me confused for a while,Love this trend,yall haven't seen the 'SALTIEST' one?,That looked like a transition in a James Bond movie,SO MANY PEOPLE ARE PUTTING FIRE EMOJIS🔥🔥🔥🔥🔥🔥,HOWWW😱😱😱😱😱😱,these are getting out of hand,dayum that’s sick,Nah bro this is to smooth,tufff,The best I've seen so far Wow .,That was smooth 🔥🔥🔥🔥🔥🔥🔥🔥,That’s not a beach it’s a coffee beach,WAIT I DIDN'T HEAR NO LET HIM COOK WAS HE JUST TOO GOOD FOR THAT WAIT WHATTT HE COOKED SO HARD THE SOUND DIDN'T EVEN PLAY 🔥🔥🔥🔥🔥🔥,Ow my brain,NAH ENOUGH MY EYES GOT THAT 4K PREMIUM FILTER,see that one before,I’m doing this,I am a bad person,this is fire,THIS IS FIRE🔥🔥,dayumn!!1!!1,The perfect transation doesn't exi-,OMG🔥"
    artefacts_file_name = "Transformation_2023-10-17"
    video_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp4"
    impression = "unloved to love watch simba incredible transformation. It's trully heartwarming"
    impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # TESTED
    # gets impression text
    # impression, new_vid_title = get_impression_and_title(vid_title, ".".join(vid_comments), get_vid_duration(video_file_path))
    # new_vid_title += " #Shorts"
    # print("impression: " + impression)
    # print("new_vid_title: " + new_vid_title)

    # TESTED
    # gets second artefact "trend_keyword_tmp_date.mp3"
    # impression_file_path = ASSETS_FOLDER + "tmp_" + artefacts_file_name + ".mp3"
    # text_to_speech(impression, impression_file_path)

    # to remove 
    # impression_file_path = ASSETS_FOLDER + "tmp_" + "Transformation_2023-10-17.mp3"

    # TESTED
    # gets third artefact "trend_keyword_date.mp4"
    # final_vid_file_path = ASSETS_FOLDER + artefacts_file_name + ".mp4"
    # make_montage(video_file_path, impression_file_path, final_vid_file_path, impression)

    # to remove
    # final_vid_file_path = ASSETS_FOLDER + "FYP_2023-10-16.mp4"
    # new_vid_title = "T-Rex Transformation: When Fear Turns You Prehistoric" #Shorts
    # impression = "Hilarious video of a girl getting scared and instantly transforming into a T-Rex, complete with cross-legged walk and tiny arms, creating a true Jurassic Park moment."


    add_impression_txt(ASSETS_FOLDER + "tmp_" + artefacts_file_name + "_blurred_final.mp4", impression)

    # TESTED
    # uploads to youtube
    # upload_to_yt(final_vid_file_path, new_vid_title, impression, "22", "unlisted")

if __name__ == '__main__':
    main()