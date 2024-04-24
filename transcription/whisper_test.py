from openai import OpenAI
from os import getcwd

client = OpenAI()

audio_file= open(getcwd() + "\\transcription\\test_mp3.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)