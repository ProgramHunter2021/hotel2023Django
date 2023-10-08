from linebot.models import *

def one2oneService():
    flex_message = FlexSendMessage(
        alt_text="專人服務",
        contents={
            "type": "bubble",
            "size": "kilo",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/YsAAuxy.png", ##待換
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "專人客服",
                    "size": "xl",
                    "weight": "bold"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "md",
                    "action": {
                    "type": "uri",
                    "label": "專人聊天室",
                    "uri": "https://lin.ee/gXfrl0X"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "sm",
                    "action": {
                    "type": "uri",
                    "label": "Call me",
                    "uri":'tel://0800270008'
                    }
                }
                ]
            }
        }
    )
    return flex_message