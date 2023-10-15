import requests
from dotenv import dotenv_values # pip3 instlal python-dotenv

secrets = dotenv_values(".env")

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/XrExE9yKIg1WjnnlVkGX"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": secrets['ELEVEN_LABS_API_KEY']
}

def text_to_speech(text_to_convert, file_path_name):
    data = {
      "text": text_to_convert,
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    response = requests.post(url, json=data, headers=headers)
    print(response)
    with open(file_path_name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    