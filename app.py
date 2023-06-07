from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfsg5sdfg545sdfg54sdfg5454fsd'

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Нет такой страницы')

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f'Профиль пользователья: {username}'



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

if __name__ == '__main__':
    app.run(debug=True)
