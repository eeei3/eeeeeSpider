# pylint: disable=C0116
"""
# /***************************************************************************************
#  This module is the crawler. Most functions though are located on spider.py
# ***************************************************************************************\
"""
import threading
import sys
from queue import Queue
from spider import Spider
from domain import get_domain_name
from general import file_to_set


class SpiderMain:
    # For counting how many pages have been crawled
    limit_count = 0

    def __init__(self, folder_name, base_link, threads, external,
                 urlmax, maxnum, limit_count, warnings):
        # The cwd of the project
        self.folder_name = folder_name
        # The base link the user provided
        self.base_link = base_link
        # The domain of the base link
        self.domain_name = get_domain_name(base_link)
        # The amount of threads allocated
        self.threads = threads
        # Whether the crawler should crawl external sites or not
        self.external = external
        # Whether the crawler has a max or not
        self.max = urlmax
        # The max (Does not apply if disabled)
        self.maxnum = maxnum - 1
        # The location of the queue file
        self.queue_file = folder_name + '/queue.txt'
        # The location of the crawled file
        self.crawled_file = folder_name + '/crawled.txt'
        # The queue
        self.queue = Queue()
        # The limit counter
        self.limit_count = limit_count
        # Whether the user wants warnings about storage size
        self.warnings = warnings
        # The amount that will trigger the warning
        self.warning_trigger = 99
        Spider(folder_name, base_link, self.domain_name
               , external)

    # Function in charge of creating threads for the spider
    def create_threads(self):
        try:
            for _ in range(self.threads):
                # The thread object
                self.thread = threading.Thread(target=self.work)
                # Setting the thread object as a daemon
                self.thread.daemon = True
                self.thread.start()
        except RuntimeError:
            sys.exit()

    # Gives the threads jobs (URLs)
    def work(self):
        while True:
            try:
                # An url fetched from the queue
                url = self.queue.get()
                Spider.crawl_page(threading.current_thread().name, url)
                self.queue.task_done()
                self.limit_count += 1
            except Exception as error:
                print(error)
                sys.exit()

    # Warns the user
    @staticmethod
    def warning_activated():
        # The user's choice of what to do
        temp = input("Please enter either 'continue' or 'stop'.\n")
        if temp.lower() == "stop":
            print("Crawling exiting...")
            return 1
        elif temp.lower() == "continue":
            print("Resuming...")
            return 0
        else:
            print("Bad input. Stopping...")
            return 1

    # Add links to queue and prepare them for crawling
    def create_jobs(self):
        # The program's kill switch
        stop_signal = False
        for link in file_to_set(self.queue_file):
            # Checking if the crawler has hit the user defined limit
            if (self.warning_trigger == self.limit_count) and self.warnings:
                print("THE CRAWLER HAS CRAWLED 100 URLs." +
                      " ARE YOU SURE YOU WISH TO CONTINUE?")
                print("CONTINUING WILL LEAD TO LARGER FILE SIZES." +
                      " IF YOU HAVE external SITES ENABLED,")
                print("CONSIDER TURNING ON COMPRESSING.")
                temp = input("Please make your choice now. Y/N?\n")
                if (SpiderMain.warning_activated() == 1) and (temp.lower() == "y"):
                    stop_signal = True
                else:
                    pass
            if ((self.limit_count != self.maxnum) or (not self.max)):
                if not stop_signal:
                    self.queue.put(link)
                    self.queue.join()
                    self.crawl()
            else:
                pass

    # Function that gets queued links and calls create_jobs to prepare them
    def crawl(self):
        queued_links = file_to_set(self.queue_file)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + " links in the queue")
            self.create_jobs()

    # Function to start crawler
    def kick_start(self):
        self.create_threads()
        self.crawl()
