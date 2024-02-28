import http.client
import urllib.request
import json
import datetime
import time
from montage_script.audio_processing.vad import does_video_have_human_voice
from dotenv import dotenv_values # pip3 instlal python-dotenv

secrets = dotenv_values(".env")
api_keys = secrets['RAPID_API_KEY'].split(",")

# unofficial TikTok API endpoints
# 50 requests max per day
headers = {
    'X-RapidAPI-Key': api_keys[0],
    'X-RapidAPI-Host': "scraptik.p.rapidapi.com"
}

conn = http.client.HTTPSConnection("scraptik.p.rapidapi.com")

# don't know what it is, default value
OFFSET = "0"
# dont know what it is
USE_FILTER = "1"
# takes the last 7 days
VIDEO_PERIOD = "7"
# means most liked
SORT_TYPE = "1"

# PARTS THAT SEARCH FOR VIDEOS WITH A CERTAIN KEYWORD AND GET NAME AND LINK
def get_vid_treding (search_keyword, nb_vid_to_scrape, nb_vid_to_return):
    data = make_request(search_keyword, nb_vid_to_scrape, headers)

    while("message" in data):
        print("Error: " + data["message"])
        print("Trying with another API key")
        api_keys.pop(0)
        if len(api_keys) == 0:
            print("No more API keys, exiting")
            exit()
            
        headers['X-RapidAPI-Key'] = api_keys[0]

        data = make_request(search_keyword, nb_vid_to_scrape, headers)

    # saves data if we want to read it without calling the api againnn
    with open("data/data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + ".json", "w") as file:
        json.dump(data, file) 

    # CODE TO GET TOP 3 VIDEOS
    share_counts = []

    for i in range(len(data["data"])):
        if data['data'][i].get("aweme_info") is not None:
            statistics = data["data"][i]["aweme_info"].get("statistics")
            if statistics is not None:
                share_count = int(statistics.get("share_count", 0))
                whatsapp_share_count = int(statistics.get("whatsapp_share_count", 0))
                total_share = share_count + whatsapp_share_count
                share_counts.append((total_share, i))

    # Sort the list by share count in descending order and get top "nb_vid_to_return"
    sorted_share_counts = sorted(share_counts, key=lambda x: x[0], reverse=True)[:nb_vid_to_return]

    # Extract the indexes of the top "nb_vid_to_return" elements
    top_x_indexes = [item[1] for item in sorted_share_counts]

    # Get the top "nb_vid_to_return" videos
    vid_titles = [data["data"][i]["aweme_info"]["desc"] for i in top_x_indexes]
    vid_urls = [data["data"][i]["aweme_info"]["video"]["bit_rate"][0]["play_addr"]["url_list"][2] for i in top_x_indexes]
    aweme_ids = [data["data"][i]["aweme_info"]["aweme_id"] for i in top_x_indexes]
    
    return vid_titles, vid_urls, aweme_ids

def make_request(search_keyword, nb_vid_to_scrape, headers):
    try:
        conn.request("GET", 
            "/search?keyword=" + search_keyword 
            + "&count=" + nb_vid_to_scrape 
            + "&offset=" + OFFSET
            + "&use_filters=" + USE_FILTER
            + "&publish_time=" + VIDEO_PERIOD 
            + "&sort_type=" + SORT_TYPE
            , headers=headers
        )

        res = conn.getresponse()
        tmpData = res.read().decode()
        return json.loads(tmpData)

    except Exception as e:
        print(f"An error occurred: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        return make_request(search_keyword, nb_vid_to_scrape, headers)


def choose_vid_no_human_voice(vid_titles, vid_urls, aweme_ids, video_file_path):
    idx_vid = 0
    download_vod(vid_urls[0], video_file_path)
    while(does_video_have_human_voice(video_file_path) and idx_vid < 2):
        idx_vid += 1
        print("Video has human voice, downloading another one")
        download_vod(vid_urls[idx_vid], video_file_path)
    if does_video_have_human_voice(video_file_path):
        print("No video without human voice found")
        exit()
    
    return vid_titles[idx_vid], vid_urls[idx_vid], aweme_ids[idx_vid]

def get_vod_comments (aweme_id, nb_comment_to_get):
    conn.request("GET", "/list-comments?aweme_id=" + aweme_id + "&count=" + nb_comment_to_get + "&cursor=0", headers=headers)
    res = conn.getresponse()
    tmp_data = res.read()
    comments_data = json.loads(tmp_data)
    comments_list = []

    for i in range(len(comments_data["comments"])):
        comments_list.append(comments_data["comments"][i]["text"])

    return comments_list

def download_vod (vid_url, artefacts_file_name):
    urllib.request.urlretrieve(vid_url, artefacts_file_name)
