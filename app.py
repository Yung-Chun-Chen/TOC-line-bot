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
from linebot.models import MessageEvent, TextMessage, PostbackEvent

from fsm import TocMachine, favorite_state, machine
from utils import favorite_movies, favorite_animates, win_game
from machine_data import  machineData

load_dotenv()

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
		
    for event in events:
        if event.source.user_id not in machine:
            machine[event.source.user_id] = TocMachine(
                states=machineData["states"],
                transitions=machineData["transitions"],
                initial=machineData["initial"],
                auto_transitions=machineData["auto_transitions"],
                show_conditions=machineData["show_conditions"]
            )
        if event.source.user_id not in favorite_movies:
            favorite_movies[event.source.user_id] = []
        if event.source.user_id not in favorite_animates:
            favorite_animates[event.source.user_id] = []
        if event.source.user_id not in win_game:
            win_game[event.source.user_id] = 0
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage) and isinstance(event.message.text, str):
                response = machine[event.source.user_id].advance(event)
        elif isinstance(event, PostbackEvent):
            if isinstance(event.postback.data, str):
                response = machine[event.source.user_id].advance_postback(event)
        print(f"\nFSM STATE: {machine[event.source.user_id].state}")
        print(f"REQUEST BODY: \n{body}")
        #if response == False:
            #send_text_message(event.reply_token, "Not Entering any State")

    return "OK"
	


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    if "graph" not in machine:
        machine["graph"] = TocMachine(
            states=machineData["states"],
            transitions=machineData["transitions"],
            initial=machineData["initial"],
            auto_transitions=machineData["auto_transitions"],
            show_conditions=machineData["show_conditions"]
        )
    machine["graph"].get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)