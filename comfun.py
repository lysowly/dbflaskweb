import os
import random

from spider.comm import img_down
from models import MovieList,CommentInfo,User
from exts import db
from log import log
from spider.moviespider import MovieSpider

# 判断图片在本地目录是否存在，如不存在重新下载图片，返回图片本地目录路径
def movie_pic(url):
    img_filename = 'movieimages/{}'.format(url.split('/')[-1])
    if not file_exits(url):
        print('下载图片：',url)
        img_down(url)
    return img_filename

def get_movie_id(url):
    return url.split('/')[-2]

# 判断图片在本地目录是否存在
def file_exits(url):
    img_filename = 'static/movieimages/{}'.format(url.split('/')[-1])
    if os.path.isfile(img_filename):
        return True
    return False

# 判断演员数量，超过设定数量的，不再显示
def actors_short(actor,num=8,sp='  '):
    actors = actor.split(',')
    if len(actors) > num :
        return sp.join(actors[0:num])+'......'
    return sp.join(actors)


def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999,100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


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


# 根据用户名，创建用户，并返回用户ID
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
        user = User.query.filter(User.username == username).first()
        log.info('创建用户成功:%s,%s。' % (user.id, username))
        return str(user.id)


if __name__ == '__main__':
    print(create_phone())