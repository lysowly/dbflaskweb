import os
import random

from spider.comm import img_down

# 判断图片在本地目录是否存在，如不存在重新下载图片，返回图片本地目录路径
def movie_pic(url):
    img_filename = 'movieimages/{}'.format(url.split('/')[-1])
    if not file_exits(url):
        print('下载图片：',url)
        img_down(url)
    return img_filename

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


if __name__ == '__main__':
    print(create_phone())