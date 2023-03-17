from flask import Flask, redirect, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_login import LoginManager, login_user
from loginform import LoginForm
from workform import WorkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
