from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    spiderlimits = False
    limitnum = 0
    external = False
    limit_counter = 0

    

    def __init__(self, project_name, base_url, domain_name, spiderlimits, limitnum, external, limit_counter):
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

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            if not Spider.external:
                Spider.add_links_to_queue(Spider.gather_links(page_url))
            else:
                Spider.add_links_to_queue_no_check(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            print(page_url + " Has been crawled")

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if Spider.spiderlimits or (Spider.limitnum > Spider.limit_counter):
                if 'text/html' in response.getheader('Content-Type'):
                    html_bytes = response.read()
                    html_string = html_bytes.decode("utf-8")
                finder = LinkFinder(Spider.base_url, page_url)
                finder.feed(html_string)
            else:
                Spider.limit_reached()
            Spider.limit_counter += 1
        except Exception as e:
            print(str(e) + "2")
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        try:
            for url in links:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                if Spider.domain_name != get_domain_name(url):
                    continue
                Spider.queue.add(url)
        except Exception as e:
            print(e)

    # Saves queue data to project files without checking domain
    @staticmethod
    def add_links_to_queue_no_check(links):
        try:
            for url in links:
                if (url in Spider.queue) or (url in Spider.crawled):
                    continue
                Spider.queue.add(url)
        except Exception as e:
            print(str(e) + "1")

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
    
    @staticmethod
    def limit_reached():
        for url in Spider.queue:
            Spider.queue.remove(url)
        return
    
    