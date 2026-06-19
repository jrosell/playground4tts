from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import torchaudio
import requests
import pandas as pd
import numpy as np

print("loading embeddings")
url = "https://huggingface.co/datasets/Matthijs/cmu-arctic-xvectors/resolve/refs%2Fpr%2F8/data/validation-00000-of-00001.parquet"
response = requests.get(url)
with open("../output/cmu-arctic-xvectors.parquet", "wb") as f:
    f.write(response.content)
df = pd.read_parquet("../output/cmu-arctic-xvectors.parquet")
print(df.dtypes)
print(df.columns)
print(df.head())

xvectors_list = df['xvector'].to_list() 
xvectors_array = np.stack(xvectors_list)  # ara dtype = float64
speaker_embeddings = torch.tensor(xvectors_array, dtype=torch.float32)


print("loaded embeddings")

print("loading processor")
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
print("loading speecht5_tts_commonvoice_ca")
model_1 = SpeechT5ForTextToSpeech.from_pretrained("wetdog/speecht5_tts_commonvoice_ca")
print("loading speecht5_tts_openslr_ca")
model_2 = SpeechT5ForTextToSpeech.from_pretrained("wetdog/speecht5_tts_openslr_ca")
print("loading speecht5_hifigan")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
print("loaded processor, models, vocoder")

text = "Bon dia Manel, avui anem a la muntanya."
inputs = processor(text=text, return_tensors="pt")

spectrogram_1 = model_1.generate_speech(inputs["input_ids"], speaker_embeddings)
spectrogram_2 = model_2.generate_speech(inputs["input_ids"], speaker_embeddings)


with torch.no_grad():
    speech_1 = vocoder(spectrogram_1)
    speech_2 = vocoder(spectrogram_2)


# Save as .wav files
output_path_1 = "../output/microsoft-tts-commonvoice-catala.wav"
output_path_2 = "../output/microsoft-tts-openslr-catala.wav"

# Save as .wav using scipy
torchaudio.save(output_path_1, speech_1.unsqueeze(0), sample_rate=16000)  # Add batch dimension back
torchaudio.save(output_path_2, speech_2.unsqueeze(0), sample_rate=16000)  # Add batch dimension back


print(f"Audio from model_1 saved to {output_path_1}")
print(f"Audio from model_2 saved to {output_path_2}")