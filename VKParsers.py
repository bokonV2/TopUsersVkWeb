import requests
import traceback

from utils import now, dates_srav, diePpl, checkOnline
from objects import Person

VKAPI = "https://api.vk.com/method/"
TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
#TOKEN = "14a571e87a41be67b7fd3464027cc8af8ecce427bb6dc797f211f8e46089621855a804b17ba7e3614bd76"
V = 5.21
VKTOKEN = f"&access_token={TOKEN}&v={V}"

class CustomError(Exception):
    pass

class VkParser:
    limit = 1000

    def __init__(self):
        # print("init")
        self.allPerson = []
        self.group = None

    def startUrl(self, name, days, sex, city, noAva, VKToken=""):
        # print("startUrl")
        if VKToken:
            self.VKTOKEN = f"&access_token={VKToken}&v={V}"
        else:
            self.VKTOKEN = f"&access_token={TOKEN}&v={V}"

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
        # print("run")
        try:
            itera = int(requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset=0&count={self.limit}&fields=bdate,photo_200{self.VKTOKEN}").json()["response"]["count"]/self.limit)
        except Exception as e:
            traceback.print_exc()
            raise CustomError(f"VKAPI: Token or something, exept {e}")

        for i in range(itera+2):
            self.addInAll(
                self.getPersonsJson(self.getRespons(i*self.limit)))
            if len(self.allPerson) >= 50:
                self.allPerson = self.allPerson[:50]
                break

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

    def getRespons(self, offset):
        # print("getRespons")
        response = requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset={offset}&count={self.limit}&fields=bdate,photo_200,sex,city,last_seen{self.VKTOKEN}")
        return response

    def getPersonsJson(self, response):
        # print("getPersonsJson")
        try:
            persons = response.json()["response"]["items"]
        except Exception as e:
            traceback.print_exc()
            raise CustomError(f"VKAPI: Token or something, exept {e}")
        return persons

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
