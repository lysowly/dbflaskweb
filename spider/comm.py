
import os
import time
import requests

from spider.header import header
from log import log

# 爬虫环境参赛设置
class glob_value():
    # cover_queues = Queue()
    # url_queues = Queue()
    img_path = 'static/movieimages'
    look_dir = 0
    # queues_cover_num = 1
    # queues_url_num = 1
    # file_path = 'file'

# 创建目录 防止多线程冲突
def Create_path(flpath):
    if os.path.isdir(os.path.dirname(flpath)):
        return True
    else:
        while True:
            if glob_value.look_dir == 1:
                time.sleep(0.2)
                continue
            else:
                glob_value.look_dir = 1
                os.makedirs(os.path.dirname(flpath))
                glob_value.look_dir = 0
                log.info('系统已经创建目录：', flpath)
                break
        return True

# 下载图片
def img_down(cover_url):
    r = requests.get(cover_url,headers=header,verify=False)
    filename = os.path.join(os.curdir,glob_value.img_path,cover_url.split('/')[-1])
    Create_path(filename)
    with open(filename,'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

if __name__ == '__main__':
    img_down('https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2206737207.webp')