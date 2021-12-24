# import os
# import sys

# from flask import Flask, jsonify, request, abort, send_file
# from dotenv import load_dotenv
# from linebot import LineBotApi, WebhookParser
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction
# from fsm import TocMachine
# from utils import send_text_message

# load_dotenv()


# machine = TocMachine(
#     states=["user","start","information","regfood",
#             'height','weight','money','age','showeat','showback',"showsuggest","showfsm",
#             "breakfast",'lunch','dinner','regtostart',
#             'nextbreakfast','nextlunch','nextdinner',
#             'money_check','calorie_check','starch_check',
#             'money_deny','calorie_deny','starch_deny',
#     ],
#     transitions=[
#         #first from initial state user to start
#         {"trigger": "advance","source": "user","dest": "information","conditions": "is_going_to_information",},
#         #from start to choose function
#         {"trigger": "advance","source": "start","dest": "regfood","conditions": "is_going_to_regfood",},
#         {"trigger": "advance","source": "start","dest": "information","conditions": "is_going_to_information",},
#         {"trigger": "advance","source": "start","dest": "showsuggest","conditions": "is_going_to_showsuggest",},
#         {"trigger": "advance","source": "start","dest": "showfsm","conditions": "is_going_to_showfsm",},
#         #input the self information (height->weight->money->age)
#         {"trigger": "advance","source": "information","dest": "height","conditions": "is_going_to_height",},
#         {"trigger": "advance","source": "height","dest": "weight","conditions": "is_going_to_weight",},
#         {"trigger": "advance","source": "weight","dest": "money","conditions": "is_going_to_money",},
#         {"trigger": "advance","source": "money","dest": "age","conditions": "is_going_to_age",},
#         #regfood(choose which meal eated) to three meal
#         {"trigger": "advance","source": "regfood","dest": "breakfast","conditions": "is_going_to_breakfast",},
#         {"trigger": "advance","source": "regfood","dest": "lunch","conditions": "is_going_to_lunch",},
#         {"trigger": "advance","source": "regfood","dest": "dinner","conditions": "is_going_to_dinner",},
#         {"trigger": "advance","source": "regfood","dest": "showeat","conditions": "is_going_to_showeat",},
#         #three meal to next 
#         {"trigger": "advance","source": "breakfast","dest": "nextbreakfast","conditions": "is_going_to_nextbreakfast",},
#         {"trigger": "advance","source": "lunch","dest": "nextlunch","conditions": "is_going_to_nextlunch",},
#         {"trigger": "advance","source": "dinner","dest": "nextdinner","conditions": "is_going_to_nextdinner",},
        
#         #three check by (money calorie starch)
#         {"trigger":"go_money","source":['nextbreakfast','nextlunch','nextdinner'],"dest":"money_check"},
#         {"trigger":"go_calorie","source":"money_check","dest":"calorie_check"},
#         {"trigger":"go_starch","source":"calorie_check","dest":"starch_check"},
#         #when check is not allow go to the deny
#         {"trigger":"go_money_deny","source":"money_check","dest":"money_deny"},
#         {"trigger":"go_calorie_deny","source":"calorie_check","dest":"calorie_deny"},
#         {"trigger":"go_starch_deny","source":"starch_check","dest":"starch_deny"},

#         #from deny to original meal(for rechoose the meal) 
#         {"trigger":"go_regfood","source":['money_deny','calorie_deny','starch_deny'],"dest":"regfood"},
#         {"trigger":"go_regfood","source":['money_deny','calorie_deny','starch_deny'],"dest":"regfood"},
#         {"trigger":"go_regfood","source":['money_deny','calorie_deny','starch_deny'],"dest":"regfood"},

#         #back to start
#         {"trigger": "advance","source": ["showsuggest","regfood","showfsm"],"dest": "regtostart","conditions": "is_going_to_regtostart",},
#         #back to start by go
#         {"trigger":"go_regtostart","source":['regtostart','age'],"dest":"start"},
#         #from showeat go to showback
#         {"trigger": "advance","source": "showeat","dest": "showback","conditions": "is_going_to_showback",},
#         #back to regfood
#         {"trigger":"go_regfood","source":['starch_check','showback'],"dest":"regfood"},
        
#     ],
#     initial="user",
#     auto_transitions=False,
#     show_conditions=True,
# )

# app = Flask(__name__, static_url_path="")

# # get channel_secret and channel_access_token from your environment variable
# channel_secret = "7bd4cc4ffdbdd3870f2596ae9ef88c9b"
# channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="
# if channel_secret is None:
#     print("Specify LINE_CHANNEL_SECRET as environment variable.")
#     sys.exit(1)
# if channel_access_token is None:
#     print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
#     sys.exit(1)

# line_bot_api = LineBotApi(channel_access_token)
# parser = WebhookParser(channel_secret)

# @app.route("/callback", methods=["POST"])
# def callback():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue

#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.message.text)
#         )

#     return "OK"

# @app.route("/webhook", methods=["POST"])
# def webhook_handler():
#     signature = request.headers["X-Line-Signature"]
#     # get request body as text
#     body = request.get_data(as_text=True)
#     # app.logger.info(f"Request body: {body}")

#     # parse webhook body
#     try:
#         events = parser.parse(body, signature)
#     except InvalidSignatureError:
#         abort(400)

#     # if event is MessageEvent and message is TextMessage, then echo text
#     for event in events:
#         if not isinstance(event, MessageEvent):
#             continue
#         if not isinstance(event.message, TextMessage):
#             continue
#         if not isinstance(event.message.text, str):
#             continue

#         print(f"\nFSM STATE: {machine.state}")
#         # print(f"REQUEST BODY: \n{body}")
#         response = machine.advance(event)
#         if response == False:
#             send_text_message(event.reply_token, "Not Entering any State")
        
#         machine.get_graph().draw("fsm.png", prog="dot", format="png")
#         send_file("fsm.png", mimetype="image/png")

#     return "OK"

# @app.route("/show-fsm", methods=["GET"])
# def show_fsm():
#     machine.get_graph().draw("fsm.png", prog="dot", format="png")
#     return send_file("fsm.png", mimetype="image/png")

# if __name__ == "__main__":
#     port = os.environ.get("PORT", 8000)
#     app.run(host="0.0.0.0", port=port, debug=True)
    



import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackTemplateAction
from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user","start","information","checknutrition",
            'height','weight','money','age','showeat','showback',"showsuggest","showfsm",
            "breakfast",'lunch','dinner','regtostart',
            'nextbreakfast','nextlunch','nextdinner',
            'money_check','calorie_check','starch_check','protein_check',
            'money_deny','calorie_deny','starch_deny','protein_deny',
    ],
    transitions=[
        #first from initial state user to start
        {"trigger": "advance","source": "user","dest": "information","conditions": "is_going_to_information",},
        #from start to choose function
        {"trigger": "advance","source": "start","dest": "checknutrition","conditions": "is_going_to_checknutrition",},
        {"trigger": "advance","source": "start","dest": "information","conditions": "is_going_to_information",},
        {"trigger": "advance","source": "start","dest": "showsuggest","conditions": "is_going_to_showsuggest",},
        {"trigger": "advance","source": "start","dest": "showfsm","conditions": "is_going_to_showfsm",},
        #input the self information (height->weight->money->age)
        {"trigger": "advance","source": "information","dest": "height","conditions": "is_going_to_height",},
        {"trigger": "advance","source": "height","dest": "weight","conditions": "is_going_to_weight",},
        {"trigger": "advance","source": "weight","dest": "money","conditions": "is_going_to_money",},
        {"trigger": "advance","source": "money","dest": "age","conditions": "is_going_to_age",},
        #checknutrition(choose which meal eated) to three meal
        {"trigger": "advance","source": "checknutrition","dest": "breakfast","conditions": "is_going_to_breakfast",},
        {"trigger": "advance","source": "checknutrition","dest": "lunch","conditions": "is_going_to_lunch",},
        {"trigger": "advance","source": "checknutrition","dest": "dinner","conditions": "is_going_to_dinner",},
        {"trigger": "advance","source": "checknutrition","dest": "showeat","conditions": "is_going_to_showeat",},
        #three meal to next 
        {"trigger": "advance","source": "breakfast","dest": "nextbreakfast","conditions": "is_going_to_nextbreakfast",},
        {"trigger": "advance","source": "lunch","dest": "nextlunch","conditions": "is_going_to_nextlunch",},
        {"trigger": "advance","source": "dinner","dest": "nextdinner","conditions": "is_going_to_nextdinner",},
        
        #three check by (money calorie starch)
        {"trigger":"go_money","source":['nextbreakfast','nextlunch','nextdinner'],"dest":"money_check"},
        {"trigger":"go_calorie","source":"money_check","dest":"calorie_check"},
        {"trigger":"go_starch","source":"calorie_check","dest":"starch_check"},
        {"trigger":"go_protein","source":"starch_check","dest":"protein_check"},
        #when check is not allow go to the deny
        {"trigger":"go_money_deny","source":"money_check","dest":"money_deny"},
        {"trigger":"go_calorie_deny","source":"calorie_check","dest":"calorie_deny"},
        {"trigger":"go_starch_deny","source":"starch_check","dest":"starch_deny"},
        {"trigger":"go_protein_deny","source":"protein_check","dest":"protein_deny"},

        #from deny to original meal(for rechoose the meal) 
        {"trigger":"go_checknutrition","source":['money_deny','calorie_deny','starch_deny','protein_deny'],"dest":"checknutrition"},
        {"trigger":"go_checknutrition","source":['money_deny','calorie_deny','starch_deny','protein_deny'],"dest":"checknutrition"},
        {"trigger":"go_checknutrition","source":['money_deny','calorie_deny','starch_deny','protein_deny'],"dest":"checknutrition"},
        {"trigger":"go_checknutrition","source":['money_deny','calorie_deny','starch_deny','protein_deny'],"dest":"checknutrition"},
        
        #back to start
        {"trigger": "advance","source": ["showsuggest","checknutrition","showfsm"],"dest": "regtostart","conditions": "is_going_to_regtostart",},
        #back to start by go
        {"trigger":"go_regtostart","source":['regtostart','age'],"dest":"start"},
        #from showeat go to showback
        {"trigger": "advance","source": "showeat","dest": "showback","conditions": "is_going_to_showback",},
        #back to checknutrition
        {"trigger":"go_checknutrition","source":['protein_check','showback'],"dest":"checknutrition"},
        
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = "7bd4cc4ffdbdd3870f2596ae9ef88c9b"
channel_access_token = "lP+b/BM0OXIegi4iJkTIDSTkaLObmNnzcOa6Q6WKhVD/brx47xAdEIIKSjebM6kT7HugaVykdrQWgjQcAwYXVoZqZN3T0dRrSAhdc5cg0qW9v8W/5gJR4K3b98xRL1in0ebUo2XM/5ibtHCi+d/ETQdB04t89/1O/w1cDnyilFU="
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info(f"Request body: {body}")


    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        print(f"\nFSM STATE: {machine.state}")
        # print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")
        
        machine.get_graph().draw("fsm.png", prog="dot", format="png")
        send_file("fsm.png", mimetype="image/png")

    return "OK"

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    