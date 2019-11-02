#encoding: utf-8

import json

from flask import Flask,render_template,request,redirect,url_for,session,g
from sqlalchemy import or_

import config
from models import User,MovieList,CommentInfo
from exts import db
from comfun import movie_pic,actors_short,create_phone,get_movie_id
from log import log
from comfun import update_movieinfo
from decorators import login_required

# 创建flask应用，以及配置文件，并初始化
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 主页
@app.route('/')
def index():
    context = {
        'movies': MovieList.query.order_by(MovieList.rank.asc()).all()
    }
    return render_template('index.html',**context,fun=movie_pic,fun2=actors_short,get_movie_id=get_movie_id)


# 分页
@app.route('/page/')
def page():

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    # paginate = Student.query.order_by('-s_id').paginate(page, per_page, error_out=False)
    movielist =  MovieList.query.order_by(MovieList.rank.asc()).paginate(page, per_page, error_out=False)
    # MovieList.query.order_by(MovieList.rank.asc()).all()
    context = {
        'movies': movielist.items,
        'fun' : movie_pic,
        'fun2' : actors_short,
        'get_movie_id' : get_movie_id,
    }
    print(context)
    return render_template('page.html',**context)

# 电影信息页面
@app.route('/info/<movie_id>/')
def info(movie_id):

    # 更新电影信息
    update_movieinfo(movie_id)
    # 数据查找出来
    context = {
        'movie' : MovieList.query.filter(MovieList.id == movie_id).first(),
        'commentinfos' : CommentInfo.query.filter(CommentInfo.movie_id == movie_id).all()
    }

    return render_template('info.html',**context,fun=movie_pic )

# 用户登录
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
            return render_template('err.html',err_info='手机号码或者密码错误，请确认后再登录！')


# 用户注册
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
            return render_template('err.html',err_info='该手机号码已被注册，请更换手机号码！')
        else:
            # password1要和password2相等才可以
            if password1 != password2:
                return render_template('err.html',err_info='两次密码不相等，请核对后再填写！')
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))


# 用户发表评论，注册用户才能发表评论
@app.route('/add_comment/',methods=['POST'])
@login_required
def add_comment():
    comment_info = request.form.get('content')
    movie_id = request.form.get('movie_id')
    commentinfo = CommentInfo(comment_info=comment_info,movie_id=movie_id)
    commentinfo.author = g.user
    db.session.add(commentinfo)
    db.session.commit()
    return redirect(url_for('info',movie_id=movie_id))


# 查找电影
@app.route('/search')
def search():
    q = request.args.get('search').split()
    if q:
        query=q[0]
        condition = or_(MovieList.title.contains(query), MovieList.related_info.contains(query))
        movies = MovieList.query.filter(condition).order_by('rank')
        return render_template('index.html', movies=movies, fun=movie_pic, fun2=actors_short, get_movie_id=get_movie_id)
    else:
        return  render_template('err.html',err_info='查询内容不能为空')


# 用户注销登录
@app.route('/logout/')
def logout():
    # 清出session的几种方式
    session.pop('user_id')
    # del session['user_id']
    # session.clear()
    return redirect(url_for('login'))


# 更新电影信息
@app.route('/addmovie/')
@login_required
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


# before_request -> 视图函数 -> context_processor
# 钩子函数，用户session跟踪
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}


if __name__ == '__main__':
    # pass
    app.run(debug=True,port=7000)
