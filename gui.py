import os
from os import system
import json
from main import SpiderMain
from crawlergui import CrawlerGUI


class Main:

    def __init__(self, directory):
        self.directory = directory
        self.queue = os.path.join(directory, "queue.txt")
        self.crawled = os.path.join(directory, "crawled.txt")
        self.settingsdir = os.path.join(directory, "configs.json")
        self.configs = {
            "threads" : 8,
            "outside_sites" : False,
            "max_links" : [False, 0]
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
            with open('crawled.csv', 'x', newline='') as csvfile:
                with open("crawled.txt", "r") as file:
                    url_list = file.read()
                    url_list = url_list.split("\n")
                    csvwriter = csv.writer(csvfile, delimiter=' ', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
                    for url in url_list:
                        csvwriter.writerow(url)
            return
        main.clear_screen()
        print("The crawler has finished")
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
            export_to_csv()
        elif choice == "Q" or choice == "quit" or choice == "q":
            return
        else:
            print("Invalid answer")

    # /***************************************************************************************
    #  Function that calls the crawler
    # ***************************************************************************************\
    def start(self):
        url = input("Url to crawl:")
        spidermain = SpiderMain(
            self.directory, url,
            self.configs["threads"],
            self.configs["outside_sites"],
            self.configs["max_links"][0],
            self.configs["max_links"][1], 0)
        spidermain.kick_start()

    # /***************************************************************************************
    #  Main function (Gets user input)
    # ***************************************************************************************\
    def main(self):
        print("Please input your choice.\nChoices\n-------------------\n1.Start crawling\n2.Change Settings\n3.Exit")
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
        else:
            pass
    # /***************************************************************************************
    #  Function that gives the user options to change the program settings
    # ***************************************************************************************\
    def settings(self):
        main.clear_screen()
        print("Which element do you want to change?\n1.Threads\n2.Crawl outside sides\n3.Max amount to crawl")
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


main = Main("results")
main.main()
