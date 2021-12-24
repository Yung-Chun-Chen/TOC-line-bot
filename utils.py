import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,ConfirmTemplate
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction

channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"
def send_fsm(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    fsm = ImageSendMessage(
        original_content_url='https://2.share.photo.xuite.net/yield.life/120e53e/19407657/1209035797_l.jpg',
        preview_image_url='https://2.share.photo.xuite.net/yield.life/120e53e/19407657/1209035797_l.jpg'
    )
    line_bot_api.reply_message(reply_token, fsm)
    return "OK"

def send_button_message(reply_token,btn_action,indicate,textdic='選擇接近的餐點',imageurl='https://2.share.photo.xuite.net/yield.life/120e53e/19407657/1209035797_l.jpg'):  
    line_bot_api = LineBotApi(channel_access_token)
    if textdic == "":
        textdic = "選擇接近的餐點"
    buttons_template = TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            thumbnail_image_url=imageurl,
            title=indicate,
            text=textdic,
            actions=btn_action
        )
    )

    line_bot_api.reply_message(reply_token, buttons_template )

    return "OK"

def send_image(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    pic = ImageSendMessage(
        original_content_url="https://2.share.photo.xuite.net/yield.life/120e53e/19407657/1209035797_l.jpg",
        preview_image_url="https://2.share.photo.xuite.net/yield.life/120e53e/19407657/1209035797_l.jpg"
    )
    line_bot_api.reply_message(reply_token, pic)
    return "OK"


def send_confirm_message( title, uptext, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)

    Confirm_template = TemplateSendMessage(
        alt_text='confirm template',
        template=ConfirmTemplate(
            title=title,
            text=uptext,
            actions=[
                MessageTemplateAction(
                    label=labels[0],
                    text=texts[0]
                ),
                MessageTemplateAction(
                    label=labels[1],
                    text=texts[1]
                ),
            ]
        )
    )

    line_bot_api.push_message( Confirm_template)

    return "Ok"
"""
def send_image_url(id, img_url):
    pass
def send_button_message(id, text, buttons):
    pass
"""
