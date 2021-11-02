import requests
import datetime
import json
import sys
import os

import vk_api
from openpyxl import load_workbook
from vk_api import VkUpload
from pprint import pprint
from loguru import logger

dir = os.path.abspath(__file__)
sys.path.append(r"D:\git\TopUsersVkWeb")
print(dir)

from utils import date_transl, date_get_days
from VKParsers import VkParser
from Drawing import Draw

wb = load_workbook('./base.xlsx')
ws = wb.active

VKAPI = "https://api.vk.com/method/"
TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
# TOKEN = "5225fcc35756b681f39a5f8666851ca3639692744092fe64f2623d666e350ea385644d98befff2cd01ba5"
#TOKEN = "14a571e87a41be67b7fd3464027cc8af8ecce427bb6dc797f211f8e46089621855a804b17ba7e3614bd76"
V = "5.21"
VKTOKEN = f"&access_token={TOKEN}&v={V}"

vkSession = vk_api.VkApi(token=TOKEN)
Upload = VkUpload(vkSession)
vk = vkSession.get_api()

message = ["""
🖐🏻Завтра у вас заканчивается услуга поздравлений для группы: {}

👰Напоминаю стоимость за месяц {} рублей
Оплатить можно на мою карту СБЕРА (Максим Д.) и прислать сюда чек:
4817 7601 1579 9250
""","""
🖐🏻Закончились оплаченные дни для группы: {}
Новое поздравление завтра уже не выйдет!

👰Cтоимость за месяц всего {} рублей
Оплатить можно на мою карту СБЕРА (Максим Д.) и прислать сюда чек:
4817 7601 1579 9250
"""]

logger.debug("load all class and config")

def sendPost(message, url):
    logger.debug(f"SendPost: Start")

    if "public" in url:
        name = url.split('/')[-1]
        id = name.replace("public","")
        logger.debug(f"SendMessage: Send to public -{id}")
    else:
        name = url.split('/')[-1]
        response = requests.get(f"{VKAPI}utils.resolveScreenName?screen_name={name}{VKTOKEN}")
        id = response.json()["response"]["object_id"]
        logger.debug(f"SendMessage: Send to group -{id}")

    photo = Upload.photo_wall("..\static\images\\tmp.jpg", group_id=id)[0]
    attachments = f"photo{photo['owner_id']}_{photo['id']}"
    logger.debug(f"SendMessage: Send photo {attachments}")
    data={
        'owner_id': f"-{id}",
        'access_token': TOKEN,
        'from_group': 1,
        'message': message,
        'attachments': attachments,
        'signed': 0,
        'v': 5.81}

    try:
        r = vk.wall.post(owner_id = id*-1, message = message, attachments = attachments)#, from_group = 1, publish_date = date)
    except:
        r = requests.post(f'{VKAPI}wall.post', data).json()

    logger.debug(f"SendMessage: End with {r}")

def sendMessage(urlSend="",urlGroup="url",coast="124", type=0):
    logger.debug(f"SendMessage: Start with type {type}")
    groupTOKEN = "9bf2d0f63a7acfa955dcc3a374ea70a2812e48e43c4e840d64fe6816f02a4d67f1d28b18d74374b2d873d"

    urlSend = urlSend.split("=")[-1]
    logger.debug(f"SendMessage: Send to {urlSend}")
    data={
        'user_id': urlSend,
        'access_token': TOKEN,
        'message': message[type].format(urlGroup, coast),
        'v': 5.81}

    r = requests.post(f'{VKAPI}messages.send', data).json()
    logger.debug(f"SendMessage: End with {r}")

def sendMessagePost(message, url): ####ALARM DON'T end#### доделать отправку в личку чела
    logger.debug(f"SendMessagePost: Start")
    # groupTOKEN = "9bf2d0f63a7acfa955dcc3a374ea70a2812e48e43c4e840d64fe6816f02a4d67f1d28b18d74374b2d873d"

    if "=" in url:
        id = url.split("=")[-1]
        logger.debug(f"SendMessagePost: {id}")
    elif "public" in url:
        name = url.split('/')[-1]
        id = name.replace("public","")
        logger.debug(f"SendMessagePost: {id}")
    elif "club" in url:
        name = url.split('/')[-1]
        id = name.replace("club","")
        logger.debug(f"SendMessagePost: {id}")
    # if "public" in url:
    #     logger.debug(f"SendMessagePost: Send to public {id}")
    # else:
    #     name = url.split('/')[-1]
    #     response = requests.get(f"{VKAPI}utils.resolveScreenName?screen_name={name}{VKTOKEN}")
    #     id = response.json()["response"]["object_id"]
    #     logger.debug(f"SendMessagePost: Send to group {id}")


    photo = Upload.photo_messages("..\static\images\\tmp.jpg")[0]
    attachments = f"photo{photo['owner_id']}_{photo['id']}_{photo['access_key']}"
    logger.debug(f"SendMessagePost: Send photo {attachments}")
    data={
        'user_id': f"-{id}",
        'access_token': TOKEN,
        'message': message,
        'attachment': attachments,
        'v': 5.81}

    # r = vk.
    r = requests.post(f'{VKAPI}messages.send', data).json()
    logger.debug(f"SendMessagePost: End with {r}")

def get_day_lost(dateX):
    if type(dateX) == type("str"):
        try:
            date = date_transl(dateX) #перевод в формат дататайма
        except Exception as e:
            logger.error(f"get day lost with {e}")
            return 505505
    else:
        date = dateX

    if date:
        day = date_get_days(date)
        return day #колличесво дней до истечения периода

def getPic(url, style):
    logger.debug(f"Draw: Start")

    vk = VkParser()
    vk.startUrl(url, 100, 0, [-1], True)
    logger.debug(f"Draw: Get vk users {len(vk.allPerson)}")

    if style == 0:
        style = "bg1"
    elif style == 1:
        style = "bg2"
    elif style == 2:
        style = "bg3"
    else:
        style = "bg3"
    logger.debug(f"Draw: Get {style} style")

    Draw().start(vk.allPerson, style, False)
    logger.debug(f"Draw: End")

def main():
    logger.debug("Run main block")
    for row in ws.rows:
        if row[0].value and row[0].value != "Группа":
            logger.debug(f"Group {row[0].value}")
            days = int(get_day_lost(row[1].value))
            logger.debug(f"{days} before end")

            if days == 0:
                sendMessage(urlSend=row[2].value,urlGroup=row[0].value,coast=row[3].value, type=0)
                logger.debug(f"1 day before end")
            if days == -1:
                sendMessage(urlSend=row[2].value,urlGroup=row[0].value,coast=row[3].value, type=1)
                logger.debug(f"last day send JamPi")
            if  days >= -1:
                logger.debug(f"Generate POST")
                if row[7].value != None:
                    style = str(row[7].value)
                    style = style.replace('.', ',')
                    style = style.split(",")
                    logger.debug(f"Get Style type:exel {style}")
                else:
                    style = [0,1,2]
                    logger.debug(f"Get Style type:code {style}")

                logger.debug(f"Url chat: {row[2].value}")
                logger.debug(f"Coast money:{row[3].value}")
                logger.debug(f"Send post type: {row[4].value}")
                logger.debug(f"Send range type: {row[5].value}")
                logger.debug(f"Send message: {row[6].value}")
                if len(style) == 1:
                    style = int(style[0])
                else:
                    import random
                    style = int(style[int(random.randint(0,len(style)-1))])

                getPic(row[0].value, style)
                if row[5].value == "Ручной":
                    sendMessagePost(row[6].value, row[0].value)
                else:
                    sendPost(row[6].value, row[0].value)


# main()
# sendMessagePost("Test", "https://vk.com/gim206760198?sel=236657896")
# sendPost("txt", "https://vk.com/z.bokan")
# sendPost("txtыфв", "https://vk.com/testsustem")
# sendPost("txtыфв", "https://vk.com/public208239466")
# sendPost("txt", "https://vk.com/club207474830")
# sendMessagePost("Test", "https://vk.com/testsustem")
# getPic("https://vk.com/testsustem")
# TODO: add 7days generator
#       fix send message last subscrabe


# sendPost("TestPublic", "https://vk.com/public208480749")
# sendPost("TestGroup", "https://vk.com/club208480690")
# sendPost("TestBrend", "https://vk.com/public208480652")
# sendPost("TestTheme", "https://vk.com/public208480584")
# sendPost("TestBisnes", "https://vk.com/public208480523")

# sendMessagePost("TestPublic", "https://vk.com/public208480749")
# sendMessagePost("TestGroup", "https://vk.com/club208480690")
# sendMessagePost("TestBrend", "https://vk.com/public208480652")
# sendMessagePost("TestTheme", "https://vk.com/public208480584")
# sendMessagePost("TestBisnes", "https://vk.com/public208480523")

"https://vk.com/public208480749" #TestPublic
"https://vk.com/club208480690" #TestGroup
"https://vk.com/public208480652" #TestBrend
"https://vk.com/public208480584" #TestTheme
"https://vk.com/public208480523" #TestBisnes
