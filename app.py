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
#Общая функция для соединения с БД
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
        return redirect(url_for('admin', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Anton' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('login', username=session['userLogged']))
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


@app.route('/admin')
def admin():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('admin.html',menu=dbase.getMenu(),  title='панель администратора', posts=dbase.getPostsAnonce())

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


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)

    return render_template('post.html',  menu=dbase.getMenu(), title=title, post=post)

@app.route("/add_post", methods=["POST", "GET"])
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
                return redirect(url_for('admin'))
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html',  menu=dbase.getMenu(), title="Добавление статьи")

@app.route('/post/<int:id_post>/edit/', methods=('GET', 'POST'))
def edit(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if request.method == 'POST':
        res = dbase.edit_Post(request.form['name'], request.form['post'], request.form['url'])
        if not res:
            flash('Ошибка редактирования статьи', category='error')
        else:
            flash('Статья отредактирована', category='success')
    else:
        flash('Ошибка редатирования', category='error')
    return render_template('edit.html', menu=dbase.getMenu(), title="Редактирование статьи")

    # @app.route('/<int:id_post>/edit', methods=('GET', 'POST'))
# def edit(id_post):
#     db = get_db()
#     dbase = FDataBase(db)
#     post = dbase.getPost(id_post)
#
#     if request.method == 'POST':
#         title = request.form['title']
#         text = request.form['text']
#
#         if not title:
#             flash('Title is required!')
#         else:
#             db = get_db()
#             db.execute('UPDATE posts SET title = ?, text = ?'
#                          ' WHERE id = ?',
#                          (title, text, id))
#             db.commit()
#             db.close()
#             return redirect(url_for('index'))

    return render_template('edit.html', post=post)



@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()

if __name__ == '__main__':
    app.run(debug=True)
