from linebot.models import *
from .models import *
from hotelbot.models import *
from datetime import datetime, time
from .utils import getFreeRoom, MyDateTime
from qrcode import make
from django.conf import settings
import os
import random 
import urllib


def     PreBookingProcessMsg(uid):
    user = Users.objects.filter(lineid=uid).first()
    bodycontents = [
        {
            "type": "text",
            "text": '訂房人資訊確認',
            "wrap": True,
            "weight": "bold",
            "size": "xl",
            "color": "#1A3852"
        },
        {
            "type": "separator",
            "margin": "sm"
        }
    ]
   
    for label in ['姓名＊', '電話＊', '地址＊', '電子載具', '公司統編']:
        value = ''
        if label == '姓名＊': 
            value = user.name if user.name else 'Empty'
        elif label == '電話＊': 
            value = user.phone if user.phone else 'Empty'
        elif label == '地址＊': 
            value = user.address if user.address else 'Empty'
        elif label == '電子載具': 
            value = user.einvoice if user.einvoice else 'Empty'
        elif label == '公司統編': 
            value = user.GUInumber if user.GUInumber else 'Empty'

        content = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "wrap": True,
                    "weight": "bold",
                    "size": "md",
                    "color": "#1A3852"
                },
                {
                    "type": "text",
                    "text": value,
                    "wrap": True,
                    "weight": "bold",
                    "size": "md",
                    "color": "#1A3852",
                    "gravity": "center",
                    "align": "end"
                }
            ]
        }
        bodycontents.append(content)
        
    rtn_msg = FlexSendMessage(
        alt_text="訂房人資訊確認",
        contents={
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": bodycontents
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "確認開始訂房",
                            "uri": "https://liff.line.me/2001073277-POyXgxDX"
                        },
                        "color": "#D5A07E"
                    }, 
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "修改個人資訊",
                            "uri": "https://liff.line.me/2001073277-xW2DpBdD"
                        },
                        "color": "#D5A07E"
                    }
                ]
            }
        }
    )

    return rtn_msg

def Get_ConfirmBookingInfo_Msg(user_id, data):
    user = Users.objects.filter(lineid=user_id).first()
    
    FreeRooms = getFreeRoom(data['room_type'], data['from'], data['to'])
    print(FreeRooms)
    if not FreeRooms:
        return TextSendMessage(text='糟糕!手速不夠快,房間已經被認定走了。')
    else:
        data['room'] = FreeRooms[0].r_id
        print(data)
        room_price = FreeRooms[0].r_type.rt_price
        bodycontents = [
            {
                "type": "text",
                "text": '確認訂房資訊',
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "color": "#1A3852"
            },
            {
                "type": "separator",
                "margin": "sm"
            }
        ]

        from_date = MyDateTime(data['from'])
        to_date = MyDateTime(data['to'])

        for label in ['房型', '進房日期', '退房日期', '天數', '總金額', '訂房人', '電話', '地址']:
            value = ''
            if label == '房型': 
                value = data['room_type']
            elif label == '進房日期': 
                value = data['from']
            elif label == '退房日期': 
                value = data['to']
            elif label == '天數': 
                value = str(from_date.comprise_between(to_date))
            elif label == '總金額': 
                value = str(from_date.comprise_between(to_date) * room_price)
            elif label == '訂房人': 
                value = user.name if user.name else 'Empty'
            elif label == '電話': 
                value = user.phone if user.phone else 'Empty'
            elif label == '地址': 
                value = user.address if user.address else 'Empty'

            content = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": label,
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": value,
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852",
                        "gravity": "center",
                        "align": "end"
                    }
                ]
            }
            bodycontents.append(content)

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": bodycontents
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "確認",
                            "data": 'action=ConfirmBooking&' + str(data),
                        },
                        "color": "#D5A07E"
                    }, 
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "取消",
                            "data": 'action=Cancelbooking',
                        },
                        "color": "#D5A07E"
                    }
                ]
            }
        }

        flex_message = FlexSendMessage(
            alt_text="確認訂房資訊",
            contents={
                "type": "carousel",
                "contents": [bubble]
            }
        )
        return flex_message

def list_all_RoomTypes(data):
    #抓取資料庫中所有產品的資料
    RoomTypes = RoomType.objects.all()
    bubbles = []
    for type in RoomTypes:
        data['room_type'] = type.rt_name
        print(data)
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": type.rt_image
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                {
                    "type": "text",
                    "text": type.rt_name,
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1A3852"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "$" + str(type.rt_price),
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": "限定" + str(type.rt_limit) + "人",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852",
                        "gravity": "center",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xl",
                    "contents": [
                    {
                        "type": "text",
                        "text": type.rt_description,
                        "wrap": True,
                        "weight": "bold",
                        "flex": 0,
                        "size": "md"
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "Book This",
                        "data": "action=BookRoomType&" + str(data),
                    },
                    "color": "#D5A07E"
                }]
            }
        }
        bubbles.append(bubble)
    #print(bubbles)
    flex_message = FlexSendMessage(
        alt_text="房型選擇",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def replyMsg_CreateBooking(uid, data):
    user = Users.objects.filter(lineid=uid).first()
    rtype = RoomType.objects.filter(rt_name = data['room_type']).first()
    rm = Room.objects.filter(r_id = data['room']).first()
    from_date = MyDateTime(data['from'])
    to_date = MyDateTime(data['to'])
    lst_date = from_date.comprise_everyday(to_date)

    print(lst_date)

    try:
        order_id = datetime.now().strftime("%y%m%d%H%M%S") + "-" + uid
        order = Order.objects.create(o_id = order_id, o_user = user, o_roomtype = rtype, o_status = '1')
        
        for date in lst_date:
            BookingRoom.objects.create(order = order, room = rm, booked_date= date)
        return BookingSuccesMsg()
    except Exception:
        return TextSendMessage(text='哦喔!訂房流程發生問題,請稍後重新嘗試或聯絡專屬管家為您服務.')
        
def BookingSuccesMsg():
    tempmsg = FlexSendMessage(
        alt_text = "預定成功通知",
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": '訂房成功',
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "separator",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": '預定請求已發送,請儘快支付訂金,確保訂房保留．',
                        "wrap": True,
                        "size": "sm",
                        "color": "#1A3852"
                    },
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "訂金付款",
                            "data": "action=paydeposit"
                        },
                        "color": "#D5A07E"
                    }, 
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "查詢訂房紀錄",
                            "data": "action=checkbookingrecord"
                        },
                        "color": "#D5A07E"
                    }
                ]
            }
        }
    )
    return tempmsg

def List_Booking_recoder(uid):
    user = Users.objects.filter(lineid=uid).first()
    records = Order.objects.filter(o_user = user).exclude(o_status__in=['4','5']).all()
    print(records)

    bubbles = []

    for record in records:
        bookeddetails = BookingRoom.objects.filter(order = record).order_by('booked_date').all()

        msg_addcomment = f'[添加備註|{record.o_id}]:'
        #msg_addcomment = msg_addcomment.encode(encoding = 'UTF-8', errors = 'NONE')
        msg_addcomment = urllib.parse.quote(msg_addcomment)
        str_uri = f'https://line.me/R/oaMessage/@875zzpvg/?{msg_addcomment}'

        footer_btn = [
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "postback",
                    "label": "取消訂房",
                    "data": 'action=CanelBookedOrder&orderid=' + record.o_id,
                },
                "color": "#D5A07E"
            },
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "添加備註",
                    "uri": str_uri
                },
                "color": "#D5A07E"
            }
        ]
        print(bookeddetails[0].booked_date.strftime('%Y-%m-%d'))
        print(datetime.today().strftime('%Y-%m-%d'))
        if (bookeddetails[0].booked_date.strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d')):
            footer_btn.insert(0, {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "入住登記",
                    "text": "@入住登記"
                },
                "color": "#D5A07E"
            })

        print(str_uri)
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": record.o_id, 
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "separator",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": '房型',
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": record.o_roomtype.rt_name,
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": '入住日期',
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": bookeddetails[0].booked_date.strftime('%Y-%m-%d'),
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": '入住天數',
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": str(len(bookeddetails)),
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": footer_btn
            }
        }
        bubbles.append(bubble)
    #print(bubbles)
    flex_message = FlexSendMessage(
        alt_text="訂房紀錄",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message
        
def Pre_CheckIn_Msg(uid):
    user = Users.objects.filter(lineid=uid).first()
    today = datetime.today()
    # date = datetime(today.year, today.month, today.day, 0,0,0)
    date = datetime.now()
    print(date)
    booked_details = BookingRoom.objects.filter(order__o_user = user, booked_date = date).all()
    print(booked_details)
    bubbles = []
    for detail in booked_details:
        daycount = BookingRoom.objects.filter(order = detail.order).count()

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": '入住資訊確認', 
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "separator",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "訂房人",
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": detail.order.o_user.name if detail.order.o_user.name else "Empty",
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "房型",
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": detail.order.o_roomtype.rt_name,
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "入住天數",
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852"
                            },
                            {
                                "type": "text",
                                "text": str(daycount),
                                "wrap": True,
                                "weight": "bold",
                                "size": "md",
                                "color": "#1A3852",
                                "gravity": "center",
                                "align": "end"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "確認入住",
                            "uri": "https://liff.line.me/2001073277-aY7JzpBJ"
                        },
                        "color": "#D5A07E"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "聯絡官家",
                            "uri": "tel:09001234567"
                        },
                        "color": "#D5A07E"
                    }
                ]
            }
        }
        bubbles.append(bubble)
    #print(bubbles)
    flex_message = FlexSendMessage(
        alt_text="訂房紀錄",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def CheckInResultMsg(uid, IDNumber):
    user = Users.objects.filter(lineid=uid).first()
    if (user.idnumber == IDNumber):
        today = datetime.today()
        date = datetime(today.year, today.month, today.day, 0,0,0)
        print(date)
        booked_details = BookingRoom.objects.filter(order__o_user = user, booked_date = date).first()
        if not booked_details:
            return TextSendMessage(text='哦喔, 查不到您的訂房紀錄哦.')
        room_No = booked_details.room.r_id
        booked_details.room.r_users.add(user)
        booked_details.room.save()

        rtn_msg = FlexSendMessage(
            alt_text="訂房人資訊確認",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": '歡迎!入住成功',
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1A3852"
                        },
                        {
                            "type": "separator",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": '您的房間號碼是 [ ' + room_No + ' ]',
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1A3852"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "取得房間密碼",
                                "text": "@房間密碼"
                            },
                            "color": "#D5A07E"
                        }, 
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "客房服務",
                                "text": "@客房服務"
                            },
                            "color": "#D5A07E"
                        }
                    ]
                }
            }
        )

        return rtn_msg
    else:
        return TextSendMessage(text='哦喔,證件資訊不匹配! CHECK IN 失敗,請聯絡專屬管家為您服務.')

def RoomKeyMsg(uid):
    user = Users.objects.filter(lineid=uid).first()
    room = Room.objects.filter(r_users = user).first(); 
    print(room)

    room_key = random.randint(100000, 999999)

    img = make(room_key)
    img_name = f'{str(room.r_id)}.png'
    img.save(os.path.join(settings.STATICFILES_DIRS[0], 'img', img_name))
    room_img_url = f'https://a115-118-233-28-122.ngrok-free.app/static/img/{room.r_id}.png'

    if not room:
        return TextSendMessage(text='很抱歉，您尚未辦理入住手續，請先辦理入住手續後在使用該功能，謝謝。')
    else:
        tempmsg = FlexSendMessage(
        alt_text = "預定成功通知",
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                    {
                        "type": "text",
                        "text": '房號: ' + room.r_id,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "separator",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": '您的房間密碼是 ['+ str(room_key) +']',
                        "wrap": True,
                        "size": "sm",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": '密碼有效時間未5分鐘',
                        "wrap": True,
                        "size": "sm",
                        "color": "#1A3852"
                    },
                    {
                        "type": "image",
                        "url": room_img_url,
                        "size": "full",
                        "aspectRatio": "15:15",
                        "aspectMode": "fit",
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "客房服務",
                            "text": "@客房服務"
                        },
                        "color": "#D5A07E"
                    }, 
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "聯絡官家",
                            "uri": "tel:09001234567"
                        },
                        "color": "#D5A07E"
                    }
                ]
            }
        }
    )
    return tempmsg

def RoomServiceMsg(uid):
    user = Users.objects.filter(lineid=uid).first()
    room = Room.objects.filter(r_users = user).first(); 
    print(room)
    if not room:
        return TextSendMessage(text='很抱歉，您尚未辦理入住手續，請先辦理入住手續後在使用該功能，謝謝。')
    else:
        msg_addcomment = f'[其他客房服務:{room.r_id}]:'
        msg_addcomment = urllib.parse.quote(msg_addcomment)
        str_uri = f'https://line.me/R/oaMessage/@875zzpvg/?{msg_addcomment}'


        flex_message = FlexSendMessage(
            alt_text="客房服務",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": room.r_id + "客房服務" ,
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1A3852"
                        },
                        {
                            "type": "separator",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": user.nick_name + " 您好,AI客房管家為您服務",
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "color": "#1A3852"
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
                            "color": "#D5A07E",
                            "margin": "sm",
                            "action": {
                                "type": "postback",
                                "label": "House Keeping",
                                "data": 'action=housekeeping&roomid=' + room.r_id,
                            }
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#D5A07E",
                            "margin": "sm",
                            "action": {
                                "type": "datatimepicker",
                                "label": "Set Morning Call",
                                "data": 'action=MorningCall&roomid=' + room.r_id ,
                                "mode":"time",
                                "initial": time(7, 30, 00).strftim("%H:%M:%S"),
                                "Max": "23:59",
                                "Min": "00:00"
                            }
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#D5A07E",
                            "margin": "sm",
                            "action": {
                                "type": "uri",
                                "label": "其他需求",
                                "uri": str_uri
                            }
                        }
                    ]
                }
            }
        )
        return flex_message