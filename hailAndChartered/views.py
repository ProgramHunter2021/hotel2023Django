from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.generic import View, TemplateView
# import base64, pickle

from hailAndChartered import models
import datetime

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from urllib.parse import quote, parse_qsl
from hailAndChartered.lineOption import *
import uuid, requests, json

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

PAY_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/request'   #測試
CONFIRM_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/{}/confirm'    #測試

LINE_PAY_ID = '1657362199'   #((改))
LINE_PAY_SECRET = '171192f29cdc223d91da297cb60c87bc'   #((改))
STORE_IMAGE_URL = 'https://i.imgur.com/fN6dgex.jpg'   #((改))

def confirmed(request):
    transaction_id = request.GET['transactionId']
    order = models.chartered_order.objects.filter(transaction_id = transaction_id).first()
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
    if request.method=='POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        message = []

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                uid = event.source.user_id
                profile = line_bot_api.get_profile(uid)
                name = profile.display_name                
                msgtext = event.message.text
                
                #訊息判斷區
                if '@關於我們' in msgtext:
                    message.append(TextSendMessage(text="本聊天室為包車叫車測試"))

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
                    nowT = str(datetime.datetime.now())
                    after7Day = str(datetime.datetime.now() + datetime.timedelta(days=7))
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

            elif isinstance(event, PostbackEvent):
                uid = event.source.user_id
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
                                                                   uri='line://oaMessage/{bid}/?{message}'.format(bid='@523goiva',message=quote(f"{chId}/輸入人數:")), # ((改))
                                                               )
                                                           )
                                                       ]
                                                   )))
                
                elif "idAndNum" in event.postback.data:   #包車step3
                    cId = event.postback.data.replace('idAndNum:','').split('/')[0]
                    Num = event.postback.data.replace('idAndNum:','').split('/')[1]
                    chDt = event.postback.params.get("datetime")
                    cartype = models.charteredOption.objects.get(id=cId)
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
                                        data=f'action=checkout&cId={cId}&Num={Num}&chDt={chDt}&cTime=10h&cost={cartype.chtdStartPrice}')),
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
                    cartype = models.charteredOption.objects.get(id=int(data.get('cId'))).carType
                    passengerAmount = int(data.get('Num'))
                    appointmentDate = datetime.datetime.strptime(data.get('chDt'),'%Y-%m-%dT%H:%M')
                    chtd_time = data.get('cTime')
                    total_cost = data.get('cost')
                    order_post = models.chartered_order.objects.create(userId = uid, appointmentDate = appointmentDate, 
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
                                                                    uri='line://oaMessage/{bid}/?{message}'.format(bid='@523goiva',message=quote(f"{oId}/請描述特殊需求(100字內):")), # ((改))
                                                               )
                                                           )
                                                       ]
                                                   )))
                elif p_action == 'booking':                    
                    message.append(linePay_confirm(data.get('oId')))  #結帳
    
            if message:
                line_bot_api.reply_message(event.reply_token, message)

        return HttpResponse()
    else:
        return HttpResponseBadRequest() 

def linePay_confirm(oId):
    order_target = models.chartered_order.objects.get(id=oId)
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
        self.redirect_url = 'https://465e-49-159-211-14.ngrok-free.app/confirm'   #((改))
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