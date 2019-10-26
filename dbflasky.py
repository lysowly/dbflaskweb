#encoding: utf-8

from flask import Flask,render_template,request,redirect,url_for,session,g
from models import User
from exts import db
from sqlalchemy import or_

import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        # 'questions': Question.query.order_by('-create_time').all() #新版本框架升级
        # 'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('index.html',**context)

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

@app.route('/question')
def question():
    return 'question'

@app.route('/search')
def search():
    return 'search'

@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))

# before_request -> 视图函数 -> context_processor

if __name__ == '__main__':
    # pass
    app.run(debug=True,port=9000)
