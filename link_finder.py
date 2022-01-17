# pylint: disable=C0116
"""
# /***************************************************************************************
#  This module is responsible for turning snippits of HTML into actual links.
# ***************************************************************************************\
"""
from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        # inheriting objects from spider.py
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # Function for finding links
    def handle_starttag(self, tag, attrs):
        try:
            if tag == 'a':
                for (attribute, value) in attrs:
                    # Grabbing a potential link
                    if attribute == 'href':
                        url = parse.urljoin(self.base_url, value)
                        # Adding the url to the set
                        self.links.add(url)

        except Exception as error:
            print(error)

    # Returns the set
    def page_links(self):
        return self.links

    # Errors
    def error(self, message):
        pass
