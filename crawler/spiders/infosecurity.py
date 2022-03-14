import re 
import os 
import logging
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor

from crawler.items import CrawledItemLoader
from urllib.parse import urlparse
from collections import defaultdict
from scrapy.exceptions import CloseSpider

from pdb import set_trace

class Spider(scrapy.Spider):
    # To-do: 
    name = "infosecurity"
    start_urls = [
        'https://www.infosecurity-magazine.com/news/',
    ]
    ## end of To-do

    data_path = '../data/'
    save_fname = os.path.join(data_path, '{}.josnl'.format(name))
    hostname = urlparse(start_urls[0]).hostname

    def parse(self, response):
        if response.status == 200:
            logging.log(logging.INFO, '[Spider] Downloaded: {}'.format(response.url))
            
            urls_extracted = LinkExtractor(allow_domains=self.hostname, \
                                           allow=['page', 'news'],  # To-do
                                           restrict_xpaths='.//body').extract_links(response) 
            
            for url in [l.url for l in urls_extracted]:
                yield scrapy.Request(url, callback=self.parse)
            
            if bool(re.search(r'news\/(?!(page))\w+', response.url)): # To-do
                # set_trace()
                # item = CrawledItemLoader.from_response(response)
                item = {
                    'url': response.url,
                    'date_collected': datetime.datetime.utcnow().strftime('%m/%d/%Y'),
                    # To-do: 
                    'title': ''.join(response.xpath('.//title/text()').extract()), # works in most cases 
                    'text': '\n'.join(response.xpath('//body//div[@id="cphContent_pnlMainContent"]//p//text()').extract()),
                    'date_written': ''.join(response.xpath('//div[@class="article-meta"]/time/@datetime').extract()) 
                    ## end of To-do
                }
                yield item
            
        else:
            logging.log(logging.ERROR, '[Spider] {} at {}'.format(response.status, response.url))            
            
    # def save_page(self, response):
    #     hostname = urlparse(response.url).hostname
    #     with open(os.path.join(self.data_path, '{}_urls.txt'.format(hostname)), 'w') as f:
    #         for url in self.saved_urls:
    #             f.write('{}\n'.format(url))

    # def extract_title(self, response):
    #     return response.xpath('.//title/text()').extract()[0]
