import requests 
import json
from dotenv import dotenv_values # pip3 instlal python-dotenv
import base64

secrets = dotenv_values(".env")

url = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"


def text_to_speech(text, output_path):
    data = {
      "input": {"text": text},
      "voice": {"name":  "en-US-Neural2-J", "languageCode": "en-US"},
      "audioConfig": {"audioEncoding": "MP3"}
    };

    headers = {"content-type": "application/json", "X-Goog-Api-Key": secrets['YOUTUBE_API_KEY'] }

    r = requests.post(url=url, json=data, headers=headers)
    content = json.loads(r.content)

    wav_file = open(output_path, "wb")
    decode_string = base64.b64decode(content['audioContent'])
    wav_file.write(decode_string)
