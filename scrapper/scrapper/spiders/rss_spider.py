from scrapy.spiders import XMLFeedSpider

import re
import html


def sanitize_content(data):
    data = html.unescape(data)
    p = re.compile(r'<.*?>')
    return p.sub('', data)


class Spider(XMLFeedSpider):
    name = "rss"
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s',
                         self.itertag, ''.join(node.extract()))

        item = {}
        item['title'] = node.xpath('title/text()',).extract_first()
        item['link'] = node.xpath('link/text()').extract_first()
        item['pubDate'] = node.xpath('pubDate/text()').extract_first()

        description = node.xpath('description/text()').extract_first()
        item['description'] = sanitize_content(description)

        return item
