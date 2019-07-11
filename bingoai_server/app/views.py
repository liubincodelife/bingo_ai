from app.forms import LoginForm, PictureForm
from flask import Flask, url_for, redirect, render_template, jsonify, request, flash, Response
from flask import send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import time
import logging
import uuid

from app.modules.classification.classification import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['UP'] = os.path.join(os.path.dirname(__file__), "static/uploads")
app.config['DOWN'] = os.path.join(os.path.dirname(__file__), "static/downloads")
app.config['CACHE'] = os.path.join(os.path.dirname(__file__), "static/cache")
app.config['CLASSIFICATION'] = os.path.join(os.path.dirname(__file__), "static/classification")


@app.route('/')
@app.route('/text')
def text():
    user = {'nickname': 'bingo'}
    return render_template("text.html", title='Home', user=user)


@app.route('/index')
def index():
    user = {'username': 'bingo'}
    posts = [
        {
            'author': {'username': 'bin'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'si'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)


def change_filename(filename, timestamp, file_uuid):
    info = os.path.splitext(filename)
    # print("picture info: ", info)
    new_file_name = timestamp.strftime("%Y%m%d%H%M%S")+"_"+file_uuid+info[-1]
    return new_file_name


@app.route('/picture', methods=['GET', 'POST'])
def picture():
    form = PictureForm()
    print('logging:', request.remote_addr)
    if form.validate_on_submit():
        filename = secure_filename(form.picture.data.filename)
        file_uuid = str(uuid.uuid4().hex)
        time_now = datetime.now()
        print("file name: ", filename)
        new_name = change_filename(filename, time_now, file_uuid)
        print(new_name)
        form.picture.data.save(app.config['UP'] + '/' + new_name)
        img_path = os.path.join(app.config['UP'], new_name)
        emotion, confidence, mark_img_name = classification(img_path)
        if emotion == 1:
            emotionStr = "嘟嘴"
            print("emotion : 嘟嘴")
        elif emotion == 2:
            emotionStr = "微笑"
            print("emotion : 微笑")
        elif emotion == 3:
            emotionStr = "张嘴"
            print("emotion : 张嘴")
        elif emotion == 4:
            emotionStr = "侧脸"
            print("emotion : 侧脸")
        else:
            emotionStr = "无表情"
            print("emotion : 无表情")
        flashStr = "表情为：" + emotionStr
        flash(flashStr, "ok")
        print("confidence: ", str(confidence)[0:5])
        print("mark_img_name: ", mark_img_name)
    return render_template('picture.html', form=form)


ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/classification', methods=['GET', 'POST'])
def get_emotion():
    file_data = request.files['file']
    if file_data and allowed_file(file_data.filename):
        filename = secure_filename(file_data.filename)
        file_uuid = str(uuid.uuid4().hex)
        time_now = datetime.now()
        print("file name: ", filename)
        # filename = time_now.strftime("%Y%m%d%H%M%S") + "_" + file_uuid + "_" + filename
        new_name = change_filename(filename, time_now, file_uuid)
        img_path = os.path.join(app.config['CLASSIFICATION'], new_name)
        file_data.save(img_path)
        print(img_path)
        emotion, confidence, mark_img_name = classification(img_path)
        if confidence is not None:
            confidenceStr = str(confidence)[0:5]
        else:
            confidenceStr = 1
        if emotion == 1:
            data = {
                "code": 0,
                "emotion": "嘟嘴",
                "confidence": confidenceStr,
                "filename": mark_img_name
            }
        elif emotion == 2:
            data = {
                "code": 0,
                "emotion": "微笑",
                "confidence": confidenceStr,
                "filename": mark_img_name
            }
        elif emotion == 3:
            data = {
                "code": 0,
                "emotion": "张嘴",
                "confidence": confidenceStr,
                "filename": mark_img_name
            }
        elif emotion == 4:
            data = {
                "code": 1,
                "emotion": "侧脸",
                "confidence": confidenceStr,
                "filename": mark_img_name
            }
        else:
            data = {
                "code": 0,
                "emotion": "无表情",
                "confidence": confidenceStr,
                "filename": mark_img_name
            }
        print("emotion type = ", emotion, "\n")
        print("return data = ", jsonify(data))

        return jsonify(data)

    return jsonify({"code": 1, "msg": u"文件格式不允许"})


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    print("download filename: ", filename)
    return send_from_directory(app.config['DOWN'], filename, as_attachment=True)
