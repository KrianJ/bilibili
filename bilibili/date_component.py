# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/16 13:57"
__doc__ = """ 构造日期列表
[2016-05, ..., 2020-10]"""
import datetime
import requests
import re
from bs4 import BeautifulSoup
from bilibili.settings import URL


def get_publish_date(url=URL):
    """获取视频发布时间"""
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'lxml')
    html_date = html.find_all('div', attrs={'class': 'video-data'})[0]
    pub_date = re.findall(pattern=re.compile('<span>(.*?)</span>'), string=str(html_date))[0]
    return pub_date[:7]


def create_date_seq(datestart, dateend=datetime.datetime.now().strftime('%Y-%m')):
    """生成指定的日期(年-月)序列"""
    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y-%m')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m'))
    while datestart < dateend:
        # 日期叠加一个月
        datestart += datetime.timedelta(days=31)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y-%m'))
    return date_list


if __name__ == '__main__':
    a = get_publish_date('https://www.bilibili.com/video/BV1xs411Q799?p=1')
    print(create_date_seq('2020-08'))
