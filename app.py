import os
import sqlite3
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from FDataBase import FDataBase
from django.contrib.auth.decorators import login_required
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g

#Конфигурация
DATABASE = '/tmp/araneus.db'
SECRET_KEY = 'dfsg5sdfg545sdfg54sdfg5454fsd'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'araneus.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

    #Вспомогательная функция для создания таблиц БД
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    """Соединение с БД если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
       g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

"""Обработка ошибки 404"""
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Нет такой страницы')

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template('inlogin.html', title='Добро пожаловать')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Anton' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация')

@app.route("/index")
@app.route("/")
def index():
    db = get_db()
    return render_template('index.html', title='Главная')

@app.route('/single')
def single():
    return render_template('single.html', title='О нас')

@app.route('/contact', methods=['POST', 'GET'])
def contact():

    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка')

    return render_template('contact.html', title='Контакты')


@app.route("/post/<alias>")
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', title=title, post=post)

@app.route('/archive')
def archive():
    return render_template('archive.html', title='Блог')

@app.route('/vologda')
def vologda():
    return render_template('vologda.html', title='Проект в Вологде')

@app.route('/kazan')
def kazan():
    return render_template('kazan.html')

@app.route('/ufa')
def ufa():
    return render_template('ufa.html')

@app.route('/razan')
def razan():
    return render_template('razan.html')

@app.route('/yola')
def yola():
    return render_template('yola.html')

@app.route("/add_post", methods=["POST", "GET"])
@login_required
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category = 'error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', title="Добавление статьи")

@app.route('/logout')
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
