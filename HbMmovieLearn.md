# 花瓣电影信息网学习笔记

## 一、网站功能需求

1.用户在网站浏览电影信息，该信息同步豆瓣电影信息。
2.用户可以对电影发表影评，展示豆瓣电影热门影评内容。
3.只有登录用户才可以发表评论

## 二、主要功能模块
### 1.电影信息爬取模块
爬取电影信息，用户查看电影详情时，实时爬去该电影热门影评。
### 2.电影信息展示模块
实现电影信息列表显示，对具体电影实现详细信息线索，并可以发表评论。
### 3.用户注册/登录模块
实现用户注册、登录，并记录用户登录情况，并控制用户行为。
### 4.数据库设计模块
根据业务需求，实现用户表、电影信息表、用户评论表等，并实现关联。
### 5.日志记录模块
实现日志记录，可以配置不同的日志等级。

## 三、目录结构

```bash
├── dbflasky.py			# 视图函数
├── comfun.py  			# 公共函数
├── config.py			# flask 配置参数
├── decorators.py		# 装饰函数 判断用户是否登录
├── environment.txt		# python环境 包配置 
├── exts.py 			# db初始化
├── log.py 				# 日志记录模块
├── manage.py 			# 数据库manage管理模块
├── migrations 			# 数据库升级自动生成文件
├── models.py 			# 数据库模型
├── setting.py 			# 日志参数配置
├── spider				# 爬虫模块
│   ├── comm.py
│   ├── getpagebase.py
│   ├── header.py 		# 爬虫头信息
│   ├── __init__.py
│   └── moviespider.py  # 数据爬取
├── static				# 静态文件
│   ├── css
│   ├── images
│   └── movieimages
├── temp 				# 临时文件
│   ├── data.txt
│   └── movielist.txt
└── templates 			# 模板
    ├── base.html
    ├── err.html
    ├── index.html
    ├── info.html
    ├── login.html
    └── regist.html
```





##  四、功能实现

### 1.数据库设计
用户表结构设计：

```python
class User(db.Model):
    # 实现用户电话、名称、ID、密码、创建时间等管理。
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
```
电影信息表机构设计：


```python
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
    related_info = db.Column(db.String(5000),nullable=True)

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
        related_info = kwargs.get('related_info')
        
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
        self.related_info = related_info

        # 将列表字段转换为字符串，默认使用逗号分割
        def listcover(self,list_column,split_mk=','):
            if isinstance(list_column,list):
                return split_mk.join(list_column)

        # 将字符串转换为列表字段，默认使用逗号分割
        def coverlist(self,strlist,split_mk=','):
            return list(strlist.split(split_mk))
```


用户评论表结构设计：

```python
class CommentInfo(db.Model):
    __tablename__ = 'commentinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_info = db.Column(db.String(2000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    movie_id = db.Column(db.String(50), db.ForeignKey('movielist.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('commentinfo'))
    movie = db.relationship('MovieList', backref=db.backref('commentinfo'))

    def __init__(self, *args, **kwargs):
        self.movie_id = kwargs.get('movie_id')
        self.author_id = kwargs.get('author_id')
        self.comment_info = kwargs.get('comment_info')
```

### 2.登录模块实现

用户登录
```python
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
```

用户注册
```python
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
```

用户注销
```python
# 用户注销登录
@app.route('/logout/')
def logout():
    # 清出session
    session.pop('user_id')
    return redirect(url_for('login'))
```

用户登录判断
```python
# 登录限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            print('ok')
            return func(*args,**kwargs)
        else:
            print('no')
            return redirect(url_for('login'))
    
    return wrapper
# 钩子函数，用户session跟踪
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user
```

### 3.评论实现

```python
@app.route('/add_comment/',methods=['POST'])
@login_required 								# 判断是否为注册用户
def add_comment():
    comment_info = request.form.get('content')
    movie_id = request.form.get('movie_id')
    commentinfo = CommentInfo(comment_info=comment_info,movie_id=movie_id)
    commentinfo.author = g.user
    db.session.add(commentinfo)
    db.session.commit()
    return redirect(url_for('info',movie_id=movie_id))
```
注：装饰器的顺序影响功能实现。

### 4.电影查找功能

```python
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
```

### 5.数据爬取实现

```python
# 更新电影简介和影评
def update_movieinfo(movie_id):

    movieinfo = MovieList.query.filter(MovieList.id == movie_id).first()
    
    # 从豆瓣电影下载该电影介绍
    movie = MovieSpider(movie_id)
    movie.get_movie_info()
    
    # 判断影片内容是否为空
    if movie.related_info:
        # 把这条数据，你需要修改的地方进行修改
        # print(movie.related_info)
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
        commentinfo = CommentInfo(movie_id=movie_id, author_id=int(author_id), 		comment_info=coment.get('comment_info'))
        commentinfo.create_time = coment.get('create_time'),
        db.session.add(commentinfo)
        try:
            db.session.commit()
            log.info('%s: 影评内容已经插入数据库' % movie.movieid)
        except:
            log.warning('%s: 影评内容出现异常，%s:%s:%s' % (movie.movieid,commentinfo.author_id,commentinfo.author,commentinfo.comment_info))
        else:
            continue
```

电影信息更新
```python
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
```

### 6.日志记录实现

```python
class LogHandler(logging.Logger):
    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()
    
    def __setFileHandler__(self, level=None):
        if not os.path.isdir(LOG_PATH):
            os.mkdir(LOG_PATH)
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name,encoding='utf-8', when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)
    
    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)
    
    def resetName(self, name):
        self.name = name
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()
```

## 五、项目部署
### 1.安装Nginx
​	sudo apt install nginx

### 2.配置文件nginx
​	/etc/nginx/sites-available/default
​	初始的server_name的值为 下划线_，把它的值改为公网的IP地址即可。
​	接着就可以在浏览器输入IP地址来测试Nginx所提供的默认网页了。如果无法访问，则可能是没有开启端口。

```bash
	# root /var/www/html;
	root /home/ubuntu/github/dbflaskweb;
	server_name 49.233.148.18;
	
	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		# try_files $uri $uri/ =404;
		include uwsgi_params;
		# uwsgi_pass 配置需要与uwsgi.ini文件的IP和端口号保持一致。
		uwsgi_pass 127.0.0.1:8080;
		uwsgi_param UWSGI_CHDIR /home/ubuntu/github/dbflaskweb;
		uwsgi_param UWSGI_PYHOME /home/ubuntu/github/dbflaskweb/venv;
		uwsgi_param UWSGI_SCRIPT app:app;
}
```

注意事项：

- Nginx监听80端口，root为项目根目录；location则保存着uWSGI的相关配置，用以方便Nginx和uWSGI的通信。
- ​	location中用到了UWSGI_PYHOME来表示虚拟环境的路径，如果没有用到虚拟环境则可以注释掉这一句。
- ​	另外就是uwsgi_pass中的IP:port和uwsgi.ini的socket的IP:port是相同的。
- ​	配置完后重新启动nginx服务：service nginx restart

### 3.安装uWSGI

```bash
sudo apt install uwsgi
sudo apt-get install uwsgi-plugin-python
```

### 4.配置文件uwsgi.ini

```bash
    [uwsgi]
    #uwsgi启动时所使用的地址与端口，端口可以使用其他端口
    socket=127.0.0.1:8080
	# 指向网站的项目根目录
	chdir=/home/ubuntu/github/dbflaskweb
	 
	#python启动程序文件
	wsgi-file=dbflasky.py
	 
	#python程序内用以启动application变量名，app = Flask(__name__)
	callable=app
	master=true
	 
	#安装uwsgi-plugin-python后需要添加的一个参数
	plugins=python  

	#处理器数目
	processes=1
	 
	#线程数
	threads=5
```

### 5.uwsgi运行

```bash
	uwsgi uwsgi.ini
	#后台运行：
	uwsgi -d --ini uwsgi.ini
```

### 6.wusgi停止

```bash
	ubuntu   22112  0.5  2.0 115868 39320 ?        S    15:18   0:00 /home/ubuntu/.local/bin/uwsgi -d --ini uwsgi_script/uwsgi.ini
	ubuntu   22492  0.0  1.6 410796 31600 ?        Sl   15:21   0:00 /home/ubuntu/.local/bin/uwsgi -d --ini uwsgi_script/uwsgi.ini
# 停止类型为S的进程
kill -9 22112  
```

### 7.网站地址

http://49.233.148.18/


