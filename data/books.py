import sqlalchemy
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
