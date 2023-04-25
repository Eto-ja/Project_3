from typing import List
import sqlalchemy
from sqlalchemy.orm import relationship, Mapped

from data.authors import Authors
from data.genres import Genres, genres_books_table
from .db_session import SqlAlchemyBase


from sqlalchemy import orm

authors_books_table = sqlalchemy.Table(
    'authors_books',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id')),
    sqlalchemy.Column('authors', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('authors.id'))
)


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    photo_path = sqlalchemy.Column(sqlalchemy.String(4095), nullable=False)
    authors: Mapped[List[Authors]] = relationship(secondary=authors_books_table)
    genres: Mapped[List[Genres]] = relationship(secondary=genres_books_table)
    description = sqlalchemy.Column(sqlalchemy.String(4095), nullable=True)
