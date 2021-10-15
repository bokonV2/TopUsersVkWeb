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
