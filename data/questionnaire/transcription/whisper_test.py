from openai import OpenAI
from os import getcwd, listdir
from os.path import isfile, join
from regex import findall
from pandas import DataFrame

#####################
client = OpenAI()

audio_files_path = getcwd() + "\\transcription\\audio_files"
audio_files = [f for f in listdir(audio_files_path) if isfile(join(audio_files_path, f))]

name_list = []
text_list = []

for file in audio_files:
    name = findall('(.*).m4a', file)[0]
    name_list.append(name)
    audio_file= open(getcwd() + "\\transcription\\audio_files\\" + file, "rb")
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    text = transcription.text
    text_list.append(text)
    print("Finished transcribing the file %s" % file)

print("Finished")

# generate new dataframe
df_dict = {
	'name': name_list,
	'text': text_list
}
transcription_df = DataFrame(df_dict)

# write new dataframe to csv file
dest_path = getcwd() + "\\transcription\\transcription.csv"
transcription_df.to_csv(dest_path, index=False)

print(" Successfully written transcription data to csv file! \n")