# pylint: disable=C0116
"""
# /***************************************************************************************
#  This module is responsible for performing many of the crawler functions.
# ***************************************************************************************\
"""
import sys
from urllib.request import urlopen, Request
from link_finder import LinkFinder
from domain import get_domain_name
from general import file_to_set, set_to_file


class Spider:

    # The queue set
    queue = set()

    # The crawled set
    crawled = set()

    # Does the user want sites unaffiliated with the original domain
    # to be crawled?
    external = False

    def __init__(self, project_name, base_url, domain_name, external):

        # The name of the directory
        Spider.project_name = project_name

        # The URL that the user provided
        Spider.base_url = base_url

        # The domain of the URL that the user provided
        Spider.domain_name = domain_name

        # Does the user want sites unaffiliated with the original domain
        # to be crawled?
        Spider.external = external

        # Variable holding the location of the queue file
        Spider.queue_file = Spider.project_name + '/queue.txt'

        # Variable holding the location of the crawled file
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():

        # Creates directory and files for project on first run
        # and starts the spider
        # Object that holds the queue
        Spider.queue = file_to_set(Spider.queue_file)

        # Object that holds the crawled
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
            # If the user does not want external sites

            if not Spider.external:

                # Varible that holds the links gathered
                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue(links)

            # If the user wants external sites
            else:

                # Variable that holds the links gathered
                links = Spider.gather_links(page_url)
                Spider.add_links_to_queue_no_check(links)

            # Removing link from queue, adding it to crawled
            # and updating the files
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):

        # Converts raw response data into readable information
        # and checks for proper html formatting
        # Object that contains the HTML in plaintext
        html_string = ''

        try:

            # Giving urllib a user agent to avoid getting Error code 403
            # Object that holds the Request object
            url = Request(page_url, headers={"User-Agent": "Mozilla/5.0"})

            # Object that contains the website response
            response = urlopen(url)

            if 'text/html' in response.getheader('Content-Type'):
                # Object that contains the HTML bytes
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")

            # Object that holds the LinkFinder module
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

        except Exception as error:

            if "403" in str(error):

                print("HTTP Error 403: Forbidden")
                print("Make sure you have permission to crawl this site.")

            elif "404" in str(error):

                pass

            else:

                print(str(error), " gather links")

            return set()

        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):

        # Saves queue data to project files
        try:

            # links here represents the list of links passed to the function
            # Adding links that, have not been parsed already and match the
            # original domain, to queue
            for url in links:

                if (url in Spider.queue) or (url in Spider.crawled):

                    continue

                if Spider.domain_name != get_domain_name(url):

                    continue

                Spider.queue.add(url)

        except Exception as error:

            print(str(error), "add links")
            print("The program has met a fatal error!")
            temp = input("Press enter to exit the program")

            sys.exit()

    @staticmethod
    def add_links_to_queue_no_check(links):

        # Saves queue data to project files without checking domain
        try:

            # links here represents the lsit of links passed to the function
            # Adding links that, have not already been parsed, to queue
            for url in links:

                if (url in Spider.queue) or (url in Spider.crawled):

                    continue

                Spider.queue.add(url)

        except Exception as error:

            print(str(error), "add links")
            print("The program has met a fatal error!")
            temp = input("Press enter to exit the program")

            sys.exit()

    @staticmethod
    def update_files():

        # Moving data from memory to drive
        try:

            set_to_file(Spider.queue, Spider.queue_file)
            set_to_file(Spider.crawled, Spider.crawled_file)

        except FileNotFoundError:

            print("The program has met a fatal error!")
            print("Either queue or crawled, or both, files are missing!")
            temp = input("Press enter to exit the program")

            sys.exit()

        except OSError:

            print("The program has met a fatal error!")
            print("Program unable to manipulate files!")
            temp = input("Press enter to exit the program")

            sys.exit()
