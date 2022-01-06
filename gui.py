import os
from os import system
import json
from main import SpiderMain
from crawlergui import CrawlerGUI
from htmlcreator import HTMLCreator


class Main:

    def __init__(self, directory):
        self.directory = directory
        self.queue = os.path.join(directory, "queue.txt")
        self.crawled = os.path.join(directory, "crawled.txt")
        self.settingsdir = os.path.join(directory, "configs.json")
        self.configs = {
            "threads": 8,
            "outside_sites": False,
            "max_links": [False, 0],
            "warnings": True,
            "compress": False,
            "classnames": "",
            "linkortext": "link",
            "headers": {
                "headers" : False,
                "headers1": False,
                "headers2" : False,
                "headers3": False,
                "headers4": False
            }
        }
        if not os.path.exists(directory):
            os.mkdir(directory)
            with open(self.queue, 'x') as f:
                f.close()
            with open(self.crawled, 'x') as f:
                f.close()
            with open(self.settingsdir, 'x') as f:
                f.write(json.dumps(self.configs))
                f.close()
        else:
            with open(self.crawled, 'w') as f:
                f.write("")
                f.close()
            with open(self.settingsdir, 'r') as f:
                self.configs = json.loads(f.read())
            try:
                os.remove(directory + "/crawled.csv")
            except Exception as e:
                pass
            try:
                os.remove(directory + "/results.html")
            except Exception as e:
                print(e)

    # /***************************************************************************************
    #  Function that clears the window
    # ***************************************************************************************\
    @staticmethod
    def clear_screen():
        _ = system('cls')
        
    # /***************************************************************************************
    #  Function that gives the user options at the end of the program
    # ***************************************************************************************\
    def finish(self):
    
        # /***************************************************************************************
        #  Function that exports the file into a CSV file for spreadsheet work
        # ***************************************************************************************\
        def export_to_csv():
            import csv
            with open(self.directory + '/crawled.csv', 'x', newline='') as csvfile:
                with open(self.directory + "/crawled.txt", "r") as file:
                    url_list = file.read()
                    url_list = url_list.split("\n")
                    csvwriter = csv.writer(csvfile, delimiter=' ', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
                    for url in url_list:
                        csvwriter.writerow(url)
            return
        
        # /***************************************************************************************
        #  Function that exports the file into a HTML file for website use
        # ***************************************************************************************\
        def export_to_html(url_list):
            HTML = HTMLCreator(url_list, self.directory + "/results.html",
                               self.configs["linkortext"], self.configs["classnames"])
            # self, headers, classname, linkortext
            print(self.configs["headers"])
            HTML.html_generator(self.configs["headers"], self.configs["classnames"])
            return 0
            
        main.clear_screen()
        print("""
/***************************************************************************
Crawler has finished!
***************************************************************************\\
    """)
        print("You can either view the URL's in the CLI, export the file to a CSV format")
        print("or exit the program right now")
        print("V to view, E to export and Q to quit")
        choice = input("")
        if choice == "V" or choice == "view" or choice == "v":
            with open(self.directory + "/crawled.txt", "r") as file:
                url_list = file.read()
                url_list = url_list.split("\n")
            viewer = CrawlerGUI()
            viewer.main(url_list)
        elif choice == "E" or choice == "export" or choice == "e":
            with open(self.directory + "/crawled.txt", "r") as file:
                url_list = file.read()
                url_list = url_list.split("\n")
            print("Export to CSV or to HTML?")
            choice = input("")
            if (choice).lower() == "csv":
                export_to_csv()
            elif (choice).lower() == "html":
                export_to_html(url_list)
        elif choice == "Q" or choice == "quit" or choice == "q":
            return
        else:
            print("Invalid answer")

    # /***************************************************************************************
    #  Function that calls the crawler
    # ***************************************************************************************\
    def start(self):
        url = input("Url to crawl:")
        print(self.directory)
        print(self.configs)
        spidermain = SpiderMain(
            self.directory, url,
            self.configs["threads"],
            self.configs["outside_sites"],
            self.configs["max_links"][0],
            self.configs["max_links"][1], 0,
            self.configs["warnings"])
        spidermain.kick_start()

    # /***************************************************************************************
    #  Main function (Gets user input)
    # ***************************************************************************************\
    def main(self):
        print("Please input your choice.\nChoices\n-------------------\n1.Start crawling\n2.Change Settings\n3.Exit\n4.Help")
        choice = input("")
        choice = choice.lower()
        # Starting the crawler
        if choice == "1" or choice == "start":
            self.start()
            self.finish()
        # Changing settings
        elif choice == "2" or choice == "settings":
            self.settings()
        # Exit
        elif choice == "3" or choice == "exit":
            quit()
        
        elif choice == "4" or choice == "help":
            print("Help is on the way!")
        else:
            pass
    # /***************************************************************************************
    #  Function that gives the user options to change the program settings
    # ***************************************************************************************\
    def settings(self):
        main.clear_screen()
        print("Which element do you want to change?\n1.Threads\n2.Crawl outside sides\n3.Max amount to crawl")
        print("\n4.HTML configs\n5.Storage Warnings\n6.Compression")
        setting_to_change = input("Type in the number\n")
        # Changing number of threads used
        if setting_to_change == "1":
            print("How many threads do you want?")
            print("Current amount of threads: " + str(self.configs["threads"]) + "\n")
            self.configs["threads"] = int(input(""))
        # Changing if the user wants to crawl outside sites
        elif setting_to_change == "2":
            print("Do you want the spider to crawl external sides?")
            print("Enter 'yes' or 'no'\n")
            temp = input()
            temp = temp.lower()
            if temp == "yes":
                self.configs["outside_sites"] = True
            elif temp == "no":
                self.configs["outside_sites"] = False
        # Changing if the user wants a max amount of pages crawled
        elif setting_to_change == "3":
            print("Do you want a limit to the amount of pages crawled?")
            print("Enter 'yes' or 'no'\n")
            temp = input()
            temp = temp.lower()
            if temp == "yes":
                self.configs["max_links"][0] = True
                print("What do you want the limit to be?\n")
                temp = int(input())
                self.configs["max_links"][1] = temp
            elif temp == "no":
                self.configs["max_links"][0] = False
        # User wishes to change HTML settings
        elif setting_to_change == "4":
            print("What config do you want to change?")
            temp = input("\n1. Headers\n2.Link or text\n3.Give text a class?\n")
            # Changing the headers
            if temp == "1":
                temp1 = input("Which header do you want to change?\n1\t2\t3\t4\n")
                if temp1 == "1":
                    self.configs["headers"]["headers1"] = bool((~self.configs["headers"]["headers1"]) + 2)
                    print("Config changed")
                elif temp1 == "2":
                    self.configs["headers"]["headers2"] = bool((~self.configs["headers"]["headers2"]) + 2)
                    print("Config changed")
                elif temp1 == "3":
                    self.configs["headers"]["headers3"] = bool((~self.configs["headers"]["headers3"]) + 2)
                    print("Config changed")
                elif temp1 == "4":
                    self.configs["headers"]["headers4"] = bool((~self.configs["headers"]["headers4"]) + 2)
                    print("Config changed")
                else:
                    print("I did not understand that.")
            # Choosing IF the user wants the urls to be entered in as links or as plain text
            elif temp == "2":
                print("Enter 'link' or 'text'. Enter e to not change anything. Current config:", self.configs["linkortext"])
                temp1 = input()
                if temp1.lower() == "e":
                    print("No changes made")
                elif temp1.lower() == "link":
                    self.configs["linkortext"] = "link"
                elif temp1.lower() == "text":
                    self.configs["linkortext"] = "text"
                else:
                    print("Bad input.")
            # Changing class name for HTML file
            elif temp == "3":
                self.configs["classnames"] = input("Enter your desired class name. Leave blank if you don't want any")
            else:
                print("I did not understand that.")
        # User wants storage warnings
        elif setting_to_change == "5":
            print("Would you like to receive warnings if the site you are crawling is very large?")
            temp1 = input("Please input either yes or no")
            if temp1.lower() == "yes":
                self.configs["warnings"] = True
                print("Setting changed")
            elif temp1.lower() == "no":
                self.configs["warnings"] = False
                print("Setting changed")
            else:
                print("I did not understand that.")
        # If the user gives bad input
        else:
            main.clear_screen()
            print("I didn't understand that")
            self.settings()
        # Writing changes to the file
        with open(self.settingsdir, 'w') as f:
            f.write(json.dumps(self.configs))
            f.close()
        main.clear_screen()
        self.main()

# Starting the application
main = Main("results")
main.main()
