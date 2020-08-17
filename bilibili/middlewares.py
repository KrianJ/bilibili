from fake_useragent import UserAgent
import requests


class UserAgentMiddleware(object):
    """user-agent池"""
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        # request.headers.setdefault('User-Agent', self.ua.random)
        request.headers['User-Agent'] = self.ua.random
        print('目前的ua是:', request.headers['User-Agent'])
        return None


class ProxyMiddleware(object):
    def get_proxy(self):
        proxypool_url = 'http://127.0.0.1:5555/random'
        return requests.get(proxypool_url).text.strip()

    def process_request(self, request, spider):
        request.meta['http_proxy'] = self.get_proxy()
        print("正在使用代理IP: ", request.meta['http_proxy'])

