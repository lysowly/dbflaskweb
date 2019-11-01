# 花瓣电影信息网学习笔记

## 一、网站功能需求

1.用户在网站浏览电影信息，该信息同步豆瓣电影信息。
2.用户可以对电影发表影评，展示DB瓣电影热门影评内容。
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

