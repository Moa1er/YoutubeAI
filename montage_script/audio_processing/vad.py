import collections
import contextlib
import wave
import webrtcvad
from pydub import AudioSegment
import wave
import numpy as np
import librosa    
import soundfile as sf
import subprocess


## THE ORIGINAL CODE FOR THE VAD CAN BE FOUND HERE :
## https://github.com/wiseman/py-webrtcvad/blob/master/example.py

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)


class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data.

    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.

    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_collector(sample_rate, frame_duration_ms,
                  padding_duration_ms, vad, frames):
    """Filters out non-voiced audio frames.

    Given a webrtcvad.Vad and a source of audio frames, yields only
    the voiced audio.

    Uses a padded, sliding window algorithm over the audio frames.
    When more than 90% of the frames in the window are voiced (as
    reported by the VAD), the collector triggers and begins yielding
    audio frames. Then the collector waits until 90% of the frames in
    the window are unvoiced to detrigger.

    The window is padded at the front and back to provide a small
    amount of silence or the beginnings/endings of speech around the
    voiced frames.

    Arguments:

    sample_rate - The audio sample rate, in Hz.
    frame_duration_ms - The frame duration in milliseconds.
    padding_duration_ms - The amount to pad the window, in milliseconds.
    vad - An instance of webrtcvad.Vad.
    frames - a source of audio frames (sequence or generator).

    Returns: A generator that yields PCM audio data.
    """
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    # We use a deque for our sliding window/ring buffer.
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    # We have two states: TRIGGERED and NOTTRIGGERED. We start in the
    # NOTTRIGGERED state.
    triggered = False

    voiced_frames = []
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if not triggered:
            ring_buffer.append((frame, is_speech))
            num_voiced = len([f for f, speech in ring_buffer if speech])
            # If we're NOTTRIGGERED and more than 90% of the frames in
            # the ring buffer are voiced frames, then enter the
            # TRIGGERED state.
            if num_voiced > 0.9 * ring_buffer.maxlen:
                triggered = True
                # We want to yield all the audio we see from now until
                # we are NOTTRIGGERED, but we have to start with the
                # audio that's already in the ring buffer.
                for f, s in ring_buffer:
                    voiced_frames.append(f)
                ring_buffer.clear()
        else:
            # We're in the TRIGGERED state, so collect the audio data
            # and add it to the ring buffer.
            voiced_frames.append(frame)
            ring_buffer.append((frame, is_speech))
            num_unvoiced = len([f for f, speech in ring_buffer if not speech])
            # If more than 90% of the frames in the ring buffer are
            # unvoiced, then enter NOTTRIGGERED and yield whatever
            # audio we've collected.
            if num_unvoiced > 0.9 * ring_buffer.maxlen:
                # sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                triggered = False
                yield b''.join([f.bytes for f in voiced_frames])
                ring_buffer.clear()
                voiced_frames = []
    # If we have any leftover voiced audio when we run out of input,
    # yield it.
    if voiced_frames:
        yield b''.join([f.bytes for f in voiced_frames])


def mp3_to_wav(audio_file_path):
    # files definition                                                                         
    src = audio_file_path
    dst = audio_file_path.split(".")[0] + "_new_format.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    wav_file = wave.open(dst)
    save_wav_channel(dst, wav_file, 0)
    y, s = librosa.load(dst, sr=32000)
    sf.write(dst, y, 32000, 'PCM_16')

    return dst

def save_wav_channel(fn, wav, channel):
    '''
    Take Wave_read object as an input and save one of its
    channels into a separate .wav file.
    '''
    # Read data
    nch   = wav.getnchannels()
    depth = wav.getsampwidth()
    wav.setpos(0)
    sdata = wav.readframes(wav.getnframes())

    # Extract channel data (24-bit data not supported)
    typ = { 1: np.uint8, 2: np.uint16, 4: np.uint32 }.get(depth)
    if not typ:
        raise ValueError("sample width {} not supported".format(depth))
    if channel >= nch:
        raise ValueError("cannot extract channel {} out of {}".format(channel+1, nch))
    # print ("Extracting channel {} out of {} channels, {}-bit depth".format(channel+1, nch, depth*8))
    data = np.fromstring(sdata, dtype=typ)
    ch_data = data[channel::nch]

    # Save channel to a separate file
    outwav = wave.open(fn, 'w')
    outwav.setparams(wav.getparams())
    outwav.setnchannels(1)
    outwav.writeframes(ch_data.tostring())
    outwav.close()

def does_video_have_human_voice(vid_file_path):
    audio_file_path = vid_file_path.split(".")[0] + "_video_sound.mp3"
    get_audio_from_video(vid_file_path, audio_file_path)
    new_file_name = mp3_to_wav(audio_file_path)
    audio, sample_rate = read_wave(new_file_name)
    #level of agressivness
    vad = webrtcvad.Vad(1)
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = vad_collector(sample_rate, 30, 300, vad, frames)
    
    nb_part = sum(1 for dummy in enumerate(segments))

    return True if nb_part > 1 else False

def get_audio_from_video(video_file, video_audio_name): 
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    subprocess.call(["ffmpeg", "-y", "-i", video_file, video_audio_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    
def get_no_voice_clip(audio_file_path):
    new_file_name = mp3_to_wav(audio_file_path)
    audio, sample_rate = read_wave(new_file_name)
    #level of agressivness
    vad = webrtcvad.Vad(1)
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    segments = vad_collector(sample_rate, 30, 300, vad, frames)

    file_name_attr = new_file_name.split(".")
    voice_free_audio_file_name = file_name_attr[0] + "_part2." + file_name_attr[1]
    
    nb_part = sum(1 for dummy in enumerate(segments))
    # print("Nb of cuts in original voice: (if 1 then no human voice)", nb_part)
    if nb_part == 1:
        return None
    elif nb_part == 2:
        for i, segment in enumerate(segments):
            if i == 0:
                continue
            elif i == 1:
                write_wave(voice_free_audio_file_name, segment, sample_rate)
    #todo instead of exit make it so that it merges the rest of the videos together bc it's ok if
    #there is a human voice in the middle/end of the video
    else:
        print("ERROR in get_no_voice_clip() vad.py")
        exit
    return voice_free_audio_file_name

    #OTHER WAY TO CALCULATE THE NB OF SECOND IF FIRST DOESN"T WORK
    #BUT NOT EFFICIENT LUL
    # segment_path = audio_file_path.split(".")[0] + '_chunk.wav'
    # for i, segment in enumerate(segments):
    #     print(' Writing %s' % (segment_path,))
    #     write_wave(segment_path, segment, sample_rate)
    #     #just want the first segment
    #     break
    # return get_audio_duration(segment_path)