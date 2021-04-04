# lambda function receives post request containing json with single message in Russian or in English and returns json:
# {"msg_time": <time of post request: str>, "msg_eng": <message in English: str>, "msg_eng": <message in Russian: str>"}
# The function assumes that the message is either English or Russian and doesn't use AWS language recognition service.

import json
import time
import boto3

transl = boto3.client('translate')


def translate_text(text, source_lang, target_lang):
    response = transl.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']


class Message:
    def __init__(self, msg, t):
        self.time = t
        self.original_msg = msg
        self.source_lang = 'en' if msg.isascii() else 'ru'
        self.target_lang = 'ru' if self.source_lang == 'en' else 'en'


def lambda_handler(event, context):
    body = json.loads(event["body"])
    msg = Message(body['message'], time.time())

    translated_message = translate_text(msg.original_msg, msg.source_lang, msg.target_lang)

    msg_time = msg.time
    if msg.source_lang == 'en':
        msg_en = msg.original_msg
        msg_ru = translated_message
    else:
        msg_ru = msg.original_msg
        msg_en = translated_message

    body = {
        "msg_time": msg_time,
        "msg_en": msg_en,
        "msg_ru": msg_ru
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
