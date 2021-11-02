import os
import sys

sys.path.append('/home/c/cv67525/myenv/lib/python3.6/site-packages/')
sys.path.append('/home/c/cv67525/public_html')
sys.path.append('/home/c/cv67525/public_html/static/images')

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

from VKParsers import VkParser
from Drawing import Draw
from objects import Person


UPLOAD_FOLDER = '/home/c/cv67525/public_html/static/images'
ALLOWED_EXTENSIONS = set(['png'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'penis'
application = app
version = "0.0.8"

dr = Draw()


class trash():
    vk = None
    def __init__(self):
        pass
        
    def sets(self, vk):
        self.vk = vk
        
    def gets(self):
        return self.vk

vk = trash()
vk.sets([Person(123, "name", "lastname", "https://static.wikia.nocookie.net/d567335d-748d-4aa9-b719-a002d842f2d4", "12.12"),]) 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #print(request.files)
        print(request.form)
        background = request.files.get('background')
        if background:
            bgName = background.filename.split('.')
            bgName[0] = "bgTMP"
            if bgName[-1] != "png":
                flash('Только в .png формате', category='error')
                return redirect("")

            bgName = ".".join(bgName)
            background.save(f"{app.config['UPLOAD_FOLDER']}/{bgName}")
            flash('Фон Загружен', category='success')
            return redirect("")

        vkId = request.form.get('vkId') #1 '123'
        if not vkId:
            flash('Выберете Файл', category='error')
            return redirect("")

        bgDef = request.form.get('BGDef') #1 'bg1'
        dayPromej = request.form.get('dayPromej') #1 ''
        try:
            dayPromej = int(dayPromej)
        except:
            dayPromej = 0
        malePos = int(request.form.get('MalePos')) #1 'all'
        idCountry = request.form.get('IDCountry') #1 ''
        if idCountry == "":
            idCountry = [-1]
        else:
            idCountry = idCountry.split(',')
            
        VKToken = request.form.get('VKToken')
        if VKToken == "":
            VKToken = None
        else:
            pass
            
        noAva = request.form.get('NoAva') #0 {'on'}
        myBG = request.form.get('bgTMP') #0 {'TMP'}
        
        if myBG:
            myBG = True
        else:
            myBG = False

        if noAva:
            noAva = False
        else:
            noAva = True

        #try:
        global vk

        vk.sets(VkParser())
        try:
            vk.vk.startUrl(vkId, dayPromej, malePos, idCountry, noAva, VKToken)
        except Exception as e:
            print(e)
            flash('VK API ERROR', category='error')
            return redirect("")
        #except:
        #    flash('Проверте группу', category='error')
        #    return redirect("")

        #try:
        if len(vk.vk.allPerson) != 0:
            dr.start(vk.vk.allPerson, bgDef, myBG)
        else:
            flash('Нет именинников', category='error')
            return redirect("")
        #except Exception as e:
        #    flash('Ошибка при создании изображения', category='error')
        #    return redirect("")
        session["vks"] = [i.gets() for i in vk.vk.allPerson]

        return redirect("/final")
    return render_template("index.html", version=version)

@app.route('/final')
def final():
    return render_template("app.html", persons = session.get('vks'), timers=datetime.now(), version=version)


@app.route('/online', methods=['GET', 'POST'])
def online():
    users = " "
    if request.method == 'POST':
        print(request.form)
        users = request.form.get("ids")
        users = users.split()
        users = ",".join(users)
        try:
            users = VkParser().getOnlineList(ids = users)
        except Exception as e:
            users = ["error", e]

    return render_template("Online-Check.html", users=users, version=version)


if __name__ == '__main__':
    app.run()