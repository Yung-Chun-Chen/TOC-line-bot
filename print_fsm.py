from transitions import Machine
from transitions.extensions import GraphMachine
from flask import Flask, jsonify, request, abort, send_file
try:
    import pygraphviz as pgv
except ImportError:
    raise
import requests
machine = GraphMachine(
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
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)
machine.get_graph().draw("fsm.png", prog="dot", format="png")