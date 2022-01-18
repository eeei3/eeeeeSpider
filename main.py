#! /usr/local/bin/python3

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
        self.folder_name = folder_name
        self.base_link = base_link
        self.domain_name = get_domain_name(base_link)
        self.threads = threads
        self.external = external
        self.max = urlmax
        self.maxnum = maxnum - 1
        self.queue_file = folder_name + '/queue.txt'
        self.crawled_file = folder_name + '/crawled.txt'
        self.queue = Queue()
        self.limit_count = limit_count
        self.warnings = warnings
        self.warning_trigger = 99
        Spider(folder_name, base_link, self.domain_name,
               urlmax, maxnum, external, 0)

    # Function in charge of creating threads for the spider
    def create_threads(self):
        try:
            for _ in range(self.threads):
                self.thread = threading.Thread(target=self.work)
                self.thread.daemon = True
                self.thread.start()
        except RuntimeError:
            sys.exit()

    # Gives the threads jobs (URLs)
    def work(self):
        while True:
            try:
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
        temp = input("Please enter either 'continue' or 'stop'.\n")
        if temp.lower() == "stop":
            print("Crawling exiting...")
            return 1
        elif temp.lower() == "continue":
            print("Resuming...")
            return 0
        else:
            print("Bad input")
            SpiderMain.warning_activated()

    # Add links to queue and prepare them for crawling
    def create_jobs(self):
        stop_signal = False
        for link in file_to_set(self.queue_file):
            # Checking if the crawler has hit the user defined limit
            if (self.warning_trigger == self.limit_count) and self.warnings:
                print("THE CRAWLER HAS CRAWLED 100 URLs." +
                      " ARE YOU SURE YOU WISH TO CONTINUE?")
                print("CONTINUEING WILL LEAD TO LARGER FILE SIZES." +
                      " IF YOU HAVE external SITES ENABLED,")
                print("CONSIDER TURNING ON COMPRESSING.")
                if SpiderMain.warning_activated() == 1:
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
