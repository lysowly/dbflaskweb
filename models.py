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


class MovieList(db.Model):
    '''
    rating:['9.6', '50'];
    rank:1;
    cover_url:https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2354179225.webp;
    is_playable:False;
    id:5133063;
    types:['喜剧'];
    regions:['英国'];
    title:憨豆先生精选辑;
    url:https://movie.douban.com/subject/5133063/;
    release_date:1997;
    actor_count:8;
    vote_count:3554;
    score:9.6;
    actors:['罗温·艾金森', 'Paul Bown', '理查德·布赖尔斯', 'Angus Deayton', '罗宾·德里斯科尔', '卡罗琳·昆汀', 'Rudolph Walker', '理查德·威尔逊'];
    is_watched:False;
    '''
    __tablename__ = 'movielist'

    rating = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.String(100), nullable=False)
    is_playable = db.Column(db.Boolean, nullable=False)
    id = db.Column(db.Integer,primary_key=True,autoincrement=False)
    types = db.Column(db.String(100),nullable=False)
    regions = db.Column(db.String(100),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    url = db.Column(db.String(100),nullable=False)
    release_date = db.Column(db.String(100),nullable=False)
    actor_count = db.Column(db.String(100),nullable=False)
    vote_count = db.Column(db.String(100),nullable=False)
    score = db.Column(db.String(100),nullable=False)
    actors = db.Column(db.String(100),nullable=False)
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
        self.rank = int(rank)
        self.cover_url = cover_url
        self.is_playable = is_playable
        self.id = int(id)
        self.types = self.listcover(types)
        self.regions = self.listcover(regions)
        self.title = title
        self.url = url
        self.release_date = release_date
        self.actor_count = actor_count
        self.vote_count = vote_count
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

