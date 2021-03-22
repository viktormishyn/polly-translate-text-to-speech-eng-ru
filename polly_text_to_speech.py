import boto3
from playsound import playsound
import os

polly = boto3.client('polly')
transl = boto3.client('translate')


def translate_text(text, source_lang, target_lang):
    response = transl.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText'], target_lang


def text_to_speech(args):
    text = args[0]
    lang = 'en-US' if args[1] == 'en' else 'ru-RU'
    voice = 'Salli' if args[1] == 'en' else 'Tatyana'
    response = polly.synthesize_speech(Text=text, LanguageCode=lang, VoiceId=voice, OutputFormat='mp3')
    body = response['AudioStream'].read()
    file_name = 'speech.mp3'

    with open(file_name, 'wb') as f:
        f.write(body)


if __name__ == '__main__':
    while True:
        text = input('\n_:')
        source_lang = 'en' if text.isascii() else 'ru'
        target_lang = 'ru' if source_lang == 'en' else 'en'
        try:
            text_to_speech(translate_text(text, source_lang, target_lang))
            playsound('speech.mp3')
        finally:
            os.remove('speech.mp3')
