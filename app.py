import os
import sqlite3
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from FDataBase import FDataBase
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g

"""миграции в консоли"""
"""from app import create_db"""
"""create_db()"""

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

# dbase = None
# @app.before_request
# def before_request():
#     """Установление соединения с БД перед выполнением запроса"""
#     global dbase
#     db = get_db()
#     dbase = FDataBase(db)

"""Обработка ошибки 404"""
@app.errorhandler(404)
def pageNotFound(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template('page404.html',  menu=dbase.getMenu(), title='Нет такой страницы')

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if 'userLogged' in session:
        return redirect(url_for('addPost', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Anton' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('addPost', username=session['userLogged']))
    return render_template('login.html', menu=dbase.getMenu(), title='Авторизация')

@app.route("/index")
@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(),  posts=dbase.getPostsAnonce(), title='Главная')

@app.route('/about')
def about():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('about.html',menu=dbase.getMenu(),  title='О нас')

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка')

    return render_template('contact.html', menu=dbase.getMenu(), title='Контакты')


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html',  menu=dbase.getMenu(), title=title, post=post)


# @app.route('/add_post', methods=['GET', 'POST'])
# def add_post():
#     if request.method == 'POST':
#         title = request.form['title']
#         post = request.form['post']
#         url = request.form['url']
#         image_id = request.form['image_id']
#         conn = sqlite3.connect('araneus.db')
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO posts (title, post, url, image_id) VALUES (?, ?, ?, ?)',
#                        (title, post, url, image_id))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('add_post'))
#     else:
#         conn = sqlite3.connect('araneus.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM images')
#         images = cursor.fetchall()
#         conn.close()
#         return render_template('add_post.html', images=images)

# @app.route('/post/<int:id>')
# def post(id):
#     conn = sqlite3.connect('araneus.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT posts.*, images.name, images.data FROM posts LEFT JOIN images ON posts.image_id=images.id WHERE posts.id=?', (id,))
#     post = cursor.fetchone()
#     conn.close()
#     return render_template('post.html', post=post)


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'], request.form['image_id'])
            if not res:
                flash('Ошибка добавления статьи', category = 'error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html',  menu=dbase.getMenu(), title="Добавление статьи")

@app.route('/add_image', methods=['GET', 'POST'])
def add_image():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        image = request.files['image']
        name = image.filename
        data = image.read()
        conn = sqlite3.connect('araneus.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO images (name, data) VALUES (?, ?)', (name, data))
        conn.commit()
        conn.close()
        return redirect(url_for('add_image'))
    else:
        return render_template('add_image.html')

if __name__ == '__main__':
    app.run(debug=True)
