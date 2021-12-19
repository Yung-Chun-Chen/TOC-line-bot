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







import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from random import choice
'''from bs4 import BeautifulSoup'''
import requests

channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="
food = ['鴨肉飯', '乾麵', '港式燒臘', '鍋燒意麵', '炒飯', '拉麵', '餛飩麵']
photo = ['https://images.zi.org.tw/ireneslife/2018/08/23222608/1535034368-95cf834c4d3687e1347ed20f3cdb7cab.jpg', 
'http://findlife.com.tw/menu/blog/wp-content/uploads/2019/04/2.jpg',
'https://fairylolita.com/wp-content/uploads/DSCF3995.jpg', 
'https://img-fnc.ebc.net.tw/EbcFnc/news/2018/01/31/1517406213_92145.jpg',
'https://i3.achangpro.com/img.mimihan.tw/pixnet/fec65ae09161ffaa49a6bb84166f2aa7.jpg',
]
'''res = requests.get('https://www.foodpanda.com.tw/city/tainan-city')
soup = BeautifulSoup(res.text,'html.parser')
'''

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_image_url(reply_token):
	line_bot_api = LineBotApi(channel_access_token)
	image_url = choice(photo)
	message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
	line_bot_api.reply_message(reply_token, message)
	
def send_food_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=choice(food)))
    return "OK"

def send_allfood_message(reply_token):
    text = ""
    line_bot_api = LineBotApi(channel_access_token)
    for x in range(len(food)): 
        text += food[x] 
    line_bot_api.reply_message(reply_token, TextSendMessage(text="現在有：\n" + ", ".join(food)))
    return "OK"

def add_food_message(recieved_message):
    food.append(recieved_message)

def delete_food_message(recieved_message):
	food.remove(recieved_message)

def is_food(recieved_message):
	return recieved_message in food
'''
def send_button_message(id, text, buttons):
    pass
'''