import datetime

# import jwt
# from jwt import ExpiredSignatureError
from flask import Flask, redirect, render_template, make_response, request
from data import db_session
from data.users import User
from data.genres import Genres
from data.authors import Authors
from data.books import Books
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
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


# сообщение при успешной регистрации
@app.route('/good_registration')
def good():
    return render_template('good_register.html', title='')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# главная страница
@app.route('/', methods=['GET'])
def index():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genres).all()
    authors = db_sess.query(Authors).all()
    books = db_sess.query(Books).all()
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        book_liked_ids = [b.id for b in user.liked]
    else:
        book_liked_ids = [0]
    return render_template('index.html', genres=genres, authors=authors, books=books, book_liked_ids=book_liked_ids)


# форма для регистрации
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
#     form = SignInForm()
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


# форма для входа в систему
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


# выход из аккаунта
@app.route('/sign_out', methods=['POST'])
def sign_out():
    logout_user()
    return redirect('/')


# это появится, если у книжки нажать на подробнее
@app.route('/more/<book_id>', methods=['GET'])
def more(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == book_id).first()
    genres = db_sess.query(Genres).all()
    return render_template('more.html', id=book_id, title=book.title, author=book.authors, size=book.size,
                           photo=book.photo_path, genre=book.genres, genres=genres, description=book.description)


# добавить в избранное книгу или удалить из избранного, находясь на главной странице
@app.route('/like/<book_id>', methods=['POST'])
@login_required
def like(book_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    book = db_sess.query(Books).filter(Books.id == book_id).first()

    for i in range(len(user.liked)):
        if user.liked[i].id == book.id:
            user.liked.remove(user.liked[i])
            db_sess.commit()
            return redirect('/')
    user.liked.append(book)

    db_sess.commit()

    return redirect('/')


# добавить в избранное книгу или удалить из избранного, находясь в избранном
@app.route('/likei/<book_id>', methods=['POST'])
@login_required
def likei(book_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    book = db_sess.query(Books).filter(Books.id == book_id).first()

    for i in range(len(user.liked)):
        if user.liked[i].id == book.id:
            user.liked.remove(user.liked[i])
            db_sess.commit()
            return redirect('/like_book')
    user.liked.append(book)

    db_sess.commit()

    return redirect('/like_book')


# избранные книги
@app.route('/like_book', methods=['GET'])
def like_book():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    book = db_sess.query(Books).all()
    genres = db_sess.query(Genres).all()

    return render_template('like.html', id=user, books=book, like=user.liked, genres=genres)


# сортировка по жанру
@app.route('/genre/<genre_id>', methods=['GET'])
def sort_genre(genre_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).all()
    genres = db_sess.query(Genres).all()
    genre = db_sess.query(Genres).filter(Genres.id == genre_id).all()
    need_books = []
    book_liked_ids = []
    if current_user.is_authenticated:
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        book_liked_ids = [b.id for b in user.liked]
    else:
        book_liked_ids = [0]
    for i in book:
        for j in i.genres:
            if int(genre_id) == int(j.id):
                need_books.append(i)

    return render_template('sort_genre.html', need_books=need_books, genres=genres, genre=genre,
                           book_liked_ids=book_liked_ids)


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    app.run(port=8080, debug=True)
    # q()
