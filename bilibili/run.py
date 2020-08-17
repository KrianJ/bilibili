# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/16 23:15"
__doc__ = """ 启动文件"""

from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'danmu'])
