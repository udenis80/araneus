from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/archive')
def archive():
    return render_template('archive.html')

@app.route('/vologda')
def vologda():
    return render_template('vologda.html')

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
