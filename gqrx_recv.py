import socket
import wave
import io
import time
from pydub import AudioSegment
import requests

UDP_IP = "127.0.0.1"
UDP_PORT = 7355
RECORD_SECONDS = 10

API_URL = "http://192.168.44.44:7860/whisper_api"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Serving on {UDP_IP}:{UDP_PORT}...")

try:
    while True:
        frames = []
        start_time = time.time()

        while time.time() - start_time < RECORD_SECONDS:
            data, addr = sock.recvfrom(1024)
            frames.append(data)

        wav_buffer = io.BytesIO()
        wav_buffer.name = "debug_audio.wav"
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            wf.writeframes(b''.join(frames))
        wav_buffer.seek(0)

        response = requests.post(API_URL, files={
            "file": (wav_buffer.name, wav_buffer.read(), "audio/wav")
        })

        print(response.json())

except KeyboardInterrupt:
    print("Received KeyboardInterrupt, exiting...")

finally:
    sock.close()
