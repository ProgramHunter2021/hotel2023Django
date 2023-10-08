from django.shortcuts import render
from linebot.models import *
from .models import *
from datetime import datetime, timedelta
from hotelbot.models import *
from urllib.parse import parse_qsl
# Create your views here.

#region service
def init_products():
    service_item_count =Service_Item.objects.all().count() 
    if service_item_count >0 :
        pass
    else:
        init_data=[
            Service_Item(
                        id = 1,
                        category='SPA',
                        img_url = 'https://i.imgur.com/XHkio0m.jpg',
                        title = '全身指壓',
                        duration = '90min',
                        description =  '指壓屬於東方式按摩，是一種強調經絡、穴道等特定位置的加壓按摩，透過按摩師的手指指尖、指腹、掌根等部位，以按壓、捏、敲打、搓揉等方式，刺激人體特定部位、放鬆深層肌肉，幫助能量經絡順暢流動、促進神經機能。',
                        price =100,
                        ),
            Service_Item(
                        id = 2,
                        category='SPA',
                        img_url = 'https://i.imgur.com/svAaI3j.jpg',
                        title = '足底按摩',
                        duration = '90min',
                        description =  '「腳底按摩」能藉著刺激各部位反射區，使血液循環順暢，排除積聚在體內的廢物或毒素，使新陳代謝作用正常運作，達到治療的效果。',
                        price =100,
            ),
            Service_Item(
                        id = 3,
                        category='美甲美睫',
                        img_url = 'https://i.imgur.com/9b42t9d.png',
                        title = '美甲',
                        duration = '一次',
                        description =  '打造專屬個人風格的亮麗指甲',
                        price =100,
            ),
            Service_Item(
                        id = 4,
                        category='美甲美睫',
                        img_url = 'https://i.imgur.com/auEtnrJ.jpg',
                        title = '美睫',
                        duration = '一次',
                        description =  '使您的雙眼閃閃動人',
                        price =100,
            )]
        for item in init_data:
            item.save()

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text = '請選擇想服務類別',
        template = ImageCarouselTemplate(
        columns = [
                ImageCarouselColumn(
                image_url = 'https://i.imgur.com/yQhVPNj.jpg',
                action = PostbackAction(
                    label = 'SPA',
                    display_text = 'SPA',
                    data = 'action=service&category=SPA'
                )
                ),
                ImageCarouselColumn(
                image_url = 'https://i.imgur.com/tE5e5p3.jpg',
                action = PostbackAction(
                    label = '美甲美睫',
                    display_text = '美甲美睫',
                    data = 'action=service&category=美甲美睫'
                )
                )
        ]
        )
    )
    return image_carousel_template_message

def list_reservation_event(event):
    reservations = Reservation.objects.filter(is_canceled = False, 
                                              reservation_date__gte = datetime.now()).order_by('reservation_date').all()
    reservation_data_text = '## 預約名單: ## \n\n'
    #跑每一筆的預約資料
    for reservation in reservations:
        user=reservation.user
        reservation_data_text += f'''預約日期: {reservation.reservation_date}
                                預約服務: {reservation.service}
                                姓名: {user.name}\n'''

    return TextSendMessage(text=reservation_data_text)

def service_event(event):
    services = Service_Item.objects.all()
    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service in services:
        if service.category == data['category']:
            bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": service.img_url
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": service.title,
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "text",
                    "text": service.duration,
                    "size": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": service.description,
                    "margin": "lg",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": f"NT$ {service.price}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0
                    }
                    ],
                    "margin": "xl"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                    "type": "postback",
                    "label": "預約",
                    "data": f"action=select_date&service_id={service.id}",
                    "displayText": f"我想預約【{service.title} {service.duration}】"
                    },
                    "color": "#b28530"
                }
                ]
            }
            }

            bubbles.append(bubble)

    flex_message = FlexSendMessage(
         alt_text = '請選擇預約項目',
         contents={
              "type":"carousel",
              "contents":bubbles
         }
    )

    return flex_message

def service_select_date_event(event):
    data = dict(parse_qsl(event.postback.data))

    weekdat_string={
          0:'一',
          1:'二',
          2:'三',
          3:'四',
          4:'五',
          5:'六',
          6:'日',
     }#休息日就拿掉

    business_day = [1,2,3,4,5,6]#休息日就拿掉

    quick_reply_buttons = []

    today = datetime.today().date()#取得當天日期
    #weekday()取得星期幾?0是星期一
    for x in range(0,5):
        day = today + timedelta(days=x)#透過datetime.timedelta()可以取得隔天的日期
        

        if day != 0 and (day.weekday() in business_day):
            quick_reply_button = QuickReplyButton(
                action = PostbackAction(label=f'{day}({weekdat_string[day.weekday()]})',
                                        text=f'我要預約{day}({weekdat_string[day.weekday()]})這天',
                                        data= f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text="請問要預約哪一天？",
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    return text_message

#選擇時間功能
def service_select_time_event(event):
    data = dict(parse_qsl(event.postback.data))

    available_time=['11:00', '14:00' ,'17:00', '20:00'] #可以自己更改時間段

    quick_reply_buttons = []

    for time in available_time:
         quick_reply_button = QuickReplyButton(action= PostbackAction(label=time,
                                                                       text=f'{time}這個時段',
                                                                       data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
         quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    return text_message

def service_confirm_event(event):
    data = dict(parse_qsl(event.postback.data))
    service = Service_Item.objects.filter(id = int(data['service_id'])).first()
    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預約項目',
        template = ConfirmTemplate(
            text=f'您即將預約\n\n{service.title} {service.duration}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                PostbackAction(
                        label='確定',
                        display_text='確定沒問題！',
                        data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                        label='重新預約',
                        text='@預約服務'
                )
            ]
        )
    )
    return confirm_template_message

def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))
    service = Service_Item.objects.filter(id = int(data['service_id'])).first()
    booking_datetime = datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')
    user = Users.objects.filter(lineid = event.source.user_id).first()
    reservation = Reservation.objects.filter(user = user, 
                                             is_canceled = False, 
                                             reservation_date__gte = datetime.now()).first()
    if reservation:
        print('Get reservation')
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.service}\n預約時段: {reservation.reservation_date}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )
        return buttons_template_message
    else:
        print('no reservation')
        reservation = Reservation(user = user, 
                                  category = service.category, 
                                  service = f'{service.title} {service.duration}',
                                  reservation_date = booking_datetime)
        reservation.save()
        return TextSendMessage(text='沒問題! 感謝您的預約，我已經幫你預約成功了喔，到時候見!')
            
#取消預約 資料庫欄位不會drop,是 is_cacnceled欄位會變成true
def service_cancel_event(event):
    user = Users.objects.filter(lineid = event.source.user_id).first()
    reservation = Reservation.objects.filter(user == user,
                                             is_canceled = False, 
                                             reservation_date__gte = datetime.now()).first()
    if reservation:
        reservation.is_canceled = True
        reservation.save()

        message = TemplateSendMessage(
            alt_text='您的預約已幫你取消了！',
            template=ConfirmTemplate(
                text='您的預約已幫你取消了！',
                actions=[                     
                    MessageAction(
                        label='重新預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )
        return message
    else:
        message = TemplateSendMessage(
            alt_text='您目前沒有預約喔！',
            template=ConfirmTemplate(
                text='您目前沒有預約喔！',
                actions=[                     
                    MessageAction(
                        label='我要預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )
        return message

#endregion 

#region food 

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

def dining_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想預約的餐點類型',
        template=ImageCarouselTemplate(
        columns = [
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/sADd21I.jpg',
                            action=PostbackAction(
                                label= '中式菜餚',
                                display_text= '想了解中式菜餚',
                                data='action=dining&category=中式'
                            )
                ),
                ImageCarouselColumn(
                            image_url= 'https://i.imgur.com/5ZMViDq.jpg',
                            action=PostbackAction(
                                label= '西式餐點',
                                display_text= '想了解西式餐點',
                                data='action=dining&category=西式'
                            )
                )
            ]
        )
    )
    return image_carousel_template_message

def dining_event(event):

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
                        "data": f"action=dining_select_date&service_id={service_id}",
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

    return flex_message

def dining_select_date_event(event):

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

    today = datetime.today().date()

    for x in range(1, 8):
        day = today + timedelta(days=x)

        if day.weekday() in business_day:
            quick_reply_button = QuickReplyButton(
                action=PostbackAction(label=f'{day} ({weekday_string[day.weekday()]})',
                                      text=f'我要預約 {day} ({weekday_string[day.weekday()]}) 這天',
                                      data=f'action=dining_select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪一天?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))

    return text_message

def dining_select_time_event(event):
     
    data = dict(parse_qsl(event.postback.data))

    available_time = ['11:00', '12:00', '18:00', '19:00']

    quick_reply_buttons = []

    for time in available_time:
        quick_reply_button = QuickReplyButton(action=PostbackAction(label=time,
                                                                    text=f'{time} 這個時段',
                                                                    data=f'action=dining_confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
        quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段?',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    return text_message
    
def dining_confirm_event(event):

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
                    data=f'action=dining_confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                ),
                MessageAction(
                    label='重新預約',
                    text='@預約餐廳服務'
                )
            ]
        )
    )

    return confirm_template_message

def dining_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))
    service = services[int(data['service_id'])]
    booking_datetime = datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')
    user = Users.objects.filter(lineid = event.source.user_id).first()
    reservation = Reservation.objects.filter(user = user, 
                                             is_canceled = False, 
                                             reservation_date__gte = datetime.now()).first()
    # if reservation:
    #     buttons_template_message = TemplateSendMessage(
    #         alt_text='您已經有預約了，是否需要取消?',
    #         template=ButtonsTemplate(
    #             title='您已經有預約了',
    #             text=f'{reservation.service}\n預約時段: {reservation.reservation_date}',
    #             actions=[
    #                 PostbackAction(
    #                     label='我想取消預約',
    #                     display_text='我想取消預約',
    #                     data='action=dining_cancel'
    #                 )
    #             ]
    #         )
    #     )
    #     return buttons_template_message
    # else :
    reservation = Reservation(user = user, 
                                category = service["category"], 
                                service = f'{service["title"]} {service["duration"]}',
                                reservation_date = booking_datetime)
    reservation.save()
    return TextSendMessage(text='感謝您的預約，已經幫您預約成功了~ 有任何問題歡迎您隨時聯絡我們~ ')

def dining_cancel_event(event):
    user = Users.objects.filter(lineid = event.source.user_id).first()
    reservation = Reservation.objects.filter(user = user, 
                                             is_canceled = False, 
                                             reservation_date__gte = datetime.now()).first()
    
    if reservation:
        reservation.is_canceled = True
        reservation.save()

        return TextSendMessage(text='您的預約已經幫你取消囉')
    else:
        return TextSendMessage(text='您目前沒有預約喔 !')


#endregion 
