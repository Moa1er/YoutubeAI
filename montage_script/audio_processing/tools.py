import wave
import json

from vosk import Model, KaldiRecognizer

from montage_script.audio_processing.vad import mp3_to_wav

# get better model here https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
def get_word_timestamp(audio_filename):
    audio_path = mp3_to_wav(audio_filename)
    model_path = "montage_script/audio_processing/models/vosk-model-small-en-us-0.15"
    # audio_filename = "some_audio_file.wav"

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

    print(len(wordlist__with_timestamp))
    
    #TODO make sure end time of one is start_time of other

    return wordlist__with_timestamp