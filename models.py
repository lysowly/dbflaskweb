#encoding: utf-8

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result


class CommentInfo(db.Model):

    __tablename__ = 'commentinfo'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    movie_id = db.Column(db.String(20),nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_info = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)



    def __init__(self,*args,**kwargs):
        self.movie_id = kwargs.get('movie_id')
        self.author = kwargs.get('author')
        self.create_time = kwargs.get('create_time')
        self.comment_info = kwargs.get('comment_info')


class MovieList(db.Model):

    __tablename__ = 'movielist'
    rating = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.String(100), nullable=False)
    is_playable = db.Column(db.Boolean, nullable=False)
    id = db.Column(db.String(50),primary_key=True,autoincrement=False)
    types = db.Column(db.String(100),nullable=False)
    regions = db.Column(db.String(100),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(100),nullable=False)
    release_date = db.Column(db.String(100),nullable=False)
    actor_count = db.Column(db.String(100),nullable=False)
    vote_count = db.Column(db.String(100),nullable=False)
    score = db.Column(db.String(100),nullable=False)
    actors = db.Column(db.String(1500),nullable=False)
    is_watched = db.Column(db.Boolean,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self,*args,**kwargs):
        rating = kwargs.get('rating')
        rank = kwargs.get('rank')
        cover_url = kwargs.get('cover_url')
        is_playable = kwargs.get('is_playable')
        id = kwargs.get('id')
        types = kwargs.get('types')
        regions = kwargs.get('regions')
        title = kwargs.get('title')
        url = kwargs.get('url')
        release_date = kwargs.get('release_date')
        actor_count = kwargs.get('actor_count')
        vote_count = kwargs.get('vote_count')
        score = kwargs.get('score')
        actors = kwargs.get('actors')
        is_watched = kwargs.get('is_watched')


        self.rating = self.listcover(rating)
        self.rank = rank
        self.cover_url = cover_url
        self.is_playable = is_playable
        self.id = int(id)
        self.types = self.listcover(types)
        self.regions = self.listcover(regions)
        self.title = title
        self.url = url
        self.release_date = str(release_date)
        self.actor_count = str(actor_count)
        self.vote_count = str(vote_count)
        self.score = score
        self.actors = self.listcover(actors)
        self.is_watched = is_watched

    # 将列表字段转换为字符串，默认使用逗号分割
    def listcover(self,list_column,split_mk=','):
        if isinstance(list_column,list):
            return split_mk.join(list_column)

    # 将字符串转换为列表字段，默认使用逗号分割
    def coverlist(self,strlist,split_mk=','):
        return list(strlist.split(split_mk))


if __name__ == '__main__':
    pass

