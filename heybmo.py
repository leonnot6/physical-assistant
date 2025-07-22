import pvporcupine
import pyaudio
import struct
import subprocess
import os

WAKE_WORD_PATH = "Hey-Bee-Mow_en_raspberry-pi_v3_0_0"  # Your downloaded wake word file
ASSISTANT_SCRIPT = "bmpotest5.py"  # Your voice music script

def main():
    porcupine = pvporcupine.create(keyword_paths=[WAKE_WORD_PATH])
    
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
                print("Wake word detected!")
                subprocess.Popen(["python3", ASSISTANT_SCRIPT])
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    main()
