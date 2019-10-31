
# 下载movie页面，提取信息

import json

import lxml
from lxml import html
from spider.getpagebase import get_page_base




class MovieSpider():

    def __init__(self,movieid):
        self.movieid = movieid
        self.url = 'https://movie.douban.com/subject/%s/' % self.movieid
        self.related_info = ''
        self.comments = []
        # print(self.__dict__)

    def get_movie_info(self):
        resp = get_page_base(url=self.url)
        cont = resp.content.decode('utf8')
        page = html.etree.HTML(cont)
        # 提取影片简介
        related_infos = [ info.replace('\n','').split() for info in page.xpath('//*[@id="link-report"]/span[1]/text()')]
        self.related_info = json.dumps(related_infos,ensure_ascii=False)

        # print(len(self.related_info),self.related_info)
        # 提取评论
        comments = page.xpath('//*[@id="hot-comments"]/div')
        for comment in comments:
            comm_time = comment.xpath('.//div/h3/span[2]/span[3]/text()')[0].replace('\n', '').split()
            if len(comm_time)<3:
                comm_time = comm_time[0]
            aa = {
            'author' : json.dumps(comment.xpath('.//div/h3/span[2]/a/text()')[0].replace('\n','').split(),ensure_ascii=False),
            'create_time' : comm_time,
            'comment_info' : json.dumps(comment.xpath('.//div/p/span/text()')[0].replace('\n','').split(),ensure_ascii=False)
            # comm = CommentInfo(movie_id=self.movieid, author=author, create_time=create_time, comment_info=comment_info)
            }
            self.comments.append(aa)
            # print(aa)
        # len(self.comments)



if __name__ == '__main__':

    movieid = '5133063'
    m1 = MovieSpider(movieid)
    m1.get_movie_info()