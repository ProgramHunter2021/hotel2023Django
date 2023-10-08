import os
import requests
from linebot import LineBotApi
from linebot.models import *
from django.conf import settings

class rich_mene():
    id_first = ""
    id_second = ""

    def __init__(self):
        self.id_first = self.get_rich_menu_id_first()
        self.id_second = self.get_rich_menu_id_second()

    def get_rich_menu_id_first(self):
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # create rich menu
        # from https://developers.line.biz/en/reference/messaging-api/#create-rich-menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=1200, height=810), #2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="NextPage",
            chat_bar_text="See Menu",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=425, y=575, width=355, height=220),
                    action=MessageAction(label='周邊娛樂', text='@週邊活動')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=25, y=550, width=355, height=235),
                    action=MessageAction(label='專屬管家', text='@專屬管家')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=421, y=20, width=760, height=240),
                    action=MessageAction(label='搭車出遊', text='@搭車出門')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=425, y=300, width=760, height=245),
                    action=MessageAction(label='設施體驗', text='@預約設施服務')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=825, y=575, width=355, height=220),
                    action=MessageAction(label='餐飲服務', text='@預約餐廳服務')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=25, y=25, width=355, height=465),
                    action=PostbackAction(label='Next Page', data='action=nextpage')),
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)
        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join(settings.STATICFILES_DIRS[0], 'img', 'firstpage.jpg'), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
        # set as default image
        url = "https://api.line.me/v2/bot/user/all/richmenu/" + rich_menu_id
        requests.post(url, headers={"Authorization": "Bearer " + settings.LINE_CHANNEL_ACCESS_TOKEN})

        return rich_menu_id

    def get_rich_menu_id_second(self):
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # create rich menu
        # from https://developers.line.biz/en/reference/messaging-api/#create-rich-menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=1200, height=810), #2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="Controller",
            chat_bar_text="Controller",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=25, y=25, width=710, height=340),
                    action=MessageAction(label='訂房服務', text='@訂房服務')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=25, y=395, width=710, height=280),
                    action=URIAction(label='IG', uri='https://liff.line.me/1657480937-rEM96eB8')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=790, y=25, width=355, height=250),
                    action=MessageAction(label='訂房查詢', text='@訂房紀錄')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=790, y=300, width=355, height=250),
                    action=MessageAction(label='我的房卡', text='@房間密碼')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=790, y=580, width=355, height=250),
                    action=MessageAction(label='客房服務', text='@客房服務')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=25, y=700, width=710, height=95),
                    action=PostbackAction(label='Previous Page', data='action=previouspage')),
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)
        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join(settings.STATICFILES_DIRS[0], 'img', 'secondpage.png'), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        return  rich_menu_id

    