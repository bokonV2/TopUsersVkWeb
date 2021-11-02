import requests

from utils import now, dates_srav, diePpl, checkOnline
from objects import Person
from pprint import pprint

VKAPI = "https://api.vk.com/method/"
TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
#TOKEN = "14a571e87a41be67b7fd3464027cc8af8ecce427bb6dc797f211f8e46089621855a804b17ba7e3614bd76"
V = "5.21"
VKTOKEN = f"&access_token={TOKEN}&v={V}"


class VkParser:
    limit = 1000
    allPerson = []
    group = None

    def __init__(self):
        pass

    def startUrl(self, name, days, sex, city, photo, VKToken):
        if VKToken != None:
            TOKEN = VKToken
            V = "5.21"
            self.VKTOKEN = f"&access_token={TOKEN}&v={V}"
        else: 
            TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
            V = "5.21"
            self.VKTOKEN = f"&access_token={TOKEN}&v={V}"
        
        self.city = city
        self.sex = sex
        self.days = days
        self.photo = photo
        # print(name, days, sex, city, photo)

        try:
            self.group = int(name)
        except:
            name = name.split('/')[-1]
            response = requests.get(f"{VKAPI}utils.resolveScreenName?screen_name={name}{self.VKTOKEN}")
            self.group = response.json()["response"]["object_id"]
        self.start()
        
    def getOnlineList(self, ids):
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

    def start(self):
        itera = int(requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset=0&count={self.limit}&fields=bdate,photo_200{self.VKTOKEN}").json()["response"]["count"]/1000)
        for i in range(itera+2):
            self.addInAll(
                self.getPersonsJson(self.getRespons(i*self.limit)))
            if len(self.allPerson) >= 50:
                break

        if len(self.allPerson) > 50:
            self.allPerson = self.allPerson[:50]
        # print(len(self.allPerson))

    def getRespons(self, offset):
        # print("GET Respons")
        response = requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset={offset}&count={self.limit}&fields=bdate,photo_200,sex,city,last_seen{self.VKTOKEN}")
        return response

    def getPersonsJson(self, response):
        # print("GET PersonsJSON")
        all = response.json()
        persons = all["response"]["items"]
        return persons

    def addInAll1(self, persons):
        # print("\tADD Person")
        for person in persons:
            try:

                id = person["id"]
                # print(f"new{id}")
                name = person["first_name"]
                # print(name)
                lastname = person["last_name"]
                # print(lastname)
                photo = person["photo_200"]
                # print(photo)
                bdate = person["bdate"]
                # print(bdate)
                sex = int(person["sex"])
                # print(sex)
                last = person["last_seen"]["time"]
                # print(last)
                try:
                    city = person["city"]["id"]
                    # print(city)
                except:
                    city = "0"
                # print(diePpl)
                # print(diePpl(now, last))
                # print("NEWCHEL")
                # print(f'{photo != "https://vk.com/images/camera_200.png"}  {self.photo}')
                if diePpl(now, last):
                    # print(f"{id} 1")
                    if photo != "https://vk.com/images/camera_200.png" or self.photo:
                        # print(f"{id} 2")
                        # print(city , self.city)
                        if str(city) in self.city or self.city[0] == -1:
                            # print(f"{id} 3")
                            if sex == self.sex or self.sex == 0:
                                # print(f"{id} 4")
                                if dates_srav(now, bdate, self.days):
                                    # print(f"{id} 5")
                                    # print(f"ADD {id} in list")
                                    self.allPerson.append(Person(id, name, lastname, photo, bdate))

            except Exception as e:
                # print(e)
                pass
                
    def addInAll(self, persons):
        # print("\tADD Person")
        for person in persons:
            stop = True

            
            id = person["id"]
            # print(f"new{id}")
            # pprint(person)
            name = person["first_name"]
            # print(name)
            lastname = person["last_name"]
            # print(lastname)
            photo = person["photo_200"]
            # print(photo)
            try:
                bdate = person["bdate"]
                # print(bdate)
            except:
                bdate = "01.01"
            sex = int(person["sex"])
            # print(sex)
            try:
                last = person["last_seen"]["time"]
                # print(last)
            except:
                last = 1634711753
            try:
                city = person["city"]["id"]
                # print(city)
            except:
                city = "0"
            # print(diePpl)
            # print(diePpl(now, last))
            # print("NEWCHEL")
            # print(f'{photo != "https://vk.com/images/camera_200.png"}  {self.photo}')
            if diePpl(now, last):
                # print(f"{id} 1")
                if photo != "https://vk.com/images/camera_200.png" or self.photo:
                    try:
                        
                        if photo == "https://sun9-32.userapi.com/c841/u46431521/d_d4d43e3a.jpg":
                            stop = False
                    except:
                        pass
                    else:
                        # print(f"{id} 2")
                        # print(city , self.city)
                        if str(city) in self.city or self.city[0] == -1:
                            # print(f"{id} 3")
                            if sex == self.sex or self.sex == 0:
                                # print(f"{id} 4")
                                if dates_srav(now, bdate, self.days) and stop:
                                    # print(f"{id} 5")
                                    # print(f"ADD {id} in list")
                                    self.allPerson.append(Person(id, name, lastname, photo, bdate))




if __name__ == '__main__':
    pass
    # a = VkParser()
    # a.startUrl("https://vk.com/kidshospiceru", 100, 0, [-1], 0)
    # for i in a.allPerson:
    	# print(i)

