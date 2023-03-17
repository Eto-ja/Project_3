import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    autor_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("authors.id"))

    genre_author = orm.relationship('Authors')
    books_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("books.id"))

    genre_book = orm.relationship('Books')
