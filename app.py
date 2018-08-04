from flask import (Flask, render_template, request,
                   redirect, url_for, session)
from peewee import *
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'çok_gizli_ve_karmaşık_metin'
database = SqliteDatabase('database.sql')


class Editor(Model):
    class Meta:
        database = database

    username = TextField()
    password = TextField()


class Post(Model):
    class Meta:
        database = database

    title = TextField()
    content = TextField()


@app.route('/')
def index():
    posts = Post.select()
    return render_template('index.html', posts=posts)


@app.route('/girisyap', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        database_record = Editor.select().where(Editor.username == username)[0]
        encrypted_password = database_record.password

        if check_password_hash(encrypted_password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cikis')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/yaziekle', methods=['GET', 'POST'])
def newpost():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        Post.create(title=title, content=content)
        return redirect(url_for('index'))

    return render_template('newpost.html')


if __name__ == "__main__":
    app.run(debug=True)
