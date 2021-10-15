import requests

from PIL import Image

from  utils import open_json


class Draw:


    def __init__(self):
        pass

    def start(self, persons, bgId=1, frameId=1):
        self.persons = persons
        lens = len(persons)
        self.sellectBg(bgId)
        self.sellectFrame(lens, frameId)
        self.drawInLen(lens)
        self.saveEnd()

    def sellectBg(self, index=1):
        self.im1 = Image.open('static/images/bg.png').convert('RGBA')

    def sellectFrame(self, len, index=1):
        self.im2 = Image.open(f'images/{len}_{index}.png').convert('RGBA')

    def saveEnd(self):
        self.im1 = self.im1.convert('RGB')
        self.im1.save('static/images/tmp.jpg', quality=95)
        self.im1.close()
        self.im2.close()

    def dowOnUrl(self, ind):
        url = self.persons[ind].photo
        try:
            resp = requests.get(url, stream=True).raw
        except requests.exceptions.RequestException as e:
            sys.exit(1)
        try:
            im3 = Image.open(resp)
        except IOError:
            print("Unable to open image")
            sys.exit(1)
        return im3

    def openPhoto(self, url=1):
        im3 = Image.open()
        return im3

    def drawInLen(self, len):
        js = open_json(len)
        for i in range(len):
            im3 = self.dowOnUrl(i)
            im3 = im3.resize((js[0][3]-2, js[0][3]-2))
            self.im1.paste(im3,(js[i][0] - js[i][3],js[i][1]))
            im3.close()
        self.im1.paste(self.im2, mask=self.im2)


# Draw().start(5)
