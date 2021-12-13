from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        try:
            if tag == 'a':
                for (attribute, value) in attrs:
                    if attribute == 'href':
                        url = parse.urljoin(self.base_url, value)
                        self.links.add(url)
        except Exception as e:
            print(e)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
