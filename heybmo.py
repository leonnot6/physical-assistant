import pvporcupine
import pyaudio
import struct
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import psutil

def is_assistant_running(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if script_name in proc.info['cmdline']:
            return True
    return False

# Set up Spotipy with your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state user-read-playback-state"
))

ACCESS_KEY = "by5UgBvBtiuXU/4OFLSAsQV58EN2mApZU8820RWDwgrIX7XEB+hu/g=="  # Replace with your key
WAKE_WORD_PATH = "Hey-Bee-Mow_en_raspberry-pi_v3_0_0.ppn"       # Custom wake word file
ASSISTANT_SCRIPT = "bpmotest5.py"  # Your music assistant

def main():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[WAKE_WORD_PATH]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for 'Hey BMO'...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm_unpacked)

            if result >= 0:
    print("Wake word detected! Pausing music...")
    try:
        sp.pause_playback()
    except SpotifyException as e:
        print(f"Spotify error: {e}")
    if not is_assistant_running(ASSISTANT_SCRIPT):
        subprocess.Popen(["python3", ASSISTANT_SCRIPT])
    time.sleep(2)


    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
