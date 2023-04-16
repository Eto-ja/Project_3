from typing import List

import sqlalchemy
from sqlalchemy.orm import Mapped, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from data.books import Books

like_table = sqlalchemy.Table(
    'like',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)

read_table = sqlalchemy.Table(
    'read',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    liked: Mapped[List[Books]] = relationship(secondary=like_table)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
