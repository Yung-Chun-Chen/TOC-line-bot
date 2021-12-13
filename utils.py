import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage


channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
