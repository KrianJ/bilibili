from scrapy import Request
from bilibili.items import *
from bilibili.date_component import create_date_seq, get_publish_date
import json
import re


class DanmuSpider(scrapy.Spider):
    __doc__ = """抓取指定av号下所有的历史弹幕"""
    name = 'danmu'
    allowed_domains = ['bilibili.com']
    custom_settings = {}

    def start_requests(self):
        """生成初始请求"""
        base_url = r'https://api.bilibili.com/x/web-interface/archive/stat?aid={0}'
        url = base_url.format(AV)
        yield Request(url=url, callback=self.info_parse)

    def info_parse(self, response):
        """视频基本信息（点赞，投币，收藏，转发等）, 并返回cid请求"""
        info = InfoItem()
        data = json.loads(response.text).get('data')
        info['aid'] = data.get('aid')
        info['bvid'] = data.get('bvid')
        info['coin'] = data.get('coin')
        info['danmaku'] = data.get('danmaku')
        info['fav'] = data.get('favorite')
        info['like'] = data.get('like')
        info['reply'] = data.get('reply')
        info['share'] = data.get('share')
        info['view'] = data.get('view')
        yield info
        part_base = 'https://api.bilibili.com/x/player/pagelist?bvid={0}&jsonp=jsonp'
        part_url = part_base.format(info['bvid'])
        yield Request(url=part_url, callback=self.cid_parse)

    def cid_parse(self, response):
        """获取cid并返回弹幕日期请求"""
        date_base = r'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={0}&month={1}'
        data = json.loads(response.text).get('data')

        cids = [str(part.get('cid')) for part in data]
        # 将cid保存至txt
        txt_path = r'D:\Pyproject\scrapy_stuff\bilibili\bilibili\middle_args\av{0}_cids.txt'.format(AV)
        with open(txt_path, 'w') as f:
            for cid in cids:
                f.write(cid + '\n')
        f.close()

        months = create_date_seq(datestart=get_publish_date())
        for cid in cids:
            for month in months:
                url = date_base.format(cid, month)
                yield Request(url=url, callback=self.date_parse, dont_filter=True)

    def date_parse(self, response):
        """获取有弹幕的日期, 并返回弹幕请求"""
        txt_path = r'D:\Pyproject\scrapy_stuff\bilibili\bilibili\middle_args\av{0}_cids.txt'.format(AV)
        with open(txt_path, 'r') as f:
            cids = [line.strip('\n') for line in f.readlines()]
        dates = json.loads(response.text).get('data')
        base_danmaku_url = r'https://api.bilibili.com/x/v2/dm/history?type=1&oid={0}&date={1}'
        for cid in cids:
            for date in dates:
                url = base_danmaku_url.format(cid, date)
                yield Request(url=url, callback=self.danmaku_parse)

    def danmaku_parse(self, response):
        """解析弹幕请求"""
        danmu_item = DanmakuItem()
        xml_string = response.text
        params = re.findall(re.compile('<d p="(.*?)">'), xml_string)
        danmaku = re.findall(re.compile('<d.*?>(.*?)</d>'), xml_string)
        for i in range(len(params)):
            param = params[i].split(',')
            danmu_item['sendID'] = param[6]
            danmu_item['sendType'] = param[5]
            danmu_item['rowID'] = param[7]
            danmu_item['content'] = danmaku[i]
            yield danmu_item








