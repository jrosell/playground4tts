from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import torchaudio

print("loading processor")
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
print("loading speecht5_tts_commonvoice_ca")
model_1 = SpeechT5ForTextToSpeech.from_pretrained("wetdog/speecht5_tts_commonvoice_ca")
print("loading speecht5_tts_openslr_ca")
model_2 = SpeechT5ForTextToSpeech.from_pretrained("wetdog/speecht5_tts_openslr_ca")
print("loading speecht5_hifigan")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
print("loaded processor, models, vocoder")

print("loading embeddings")
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
print("loaded embeddings")

text = "Bon dia Manel, avui anem a la muntanya."
inputs = processor(text=text, return_tensors="pt")

speaker_embeddings = torch.tensor(embeddings_dataset[3000]["xvector"]).unsqueeze(0)
spectrogram_1 = model_1.generate_speech(inputs["input_ids"], speaker_embeddings)
spectrogram_2 = model_2.generate_speech(inputs["input_ids"], speaker_embeddings)


with torch.no_grad():
    speech_1 = vocoder(spectrogram_1)
    speech_2 = vocoder(spectrogram_2)



# Save as .wav files
output_path_1 = "../output/microsoft-tts-commonvoice-catala.wav"
output_path_2 = "../output/microsoft-tts-openslr-catala.wav"

import scipy.io.wavfile as wav

# Convert the waveform to a numpy array
speech_1 = speech_1.squeeze(0).float()  # Remove the batch dimension
speech_2 = speech_2.squeeze(0).float()  # Remove the batch dimension

# Save as .wav using scipy
torchaudio.save(output_path_1, speech_1.unsqueeze(0), sample_rate=16000)  # Add batch dimension back
torchaudio.save(output_path_2, speech_2.unsqueeze(0), sample_rate=16000)  # Add batch dimension back


print(f"Audio from model_1 saved to {output_path_1}")
print(f"Audio from model_2 saved to {output_path_2}")