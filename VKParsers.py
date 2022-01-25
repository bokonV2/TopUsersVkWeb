import requests
import traceback

import vk_api
from loguru import logger
from vk_api import VkUpload
from config import dir
from utils import now, dates_srav, diePpl, checkOnline
from objects import Person
from pprint import pprint

VKAPI = "https://api.vk.com/method/"
TOKEN = "2b319b6859e9149c9cf57bc79b8c9a1988ddf2f282f82f9418b2f044688100c68e6c23465038a740b296d"
V = 5.21
VKTOKEN = f"&access_token={TOKEN}&v={V}"

vkSession = vk_api.VkApi(token=TOKEN)
Upload = VkUpload(vkSession)

class CustomError(Exception):
    pass

class VkParser:

    def __init__(self):
        # print("init")
        self.allPerson = []
        self.group = None

    def startUrl(self, name, days, sex, city, noAva, VKToken=""):
        # print("startUrl")
        if VKToken:
            self.VKTOKEN = f"&access_token={VKToken}&v={V}"
            self.VkToken = VKToken
        else:
            self.VKTOKEN = f"&access_token={TOKEN}&v={V}"
            self.VkToken = TOKEN

        self.city = city #[-1]
        self.sex = sex  # 0
        self.days = days # 0
        self.noAva = noAva # False

        if name.isdigit():
            self.group = int(name)
        else:
            response = requests.get(f"{VKAPI}utils.resolveScreenName?screen_name={name.split('/')[-1]}{self.VKTOKEN}")
            try:
                self.group = response.json()["response"]["object_id"]
            except Exception as e:
                traceback.print_exc()
                raise CustomError(f"URL: ({name}) incorrect or Token")

        self.run()

    def run(self):
        data = {
        "code": f"""
                var members = [];
                var offset = 0;
                members.push(API.groups.getMembers({{"group_id": "{self.group}", "v": "5.21"}}).count);
                while (offset < 24000)
                {{
                members.push(API.groups.getMembers({{"group_id": "{self.group}", "v": "5.21", "sort": "id_asc", "count": "1000", "offset": offset, "fields":"bdate,photo_200,sex,city,last_seen"}}).items);
                offset = offset + 1000;
                }};
                return members;""",
        "access_token": self.VkToken,
        "v": V,
        }
        response = requests.post(f"{VKAPI}execute",data=data)
        try:
            response = response.json()['response']
            count = response.pop(0)
            self.addInAll([item for sublist in response for item in sublist])
            if len(self.allPerson) >= 50:
                self.allPerson = self.allPerson[:50]
        except:
            traceback.print_exc()
            raise CustomError(f"VKAPI: Token or something, exept {e}")
            pprint(response.json())

    def sendPost(self, message, url):
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

        photo = Upload.photo_wall("static\images\\tmp.jpg", group_id=id)[0]
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
        return r

    def getOnlineList(self, ids):
        # print("getOnlineList")
        response = requests.get(f"{VKAPI}users.get?user_ids={ids}&fields=last_seen,id{VKTOKEN}")
        response = response.json()["response"]
        users = []
        for pipl in response:
            try:
                if checkOnline(now, pipl["last_seen"]["time"]):
                    users.append(pipl["id"])
            except:
                pass
        return users

    def addInAll(self, persons):
        # print("addInAll")
        for person in persons:
            stop = True

            id = person["id"]
            name = person["first_name"]
            lastname = person["last_name"]
            photo = person["photo_200"]
            sex = int(person["sex"])
            try:
                bdate = person["bdate"]
            except:
                stop = False
            try:
                last = person["last_seen"]["time"]
            except:
                last = 1634711753
            try:
                city = person["city"]["id"]
            except:
                city = "0"

            if stop:
                if diePpl(now, last):
                    if photo != "https://vk.com/images/camera_200.png" or self.noAva:
                        if str(city) in self.city or self.city[0] == -1:
                            if sex == self.sex or self.sex == 0:
                                if dates_srav(now, bdate, self.days):
                                    self.allPerson.append(Person(id, name, lastname, photo, bdate))
                                    print(id, name, lastname, photo, bdate)
