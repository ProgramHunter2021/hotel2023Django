from .models import *
from linebot.models import *

import googlemaps

from django.conf import settings

def list_activity_type():
    types = ActivityType.objects.all()
    buttons = []
    for t in types:
        btn = {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "message",
                "label": t.at_name,
                "text": "[周邊類別]:" + t.at_id,
            }
        }
        buttons.append(btn)
    
    buble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "選擇您要搜尋的類別",
                    "weight": "bold",
                    "size": "xl"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": buttons
        }
    }

    flex_message =FlexSendMessage(
        alt_text="活動類別",
        contents= buble
    )
    return flex_message

def list_all_activities(aid):
    #抓取資料庫中所有週邊活動
    allactivities = Activities.objects.filter(a_type__at_id__contains = aid).all()
    print(allactivities.count)
    bubbles = []

    for activity  in allactivities:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": activity.a_img,
                "action": {
                "type": "uri",
                "label": "活動網址",
                "uri": activity.a_url,
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                {
                    "type": "text",
                    "text": activity.a_name,
                    "size": "xl",
                    "weight": "bold",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "活動日期",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_date,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "活動地點",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_address,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "主辦單位",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_organizer,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "費用",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_price,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "43px"
                    }
                    ],
                    "margin": "md"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "label": "CALL",
                        "uri": "tel:" + activity.a_phone
                        }
                    },
                    {
                        "type": "button",
                        "style": "link",
                        "height": "sm",
                        "action": {
                        "type": "message",
                        "label": "取得地圖",
                        "text": "[GET MAP]:" + activity.a_name,
                        }
                    }
                ]
            }
        } 
        bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text="週邊活動",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def GetMapMessage(strLocationName):
    map = Activities.objects.filter(a_name=strLocationName).first()
    message = None

    if map is None:
        message = TextSendMessage(text = '抱歉系統錯誤暫時無法查到您所指定的地點...')
    else:
        if map.comment != None:
            x,y = map.comment.split(',') 
            message = LocationSendMessage(title=strLocationName, address=map.a_address if map.a_address is not None else strLocationName,
                        latitude= float(x), longitude= float(y))
        else:
            gmaps = googlemaps.Client(key=settings.GOOGLE_API)

            # Geocoding an address
            geocode_result = gmaps.geocode(map.Address)
            f_lat = float(geocode_result[0]['geometry']['location']['lat'])
            f_lng = float(geocode_result[0]['geometry']['location']['lng'])
            message = LocationSendMessage(title=strLocationName, address=map.Address if map.Address is not None else strLocationName,
                        latitude= f_lat, longitude= f_lng)

    return message



