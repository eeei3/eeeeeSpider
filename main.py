import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


class SpiderMain:
    # For counting how many pages have been crawled
    limit_count = 0

    def __init__(self, folder_name, base_link, threads, external, urlmax, maxnum, limit_count, warnings):
        self.FOLDER_NAME = folder_name
        self.BASE_LINK = base_link
        self.DOMAIN_NAME = get_domain_name(base_link)
        self.THREADS = threads
        self.EXTERNAL = external
        self.MAX = urlmax
        self.MAXNUM = maxnum - 1
        self.QUEUE_FILE = folder_name + '/queue.txt'
        self.CRAWLED_FILE = folder_name + '/crawled.txt'
        self.queue = Queue()
        self.limit_count = limit_count
        self.WARNINGS = warnings
        self.WARNING_TRIGGER = 99
        Spider(folder_name, base_link, self.DOMAIN_NAME, urlmax, maxnum, external, 0)

    # Function in charge of creating threads for the spider
    def create_threads(self):
        try:
            for _ in range(self.THREADS):
                self.t = threading.Thread(target=self.work)
                self.t.daemon = True
                self.t.start()
        except Exception as e:
            print(e)
            
    # Gives the threads jobs (URLs)
    def work(self):
        while True:
            try:
                url = self.queue.get()
                Spider.crawl_page(threading.current_thread().name, url)
                self.queue.task_done()
                self.limit_count += 1
            except Exception as e:
                print(e)
                
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
            SpiderMain.warning_activated()

    # Add links to queue and prepare them for crawling
    def create_jobs(self):
        stop_signal = False
        print("Creating Jobs")
        for link in file_to_set(self.QUEUE_FILE):
            # Checking if the crawler has hit the user defined limit
            if (self.WARNING_TRIGGER == self.limit_count) and (self.WARNINGS == True):
                print("THE CRAWLER HAS CRAWLED 100 URLs. ARE YOU SURE YOU WISH TO CONTINUE?")
                print("CONTINUEING WILL LEAD TO LARGER FILE SIZES. IF YOU HAVE EXTERNAL SITES ENABLED,")
                print("CONSIDER TURNING ON COMPRESSING.")
                if SpiderMain.warning_activated() == 1:
                    stop_signal = True
                else:
                    pass
            if ((self.limit_count != self.MAXNUM) or (self.MAX == False)) and (stop_signal == False):
                self.queue.put(link)
                self.queue.join()
                self.crawl()
            else:
                pass

    # Function that gets queued links and calls create_jobs to prepare them
    def crawl(self):
        queued_links = file_to_set(self.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + " links in the queue")
            self.create_jobs()

    # Function to start crawler
    def kick_start(self):
        self.create_threads()
        self.crawl()