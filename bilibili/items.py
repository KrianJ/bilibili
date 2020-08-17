import scrapy
from scrapy import Item
from scrapy import Field
from bilibili.settings import AV


class InfoItem(Item):
    """视频基本信息"""
    collection = 'baseInfo'
    aid = Field()
    bvid = Field()
    coin = Field()
    danmaku = Field()
    fav = Field()
    like = Field()
    reply = Field()
    share = Field()
    view = Field()


class DanmakuItem(Item):
    """解析弹幕xml文件中参数"""
    collection = 'av'+str(AV)+'_danmakus'
    sendID = Field()        # 发送者id
    sendType = Field()      # 弹幕类型，0普通池，1字幕池，2特殊池(高级弹幕)
    rowID = Field()         # 弹幕在弹幕数据库中的id，用于历史弹幕
    content = Field()       # 弹幕内容
