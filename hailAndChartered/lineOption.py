from linebot.models import *
from hailAndChartered import models
from urllib.parse import quote, parse_qsl

def HeilList(): #叫車選單
    agencys = models.hailOption.objects.all()
    bubbles = []
    for agcs in agencys:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": agcs.imgUrl,                
                "position": "relative",
                "backgroundColor": "#F6F1F1"
            },
            "body": {
                "type": "box",
                "layout": "vertical",                
                "contents": [
                    {
                        "type": "text",
                        "text": agcs.agencyName,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#002E40"
                    },                                          
                    {
                        "type": "separator",
                        "margin": "sm"
                    }
                ],                
                "backgroundColor": "#F6F1F1"
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
                        "label": "連結",
                        "uri": str(agcs.agencyUrl)
                    },
                    "color": "#EA5B1F"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="叫車選項",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def CharteredList():    #包車選單
    carTypes = models.charteredOption.objects.all()
    bubbles = []
    for cT in carTypes:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",                
                "url": cT.carImgUrl
            },
            "body": {
                "type": "box",
                "layout": "vertical",       
                "contents": [
                    {
                        "type": "text",
                        "text": cT.carType,
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                    }, 
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [ 
                                    {
                                        "type": "text",
                                        "text": "半天(5小時)",
                                        "color": "#002E40",
                                        "wrap": True,
                                        "weight": "bold",
                                        "size": "md",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "NT$" + str(cT.chtdStartPrice),
                                        "color": "#002E40"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [                                               
                                    {
                                        "type": "text",
                                        "text": "全天(10小時)",
                                        "color": "#002E40",
                                        "wrap": True,
                                        "weight": "bold",
                                        "size": "md",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "NT$" + str(cT.chtdAlldayPrice),
                                        "color": "#002E40"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [                                               
                                    {
                                        "type": "text",
                                        "text": "逾時",
                                        "color": "#002E40",
                                        "weight": "bold",
                                        "size": "sm",
                                        "flex": 1,
                                    },
                                    {
                                        "type": "text",
                                        "text": "NT$" + str(cT.timeOutPrice)+ "/小時",
                                        "size": "sm",
                                        "color": "#002E40"
                                    }
                                ]
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
                            "label": "選擇",
                            "data": f"action=carCheck&chId={cT.id}"
                        },
                        "color": "#EA5B1F"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "margin": "sm"
                    }
                ],                
            }
        }
        bubbles.append(bubble)
    
    flex_message = FlexSendMessage(
        alt_text="包車選擇",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def carServiceCheck(cId,Num,chDt,cTime,cost): #包車預約確認
    carId = cId
    cartype = models.charteredOption.objects.get(id=int(carId))  
    passengerAmount = Num
    appointmentDate = chDt.replace('T',' ')
    chtd_time = '半天' if cTime == '5h' else '全天'
    total_cost = cost
    message = FlexSendMessage(
        alt_text="包車預約單",
        contents={
            "type": "carousel",
            "contents": [{
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": cartype.carImgUrl
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [                        
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [ 
                            {
                                "type": "text",
                                "text": "預約車型",
                                "size": "md",
                                "weight": "bold",
                                "align": "start"
                            },
                            {
                                "type": "text",
                                "text": cartype.carType,
                                "size": "xl",
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "預約時間",
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": appointmentDate,
                                        "wrap": True,
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 2
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "預計人數",
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": passengerAmount+" 人",
                                        "wrap": True,
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 2
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": chtd_time,
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": "NT$" + total_cost,
                                        "wrap": True,
                                        "color": "#002E40",
                                        "size": "lg",
                                        "flex": 2
                                    }
                                ]
                            }
                        ]
                    }]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [                            
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "注意:逾時加收",
                                        "color": "#BF827F",
                                        "flex": 1,
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "NT$"+str(cartype.timeOutPrice)+"/小時",
                                        "size": "sm",
                                        "color": "#002E40"
                                    }
                                ],
                                "spacing": "sm"
                            }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "postback",
                            "label": "確認預約",
                            "data": f"action=questNote&cId={cId}&Num={Num}&chDt={chDt}&cTime={chtd_time}&cost={total_cost}"
                        },
                        "color": "#EA5B1F"
                    }
                    ],
                    "margin": "lg"
                }
                }]})
    return message

def receipt(r_data):    #LinePay支付收據
    message = FlexSendMessage(
        alt_text="LinePay收據(包車)",
        contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "包車收據",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "none",
                        "color": "#EA5B1F",
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "訂單日期",
                                "size": "sm",
                                "color": "#002E40",
                                "flex": 0,
                                "margin": "none"
                            },
                            {
                                "type": "text",
                                "text": str(r_data.pub_datetime),
                                "size": "sm",
                                "color": "#002E40",
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
                                "text": "預約車型",
                                "size": "sm",
                                "color": "#002E40",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": r_data.carType,
                                "size": "sm",
                                "color": "#002E40",
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
                                "text": "預約時間",
                                "size": "sm",
                                "color": "#002E40",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": str(r_data.appointmentDate),
                                "size": "sm",
                                "color": "#002E40",
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
                                "text": "包車預計總時",
                                "size": "sm",
                                "color": "#002E40",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": r_data.chtd_time,
                                "size": "sm",
                                "color": "#002E40",
                                "align": "end"
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "text",
                                "text": "已支付金額",
                                "size": "lg",
                                "color": "#002E40"
                            },
                            {
                                "type": "text",
                                "text": "NT$" + str(r_data.total_cost),
                                "size": "lg",
                                "color": "#EA5B1F",
                                "align": "end"
                            }
                            ]
                        }
                        ]
                    }
                    ]
                },
                "styles": {
                    "footer": {
                    "separator": True
                    }
                }
                }
    )
    return message  