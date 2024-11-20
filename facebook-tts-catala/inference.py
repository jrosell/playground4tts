# python3 -m venv venv
# source venv/bin/activate
# pip install transformers accelerate torch torchaudio

from transformers import VitsModel, AutoTokenizer
import torch
import torchaudio

model = VitsModel.from_pretrained("facebook/mms-tts-cat")
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-cat")

text = "Bon dia Manel, avui anem a la muntanya."
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    waveform = model(**inputs).waveform

# Write the WAV file
torchaudio.save("../output/facebook-tts-catala.wav", waveform, sample_rate=model.config.sampling_rate)
