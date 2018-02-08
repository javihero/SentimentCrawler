import scrapy

from scrapy.spiders import XMLFeedSpider


class Spider(XMLFeedSpider):
    name = "rss"
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s',
                         self.itertag, ''.join(node.extract()))

        item = {}
        # define XPath for title
        item['title'] = node.xpath('title/text()',).extract_first()
        item['link'] = node.xpath('link/text()').extract_first()
        item['pubDate'] = node.xpath('link/pubDate/text()').extract_first()
        item['description'] = node.xpath('description/text()').extract_first()
        return item
