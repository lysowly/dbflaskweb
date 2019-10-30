
import requests

from spider.header import header
from log import log


# 请求指定url网页，并返回下载内容
def get_page_base(url, headers=header):
    resp = requests.get(url=url, headers=headers,verify=False)

    if str(resp.status_code)[0] == '2':
        log.info('下载成功,状态为%s,url:%s:。' % (resp.status_code, url))
        return resp
    else:
        log.warning('下载不成功,状态为%s,url:%s:。' % (resp.status_code, url))
        return resp