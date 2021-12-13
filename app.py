# import os
# import sys

# from flask import Flask, jsonify, request, abort, send_file
# from dotenv import load_dotenv
# from linebot import LineBotApi, WebhookParser
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

# from fsm import TocMachine
# from utils import send_text_message

# load_dotenv()



# machine = TocMachine(
#     states=["user", "state1", "state2"],
#     transitions=[
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state1",
#             "conditions": "is_going_to_state1",
#         },
#         {
#             "trigger": "advance",
#             "source": "user",
#             "dest": "state2",
#             "conditions": "is_going_to_state2",
#         },
#         {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
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
#     app.logger.info(f"Request body: {body}")

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
#         print(f"REQUEST BODY: \n{body}")
#         response = machine.advance(event)
#         if response == False:
#             send_text_message(event.reply_token, "Not Entering any State")

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
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "menu", "exchange","stock","exchange_USD", "exchange_JPY","exchange_CNY","exchange_else","show_fsm_pic", "price", "show_price","technical","show_technical","stock_else"],
    transitions=[
        { #第1階段
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        { #第2-1-查詢匯率
            "trigger": "advance",
            "source": "menu",
            "dest": "exchange",
            "conditions": "is_going_to_exchange",
        },
        { #第2-2-查詢股票
            "trigger": "advance",
            "source": "menu",
            "dest": "stock",
            "conditions": "is_going_to_stock",
        },
        { #第3-1 美金
            "trigger": "advance",
            "source": "exchange",
            "dest": "exchange_USD",
            "conditions": "is_going_to_exchange_USD",
        },
        { #第3-2 日元
            "trigger": "advance",
            "source": "exchange",
            "dest": "exchange_JPY",
            "conditions": "is_going_to_exchange_JPY",
        },
        { #第3-3 人民幣
            "trigger": "advance",
            "source": "exchange",
            "dest": "exchange_CNY",
            "conditions": "is_going_to_exchange_CNY",
        },
        { #第3-4 其他
            "trigger": "advance",
            "source": "exchange",
            "dest": "exchange_else",
            "conditions": "is_going_to_exchange_else",
        },
        { #第4-1-查詢股價
            "trigger": "advance",
            "source": "stock",
            "dest": "price",
            "conditions": "is_going_to_price",
        },
        { #第4-1-1-查詢股價結果
            "trigger": "advance",
            "source": "price",
            "dest": "show_price",
            "conditions": "is_going_to_show_price",
        },
        { #第4-2-股票基本面
            "trigger": "advance",
            "source": "stock",
            "dest": "technical",
            "conditions": "is_going_to_technical",
        },
        { #第4-2-1-查詢股票基本面
            "trigger": "advance",
            "source": "technical",
            "dest": "show_technical",
            "conditions": "is_going_to_show_technical",
        },
        { #第4-3-查詢其他
            "trigger": "advance",
            "source": "stock",
            "dest": "stock_else",
            "conditions": "is_going_to_stock_else",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "show_fsm_pic",
            "conditions": "is_going_to_show_fsm_pic",
        },
        {"trigger": "go_back", "source": ["menu", "exchange","stock","exchange_USD", "exchange_JPY","exchange_CNY","exchange_else","show_fsm_pic", "price", "show_price","technical","show_technical","stock_else"], "dest": "user"},
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

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

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
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)