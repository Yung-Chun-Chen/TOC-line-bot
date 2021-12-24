from transitions.extensions import GraphMachine
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction
# from utils import send_button_message,send_text_message,send_fsm
from utils import *

class TocMachine(GraphMachine):
    breakfast = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'} #starch:澱粉
    lunch     = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'}   
    dinner    = {'calorie':0,'starch':0,'protein':0,'money':0,'meal':'none'}
    height = 160
    weight = 60
    Totalmoney = 0
    Totalcalorie = 0
    Totalstarch = 0
    Totalprotein = 0
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    #start
    def is_going_to_start(self, event):
        text = event.message.text
        return text.lower() == "start"
    def on_enter_start(self, event):
        TocMachine.breakfast['calorie'] = 0
        TocMachine.breakfast['starch'] = 0
        TocMachine.breakfast['protein'] = 0
        TocMachine.breakfast['money'] = 0
        TocMachine.breakfast['meal'] = 'none'
        
        TocMachine.lunch['calorie'] = 0
        TocMachine.lunch['starch'] = 0
        TocMachine.lunch['protein'] = 0
        TocMachine.lunch['money'] = 0
        TocMachine.lunch['meal'] = 'none'
        
        TocMachine.dinner['calorie'] = 0
        TocMachine.dinner['starch'] = 0
        TocMachine.dinner['protein'] = 0
        TocMachine.dinner['money'] = 0
        TocMachine.dinner['meal'] = 'none'
        
        btn_action=[
            MessageTemplateAction(
                label='設定個人資訊',
                text='modified information'
            ),
            MessageTemplateAction(
                label='訂閱資訊',
                text='check nutrition'
            ),
            MessageTemplateAction(
                label='推薦電影',
                text='show suggestion'
            ),
            MessageTemplateAction(
                label='show FSM',
                text='show fsm'
            ),
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"功能表單","提供以下功能")

    #input the food
    def is_going_to_checknutrition(self, event):
        text = event.message.text
        return text.lower() == "check nutrition"
    def on_enter_checknutrition(self, event):
        btn_action=[
            MessageTemplateAction(
                label='華片',
                text='breakfast'
            ),
            MessageTemplateAction(
                label='韓劇',
                text='lunch'
            ),
            MessageTemplateAction(
                label='動漫劇場版',
                text='dinner'
            ),
            MessageTemplateAction(
                label='顯示您的訂閱資訊',
                text='show nutrition'
            ),
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"選擇片子","返回功能選單請輸入return")
    
    #input the information
    def is_going_to_information(self, event):
        text = event.message.text
        if(text.lower() == "start" or text.lower() == "modified information"):
            return True
        else:
            return False
        # return text.lower() == "information"
    def on_enter_information(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "歡迎光臨機上盒服務!\n******請先輸入基本資訊******\n\n輸入姓名")
    #input the height
    def is_going_to_height(self, event):
        text = event.message.text
        return True
    def on_enter_height(self, event):
        print("in height")
        text = event.message.text
        TocMachine.height = int(text)
        reply_token = event.reply_token
        send_text_message(reply_token, "是否為會員")
    #input the weight
    def is_going_to_weight(self, event):
        text = event.message.text
        return True
    def on_enter_weight(self, event):
        text = event.message.text
        TocMachine.weight = int(text)
        print("in weight")
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入預算(dollar)")

    #input the money
    def is_going_to_money(self, event):
        text = event.message.text
        return True
    def on_enter_money(self, event):
        text = event.message.text
        TocMachine.Totalmoney = int(text)
        print("in money")
        reply_token = event.reply_token
        send_text_message(reply_token, "輸入年齡")
    #input the age
    def is_going_to_age(self, event):
        text = event.message.text
        return True
    def on_enter_age(self, event):
        text = event.message.text
        TocMachine.age = int(text)
        # bmr = (13.7 x 體重) + (5.0 x 身高) – (6.8 x 年齡) + 66
        bmr = (13.7*TocMachine.weight) + (5*TocMachine.height) - (6.8*TocMachine.age) + 66
        tdee = bmr * 1.375 - 300
        TocMachine.Totalstarch = tdee * 0.3/4 #starch=tdee*0.3/4
        TocMachine.Totalcalorie = tdee
        TocMachine.Totalprotein = TocMachine.weight #(1 kg need 1g protein)
        print(TocMachine.Totalmoney,"totalmoney")
        print(tdee,'tdee')
        print(TocMachine.Totalcalorie,"Totalcalorie")
        print(TocMachine.Totalstarch,"Totalstarch")
        print(TocMachine.Totalprotein,"Totalprotein")
        self.go_regtostart(event)

    #check
    def on_enter_examine(self, event, strback):
        print("in examine")
        print(strback)
        self.go_money(event,strback)
    
    def on_enter_money_check(self, event, strback):
        print("in money check")
        sum = TocMachine.dinner['money'] +TocMachine.breakfast['money'] + TocMachine.lunch['money'] 
        print(TocMachine.breakfast['money'],"breakfast")
        print(TocMachine.lunch['money'],"lunch")
        print(TocMachine.dinner['money'],"dinner")
        print(sum,"sum = ")
        if sum <= TocMachine.Totalmoney:
            self.go_calorie(event,strback)
        else:
            self.go_money_deny(event,strback,sum)

    def on_enter_calorie_check(self, event,strback):
        print("in calorie check")
        sum = TocMachine.dinner['calorie'] + TocMachine.breakfast['calorie'] + TocMachine.lunch['calorie'] 
        print(TocMachine.breakfast['calorie'],"breakfast")
        print(TocMachine.lunch['calorie'],"lunch")
        print(TocMachine.dinner['calorie'],"dinner")
        print(sum,"sum = ")

        if sum < TocMachine.Totalcalorie:
            self.go_starch(event,strback)
        else:
            self.go_calorie_deny(event,strback,sum)
        
    def on_enter_starch_check(self, event,strback):
        print("in starch check")
        sum = TocMachine.dinner['starch'] +TocMachine.breakfast['starch'] + TocMachine.lunch['starch'] 
        print(TocMachine.breakfast['starch'],"breakfast")
        print(TocMachine.lunch['starch'],"lunch")
        print(TocMachine.dinner['starch'],"dinner")
        print(sum,"sum = ")
        if sum < TocMachine.Totalstarch:
            self.go_protein(event,strback)
        else:
            self.go_starch_deny(event,strback,sum)

    def on_enter_protein_check(self, event,strback):
        print("in protein check")
        sum = TocMachine.dinner['protein'] +TocMachine.breakfast['protein'] + TocMachine.lunch['protein'] 
        print(TocMachine.breakfast['protein'],"breakfast")
        print(TocMachine.lunch['protein'],"lunch")
        print(TocMachine.dinner['protein'],"dinner")
        print(sum,"sum = ")
        if sum < TocMachine.Totalprotein:
            self.go_checknutrition(event)
        else:
            self.go_protein_deny(event,strback,sum)
    
    #deny
    def on_enter_money_deny(self, event, strback,sum):
        reply_token = event.reply_token
        msg0="您不是VIP\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in money deny")
        
        if strback == "breakfast":
            sum -= TocMachine.breakfast['money']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['money']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['money']
            self.go_checknutrition(event)
        
    def on_enter_calorie_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="餘額不足\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in calorie deny")
        if strback == "breakfast":
            sum -= TocMachine.breakfast['calorie']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['calorie']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['calorie']
            self.go_checknutrition(event)
        
    def on_enter_starch_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="年紀不足\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in starch deny")

        if strback == "breakfast":
            sum -= TocMachine.breakfast['starch']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['starch']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['starch']
            self.go_checknutrition(event)

    def on_enter_protein_deny(self, event,strback,sum):
        reply_token = event.reply_token
        msg0="血腥畫面太多\n輸入return返回功能表單"
        send_text_message(reply_token,msg0)
        print("in protein deny")

        if strback == "breakfast":
            sum -= TocMachine.breakfast['protein']
            self.go_checknutrition(event)
        elif strback == "lunch":
            sum -= TocMachine.lunch['protein']
            self.go_checknutrition(event)
        else:
            sum -= TocMachine.dinner['protein']
            self.go_checknutrition(event)
 
    #showeat
    def is_going_to_showeat(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show nutrition"
    def on_enter_showeat(self, event ,indic=""):  
        msg0 = '片名:\n       華片%10s\n       韓劇%10s\n       動漫劇場版%10s\n' % (TocMachine.breakfast['meal'],TocMachine.lunch['meal'],TocMachine.dinner['meal'])
        msg1 = '金額:\n       華片%20d卡\n       韓劇%20d卡\n       動漫劇場版%20d卡\n' % (TocMachine.breakfast['calorie'],TocMachine.lunch['calorie'],TocMachine.dinner['calorie'])
        msg2 = '需求年紀:\n       華片%20d克\n       韓劇%20d克\n       動漫劇場版%20d克\n' % (TocMachine.breakfast['starch'],TocMachine.lunch['starch'],TocMachine.dinner['starch'])
        msg3 = '血腥分類:\n       華片%20d克\n       韓劇%20d克\n       動漫劇場版%20d克\n' % (TocMachine.breakfast['protein'],TocMachine.lunch['protein'],TocMachine.dinner['protein'])
        msg4 = '需要VIP會員:\n       華片%20d元\n       韓劇%20d元\n       動漫劇場版%20d元\n' % (TocMachine.breakfast['money'],TocMachine.lunch['money'],TocMachine.dinner['money'])
        msg5 = '返回請輸入return'
        reply_token = event.reply_token
        send_text_message(reply_token,msg0+msg1+msg2+msg3+msg4+msg5)
    #show back
    def is_going_to_showback(self, event,indic=""):
        text = event.message.text
        return text.lower() == "return"
    def on_enter_showback(self, event ,indic=""):  
        self.go_checknutrition(event)

    #showsuggest
    def is_going_to_showsuggest(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show suggestion"
    def on_enter_showsuggest(self, event ,indic=""):
        print("in show suggest")  
        print(TocMachine.Totalmoney,"totalmoney")
        print(TocMachine.Totalcalorie,"Totalcalorie")
        print(TocMachine.Totalstarch,"Totalstarch")
        print(TocMachine.Totalprotein,"Totalprotein")
        
        #msg0 = '設定完身高體重即可換算\n\n'
        msg1 = '推薦:上流戰爭\n' % (TocMachine.Totalcalorie)
        msg2 = '您是否為VIP:%20d公克\n' % (TocMachine.Totalstarch)
        msg3 = '您的年紀:%15d公克\n' % (TocMachine.Totalprotein)
        msg4 = '您的預算:         %20d元\n\n' % (TocMachine.Totalmoney)
        msg5 = '返回請輸入return'
        reply_token = event.reply_token
        send_text_message(reply_token,msg1+msg2+msg3+msg4+msg5)
    
    #showfsm
    def is_going_to_showfsm(self, event,indic=""):
        text = event.message.text
        return text.lower() == "show fsm"

    def on_enter_showfsm(self, event ,indic=""):
        reply_token = event.reply_token
        send_fsm(reply_token)

    #checknutrition back to start
    def is_going_to_regtostart(self, event,indic=""):
        text = event.message.text
        reply_token = event.reply_token
        if text.lower() != "return":
            send_text_message(reply_token,"輸入return回到上一個階段")
        return text.lower() == "return"
    def on_enter_regtostart(self, event ,indic=""):  
        print(" go to start")
        self.go_regtostart(event)
    
    #breakfast
    def is_going_to_breakfast(self, event,indic=""):
        text = event.message.text
        return text.lower() == "breakfast"
    def on_enter_breakfast(self, event ,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='痞子英雄($500)',
                text='sandwitch'
            ),
            MessageTemplateAction(
                label='聽說($200)',
                text='chiomelet'
            ),
            MessageTemplateAction(
                label='翻滾吧男孩($350)',
                text='riceball'
            ),
            MessageTemplateAction(
                label='那些年我們一起追的女孩($550)',
                text='hamburger'
            ),
        ]
        
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"華片",indic)

    #next breakfast
    def is_going_to_nextbreakfast(self, event):
        text = event.message.text
        return True
    def on_enter_nextbreakfast(self, event):
        text = event.message.text
        input = text.split()
        #print(event.message.text)
        print(input)

        if event.message.text == 'sandwitch':
            TocMachine.breakfast['calorie'] = 270
            TocMachine.breakfast['starch']  = 20
            TocMachine.breakfast['protein'] = 13
            TocMachine.breakfast['money']   = 500
            TocMachine.breakfast['meal'] = '痞子英雄'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in sandwitch")
            
        elif event.message.text == 'chiomelet':
            TocMachine.breakfast['calorie'] = 230
            TocMachine.breakfast['starch']  = 25
            TocMachine.breakfast['protein'] = 6
            TocMachine.breakfast['money']   = 200
            TocMachine.breakfast['meal'] = '聽說'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in chiomelet")

        elif event.message.text == 'riceball':
            TocMachine.breakfast['calorie'] = 220
            TocMachine.breakfast['starch']  = 40
            TocMachine.breakfast['protein'] = 5
            TocMachine.breakfast['money']   = 350
            TocMachine.breakfast['meal'] = '翻滾吧男孩'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in riceball")

        elif event.message.text == 'hamburger':
            TocMachine.breakfast['calorie'] = 230
            TocMachine.breakfast['starch']  = 38
            TocMachine.breakfast['protein'] = 15
            TocMachine.breakfast['money']   = 550
            TocMachine.breakfast['meal'] = '那些年我們一起追的女孩'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in hamburger")

        self.go_money(event,"breakfast")

    #lunch
    def is_going_to_lunch(self, event):
        text = event.message.text
        return text.lower() == "lunch"
    def on_enter_lunch(self, event,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='上流戰爭($90)',
                text='Katsudon'
            ),
            MessageTemplateAction(
                label='來自星星的你($65)',
                text='friedrice'
            ),
            MessageTemplateAction(
                label='魷魚遊戲($40)',
                text='noodles'
            ),
            MessageTemplateAction(
                label='繼承者們($65)',
                text='chicken boxedlunch'
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"韓劇",indic)
    #next lunch
    def is_going_to_nextlunch(self, event):
        text = event.message.text
        return True
    def on_enter_nextlunch(self, event):
        text = event.message.text
        input = text.split()
        print(input)
        if event.message.text == 'Katsudon':
            TocMachine.lunch['calorie'] = 500
            TocMachine.lunch['starch']  = 55
            TocMachine.lunch['protein'] = 35
            TocMachine.lunch['money']   = 90
            TocMachine.lunch['meal'] = '上流戰爭'
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in Katsudon")
        elif event.message.text == 'friedrice':
            TocMachine.lunch['calorie'] = 600
            TocMachine.lunch['starch']  = 80
            TocMachine.lunch['protein'] = 10
            TocMachine.lunch['money'] = 65
            TocMachine.lunch['meal'] = '來自星星的你'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in friedrice")

        elif event.message.text == 'noodles':
            TocMachine.lunch['calorie'] = 600
            TocMachine.lunch['starch']  = 60
            TocMachine.lunch['protein'] = 10
            TocMachine.lunch['money']   = 40
            TocMachine.lunch['meal'] = '魷魚遊戲'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in noodles")
        elif event.message.text == 'chicken boxedlunch':
            TocMachine.lunch['calorie'] = 800
            TocMachine.lunch['starch']  = 80
            TocMachine.lunch['protein'] = 40
            TocMachine.lunch['money']   = 65
            TocMachine.lunch['meal'] = '繼承者們'
            
            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in chicken boxedlunch")
        self.go_money(event,"lunch")
    
    #dinner
    def is_going_to_dinner(self, event):
        text = event.message.text        
        return text.lower() == "dinner"
    def on_enter_dinner(self, event,indic=""):
        btn_action=[
            MessageTemplateAction(
                label='你的名字($75)',
                text= 'sushi'
            ),
            MessageTemplateAction(
                label='天空的遇難船($70)',
                text='oden'
            ),
            MessageTemplateAction(
                label='失落之塔($100)',
                text='hot pot'
            ),
            MessageTemplateAction(
                label='宇宙人Pi力來襲($80)',
                text='Curry rice'
            )
        ]
        reply_token = event.reply_token
        send_button_message(reply_token,btn_action,"動漫劇場版",indic)
    #next dinner
    def is_going_to_nextdinner(self, event):
        text = event.message.text
        return True
    def on_enter_nextdinner(self, event):
        text = event.message.text
        input = text.split()
        print(input)
        # print(text,"check the nextdinner")
        if event.message.text == 'sushi':
            TocMachine.dinner['calorie'] = 800
            TocMachine.dinner['starch']  = 80
            TocMachine.dinner['protein'] = 50

            TocMachine.dinner['money']   = 75
            TocMachine.dinner['meal'] = '你的名字'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in sushi")
        elif event.message.text == 'oden':
            TocMachine.dinner['calorie'] = 800
            TocMachine.dinner['starch']  = 90
            TocMachine.dinner['protein'] = 30
            TocMachine.dinner['money']   = 70
            TocMachine.dinner['meal'] = '天空的遇難船'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in oden")

        elif event.message.text == 'hot pot':
            TocMachine.dinner['calorie'] = 1000
            TocMachine.dinner['starch']  = 100
            TocMachine.dinner['protein'] = 75
            TocMachine.dinner['money']   = 100
            TocMachine.dinner['meal'] = '失落之塔'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in hot pot")
        elif event.message.text == 'Curry rice':
            TocMachine.dinner['calorie'] = 600
            TocMachine.dinner['starch']  = 90
            TocMachine.dinner['protein'] = 30
            TocMachine.dinner['money']   = 80
            TocMachine.dinner['meal'] = '宇宙人Pi力來襲'

            print(TocMachine.breakfast['money'],"breakfast")
            print(TocMachine.lunch['money'],"lunch")
            print(TocMachine.dinner['money'],"dinner")
            print("in Curry rice")
        self.go_money(event,"dinner")
