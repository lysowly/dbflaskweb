
# 下载movie页面，提取信息

import lxml
from lxml import html
from spider.getpagebase import get_page_base
from spider.movieinfo import MovieInfo
from spider.comment import CommentInfo



class MovieSpider():

    def __init__(self,movieid):
        self.movieid = movieid
        self.url = 'https://movie.douban.com/subject/%s/' % self.movieid
        self.related_infos = []
        self.comments = []

    def get_movie_info(self):
        resp = get_page_base(url=self.url)
        cont = resp.content.decode('utf8')
        page = html.etree.HTML(cont)
        # 提取影片简介
        self.related_infos = [ related_info.replace('\n','').split() for related_info in page.xpath('//*[@id="link-report"]/span[1]/text()')]

        print(len(self.related_infos),self.related_infos)
        # 提取评论
        comments = page.xpath('//*[@id="hot-comments"]/div')
        for comment in comments:
            author = comment.xpath('.//div/h3/span[2]/a/text()')[0].replace('\n','').split()

            create_time = comment.xpath('.//div/h3/span[2]/span[3]/text()')[0].replace('\n','').split()
            comment_info = comment.xpath('.//div/p/span/text()')[0].replace('\n','').split()
            comm = CommentInfo(movie_id=self.movieid, author=author, create_time=create_time, comment_info=comment_info)
            self.comments.append(comm)
            print(comm.__dict__)
        len(self.comments)


if __name__ == '__main__':

    movieid = '1292063'
    m1 = MovieSpider(movieid)
    m1.get_movie_info()