import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Books(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    autor_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("authors.id"))
    book_author = orm.relationship('Authors')
    genre_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("genres.id"))
    book_genre = orm.relationship('Genres')
