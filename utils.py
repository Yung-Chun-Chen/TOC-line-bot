import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction, ButtonsTemplate, MessageTemplateAction, ImageSendMessage



channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_carousel_message(reply_token, col):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = ImageCarouselTemplate(columns = col)
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

"""
def send_image_url(id, img_url):
    pass
def send_button_message(id, text, buttons):
    pass
"""








# import os

# from linebot import LineBotApi, WebhookParser
# from linebot.models import MessageEvent, TextMessage, TextSendMessage


# channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="


# def send_text_message(reply_token, text):
#     line_bot_api = LineBotApi(channel_access_token)
#     line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

#     return "OK"


# """
# def send_image_url(id, img_url):
#     pass
# def send_button_message(id, text, buttons):
#     pass
# """







