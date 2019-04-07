import scrapy
import string
from collections import Counter


class GFDSpider(scrapy.Spider):
    name = "gfd_spider"

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url is not None:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth':1})

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GFDSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)

    def parse(self, response):
        text = []
        table = str.maketrans('', '', string.punctuation)
        pieces = list(map(str.strip, response.xpath('//*[not(self::script or self::style)]/text()[re:test(., "\w+")]').extract()))

        for piece in pieces:
            words = piece.split()
            words_no_punc = []
            for w in words:
                wnp = w.translate(table).lower()
                if wnp:
                    words_no_punc.append(wnp)
            text.extend(words_no_punc)

        yield {
            'url': response.url,
            'title': response.xpath('//title/text()').get(),
            'text': Counter(text),
        }

        print('Number of words %s' % len(Counter(text)))

        depth = response.meta['depth']
        if depth < 3:
            for href in response.css('a::attr(href)'):
                print(href)
                yield response.follow(href, callback=self.parse, meta={'depth': depth+1})