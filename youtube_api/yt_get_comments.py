from dotenv import dotenv_values # pip3 instlal python-dotenv
import os
import googleapiclient.discovery # pip3 install google-api-python-client

secrets = dotenv_values("../.env")

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = secrets['YOUTUBE_API_KEY']

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="B8yg1x5ohG0",
    )
    response = request.execute()

    allComments = []
    for i in range(0, len(response['items'])):
        allComments.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'])
    if len(allComments) == 0:
        print(response)
    else:
        print(allComments)

    print(response)


if __name__ == "__main__":
    main()