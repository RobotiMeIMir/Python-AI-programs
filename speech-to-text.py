from cProfile import label
import threading #record a audio more than once and can analyze it at the same time
import sys #syste,
try:
    import pyaudio
    import numpy as np
    import matplotlib.pyplot as plt
    import speech_recognition as sr
except ImportError as e:
    print(f"Error: {e}. Please install the required libraries: pyaudio, numpy, matplotlib, speechrecognition")
    sys.exit(1)
    
stop_event = threading.Event()
def wait_for_enter():
    input()
    stop_event.set()
def audio_rec(label):
    stop_event.clear()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    print(f"Recording {label}... Press Enter to stop.")
    threading.Thread(target=wait_for_enter).start()
    print("Listening...", end="", flush=True)
    while not stop_event.is_set():
        frames.append(stream.read(1024))
        print(".", end="", flush=True)

    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b"".join(frames), width
def audio_analysis(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    return{
        "duration": len(samples) / rate,
        "peak": np.max(np.abs(samples)),
        "rms": np.sqrt(np.mean(samples**2))
    }
def transcribe_audio(data, rate, wodth):
    recogniser = sr.Recognizer()
    try:
        return recogniser.recognize_google(sr.AudioData(data, rate, wodth))
    except Exception:
        return "[Transcription failed]"
def display_status(status, text, label):
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
        diff = stats1["duration"] - stats2["duration"]
    else:
        print("???? Longer duration: Audio 2")
        longer = "Audio 2"
        diff = stats2["duration"] - stats1["duration"]
    if stats1["avg_volume"] > stats2["avg_volume"]:
        louder = "Audio 1"
        diff = stats1["avg_volume"] - stats2["avg_volume"]
    else:
        louder = "Audio 2"
        diff = stats2["avg_volume"] - stats1["avg_volume"]
    print(f"???? Louder: {louder}")
def new_method(status1, status2, rate):
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
    audio1, rate, width = audio_rec("Audio 1")
    stats1 = audio_analysis(audio1, rate)
    text1 = transcribe_audio(audio1, rate, width)
    display_status(stats1, text1, "Audio 1")
    input("\nPress Enter to record Audio 2...")
    audio2, rate, width = audio_rec("Audio 2")
    stats2 = audio_analysis(audio2, rate)
    text2 = transcribe_audio(audio2, rate, width)
    display_status(stats2, text2, "Audio 2")
    compare_audio_stats(stats1, stats2)
    new_method(stats1, stats2, rate)
if __name__ == "__main__":
    main()