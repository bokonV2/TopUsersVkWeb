import os

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from VKParsers import VkParser
from Drawing import Draw
from objects import Person


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png'])


class Server():
    dr = Draw()
    vk = None
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
                        flash('Сообщение отправлено', category='error')
                        return redirect("")

                    bgName = ".".join(bgName)
                    background.save(f"{app.config['UPLOAD_FOLDER']}/{bgName}")
                    return redirect("")

                vkId = request.form.get('vkId') #1 '123'
                if not vkId:
                    flash('Сообщение отправлено', category='error')
                    return redirect("")

                bgDef = request.form.get('BGDef') #1 'bg1'
                dayPromej = request.form.get('dayPromej') #1 ''
                malePos = request.form.get('MalePos') #1 'all'
                idCountry = request.form.get('IDCountry') #1 ''
                noAva = request.form.get('NoAva') #0 {'on'}

                self.vk = VkParser(vkId)
                self.vk.start()
                self.dr.start(self.vk.allPerson)
                #
                # background
                # vkId
                # BGDef
                # dayPromej
                # MalePos
                # IDCountry
                # NoAva
                #
                # print("background"*20)
                return redirect("/final")
            return render_template("index.html")
            # return redirect(f"/final")


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
