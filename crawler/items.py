import scrapy
from scrapy.http import Request, Response
import hashlib
import datetime

# class urlItem(scrapy.Item):
#     url = scrapy.Field()
#     date_written = scrapy.Field()
#     date_collected = scrapy.Field()
#     text = scrapy.Field()


class CrawledItemLoader():

    @classmethod
    def from_response(cls, response):

        request = response.request
        content = response.body

        item = {
            'url': response.url,
            'date_written': ''.join(response.xpath('///div[@class="posted meta"]/span/text()').extract()),
            'date_collected': datetime.datetime.utcnow().strftime('%m/%d/%Y'),
            'title': ''.join(response.xpath('.//title/text()').extract()),
            'text': '\n'.join(response.xpath('//main//div[@class="col content-wrap"]//p//text()').extract()),
        }
        # from pdb import set_trace
        # set_trace()

        return item
    