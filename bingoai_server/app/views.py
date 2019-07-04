from app.forms import LoginForm
from app.forms import PictureForm
from flask import url_for, redirect, render_template, jsonify, request, flash, Response
from flask import Flask
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import time
import logging
# import cv2
import uuid
import codecs
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['UP'] = os.path.join(os.path.dirname(__file__), "static/uploads")
app.config['CACHE'] = os.path.join(os.path.dirname(__file__), "static/cache")


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
        logo = change_filename(filename, time_now, file_uuid)
        print(logo)
        form.picture.data.save(app.config['UP'] + '/' + logo)
        flash(u"文件传输成功", "ok")
    return render_template('picture.html', form=form)
