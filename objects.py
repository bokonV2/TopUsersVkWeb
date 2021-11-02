from utils import date_transl, date_get_days

class Person:
    id = int()
    name = str()
    lastname = str()
    photo = str()
    bdate = str()

    def __init__(self, id, name, lastname, photo, bdate):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.photo = photo
        self.bdate = bdate

    def gets(self):
    	return f"*id{self.id} ({self.name} {self.lastname})"


class Groups:
    url_group = str()
    date = "datetime"
    url_chat = str()
    money = int()
    type_send = str()
    range_send = str()
    message = str()
    design = list()

    days = int()

    def __init__(self,
        url_group="", date=None,
        url_chat="", money=0,
        type_send="", range_send="",
        message="", design=[]):

        if type(date) == type("str"):
            date = date_transl(date)

        self.url_group = url_group
        self.date = date
        self.url_chat = url_chat
        self.money = money
        self.type_send = type_send
        self.range_send = range_send
        self.message = message
        self.design = design

        self.days = date_get_days(date)
