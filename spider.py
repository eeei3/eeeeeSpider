#! /usr/local/bin/python3

# pylint: disable=C0116


"""
# /***************************************************************************************
#  This module is responsible for performing many of the crawler functions.
# ***************************************************************************************\
"""
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import get_domain_name
from general import file_to_set, set_to_file
import sys


class Spider:
    queue = set()
    crawled = set()
    spiderlimits = False
    limitnum = 0
    external = False
    limit_counter = 0

    def __init__(self, project_name, base_url, domain_name,
                 spiderlimits, limitnum, external, limit_counter):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.spiderlimits = spiderlimits
        Spider.limitnum = int(limitnum)
        Spider.external = external
        Spider.limit_counter = limit_counter
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        # Creates directory and files for project on first run
        # and starts the spider
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        # Updates user display, fills queue and updates files
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) +
                  ' | Crawled  ' + str(len(Spider.crawled)))
            # Checking if the user wants to crawl sites
            # not related to original domain
            if not Spider.external:
                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue(links)
            else:
                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue_no_check(links)

            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        # Converts raw response data into readable information
        # and checks for proper html formatting
        html_string = ''
        try:
            response = urlopen(page_url)
            print(Spider.spiderlimits)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as error:
            print(str(error))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        # Saves queue data to project files
        try:
            for url in links:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                if Spider.domain_name != get_domain_name(url):
                    continue
                Spider.queue.add(url)
        except Exception as error:
            print(str(error))
            sys.exit()

    @staticmethod
    def add_links_to_queue_no_check(links):
        # Saves queue data to project files without checking domain
        try:
            for url in links:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                Spider.queue.add(url)
        except Exception as error:
            print(str(error))
            sys.exit()

    @staticmethod
    def update_files():
        # Moving data from memory to drive
        try:
            set_to_file(Spider.queue, Spider.queue_file)
            set_to_file(Spider.crawled, Spider.crawled_file)
        except FileNotFoundError:
            sys.exit()
        except OSError:
            sys.exit()
