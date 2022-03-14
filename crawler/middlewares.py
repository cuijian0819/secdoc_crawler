import random

class HttpProxyPoolMiddleware(object):

    def __init__(self):
        self.proxies = []


    @classmethod
    def from_crawler(cls, crawler):
        mw = cls()
        proxies = crawler.settings.get('HTTP_PROXY_TOR_PROXIES')
        mw.proxies = proxies if isinstance(proxies, list) else [proxies]
        return mw

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)

