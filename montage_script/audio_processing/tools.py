import wave
import json
from mutagen.mp3 import MP3 # pip install mutagen

from vosk import Model, KaldiRecognizer

from montage_script.audio_processing.vad import mp3_to_wav

# get better model here https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
def get_word_timestamp(audio_filename):
    #TO REMOVE
    audio_path = mp3_to_wav(audio_filename)
    # if not downloded bigger model, uncomment this
    # model_path = "montage_script/audio_processing/models/vosk-model-small-en-us-0.15"
    # bigger model that needs to me downloaded. It is rly more precise so use this one
    # there is a model even more precise but I don't think it is needed as this model
    # already make no mistake (for now)
    model_path = "montage_script/audio_processing/models/vosk-model-en-us-0.22"

    model = Model(model_path)
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)  # Include the start and end times for each word in the output

    # get the list of JSON dictionaries
    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    wf.close()  # close audiofile

    wordlist__with_timestamp = []

    for i in range(0, len(results[0]["result"])):
        start_time = results[0]["result"][i]["start"]
        end_time = results[0]["result"][i]["end"]
        wordlist__with_timestamp.append((start_time, end_time))    

    return verify_timestamps(wordlist__with_timestamp, get_audio_duration(audio_path))
    
def verify_timestamps(word_timings, audio_duration):
    for i in range(1, len(word_timings)):
        prev_start, prev_end = word_timings[i-1]
        # [1] is the index of the start_time
        curr_start = word_timings[i][0]

        word_timings[i] = (word_timings[i][0], word_timings[i][1])
        # Check if the end time of the previous word is not equal to the start time of the current word
        if prev_end != curr_start:
            word_timings[i-1] = (prev_start, curr_start)
        
        if i == len(word_timings) - 1:
            word_timings[i] = (word_timings[i][0], word_timings[i][1])
            
    return word_timings

def get_audio_duration(audio_file_path):
    duration_seconds = 0
    with wave.open(audio_file_path) as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
    return duration_seconds

def get_audio_duration_mp3(audio_file_path):
    audio = MP3(audio_file_path)
    return audio.info.length