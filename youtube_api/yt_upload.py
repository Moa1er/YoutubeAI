import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from telegram_bot.telegram_bot import *
import builtins
import io
from contextlib import redirect_stdout
import sys
from pyKey import sendSequence
import threading
import cursor
cursor.hide()


SCOPES = ["https://www.googleapis.com/auth/youtube"]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
TOKEN_PATH = 'youtube_api/token.pickle'
CLIENT_SECRETS_FILE = "youtube_api/yt-credentials.json"


def add_vid_to_yt(
        category_id, 
        description, 
        title, 
        tags, 
        privacy_status, 
        file_to_upload_path, 
        playlist_id, 
        thumbnail_path
        ):
    credentials = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            credentials = pickle.load(token)

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        authorization_url, _ = flow.authorization_url()
        #sends auth url on my telegram
        send_telegram_message(authorization_url)
        # waits 300s for me to give the code
        response = read_telegram_messages()
        # sends the code delayed as key pressed to give it to the console
        # this is fricking genius
        t = threading.Thread(target=delayed_keyStrokes, args=(response,))
        t.start()
        credentials = flow.run_console()

    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        # Save the credentials for the next run
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(credentials, token)
        
    # upload video
    vid_id = upload_vid(youtube, category_id, description, title, tags, privacy_status, file_to_upload_path)
    # make video in playlist
    add_vid_to_playlist(youtube, vid_id, playlist_id)
    # gives it a thumbnail
    add_thumbnail(youtube, vid_id, thumbnail_path)
    


def delayed_keyStrokes(string_to_send):
    time.sleep(1)
    sendSequence(string_to_send + '\n')

def upload_vid(youtube, category_id, description, title, tags, privacy_status, file_to_upload_path):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category_id,
                "description": description,
                "title": title,
                "defaultLanguage": "en_US",
                "tags": tags,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": True,
            }
        },
        media_body=MediaFileUpload(file_to_upload_path)
    )
    response = request.execute()

    print(response)

    return response["id"]

def add_vid_to_playlist(youtube, video_id, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()

    print(response)

def add_thumbnail(youtube, video_id, thumbnail_path):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path, mimetype='image/jpeg', chunksize=-1, resumable=True)
    )
    response = request.execute()

    print(response)