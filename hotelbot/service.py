from line_bot_api import *
from urllib.parse import parse_qsl

from extensions import db
from models.user import User
from models.reservation import Reservation

import datetime

services = {
    1:{
        'category': '中式',
        'img_url': 'https://i.imgur.com/x6neJti.jpg',
        'title': '家常菜',
        'duration': '等待 15 mins',
        'description': '嚴選在地地方料理(適合4人以下)',
        'price': 'NT$ 500'
    },
    
    2:{
        'category': '中式',
        'img_url': 'https://i.imgur.com/0k52inF.jpg',
        'title': '麵食類',
        'duration': '等待 25 mins',
        'description': '精選數道北方麵食的必吃料理(適合4人以下)',
        'price': 'NT$ 500'
    },

    3:{
        'category': '中式',
        'img_url': 'https://i.imgur.com/sidfS7p.jpg',
        'title': '海鮮',
        'duration': '等待 20 mins',
        'description': '主廚精心設計的數道海鮮料理(適合6人以下)',
        'price': 'NT$ 800'
    },

    4:{
        'category': '西式',
        'img_url': 'https://i.imgur.com/GihkzAZ.jpg',
        'title': '法式小點',
        'duration': '等待 30 mins',
        'description': '經典法式餐點',
        'price': 'average NT200'
    },

    5:{
        'category': '西式',
        'img_url': 'https://i.imgur.com/HU9TotJ.jpg',
        'title': '義大利麵',
        'duration': '等待 20 mins',
        'description': '紅醬＆白醬為主搭配口感極佳的手工麵',
        'price': 'average NT150'
    },

    6:{
        'category': '西式',
        'img_url': 'https://i.imgur.com/kJg3RvM.jpg',
        'title': '排餐類',
        'duration': '等待 15 mins',
        'description': '精心挑選肉品，雞豬牛羊一次滿足',
        'price': 'average NT200'
    }
}

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想預約的餐點類型',
        template=ImageCarouselTemplate(
        columns = [
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/sADd21I.jpg',
                            action=PostbackAction(
                                label= '中式菜餚',
                                display_text= '想了解中式菜餚',
                                data='action=service&category=中式'
                            )
                ),
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/5ZMViDq.jpg',
                            action=PostbackAction(
                                label= '西式餐點',
                                display_text= '想了解西式餐點',
                                data='action=service&category=西式'
                            )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])


def service_event(event):

    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service_id in services:
            if services[service_id]['category'] == data['category']:
                service = services[service_id]
                bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": service['img_url'],
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": service['title'],
                        "weight": "bold",
                        "wrap": True,
                        "size": "xl",
                        "color": "#854955"
                    },
                    {
                        "type": "text",
                        "text": service['duration'],
                        "size": "sm",
                        "weight": "bold",
                        "color": "#BF827F"
                    },
                    {
                        "type": "text",
                        "text": service['description'],
                        "wrap": True,
                        "size": "md",
                        "margin": "lg",
                        "color": "#CAA4A3"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"{service['price']}",
                            "size": "xl",
                            "weight": "bold",
                            "wrap": True,
                            "color": "#854955",
                            "flex": 0
                        }
                        ],
                        "margin": "xl"
                    }
                    ],
                    "spacing": "sm"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service_id}",
                        "displayText": f"我想預約【{service['title']} {service['duration']}】"
                        },
                        "style": "primary",
                        "color": "#EA5B1F"
                    }
                    ],
                    "spacing": "sm"
                }
                }

                bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text='請選擇訂餐項目',
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])
    

def service_select_date_event(event):

    data = dict(parse_qsl(event.postback.data))
    
    weekday_string ={
        0: '一',
        1: '二',
        2: '三',
        3: '四',
        4: '五',
        5: '六',
        6: '日'
    }

    business_day = [0, 1, 2, 3, 4, 5, 6]

    quick_reply_buttons = []

    today = datetime.datetime.today().date()

    for x in range(1, 8):
        day = today + datetime.timedelta(days=x)

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day} ({weekday_string[day.weekday()]})',
                                      text=f'我要預約 {day} ({weekday_string[day.weekday()]}) 這天',
                                      data=f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪一天?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))

    line_bot_api.reply_message(
        event.reply_token,
        [text_message])


def service_select_time_event(event):
     
    data = dict(parse_qsl(event.postback.data))

    available_time = ['11:00', '12:00', '18:00', '19:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(action=PostbackAction(label=time,
                                                                    text=f'{time} 這個時段',
                                                                    data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
        event.reply_token,
        [text_message])
    

def service_confirm_event(event):

    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])]

    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預約項目',
        template=ConfirmTemplate(
            text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                PostbackAction(
                    label='確定',
                    display_text='確認沒問題',
                    data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                    label='重新預約',
                    text='我想重新預約'
                )
            ]
        )
    )

    line_bot_api.reply_message(
        event.reply_token,
        [confirm_template_message])


def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           
    if reservation:
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False


def service_confirmed_event(event):

    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if is_booked(event, user):
        return
    
    reservation = Reservation(
        user_id=user.id,
        booking_service_category=f'{booking_service["category"]}',
        booking_service=f'{booking_service["title"]} {booking_service["duration"]}',
        booking_datetime=booking_datetime)
    
    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='感謝您的預約，已經幫您預約成功了~ 有任何問題歡迎您隨時聯絡我們~ ')])
    

def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_canceled = True
        
        db.session.add(reservation)
        db.session.commit()

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您的預約已經幫你取消囉')])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='您目前沒有預約喔 !')])