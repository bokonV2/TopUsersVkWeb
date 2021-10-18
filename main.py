import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from VKParsers import VkParser
from Drawing import Draw
from objects import Person


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png'])


class Server():
    dr = Draw()
    vk = [Person(123, "name", "lastname", "https://static.wikia.nocookie.net/d567335d-748d-4aa9-b719-a002d842f2d4", "12.12"),]

    def __init__(self):
        self.flaskServer()

    def flaskServer(self):
        app = Flask(__name__)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['SECRET_KEY'] = 'penis'

        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                print(request.files)
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
                    dayPromej = 1
                malePos = int(request.form.get('MalePos')) #1 'all'
                idCountry = request.form.get('IDCountry') #1 ''
                if idCountry == "":
                    idCountry = [-1]
                else:
                    idCountry = idCountry.split(',')
                noAva = request.form.get('NoAva') #0 {'on'}

                if noAva:
                    noAva = False
                else:
                    noAva = True

                try:
                    self.vk = VkParser()
                    self.vk.startUrl(vkId, dayPromej, malePos, idCountry, noAva)
                except:
                    flash('Проверте группу', category='error')
                    return redirect("")

                try:
                    self.dr.start(self.vk.allPerson, bgDef)
                except Exception as e:
                    print(e)
                    flash('Ошибка при создании изображения', category='error')
                    return redirect("")
                # background
                # vkId
                # BGDef
                # dayPromej
                # MalePos
                # IDCountry
                # NoAva
                return redirect("/final")
            return render_template("index.html")

        @app.route('/final')
        def final():
            try:
                return render_template("app.html", persons = self.vk.allPerson)
            except:
                return render_template("app.html", persons = self.vk)

        app.debug = True
        app.run()


if __name__ == '__main__':
    Server()

    # TO DO
"""
    добавить логику работы для разных видов стилей
    логика для выброса челов без аватарки
    ну кста это не легко
    хотя и норм
"""
