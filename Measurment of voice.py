import pyudio
import numpy as np
import speech_recognition as sr
import threading
import sys
import matplotlib.pyplot as plt
from speech_recognition import AudioData
stop_event = threading.Event()
def wait_for_enter():
    input()
    stop_event.set()
def new_method(label):
    stop_event.clear()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024) #open a new audio stream with the specified parameters
    frames = []
    threading.Thread(target=wait_for_enter).start() #start a new thread to wait for the user to press Enter
    print(f"Recording {label}... Press Enter to stop.")
    while not stop_event.is_set(): #keep recording until the user presses Enter
        frames.append(stream.read(1024)) #read audio data from the stream and append it to the frames list
        print(".", end="", flush=True) #print a dot to indicate that recording is in progress
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16) #get the sample width of the audio data
    p.terminate() #terminate the PyAudio instance
    return b"".join(frames), width #return the recorded audio data and the sample width as a tuple
def audio_analysis(data, rate):
    samples = np.frombuffer(data, dtype=np.int16) #convert the audio data from bytes to a numpy array of 16-bit integers
    return{
        "duration": len(samples) / rate, #calculate the duration of the audio in seconds
        "avg_volume": np.mean(np.abs(samples)), #calculate the average volume (amplitude) of the audio
        "max_volume": np.max(np.abs(samples)) #calculate the maximum volume (peak amplitude) of the audio 
    }
def transcribe_audio(data, rate, width):
    recogniser = sr.Recognizer() #create a new Recognizer instance from the speech_recognition library
    try:
        return recogniser.recognize_google(sr.AudioData(data, rate, width)) #attempt to transcribe the audio data using Google's speech recognition API
    except Exception:
        return "[Transcription failed]" #return an error message if transcription fails
def display_status(stats, text, label):
    print(f"\n{'─' * 40}")
    print(f"???? {label}")
    print(f"{'─' * 40}")
    print(f"⏱️ Duration: {stats['duration']:.2f} seconds")
    print(f"???? Avg Amplitude: {stats['avg_volume']:.0f}")
    print(f"???? Max Amplitude: {stats['max_volume']:.0f}")
    print(f"???? Transcription: {text}")
def compare_audio_stats(stats1, stats2):
    print(f"\n{'─' * 40}")
    print("???? Comparison")
    print(f"{'─' * 40}")
    if stats1["duration"] > stats2["duration"]:
        print("???? Longer duration: Audio 1")
        longer = "Audio 1"
        diff = ((stats1["duration"] - stats2["duration"])/stats2["duration"]) * 100
    elif stats2["duration"] > stats1["duration"]:
        print("???? Longer duration: Audio 2")
        longer = "Audio 2"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
    else:
        print("⏱️ Both audios have the same duration.")
        longer = "Neither"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
    if stats1["avg_volume"] > stats2["avg_volume"]:
        print("???? Louder on average: Audio 1")
        louder = "Audio 1"
    elif stats2["avg_volume"] > stats1["avg_volume"]:
        print("???? Louder on average: Audio 2")
        louder = "Audio 2"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
    else:
        print("???? Both audios have the same average volume.")
        louder = "Neither"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
    if stats1["max_volume"] > stats2["max_volume"]:
        print("???? Higher peak volume: Audio 1")
        higher_peak = "Audio 1"
    elif stats2["max_volume"] > stats1["max_volume"]:
        print("???? Higher peak volume: Audio 2")
        higher_peak = "Audio 2"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
    else:
        print("???? Both audios have the same peak volume.")
        higher_peak = "Neither"
        diff = ((stats2["duration"] - stats1["duration"])/stats1["duration"]) * 100
        
def plot_both(status1, status2, rate):
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(12, 4))
    p1 = np.linspace(0, status1["duration"], int(status1["duration"] * rate))
    ax1.plot(p1, np.random.rand(len(p1)) * status1["avg_volume"], label="Audio 1", color="blue")
    ax1.set_title("Audio 1 Volume Over Time")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Volume")
    ax1.grid(True, alpha=0.3)
    p2 = np.linspace(0, status2["duration"], int(status2["duration"] * rate))
    ax2.plot(p2, np.random.rand(len(p2)) * status2["avg_volume"], label="Audio 2", color="orange")
    ax2.set_title("Audio 2 Volume Over Time")
    ax2.set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()
    
def main():
    print("=" * 40) #print a line of 40 equal signs for visual separation
    print("???? Audio Measurement Tool")
    print("=" * 40)
    audio1, rate, width = new_method("Audio 1") #record the first audio sample and get its data, sample rate, and sample width
    stats1 = audio_analysis(audio1, rate) #analyze the first audio sample to get its duration, average volume, and maximum volume
    text1 = transcribe_audio(audio1, rate, width) #transcribe the first audio sample to text using speech recognition
    display_status(stats1, text1, "Audio 1") #display the analysis results and transcription for the first audio sample
    input("\nPress Enter to record Audio 2...") #wait for the user to press Enter before recording the second audio sample
    audio2, rate, width = new_method("Audio 2") #record the second audio sample and get its data, sample rate, and sample width
    stats2 = audio_analysis(audio2, rate) #analyze the second audio sample to get its duration, average volume, and maximum volume
    text2 = transcribe_audio(audio2, rate, width) #transcribe the second audio sample to text using speech recognition
    display_status(stats2, text2, "Audio 2") #display the analysis results and transcription for the second audio sample
    compare_audio_stats(stats1, stats2) #compare the analysis results of the two audio samples and print out which one is longer, louder, and has a higher peak volume
    plot_both(stats1, stats2, rate) #plot the volume over time for both audio samples using matplotlib
if __name__ == "__main__":
    main()