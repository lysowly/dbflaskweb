#encoding: utf-8

import json

from flask import Flask,render_template,request,redirect,url_for,session,g
from sqlalchemy import or_

import config
from models import User,MovieList
from exts import db
from comfun import movie_pic,actors_short,create_phone
from log import log


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'movies': MovieList.query.order_by(MovieList.rank.asc()).all()
    }
    return render_template('index.html',**context,fun=movie_pic,fun2=actors_short)


# 电影信息页面
@app.route('/info/<movie_id>/')
def info(movie_id):

    return movie_id

# # 第一种最简单
# db.session.query(User).order_by('id desc').all()
#
# # 第二种比较符合 SQLAlchemy 语法
# db.session.query(User).order_by(User.id.desc()).all()

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

# @app.route('/question')
# def question():
#     return 'question'

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
@app.route('/create/<username>')
def create_user(username):

    user = User.query.filter(User.username == username).first()
    if user:
        return str(user.id)
    else:
        print('else')
        telephone = create_phone()
        username = username
        password = '111'
        user = User(telephone=telephone,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        log.info('%s： 用户已经创建' % username)
        user = User.query.filter(User.username == username).first()
        return str(user.id)


if __name__ == '__main__':
    # pass
    app.run(debug=True,port=7000)
