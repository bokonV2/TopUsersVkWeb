import requests

from pprint import pprint

from utils import now, dates_srav
from objects import Person

VKAPI = "https://api.vk.com/method/"
TOKEN = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
V = "5.21"
VKTOKEN = f"&access_token={TOKEN}&v={V}"


class VkParser:
    limit = 1000
    allPerson = []
    lenPers = 1000
    group = None

    def __init__(self):
        pass

    def startUrl(self, name, days):
        self.days = days
        try:
            self.group = int(name)
        except:
            name = name.split('/')[-1]
            response = requests.get(f"{VKAPI}utils.resolveScreenName?screen_name={name}{VKTOKEN}")
            self.group = response.json()["response"]["object_id"]
        self.start()


    def start(self):
        itera = int(requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset=0&count={self.limit}&fields=bdate,photo_200{VKTOKEN}").json()["response"]["count"]/1000)
        for i in range(itera):
            i+=1
            self.addInAll(
                self.getPersonsJson(self.getRespons(i*self.limit)))
            if len(self.allPerson) >= 50:
                break

        if len(self.allPerson) > 50:
            self.allPerson = self.allPerson[:50]
        print(len(self.allPerson))

    def getRespons(self, offset):
        # print("GET Respons")
        response = requests.get(f"{VKAPI}groups.getMembers?lang=0&group_id={self.group}&offset={offset}&count={self.limit}&fields=bdate,photo_200{VKTOKEN}")

        # pprint(response.json())
        return response

    def getPersonsJson(self, response):
        # print("GET PersonsJSON")
        all = response.json()
        persons = all["response"]["items"]
        self.lenPers = len(persons)
        # print(f"{self.lenPers} LEN Persons")
        return persons

    def addInAll(self, persons):
        # print("\tADD Person")
        for person in persons:
            try:
                id = person["id"]
                # print(f"ADD {id}")
                name = person["first_name"]
                lastname = person["last_name"]
                photo = person["photo_200"]
                bdate = person["bdate"]
                if dates_srav(now, bdate, self.days):
                    print(f"ADD {id} in list")
                    self.allPerson.append(Person(id, name, lastname, photo, bdate))
            except:
                    pass


if __name__ == '__main__':
    VkParser().startUrl("https://vk.com/codeupnumber1")
    # VkParser().startUrl("168300060")
    pass
