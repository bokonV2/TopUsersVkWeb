import requests
import traceback

from PIL import Image, ImageDraw

from utils import open_json
from objects import Person
from config import dir


class CustomError(Exception):
    pass

class OpenError(Exception):
    pass


class Draw:
    def __init__(self):
        pass

    def start(self, persons, bgDef, stDef, myBG):
        self.persons = persons

        if myBG:
        	self.index = "bgTMP"
        else:
            self.index = bgDef

        lens = len(persons)
        self.sellectBg()

        if stDef == "st1":
            self.sellectFrame(lens)
            self.drawInLenBg1(lens)
        elif stDef == "st2":
            self.drawInLenBg2(lens)
        elif stDef == "st3":
            self.drawInLenBg3(lens)

        self.saveEnd()

    def sellectBg(self):
        self.im1 = Image.open(f'{dir}/static/images/backgrounds/{self.index}.png').convert('RGBA').resize((1064,946))

    def sellectFrame(self, len):
        self.im2 = Image.open(f'{dir}/static/images/frame/{len}_1.png').convert('RGBA')
        self.im2_1 = Image.open(f'{dir}/static/images/frame/{len}_2.png').convert('RGBA')

    def saveEnd(self):
        self.im1 = self.im1.convert('RGB')
        self.im1.save(f'{dir}/static/images/tmp.jpg', quality=95)

    def dowOnUrl(self, ind):
        url = self.persons[ind].photo
        try:
            resp = requests.get(url, stream=True).raw
        except Exception as e:
            traceback.print_exc()
            raise CustomError(f"Unable to load image {url} <{e}")

        try:
            im3 = Image.open(resp).convert("RGBA").resize((200,200))
        except IOError:
            traceback.print_exc()
            raise OpenError(ind)
        return im3

    def drawInLenBg1(self, len):
        js = open_json(len)
        for i in range(len):
            im3 = self.dowOnUrl(i)
            im3 = im3.resize((js[0][3]-2, js[0][3]-2))
            self.im1.paste(im3,(js[i][0] - js[i][3],js[i][1]))
            im3.close()
        self.im1.paste(self.im2, mask=self.im2)
        if self.im2_1:
            self.im1.paste(self.im2_1, mask=self.im2_1)

    def drawInLenBg2(self, len):
        js = open_json(len, "2")
        colors = [(255, 29, 95, 255),(249, 122, 0, 255),(22, 171, 123, 255)]
        color = 0
        rad = 125
        size = 500
        mask = Image.new("L", (size,size), 0)
        maskD = ImageDraw.Draw(mask)
        maskD.rounded_rectangle((0, 0, size, size), fill=255, radius=rad)
        for i in range(len):
            im2 = self.dowOnUrl(i)
            im2 = im2.resize((size,size))
            avatar = Image.new("RGBA", (size,size), (0,0,0,0))
            avatarD = ImageDraw.Draw(avatar)
            avatar.paste(im2, (0, 0), mask)
            avatarD.rounded_rectangle((0, 0, size, size), outline=colors[color], radius=rad, width=25)
            color += 1
            if color == 3:
                color = 0
            #print(js[i][1][0])
            avatar.thumbnail((js[i][1][0],js[i][1][0]), resample=3)
            avatars = avatar
            self.im1.paste(avatars,(js[i][0][0],js[i][0][1]), avatars)

    def drawInLenBg3(self, len):
        js = open_json(len, "2")
        rot = [-5,4.75,3.4,9]
        ang = 0

        for i in range(len):
            im2 = self.dowOnUrl(i)
            # print(js[i][1][0])
            im2D = ImageDraw.Draw(im2)
            im2D.rectangle((0,0,im2.width,im2.height), outline="white", width=6)
            im2 = im2.resize((js[i][1][0],js[i][1][0]), resample=3)
            im2 = im2.rotate(rot[ang], resample=3, expand=True)
            self.im1.paste(im2,(js[i][0][0],js[i][0][1]), im2)
            ang += 1
            if ang == 4:
                ang = 0


if __name__ == '__main__':
    i = Person(1, "1", "1", "https://sun9-71.userapi.com/c855728/v855728961/4c82a/syoyTxKpVXc.jpg?ava=1", "1")
    all = [i for g in range(5)]
    all.append(Person(1,"1","1","https://sun9-32.userapi.com/c841/u46431521/d_d4d43e3a.jpg", "1"))
    all.append(Person(1,"1","1","https://sun9-8.userapi.com/c1240/u879176/d_ba0ebb57.jpg", "1"))
    a = Draw()
    def run():
        global all
        try:
            a.start(all, "bg3", 0)
        except Exception as exc:
            print(exc)
            all.pop(int(int(exc.args[0])))
            run()
    run()
