## RTL-SDR DEVEL

Use gqrx with an SDR device (such as the USB device shown in the image below) to send audio data to the loopback address. Then, use gqrx_recv.py to receive and assemble the audio into WAV format, which is then sent to the whisper_server.py service for speech recognition. Have fun experimenting!

<img src="screenshot.jpg" title="USB SDR" width="50%">

```zsh
➜  rtlsdr_radio2_whisper git:(master) ✗ python gqrx_recv.py
Serving on 127.0.0.1:7355...
{'text': ' Thank you.'}
^CReceived KeyboardInterrupt, exiting...
```

<img src="sdr.jpg" title="USB SDR" width="50%">

```bash
# whisper server
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install --upgrade pip accelerate fastapi uvicorn pyqt5 pyqtwebengine python-multipart
pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate "datasets[audio]"
```
