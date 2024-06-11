import json
# from gtts import gTTS
import os
import time
import random

from google.cloud import texttospeech as tts

import textwrap

def text_to_wav(voice_name: str, text: str, file_name: str):
    language_code = "-".join(voice_name.split("-")[:2])
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    client = tts.TextToSpeechClient()
    
    # Split text into chunks with maximum length of 2000 characters
    chunks = textwrap.wrap(text, width=2000, break_long_words=False)
    
    # Generate WAV file for each chunk
    for i, chunk in enumerate(chunks):
        response = client.synthesize_speech(
            input=tts.SynthesisInput(text=chunk),
            voice=voice_params,
            audio_config=audio_config,
        )
        with open(f"{file_name}_{i}.mp3", "wb") as out:
            out.write(response.audio_content)
            print(f"Chunk {i} done!")
    
    # Concatenate all WAV files into a single file
    with open(f"{file_name}.mp3", "wb") as out:
        for i, _ in enumerate(chunks):
            with open(f"{file_name}_{i}.mp3", "rb") as in_file:
                out.write(in_file.read())
        os.system(f"rm {file_name}_*.mp3")
        print(f"File {file_name}.mp3 done!")
        
        
def format_date(date):
    '''Format date to be spoken by the TTS engine'''
    months = {
        '01': 'Janeiro',
        '02': 'Fevereiro',
        '03': 'Março',
        '04': 'Abril',
        '05': 'Maio',
        '06': 'Junho',
        '07': 'Julho',
        '08': 'Agosto',
        '09': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro'
    }
    
    day = date[8:10]
    month = months[date[5:7]]
    year = date[:4]
    
    return f"dia {day} de {month} de {year}"
           
    

def main():
    folder = '/Users/rdsilva01/Desktop/GITHUB_REPO_ARQUIVONC/news_data'
    
    nid_list = []
    
    voice_fem = "pt-PT-Wavenet-D"
    voice_masc = "pt-PT-Wavenet-B"
    
    for year in range(2016,2020):
        with open(f'{folder}/{year}/key_moments_photos_{year}_tmp_5.json', 'r') as f:
            data = json.load(f)
        
        articles_processed = 0
        last_article = -1
        for i,article in enumerate(data):
            if i > last_article:
                nid = article['nid']
                if nid not in nid_list:
                # if nid not in nid_list:
                    title = article['title']
                    content = article['content']
                    text_snippet = article['text_snippet']
                    if text_snippet != "":
                        content = content.replace(text_snippet, text_snippet + ".")
                        content = content.replace("..", ".")
                        #print(content[:200])
                    
                    author = article['author']
                    date = article['date']
                    date = format_date(date)
                    text = date + ". " + title + '. ' + content
                    if author != "":
                        text += '. Esta notícia foi escrita por: ' + author
                        
                    text += '. Ouvida a partir do ArquivoNC, o arquivo web do Notícias da Covilhã.'
                
                    while True:
                        try:
                            text_to_wav(voice_fem, text, f"{nid}_fem")
                            text_to_wav(voice_masc, text, f"{nid}_masc")
                            articles_processed += 1
                            print(f"Article {nid} done!")
                            break
                        except Exception as e:
                            print(f"Error processing article {nid}: {e}")
                            print("Retrying after waiting...")

        
        print(f"Year {year} done! Articles processed: {articles_processed}")
    
    print("All articles done!")

if __name__ == '__main__':
    main()
