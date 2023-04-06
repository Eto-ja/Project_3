import datetime

import jwt
# from jwt import ExpiredSignatureError
from flask import Flask, redirect, render_template, make_response, request
from data import db_session
from data.users import User
from data.genres import Genres
from data.books import Books
from flask_login import LoginManager, login_user
from registerform import RegisterForm
from sign_inform import SignInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def aga():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    genre = Genres(name='Фэнтези')
    db_sess.add(genre)
    db_sess.commit()


def q():
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    book = Books(title='SSS', size=123)
    db_sess.add(book)
    db_sess.commit()


@app.route('/good_registration')
def good():
    return render_template('good_register.html', title='')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET'])
def index():
    # db_sess = db_session.create_session()
    # genres = db_sess.query(Genres).all()
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            age=form.age.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/good_registration')
    return render_template('register.html', title='Регистрация', form=form)


# @app.route('/sign_in', methods=['GET', 'POST'])
# def sign_in():
#     form = SignInForm
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.email == form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('sign_in.html',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('sign_in.html', title='Вход', form=form)
    #     email = form.email.data
    #     password = form.password.data
    #
    #     # TODO: check is exists user
    #     payload = {'mail': email, 'time': str(datetime.datetime.now()), 'exp': 10 * 60}
    #     token = jwt.encode(payload, key='secret')
    #
    #     response = make_response(render_template('sign_in.html'))
    #     response.set_cookie('token', token)
    #
    #     return response

#
#
# @app.route('/like')
# def like_book():
#     token = request.cookies.get('jwt', None)
#     if token is None:
#         return redirect('/')
#
#     try:
#         payload = jwt.decode(token, key='secret')
#     except ExpiredSignatureError:
#         return redirect('/')
#
#     mail = payload['mail']
#     # TODO: add book to favourite


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', title='', form=form)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, debug=True)
    # q()
