#encoding: utf-8

import json

from flask import Flask,render_template,request,redirect,url_for,session,g
from sqlalchemy import or_

import config
from models import User,MovieList,CommentInfo
from exts import db
from comfun import movie_pic,actors_short,create_phone
from log import log
from spider.moviespider import MovieSpider


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'movies': MovieList.query.order_by(MovieList.rank.asc()).all()
    }
    return render_template('index.html',**context,fun=movie_pic,fun2=actors_short)

# 更新电影简介和影评
def update_movieinfo(movie_id):

    movieinfo = MovieList.query.filter(MovieList.id == movie_id).first()

    # 从豆瓣电影下载该电影介绍
    movie = MovieSpider(movie_id)
    movie.get_movie_info()

    # 判断影片内容是否为空
    if movie.related_info:
        # 把这条数据，你需要修改的地方进行修改
        print(movie.related_info)
        movieinfo.related_info = movie.related_info
        #  做事务的提交,将电影介绍提交到数据库
        db.session.commit()
        log.info('%s: 电影简介内容已经插入数据库' % movie.movieid)
    else:
        log.warning('%s: 获取电影简介内容为空' % movie.movieid)

    # 从豆瓣电影下载电影评论,并插入到数据库
    # print('coment', len(movie.comments))
    for coment in movie.comments:
        com_a = CommentInfo.query.filter(CommentInfo.comment_info == coment.get('comment_info')).first()
        if com_a:
            log.info('%s: 影评内容重复，不需要插入数据库' % movie.movieid)
            continue
        author_id = create_user(coment.get('author'))
        commentinfo = CommentInfo(movie_id=movie_id, author_id=int(author_id), comment_info=coment.get('comment_info'))
        commentinfo.create_time = coment.get('create_time'),
        db.session.add(commentinfo)
        try:
            db.session.commit()
            log.info('%s: 影评内容已经插入数据库' % movie.movieid)
        except:
            log.warning('%s: 影评内容出现异常，%s:%s:%s' % (movie.movieid,commentinfo.author_id,commentinfo.author,commentinfo.comment_info))
        else:
            continue


# 电影信息页面
@app.route('/info/<movie_id>/')
def info(movie_id):

    # 更新电影信息
    # update_movieinfo(movie_id)
    # 数据查找出来
    context = {
    'movie' : MovieList.query.filter(MovieList.id == movie_id).first(),
    'commentinfos' : CommentInfo.query.filter(CommentInfo.movie_id == movie_id).all()
    }
    # print(movieinfo.__dict__)
    # for commentinfo in commentinfos:
    #     print(commentinfo.__dict__)
    return render_template('info.html',**context,fun=movie_pic )


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            # password1要和password2相等才可以
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


@app.route('/search')
def search():
    return 'search'

@app.route('/logout/')
def logout():
    session.pop('user_id')
    del session['user_id']
    session.clear()
    return redirect(url_for('login'))

# before_request -> 视图函数 -> context_processor

# 更新电影信息
@app.route('/addmovie/')
def addmovie():
    with open('temp/movielist.txt','r',encoding='utf8') as f:
        movie_list = f.read()

    movies = json.loads(movie_list)
    for movie in movies:
        movie_info = MovieList.query.filter(MovieList.id == movie.get('id','')).first()
        if not movie_info:
            movielist = MovieList(**movie)
            db.session.add(movielist)
            db.session.commit()
            log.info('%s :该影片已保存到数据库。' % movie.get('title', ''))
        else:
            log.info('%s :该影片已有，不需要更新。' % movie.get('title',''))

    return  redirect(url_for('index'))


# 根据用户名，创建用户，并返回用户ID
# @app.route('/create/<username>')
def create_user(username):

    user = User.query.filter(User.username == username).first()
    if user:
        log.info('%s： 该用户已存在，不需要创建。' % username)
        return str(user.id)
    else:
        telephone = create_phone()
        username = username
        password = '111'
        user = User(telephone=telephone,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        log.info('%s： 创建用户成功。' % username)
        user = User.query.filter(User.username == username).first()
        return str(user.id)


if __name__ == '__main__':
    # pass
    app.run(debug=True,port=7000)
