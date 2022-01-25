from loguru import logger


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


class Group:

    def __init__(self, urlGroup, endDay, urlChat, money, typeSend, rangeSend, messageSend, stylePic):
        self.urlGroup = urlGroup
        self.endDay = endDay
        self.urlChat = urlChat
        self.money = money
        self.typeSend = typeSend
        self.rangeSend = rangeSend
        self.messageSend = messageSend
        self.stylePic = stylePic

    def getDict(self):
        grDict = {
            "urlGroup":self.urlGroup,
            "endDay":self.endDay,
            "urlChat":self.urlChat,
            "money":self.money,
            "typeSend":self.typeSend,
            "rangeSend":self.rangeSend,
            "messageSend":self.messageSend,
            "stylePic":self.stylePic,
            }
        return grDict

    def print(self):
        logger.debug(f"group \t{self.urlGroup}")
        logger.debug(f"end \t{self.endDay}")
        logger.debug(f"chat \t{self.urlChat}")
        logger.debug(f"money \t{self.money}")
        logger.debug(f"type \t{self.typeSend}")
        logger.debug(f"range \t{self.rangeSend}")
        logger.debug(f"message \t{self.messageSend}")
        logger.debug(f"style \t{self.stylePic}")
        logger.debug(f"<==+==>")
