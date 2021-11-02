import os
import sys
    ####PATH####
sys.path.append('/home/c/cv67525/myenv/lib/python3.6/site-packages/')
sys.path.append('/home/c/cv67525/public_html')
sys.path.append('/home/c/cv67525/public_html/static/images')
    ####PATH####
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pprint import pprint

from VKParsers import VkParser
from Drawing import Draw, OpenError
from objects import Person
from config import dir



# dir = "D:/git/TopUsersVkWeb"
# dir = "/home/c/cv67525/public_html"
UPLOAD_FOLDER = f'{dir}/static/images/backgrounds'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'awf35q6nery57a5a43'
application = app
version = "0.0.9"

dr = Draw()

@app.route('/loadFile', methods=['GET', 'POST'])
def loadFile():
    if request.method == 'POST':
        print(request.files)
        background = request.files.get('background')
        if background:
            if "png" in background.filename:
                background.save(f"{app.config['UPLOAD_FOLDER']}/bgTMP.png")
                flash('Фон Загружен', category='success')
            else:
                flash('Только в .png формате', category='error')
                return redirect("/")
        else:
            flash('Выберете фон', category='error')
            return redirect("/")
    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)

        vkId = request.form.get('vkId') #1 '123'
        bgDef = request.form.get('BGDef') #1 'bg1'
        stDef = request.form.get('STDef') #1 'st1'
        dayPromej = request.form.get('dayPromej') #1 ''
        malePos = int(request.form.get('MalePos')) #1-'all', 2-'women', 3-'men'
        idCountry = request.form.get('IDCountry') #1 ''
        noAva = request.form.get('NoAva') #0 {'on'}
        myBG = request.form.get('bgTMP') #0 {'TMP'}
        VKToken = request.form.get('VKToken') #1 ''

        ####CHECK####
        try:
            dayPromej = int(dayPromej)
        except:
            dayPromej = 0
        ####
        if idCountry == "":
            idCountry = [-1]
        else:
            idCountry = idCountry.split(',')
        ####
        if VKToken == "":
            VKToken = None
        else:
            pass
        ####
        if myBG:
            myBG = True
        else:
            myBG = False
        ####
        if noAva:
            noAva = False
        else:
            noAva = True
        ####CHECK####

        vk = VkParser()
        try:
            vk.startUrl(vkId, dayPromej, malePos, idCountry, noAva, VKToken)
        except Exception as e:
            flash(f"{e}", category='error')
            return redirect("")

        if len(vk.allPerson) != 0:
            def run():
                try:
                    dr.start(vk.allPerson, bgDef, stDef, myBG)
                except OpenError as exc:
                    vk.allPerson.pop(int(exc.args[0]))
                    run()
                except Exception as exc:
                    flash(f"{exc}", category='error')
                    return lambda x: redirect(x)
                return None
            bug = run()
            if bug: return bug("")
        else:
            flash('Нет именинников', category='error')
            return redirect("")

        session["vks"] = [i.gets() for i in vk.allPerson]

        return redirect("/final")
    return render_template("index.html", version=version, title="Главная")

@app.route('/final')
def final():
    return render_template("app.html", persons = session.get('vks'), timers=datetime.now(), version=version, title="Итог")

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

    return render_template("Online-Check.html", users=users, version=version, title="Онлайн")

@app.errorhandler(404)
def bar(error):
        return render_template('error.html', version=version, title="Ошибка"), 404

if __name__ == '__main__':
    app.run(debug=True)
