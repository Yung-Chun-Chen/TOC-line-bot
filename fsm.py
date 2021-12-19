# from transitions.extensions import GraphMachine

# from utils import send_text_message


# class TocMachine(GraphMachine):
#     def __init__(self, **machine_configs):
#         self.machine = GraphMachine(model=self, **machine_configs)

#     def is_going_to_state1(self, event):
#         text = event.message.text
#         return text.lower() == "go to state1"

#     def is_going_to_state2(self, event):
#         text = event.message.text
#         return text.lower() == "go to state2"

#     def on_enter_state1(self, event):
#         print("I'm entering state1")

#         reply_token = event.reply_token
#         send_text_message(reply_token, "Trigger state1")
#         self.go_back()

#     def on_exit_state1(self):
#         print("Leaving state1")

#     def on_enter_state2(self, event):
#         print("I'm entering state2")

#         reply_token = event.reply_token
#         send_text_message(reply_token, "Trigger state2")
#         self.go_back()

#     def on_exit_state2(self):
#         print("Leaving state2")



from transitions.extensions import GraphMachine

import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

from utils import send_text_message, send_carousel_message, send_button_message, send_image_message

import requests as rs
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import twstock

import time,datetime
from datetime import datetime,timezone,timedelta

stock_number=0
dt = datetime.utcnow()
dt = dt.replace(tzinfo=timezone.utc)
tzutc_8 = timezone(timedelta(hours=8))
local_dt = dt.astimezone(tzutc_8)
local_dt=str(local_dt)
hour_time=local_dt[11]+local_dt[12]+local_dt[14]+local_dt[15]
hour_time=int(hour_time)
print(hour_time)
weekdays=int(datetime.today().weekday())


#import message_template

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text == "早安" 

    def on_enter_menu(self, event):
        title = '請選擇您要查詢的項目'
        text = '『匯率』還是『台灣股市』還是『查看fsm結構圖』'
        btn = [
            MessageTemplateAction(
                label = '匯率',
                text ='匯率'
            ),
            MessageTemplateAction(
                label = '台灣股市',
                text = '台灣股市'
            ),
        ]
        url = 'https://image.flaticon.com/icons/png/512/438/438526.png'
        send_button_message(event.reply_token, title, text, btn, url)


    def is_going_to_exchange(self, event):
        text = event.message.text
        if (text == '匯率'):
            return True
        return False

    def on_enter_exchange(self, event):
        title = '請選擇您要查詢的幣別'
        text = '『美金』 『日元』 『人民幣』 『其他』'
        btn = [
            MessageTemplateAction(
                label = '美金',
                text ='美金'
            ),
            MessageTemplateAction(
                label = '日元',
                text = '日元'
            ),
            MessageTemplateAction(
                label = '人民幣',
                text = '人民幣'
            ),
            MessageTemplateAction(
                label = '其他',
                text = '其他'
            ),
        ]
        url = 'https://i.imgur.com/MPY9qbQ.png'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_exchange_USD(self, event):
        text = event.message.text
        return text == "美金"

    def on_enter_exchange_USD(self, event):
        index=1
        value_USD = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_USD+'\n輸入「早安」回到主選單'))
        self.go_back()

    def is_going_to_exchange_JPY(self, event):
        text = event.message.text
        return text == "日元"

    def on_enter_exchange_JPY(self, event):
        index=2
        value_JPY = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_JPY+'\n輸入「早安」回到主選單'))
        self.go_back()

    def is_going_to_exchange_CNY(self, event):
        text = event.message.text
        return text == "人民幣"

    def on_enter_exchange_CNY(self, event):
        index=3
        value_CNY = get_exchange_value(index)
        reply_token = event.reply_token
        send_text_message(reply_token, str(value_CNY+'\n輸入「早安」回到主選單'))
        self.go_back()

    def is_going_to_exchange_else(self, event):
        text = event.message.text
        return text == "其他"

    def on_enter_exchange_else(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請至台灣銀行官網查詢： \n https://rate.bot.com.tw/xrt?Lang=zh-TW"+'\n輸入「早安」回到主選單')
        self.go_back()


    def is_going_to_stock(self, event):
        text = event.message.text
        if text == '台灣股市':
            return True
        return False

    def on_enter_stock(self, event):
        title = '請選擇您要查詢的項目'
        text = '『股票股價』 『股票基本面』『其他』'
        btn = [
            MessageTemplateAction(
                label = '股票股價',
                text ='股票股價'
            ),
            MessageTemplateAction(
                label = '股票基本面',
                text = '股票基本面'
            ),
            MessageTemplateAction(
                label = '其他資訊',
                text = '其他資訊'
            ),

        ]
        url = 'https://i.imgur.com/DwpLSha.png'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_price(self, event):
        text = event.message.text
        return text == "股票股價"
    
    def on_enter_price(self, event):
        send_text_message(event.reply_token, '請輸入股票代碼')

    
    def is_going_to_show_price(self, event):
        global stock_number
        text = event.message.text
        stock_number=str(text)
        return True
    
    def on_enter_show_price(self, event):
        global stock_number
        stock = twstock.Stock(stock_number)
        reply_token = event.reply_token
        
        

        if weekdays==5 or weekdays==6:
            send_text_message(reply_token, '今日為週末，未開盤 \n近5個開盤日股價為： \n'+ str(stock.price[-5:])+'\n輸入「早安」回到主選單')
        else:
            if hour_time<900:
                send_text_message(reply_token, '今日尚未開盤\n近5個開盤日股價為： \n'+ str(stock.price[-5:])+'\n輸入「早安」回到主選單')
            elif hour_time>=900 and hour_time<1330:
                send_text_message(reply_token, '目前開盤中，查詢時間為：'+str(local_dt)+'\n 近4個開盤日股價及現在股價為： \n'+ str(stock.price[-5:])+'\n輸入「早安」回到主選單')
            elif hour_time>=1330:
                send_text_message(reply_token, '今日已收盤\n近4個開盤日股價及今日收盤股價為： \n'+ str(stock.price[-5:])+'\n輸入「早安」回到主選單')
                
        self.go_back()


    def is_going_to_technical(self, event):
        text = event.message.text
        return text == "股票基本面"
    
    def on_enter_technical(self, event):
        send_text_message(event.reply_token, '請輸入股票代碼')

    
    def is_going_to_show_technical(self, event):
        global stock_number
        text = event.message.text
        stock_number=str(text)
        return True
    
    def on_enter_show_technical(self, event):
        global stock_number
        stock = twstock.Stock(stock_number)
        bfp = twstock.BestFourPoint(stock)
        comment=bfp.best_four_point_to_buy()
        reply_token = event.reply_token
        send_text_message(reply_token, '請至以下網址查詢： \n'+'https://tw.stock.yahoo.com/q/ta?s='+ str(stock_number)+'\n簡評：'+str(comment)+'\n\n輸入「早安」回到主選單')
        self.go_back()

    def is_going_to_stock_else(self, event):
        text = event.message.text
        return text == "其他資訊"

    def on_enter_stock_else(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請至台灣證交所官網查詢： \nhttps://www.twse.com.tw/zh/"+'\n輸入「早安」回到主選單')
        self.go_back()
    
    def is_going_to_show_fsm_pic(self,event):
        text=event.message.text
        return text.lower()=='fsm'
        
    def on_enter_show_fsm_pic(self,event):
        reply_token = event.reply_token
        url='https://raw.githubusercontent.com/CrazyRyan0812/CrazyRyan-TOC/master/fsm.png'
        send_image_message(reply_token, url)
        self.go_back()


def get_exchange_value(index):
    if index==1:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/USD')
    elif index==2:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/JPY')
    elif index==3:
        res = rs.get('https://rate.bot.com.tw/xrt/quote/ltm/CNY')
    # get html
    res.encoding = 'utf-8'
    # get data table
    soup = BeautifulSoup(res.text, 'lxml')
    table = soup.find('table', {'class': 'table table-striped table-bordered table-condensed table-hover'})
    table = table.find_all('tr')
    # remove table title
    table = table[2:]
    # add to dataframe
    col = ['掛牌日期', '幣別', '現金買入', '現金賣出', '匯率買入', '匯率賣出']
    data = []
    for row in table:
        row_data = []
        date = row.find('td',{'class':'text-center'}).text
        currency = row.find('td',{'class':'text-center tablet_hide'}).text
        cash = row.find_all('td',{'class':'rate-content-cash text-right print_table-cell'})
        sight = row.find_all('td',{'class':'rate-content-sight text-right print_table-cell'})
        row_data.append(date)
        row_data.append(currency)
        row_data.append(cash[0].text)
        row_data.append(cash[1].text)
        row_data.append(sight[0].text)
        row_data.append(sight[1].text)
        data.append(row_data)
    df = pd.DataFrame(data)
    df.columns = col
    df['掛牌日期'] = pd.to_datetime(df['掛牌日期'])
    df.set_index('掛牌日期', inplace=True)
    # value query
    pre_output=df.iloc[0]
    pre_output=str(pre_output)[:-24]
    output = pre_output.replace('Name: ','牌告日期：')
    return output