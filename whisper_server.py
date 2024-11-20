#!/usr/bin/env python3
from fastapi import FastAPI, Request, UploadFile
import uvicorn
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = FastAPI()


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "./models/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)


@app.post("/whisper_api")
async def pic_detect(request: Request, file: UploadFile):
    if request.method == "POST":
        return pipe(file.file.read())


if __name__ == "__main__":
    model.eval()
    uvicorn.run(app, host="0.0.0.0", port=7860, workers=1)
