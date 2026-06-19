from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
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

 
output_path_1 = "../output/microsoft-tts-commonvoice-catala-simple.wav"
output_path_2 = "../output/microsoft-tts-openslr-catala-simple.wav"
 


text = "Bon dia Manel, avui anem a la muntanya."
inputs = processor(text=text, return_tensors="pt")

with torch.no_grad():
    speaker_embedding1 = torch.zeros((1, model_1.config.speaker_embedding_dim))
    speech_features1 = model_1.generate_speech(inputs["input_ids"], speaker_embeddings=speaker_embedding1, vocoder=vocoder)
torchaudio.save(output_path_1, speech_features1.unsqueeze(0), 16000)

with torch.no_grad():
    speaker_embedding2 = torch.zeros((1, model_2.config.speaker_embedding_dim))
    speech_features2 = model_2.generate_speech(inputs["input_ids"], speaker_embeddings=speaker_embedding2, vocoder=vocoder)
torchaudio.save(output_path_2, speech_features2.unsqueeze(0), 16000)

print(f"Audio from model_1 saved to {output_path_1}")
print(f"Audio from model_2 saved to {output_path_2}")


