import pvporcupine
import pyaudio
import struct
import subprocess

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
                print("Wake word detected! Launching music assistant...")
                subprocess.Popen(["python3", ASSISTANT_SCRIPT])
                sp.pause_playback()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
