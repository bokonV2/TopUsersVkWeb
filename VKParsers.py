import requests

from utils import now, dates_srav
from objects import Person


class VkParser:
    token = "caa98e2ec949004908c7487f243f3aae1f4946e8226b09ed8fb7bfc3f5127f48b848a333a04f032d8517a"
    limit = 1000
    allPerson = []
    lenPers = 1000

    def __init__(self, group = 168300060):
        self.group = group

    def start(self):
        offset = 0
        while len(self.allPerson) < 50 and self.lenPers != 0:
            # print(offset*self.limit)
            self.addInAll(
                self.getPersonsJson(self.getRespons(offset*self.limit)))
            # print(str(len(self.allPerson))+" LEN")
            offset += 1

        if len(self.allPerson) > 50:
            self.allPerson = self.allPerson[:50]
        print(offset*self.limit)
        print(len(self.allPerson))

    def getRespons(self, offset):
        # print("GET Respons")
        response = requests.get(f"https://api.vk.com/method/groups.getMembers?lang=0&group_id={self.group}&offset={offset}&count={self.limit}&fields=bdate,photo_200&access_token={self.token}&v=5.21")
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
                if dates_srav(now, bdate):
                    # print(f"ADD {id} in list")
                    self.allPerson.append(Person(id, name, lastname, photo, bdate))
            except:
                    pass


if __name__ == '__main__':
    VkParser().start()
    pass
