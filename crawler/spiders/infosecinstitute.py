import scrapy
import re 
import os 
import logging
from crawler.items import CrawledItemLoader
from pdb import set_trace
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from collections import defaultdict
from scrapy.exceptions import CloseSpider

import datetime

class Spider(scrapy.Spider):
    name = "infosecinstitute"
    start_urls = [
        'https://resources.infosecinstitute.com/article-archive/',
   ]
    data_path = '../data/'
    save_fname = os.path.join(data_path, '{}.josnl'.format(name))
    hostname = urlparse(start_urls[0]).hostname

    def parse(self, response):
        if response.status == 200:
            logging.log(logging.INFO, '[Spider] Downloaded: {}'.format(response.url))
            
            hostname = urlparse(response.url).hostname
            # urls_to_follow = LinkExtractor(allow_domains=hostname, allow='page', restrict_xpaths='.//main').extract_links(response)
            # urls_to_save = LinkExtractor(allow_domains=hostname, deny=['page', 'career'], restrict_xpaths='.//main').extract_links(response)
            urls_extracted = LinkExtractor(allow_domains=hostname, \
                                           allow=['page', 'topic', 'certification'], 
                                           restrict_xpaths='.//main').extract_links(response) 
            
            for url in [l.url for l in urls_extracted]:
                yield scrapy.Request(url, callback=self.parse)
            
  
            if bool(re.search(r'certification\/\w+|topic\/\w+', response.url)): # To-do
                # item = CrawledItemLoader.from_response(response)
                item = {
                    'url': response.url,
                    'date_collected': datetime.datetime.utcnow().strftime('%m/%d/%Y'),
                    # To-do: 
                    'title': ''.join(response.xpath('.//title/text()').extract()),
                    'text': '\n'.join(response.xpath('//main//div[@class="col content-wrap"]//p//text()').extract()), 
                    'date_written': ''.join(response.xpath('///div[@class="posted meta"]/span/text()').extract()),
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
