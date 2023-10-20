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


def add_vid_to_yt(category_id, description, title, tags, privacy_status, file_to_upload_path, playlist_id):
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

    vid_id = upload_vid(youtube, category_id, description, title, tags, privacy_status, file_to_upload_path)
    add_vid_to_playlist(youtube, vid_id, playlist_id)
    
    # Save the credentials for the next run
    with open(TOKEN_PATH, 'wb') as token:
        pickle.dump(credentials, token)


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

# def add_vid_to_playlist(video_id, playlist_id):
#     credentials = None

#     if os.path.exists(TOKEN_PATH):
#         with open(TOKEN_PATH, 'rb') as token:
#             credentials = Credentials.from_authorized_user_file(TOKEN_PATH)

#     # Disable OAuthlib's HTTPS verification when running locally.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     # Get credentials and create an API client
#     if credentials and credentials.expired and credentials.refresh_token:
#         credentials.refresh(Request())
#     elif not credentials or not credentials.valid:
#         flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#         credentials = flow.run_console()
    
#     youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

#     request = youtube.playlistItems().insert(
#         part="snippet",
#         body={
#             "snippet": {
#                 "playlistId": playlist_id,
#                 "resourceId": {
#                     "kind": "youtube#video",
#                     "videoId": video_id
#                 }
#             }
#         }
#     )
#     response = request.execute()

#     # Save the credentials for the next run
#     with open(TOKEN_PATH, 'w') as token:
#         token.write(credentials.to_json())
    
#     print(response)



# import os
# import google_auth_oauthlib.flow # pip3 install google-auth-oauthlib
# import googleapiclient.discovery
# import googleapiclient.errors
# from google.auth.transport.requests import Request
# from googleapiclient.http import MediaFileUpload
# import pickle
# import httplib2

# scopes = ["https://www.googleapis.com/auth/youtube"]

# def upload_to_yt(file_to_upload_path, title, description, tags, category_id, privacy_status):
#     credentials = None
#     if os.path.exists('youtube_api/token.pickle'):
#         with open('youtube_api/token.pickle', 'rb') as token:
#             credentials = pickle.load(token)

#     # Disable OAuthlib's HTTPS verification when running locally.
#     # *DO NOT* leave this option enabled in production.
#     os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#     api_service_name = "youtube"
#     api_version = "v3"
#     client_secrets_file = "youtube_api/yt-credentials.json"

#     if not credentials or not credentials.valid:
#         if credentials and credentials.expired and credentials.refresh_token:
#             credentials.refresh(Request())
#         else:
#             # Get credentials and create an API client
#             flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#                 client_secrets_file, scopes)
#             credentials = flow.run_console()
#     youtube = googleapiclient.discovery.build(
#         api_service_name, api_version, credentials=credentials)

#     request = youtube.videos().insert(
#         part="snippet,status",
#         body={
#             "snippet": {
#                 "categoryId": category_id,
#                 "description": description,
#                 "title": title,
#                 "defaultLanguage": "en_US",
#                 "tags": tags,
                
#             },
#             "status": {
#                 "privacyStatus": privacy_status,
#                 "selfDeclaredMadeForKids": True,
#             }
#         },
    
#         media_body=MediaFileUpload(file_to_upload_path)
#     )
#     response = request.execute()

#     # Save the credentials for the next run
#     with open('youtube_api/token.pickle', 'wb') as token:
#         pickle.dump(credentials, token)

#     print(response)