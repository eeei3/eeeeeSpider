from html.parser import HTMLParser
from urllib import parse


"""
# /***************************************************************************************
#  This module is responsable for turning snippits of HTML into acutal links.
# ***************************************************************************************\
"""

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        # inheriting objects from spider.py
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        # Function for finding links
        try:
            if tag == 'a':
                for (attribute, value) in attrs:
                    # Grabbing a potential link
                    if attribute == 'href':
                        url = parse.urljoin(self.base_url, value)
                        # Adding the url to the set
                        self.links.add(url)
                        
        except Exception as e:
            print(e)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
