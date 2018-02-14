from scrapy.spiders import XMLFeedSpider
from scrapper.helpers import sanitize_content


class AtomSpider(XMLFeedSpider):
    name = "atom"
    namespaces = [('atom', 'http://www.w3.org/2005/Atom')]
    iterator = 'xml'
    itertag = 'atom:entry'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s',
                         self.itertag, ''.join(node.extract()))

        entry = {}
        entry['title'] = node.xpath('atom:title/text()',).extract_first()
        entry['link'] = node.xpath('atom:link/text()').extract_first()
        entry['date'] = node.xpath('atom:updated/text()').extract_first()

        content = node.xpath('atom:content/text()').extract_first()
        entry['description'] = sanitize_content(content)

        return entry
