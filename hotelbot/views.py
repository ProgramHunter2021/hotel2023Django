from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.forms.models import model_to_dict
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from .models import * 

from .MsgBuilder import *
from booking.MsgBuilder import * 
from activity.MsgBuilder import *

from hotelbot.RichMenu import *
from hailAndChartered.lineOption import *
from hailAndChartered.models import *


from booking.utils import *
import re
import ast
from datetime import datetime, timedelta
import uuid, requests, json

from reservation.views import *

# Create your views here.

# region Linebot

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

# line_pay_api = LineBotApi(settings.PAY_API_URL)
# line_pay_comfirm = LineBotApi(settings.CONFIRM_API_URL)
# line_pay_id = LineBotApi(settings.LINE_PAY_ID)
# line_pay_secret = LineBotApi(settings.LINE_PAY_SECRET)
# qrcode_image = 

PAY_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/request'   #測試
CONFIRM_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/{}/confirm'    #測試

LINE_PAY_ID = '1657362199'   #((改))
LINE_PAY_SECRET = '171192f29cdc223d91da297cb60c87bc'   #((改))
STORE_IMAGE_URL = 'https://i.imgur.com/fN6dgex.jpg'   #((改))


richmenu = rich_mene()
#init_products()

def confirmed(request):
    transaction_id = request.GET['transactionId']
    order = chartered_order.objects.filter(transaction_id = transaction_id).first()
    if order:
        line_pay = LinePay()
        line_pay.confirm(transaction_id=transaction_id, amount=order.total_cost)
                
        order.paid = True #確認收款無誤時,改成已付款
        order.save()
        
        #傳收據給用戶
        message = receipt(order) 
        line_bot_api.push_message(to=order.userId, messages=message)
        thxMsg = '付款已完成，感謝您的消費'
        return render(request, 'paySuccess.html', {'thxMsg': thxMsg}) #((要改))render之類的


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            uid=event.source.user_id
            message=[]
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url

                user = Users.objects.filter(lineid=uid).first()
                if not user:
                    Users.objects.create(lineid=uid,nick_name=name,image_url=pic_url)
                    # message.append(TextSendMessage(text='會員資料新增完畢'))
                else:
                    user.nick_name = name
                    user.image_url = pic_url
                    user.save(); 
                    # message.append(TextSendMessage(text='已經有建立會員資料囉'))

                msgtext = event.message.text
                
                # region 訊息判斷

                if '@週邊活動' in msgtext or '@周邊景點' in msgtext:
                    #message.append(list_all_activities())
                    message.append(list_activity_type())

                elif '[周邊類別]' in msgtext:
                    straid = msgtext.split(':')[1] 
                    message.append(list_all_activities(straid))

                elif '@訂房服務' in msgtext:
                    message.append(PreBookingProcessMsg(uid)) 

                elif '[UpdateUserInfo]' in msgtext:
                    msgtext = msgtext.replace('[UpdateUserInfo]','')
                    datacontexts = re.split('{|,|}', msgtext)
                    data = {}
                    for context in datacontexts:
                        if context:
                            key_val = context.split(':')
                            data[key_val[0]] = key_val[1] if key_val[1] else ''
                    user.name = data['name']
                    user.birthday = data['Birth']
                    user.email = data['email']
                    user.address = data['addr']
                    user.phone = data['phone']
                    user.einvoice = data['einvoice']
                    user.GUInumber = data['GUI']
                    user.save()
                    message.append(TextSendMessage(text=f'{user.name} 您好, 您的個人資料已經更新.'))

                elif '[SearchRoom]' in msgtext:
                    msgtext = msgtext.replace('[SearchRoom]','')
                    datacontexts = re.split('{|,|}', msgtext)
                    data = {}
                    for context in datacontexts:
                        if context:
                            key_val = context.split(':')
                            data[key_val[0]] = key_val[1]
                    message.append(list_all_RoomTypes(data))

                elif '@訂房紀錄' in msgtext:
                    message.append(List_Booking_recoder(uid))

                elif '@入住登記' in msgtext or '@CHECKIN' in msgtext:
                    # Pre_CheckIn_Msg(uid)
                    message.append(Pre_CheckIn_Msg(uid))

                elif '[IDScanResult]' in msgtext:
                    idnum = msgtext.split(':')[1] 
                    message.append(CheckInResultMsg(uid, idnum))
                
                elif '@房間密碼' in msgtext:
                    message.append(RoomKeyMsg(uid))
                    #message.append(RoomKeyMsg(uid))

                elif '@客房服務' in msgtext:
                    message.append(RoomServiceMsg(uid))

                elif '[其他客房服務' in msgtext:
                    roomid = msgtext.split(':')[0].split('|')[1].replace(']','')
                    message.append(TextSendMessage(text=f'{user.nick_name} 您好, [{roomid}] 的客房服務需求已經為您送出,我們將盡快為您服務.'))

                elif '添加備註' in msgtext:
                    orderid = msgtext.split(':')[0].split('|')[1].replace(']','')
                    # 修改資料庫
                    message.append(TextSendMessage(text=f'{user.nick_name} 您好, [{orderid}] 訂單的備註已經為您新增,謝謝.'))

                elif '@專屬管家' in msgtext:
                    message.append(TextSendMessage(text=f'{user.nick_name} 您好,請留言您的相詢問的問題,您的專屬管家將儘快為您服務.'))

                elif '[GET MAP]' in msgtext:
                    strLocationName = msgtext.split(':')[1] 
                    message.append(GetMapMessage(strLocationName))

                #包車
                elif '@搭車出門' in msgtext:                    
                    message.append(TextSendMessage(
                        text='請問您要叫車? 還是包車出遊呢?',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label='我要叫車',
                                        display_text='我要叫車',
                                        data='action=heil')),
                                QuickReplyButton(
                                    action=PostbackAction(
                                        label='我要包車',
                                        display_text='我要包車',
                                        data='action=chartered')),
                            ]
                        )
                    ))

                elif "輸入人數:" in msgtext:  #包車step2
                    #字串整理
                    n_msg = msgtext.replace('輸入人數:','')
                    nowT = str(datetime.now())
                    after7Day = str(datetime.now() + timedelta(days=7))
                    message.append(TextSendMessage(
                        text='請問您什麼時間要包車呢?',
                        quick_reply=QuickReply(
                            items=[
                                QuickReplyButton(
                                    action=DatetimePickerAction(
                                        label="選擇時間",
                                        data = "idAndNum:" + n_msg,
                                        mode = 'datetime',
                                        initial = nowT[:10]+'t'+nowT[11:16],
                                        max = after7Day[:10]+'t'+after7Day[11:16],
                                        min = nowT[:10]+'t'+nowT[11:16])
                                )
                            ]
                        )
                    ))

                elif "請描述特殊需求(" in msgtext:                    
                    oId = msgtext.split('/請描述')[0]
                    spnd = msgtext.split('(100字內):')[1]
                    order_target = models.chartered_order.objects.get(id = oId)
                    if order_target.userId == uid:
                        order_target.questNote = spnd
                        order_target.save()
                        message.append(TextSendMessage(text="請按下方送出特殊需求",
                                                   quick_reply=QuickReply(
                                                       items=[
                                                            QuickReplyButton(
                                                                action=PostbackAction(
                                                                    label='送出',
                                                                    display_text='送出',
                                                                    data=f'action=booking&oId={oId}'))
                                                       ])))
                    else:
                        message.append(TextSendMessage(text='抱歉，此包車預約並非您本人提出，無法更動。'))

                # endregion
                
                elif '@預約設施服務' in msgtext:
                    message.append(service_category_event(event))

                elif '@預約紀錄' in msgtext:
                    message.append(list_reservation_event(event))

                elif '@預約餐廳服務' in msgtext:
                    message.append(dining_category_event(event))

                elif msgtext == '@取消預約':
                    pass
            
            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')
                if event.postback.data == "action=nextpage":
                    line_bot_api.link_rich_menu_to_user(uid, richmenu.id_second)

                elif event.postback.data == "action=previouspage":
                    line_bot_api.link_rich_menu_to_user(uid, richmenu.id_first)

                elif event.postback.data.startswith('action=BookRoomType'):
                    strdata = event.postback.data.replace('action=BookRoomType&','')
                    data = ast.literal_eval(strdata)
                    print(datetime.strptime(data['from'], '%Y-%m-%d'))
                    print(datetime.today())
                    if (datetime.strptime(data['from'], '%Y-%m-%d')<datetime.today()+timedelta(days=1)):
                        message.append(TextSendMessage(text='連接已經失效,請重新操作訂房流程.'))
                    else :
                        # Get_ConfirmBookingInfo_Msg(uid, data)
                        message.append(Get_ConfirmBookingInfo_Msg(uid, data))

                elif event.postback.data.startswith('action=ConfirmBooking'):
                    strdata = event.postback.data.replace('action=ConfirmBooking&','')
                    data = ast.literal_eval(strdata)
                    print(data)
                    message.append(replyMsg_CreateBooking(uid, data))

                elif event.postback.data == "action=Cancelbooking":
                    #未送出訂單取消訂房流程
                    message.append(TextSendMessage(text='訂房流程已取消,我們感到非常的遺憾,希望日後還可以為您服務.'))

                elif event.postback.data == "action=paydeposit":
                    #支付訂金
                    pass

                elif event.postback.data == "action=checkbookingrecord":
                    #訂房紀錄
                    message.append(List_Booking_recoder(uid))

                elif event.postback.data.startswith("action=CanelBookedOrder"):
                    #取消訂房紀錄
                    orderid = event.postback.data.split('&')[1].split('=')[1]
                    order = Order.objects.filter(o_id = orderid).first(); 
                    BookingRoom.objects.filter(order = order).all().delete()
                    order.delete()
                    message.append(TextSendMessage(text=f'您的訂房紀錄[{orderid}]已經取消,希望日後還有機會為您服務.'))

                elif "action=housekeeping" in event.postback.data:
                    roomid = event.postback.data.split('&')[1].split('=')[1]
                    message.append(TextSendMessage(text=f'{user.nick_name} 您好, 我們將儘快前往 [{roomid}] 進行清潔.'))

                elif "action=MorningCall" in event.postback.data:
                    roomid = event.postback.data.split('&')[1].split('=')[1]
                    strtime = event.postback.params.get('time')
                    message.append(TextSendMessage(text=f'{user.nick_name} 您好, 為您設定 Morning call 的時間為 {strtime}'))

                else: 
                    data = dict(parse_qsl(event.postback.data)) #先將postback中的資料轉成字典
                    p_action = data.get('action') #get action裡面的值
                    if p_action == "heil":  #叫車選單
                        message.append(HeilList())

                    #包車選項流程    
                    elif p_action == "chartered":   #呼叫選單
                        message.append(CharteredList()) 

                    elif p_action == "carCheck":  #包車step1
                        chId = data.get('chId')
                        message.append(TextSendMessage(text="請問有多少乘客呢?",
                                                    quick_reply=QuickReply(
                                                        items=[
                                                            QuickReplyButton(
                                                                action=URIAction(
                                                                    label="輸入人數",
                                                                    uri='line://oaMessage/{bid}/?{message}'.format(bid='@774ulqej',message=quote(f"{chId}/輸入人數:")), # ((改))
                                                                )
                                                            )
                                                        ]
                                                    )))
                    
                    elif "idAndNum" in event.postback.data:   #包車step3
                        cId = event.postback.data.replace('idAndNum:','').split('/')[0]
                        Num = event.postback.data.replace('idAndNum:','').split('/')[1]
                        chDt = event.postback.params.get("datetime")
                        cartype = charteredOption.objects.get(id=cId)
                        message.append(TextSendMessage(
                            text='您當天要包車全天(10小時)還是半天(5小時)呢?',
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            label=f'半天(${cartype.chtdStartPrice})',
                                            display_text='半天',
                                            data=f'action=checkout&cId={cId}&Num={Num}&chDt={chDt}&cTime=5h&cost={cartype.chtdStartPrice}')),
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            label=f'全天(${cartype.chtdAlldayPrice})',
                                            display_text='全天',
                                            data=f'action=checkout&cId={cId}&Num={Num}&chDt={chDt}&cTime=10h&cost={cartype.chtdAlldayPrice}')),
                                ]
                            )
                        ))
                    
                    elif p_action == "checkout":  #包車step4
                        cId = data.get('cId')
                        Num = data.get('Num')
                        chDt = data.get('chDt')
                        cTime = data.get('cTime')
                        cost = data.get('cost')
                        message.append(carServiceCheck(cId,Num,chDt,cTime,cost))    #呼叫選單

                    elif p_action == "questNote":  #包車寫入，並詢問特殊需求
                        cartype = charteredOption.objects.get(id=int(data.get('cId'))).carType
                        passengerAmount = int(data.get('Num'))
                        appointmentDate = datetime.strptime(data.get('chDt'),'%Y-%m-%dT%H:%M')
                        chtd_time = data.get('cTime')
                        total_cost = data.get('cost')
                        order_post = chartered_order.objects.create(userId = uid, appointmentDate = appointmentDate, 
                                                                            carType = cartype, passengerAmount = passengerAmount,
                                                                            chtd_time = chtd_time, total_cost = int(total_cost))
                        oId = order_post.id
                        message.append(TextSendMessage(text="最後，請問這次包車有什麼特殊需求需要幫您注意的嗎?",
                                                    quick_reply=QuickReply(
                                                        items=[
                                                                QuickReplyButton(
                                                                    action=PostbackAction(
                                                                        label='沒有，直接結帳',
                                                                        display_text='結帳',
                                                                        data=f'action=booking&oId={oId}')), 
                                                                QuickReplyButton(
                                                                    action=URIAction(
                                                                        label="我想填寫需求",
                                                                        uri='line://oaMessage/{bid}/?{message}'.format(bid='@774ulqej',message=quote(f"{oId}/請描述特殊需求(100字內):")), # ((改))
                                                                )
                                                            )
                                                        ]
                                                    )))
                    
                    elif p_action == 'booking':                    
                        message.append(linePay_confirm(data.get('oId')))  #結帳
    
                    elif p_action == 'service':
                        message.append(service_event(event))
                    
                    elif p_action == 'select_date':
                        message.append(service_select_date_event(event))
                    
                    elif p_action == 'select_time':
                        message.append(service_select_time_event(event))
                    
                    elif p_action == 'confirm':
                        message.append(service_confirm_event(event))
                    
                    elif p_action == 'confirmed':
                        message.append(service_confirmed_event(event))
                    
                    elif p_action == 'cancel':
                        message.append(service_cancel_event(event))

                    elif data.get('action') == 'dining':
                        message.append(dining_event(event))
                    elif data.get('action') == 'dining_select_date':
                        message.append(dining_select_date_event(event))
                    elif data.get('action') == 'dining_select_time':
                        message.append(dining_select_time_event(event))
                    elif data.get('action') == 'dining_confirm':
                        message.append(dining_confirm_event(event))
                    elif data.get('action') == 'dining_confirmed':
                        message.append(dining_confirmed_event(event))
                    elif data.get('action') == 'dining_cancel':
                       message.append(dining_cancel_event(event))

            elif isinstance(event, FollowEvent):
                print('加入好友')

            elif isinstance(event, UnfollowEvent):
                print('取消好友')

            elif isinstance(event, JoinEvent):
                print('進入群組')

            elif isinstance(event, LeaveEvent):
                print('離開群組')

            elif isinstance(event, MemberJoinedEvent):
                print('有人入群')

            elif isinstance(event, MemberLeftEvent):
                print('有人退群')

            if len(message):
                line_bot_api.reply_message(event.reply_token,message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
# endregion

# Line Pay
def linePay_confirm(oId):
    order_target = chartered_order.objects.get(id=oId)
    if order_target.paid == False:
        order_uuid = uuid.uuid4().hex
        cost = order_target.total_cost

        line_pay = LinePay()
        info = line_pay.pay(product_name='Chengyi_chartered_service',
                            amount=cost,
                            order_id=order_uuid,
                            product_image_url=STORE_IMAGE_URL)  
        pay_web_url = info['paymentUrl']['web'] 
        transaction_id = info['transactionId']
        order_target.transaction_id = transaction_id   #登錄官方回傳值
        order_target.save()
        msg = TemplateSendMessage(
            alt_text='Thanks message',
            template=ButtonsTemplate(
                text='請點選下方金額進行LinePay支付',
                actions=[
                    URIAction(label=f'Pay NT${cost}', uri=pay_web_url)
                ]
            )
        )
    else:
        msg = TextSendMessage(text="您已經支付此訂單訂金")
    return msg 

class LinePay():
    def __init__(self, currency='TWD'):
        self.channel_id = LINE_PAY_ID
        self.secret = LINE_PAY_SECRET
        self.redirect_url = 'https://f47f-2001-b011-3003-3da8-e171-e7f0-bc38-9e14.ngrok-free.app/confirm'   #((改))
        self.currency = currency

    def _headers(self, **kwargs): #會自動帶入上述三個設定
        return {**{'Content-Type': 'application/json',
                   'X-LINE-ChannelId': self.channel_id,
                   'X-LINE-ChannelSecret': self.secret},
                **kwargs}

    def pay(self, product_name, amount, order_id, product_image_url=None):
        data = {    #pay方法用字典帶入我們所需要的值
            'productName': product_name,
            'amount': amount,
            'currency': self.currency,
            'confirmUrl': self.redirect_url,
            'orderId': order_id,
            'productImageUrl': product_image_url
        }
        #把上面資料轉換成json格式並帶入headers，利用post方法送出資料
        response = requests.post(PAY_API_URL, headers=self._headers(), data=json.dumps(data).encode('utf-8'))
        #response就是line的回應
        return self._check_response(response)   #取得回應後透過_check_response確認

    def confirm(self, transaction_id, amount):  #首先會接收transaction_id, total_cost
        data = json.dumps({#接著把這些資料轉成json格式
            'amount': amount,
            'currency': self.currency
        }).encode('utf-8')
        response = requests.post(CONFIRM_API_URL.format(transaction_id), headers=self._headers(), data=data)

        return self._check_response(response)

    def _check_response(self, response):
        res_json = response.json()
        print(f"returnCode: {res_json['returnCode']}")
        print(f"returnMessage: {res_json['returnMessage']}")

        if 200 <= response.status_code < 300:
            if res_json['returnCode'] == '0000':#確認狀態為0000再return res_json['info']
                return res_json['info']
        #裡面的資料包含有付款的URL & transaction_id
        raise Exception('{}:{}'.format(res_json['returnCode'], res_json['returnMessage']))

