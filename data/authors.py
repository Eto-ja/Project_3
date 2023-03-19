import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

genres_authors_table = sqlalchemy.Table(
    'genres_authors',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('authors', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('authors.id')),
    sqlalchemy.Column('genres', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)


class Authors(SqlAlchemyBase):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
