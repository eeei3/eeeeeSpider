# pylint: disable=C0116
# pylint: disable=W0105
"""
# /***************************************************************************************
#  This is the main part of this application. This is the code to run to start the program.
#  Here you will find the CLI prompts, configuration choices and start up and end functions.
# ***************************************************************************************\
"""
import os
import sys
from os import system
from tkinter import Tk, Scrollbar, RIGHT, TOP, Y, Text, NONE, X, END
import csv
import zipfile
import json
from main import SpiderMain
from htmlcreator import HTMLCreator


class Main:
    """
    /***************************************************************************************
    Main function of the program. Houses all functions.
    ***************************************************************************************\
    """
    def __init__(self, directory, cdirectory="configs"):
        # The location of the results folder
        self.directory = directory
        # The directory of the configs folder
        self.cdirectory = cdirectory
        # The location of the queue file
        self.queue = os.path.join(directory, "queue.txt")
        # The location of the crawled file
        self.crawled = os.path.join(directory, "crawled.txt")
        # The location of the configs file
        self.settingsdir = os.path.join(cdirectory, "configs.json")
        # The settings the crawler abides by
        self.configs = {
            # The amount of threads allotted to the crawler
            "threads": 8,
            # If the crawler is allowed to crawl external sites
            "outside_sites": False,
            # If the crawler has a limit imposed on the max amount of sites it can crawl
            "max_links": [False, 0],
            # If the crawler should warn the user of large sites
            "warnings": True,
            # If the crawler should compress the results
            "compress": False,
            # If the HTML should be given a class name
            "classnames": "",
            # If the HTML should be in link form or text
            "linkortext": "link",
            # If the HTML should be in header form
            "headers": {
                "headers1": False,
                "headers2": False,
                "headers3": False,
                "headers4": False
            }
        }

        if not os.path.exists(cdirectory):
            # Making sure the configs directory exists
            os.mkdir(cdirectory)
            with open(self.settingsdir, 'x', encoding='utf8') as file:
                file.write(json.dumps(self.configs))
                file.close()

        else:
            # Making sure the configs file is present and attempt to load the data
            try:
                with open(self.settingsdir, 'r', encoding='utf8') as file:
                    self.configs = json.loads(file.read())
            except FileNotFoundError:
                print("""Panic! Configs folder not found!
                         Loading in default values.""")
                with open(self.settingsdir, 'w', encoding='utf8') as file:
                    file.write(self.configs)

        if not os.path.exists(directory):
            # Making sure the results directory exists
            os.mkdir(directory)
            with open(self.queue, 'x', encoding='utf8') as file:
                file.close()
            with open(self.crawled, 'x', encoding='utf8') as file:
                file.close()

        else:
            # Making sure the crawled file is present and now empty
            with open(self.crawled, 'w', encoding='utf8') as file:
                file.write("")
                file.close()
            # Making sure the queue file is present
            try:
                with open(self.queue, 'w', encoding='utf8') as file:
                    file.close()
            except FileExistsError:
                pass
            # Removing superfluous data from previous runs
            try:
                os.remove(directory + "/crawled.csv")
            except os.error:
                pass
            try:
                os.remove(directory + "/results.html")
            except os.error:
                pass

    """
    /***************************************************************************************
    Function that clears the window
    ***************************************************************************************\
    """
    @staticmethod
    def clear_screen():
        try:
            # Command to clear the window
            _ = system('cls')
        except Exception as error:
            pass

    """
    /***************************************************************************************
    Function that creates a gui using Tkinter. Then it creates a scrollbar object
    and the text element that is created gets populated with the links.
    ***************************************************************************************\
    """
    @staticmethod
    def create_viewing_gui(links):
        # Variable that holds the height of the window
        y_height = 0
        # Setting an appropriate height
        for _ in links:
            y_height = y_height + 1
        # Creating root window
        # Object holding the main window
        root = Tk()
        # Creating the scrollbar
        # Object holding the scrollbar
        vertical = Scrollbar(root, orient='vertical')
        vertical.pack(side=RIGHT, fill=Y)
        # Object holding the text widget
        text = Text(root, width=15, height=y_height, wrap=NONE,
                    yscrollcommand=vertical.set)

        text.pack(side=TOP, fill=X)

        vertical.config(command=text.yview)
        # Populating text widget
        # links is the variable passed to the function
        for link in links:
            text.insert(END, link + "\n")

        root.minsize(500, y_height)
        root.title("Link Viewer")
        root.mainloop()

    """
    /***************************************************************************************
    Function that gives the user options at the end of the program
    ***************************************************************************************\
    """
    def finish(self):
        """
        /***************************************************************************************
        Function that exports the file into a CSV file for spreadsheet work
        ***************************************************************************************\
        """
        def export_to_csv():
            with open(self.directory + '/crawled.csv', 'x',
                      newline='', encoding='utf8') as csvfile:
                with open(self.directory + "/crawled.txt", "r", encoding='utf8') as result_file:
                    # String containing each url
                    craweld_url_list = result_file.read()
                    # List containing each url
                    craweld_url_list = craweld_url_list.split("\n")
                    # Object holding the csv.writer function
                    csvwriter = csv.writer(csvfile, delimiter=' ',
                                           quotechar='|',
                                           quoting=csv.QUOTE_MINIMAL)
                    for url in craweld_url_list:
                        csvwriter.writerow(url)
            return 0

        """
        /***************************************************************************************
        Function that exports the file into a HTML file for website use
        ***************************************************************************************\
        """
        def export_to_html(url_list):
            # The object holding the HTMLCreator module
            html_obj = HTMLCreator(url_list,
                                   self.directory + "/results.html",
                                   self.configs["linkortext"],
                                   self.configs["classnames"])
            html_obj.html_generator(self.configs["headers"],
                                    self.configs["classnames"])
            return 0

        # Checking if the user wanted to compress their file or not
        # and then using the deflated algorithm to compress it
        if self.configs["compress"]:
            # The object holding the zipfile.ZipFile function
            compressedfile = zipfile.ZipFile(self.directory +
                                             '/crawled.zip', 'w',
                                             zipfile.ZIP_DEFLATED)
            compressedfile.write(self.directory + '/crawled.txt')
            compressedfile.close()

        main.clear_screen()

        print("""
/***************************************************************************
Crawler has finished!
***************************************************************************\
        """)
        print("""You can either view the URL's in the CLI,
              export the file to a CSV format""")
        print("or exit the program right now")
        print("V to view, E to export and Q to quit")
        # The user's choice of action
        choice = input("")
        choice = choice.lower()
        # The user wishes to view the links in a GUI
        if choice == "v":
            print("viewing")
            with open(self.directory + "/crawled.txt", "r", encoding='utf8') as file:
                # String holding the URLs
                url_list = file.read()
                # List holding the URLs
                url_list = url_list.split("\n")
            Main.create_viewing_gui(url_list)
        # The user wishes to export the results in a format of their choice
        elif choice == "e":
            with open(self.directory + "/crawled.txt", "r", encoding='utf8') as file:
                url_list = file.read()
                url_list = url_list.split("\n")
            print("Export to CSV or to HTML?")
            print("Exports are wiped on start of program! Remember to backup!")
            # The user's choice of action
            choice = input("")
            # The user is exporting to csv
            if choice.lower() == "csv":
                export_to_csv()
            # The user is exporting to html
            elif choice.lower() == "html":
                export_to_html(url_list)
        # The user wishes to do nothing with the results
        elif choice == "q":
            return
        # The user gave bad input
        else:
            print("Invalid answer")
            main.finish()

    """
    /***************************************************************************************
    Function that calls the crawler
    ***************************************************************************************\
    """
    def start(self):
        # The URL that the user wants to crawl
        url = input("Url to crawl:\n")
        # Passing data to the Spider module
        # The object holding the SpiderMain class
        spidermain = SpiderMain(
            self.directory, url,
            self.configs["threads"],
            self.configs["outside_sites"],
            self.configs["max_links"][0],
            self.configs["max_links"][1], 0,
            self.configs["warnings"])
        # Starting the crawler
        spidermain.kick_start()

    """
    /***************************************************************************************
    Main function (Gets user input)
    ***************************************************************************************\
    """
    def main(self):
        # Getting user input
        print("Please input your choice.\nChoices\n-------------------")
        print("1.Start crawling\n2.Change Settings\n3.Exit\n")
        # The user's choice of action
        choice = input("")
        choice = choice.lower()
        # User chose to start crawling
        if choice in "start1":
            self.start()
            self.finish()
        # User chose to configure the crawler
        elif choice in "settings2":
            self.settings()
        # User chose to quit
        elif choice in "exit3":
            sys.exit()
        else:
            print("Bad choice. Restarting")
            self.clear_screen()
            self.main()
    """
    /***************************************************************************************
    Function that gives the user options to change the program settings
    ***************************************************************************************\
    """
    def settings(self):
        main.clear_screen()
        print("Which element do you want to change?\n1.Threads")
        print("2.Crawl outside sides\n3.Max amount to crawl")
        print("4.HTML configs\n5.Storage Warnings\n6.Compression")
        print("7.Regenerate config file\n8.Nothing and return")
        # The setting the user wishes to change
        setting_to_change = input("Type in the number\n")
        # Changing number of threads used
        if setting_to_change == "1":
            print("How many threads do you want?")
            print("Current amount of threads: " + str(self.configs["threads"]))
            try:
                # The amound of threads allocated for the crawler
                self.configs["threads"] = int(input(""))
            except ValueError:
                print("Bad value detected!")
                self.settings()
        # Changing if the user wants to crawl outside sites
        elif setting_to_change == "2":
            print("Do you want the spider to crawl external sites?")
            print("Enter 'yes' or 'no'")
            # Does the user want external sites crawled?
            temp = input("")
            temp = temp.lower()
            if temp == "yes":
                # Whether the crawler will crawl external sites
                self.configs["outside_sites"] = True
            elif temp == "no":
                self.configs["outside_sites"] = False
            else:
                print("Bad input. Skipping")
                self.settings()
        # Changing if the user wants a max amount of pages crawled
        elif setting_to_change == "3":
            print("Do you want a limit to the amount of pages crawled?")
            print("Enter 'yes' or 'no'\n")
            # Does the user want a limit on sites crawled?
            temp = input("")
            temp = temp.lower()
            if temp == "yes":
                # The users choice on a limit
                self.configs["max_links"][0] = True
                print("What do you want the limit to be?\n")
                # What should the limit be?
                temp = int(input(""))
                # The limit the user defined
                self.configs["max_links"][1] = temp
            elif temp == "no":
                self.configs["max_links"][0] = False
            else:
                print("Bad input. Skipping")
                self.settings()
        # User wishes to change HTML settings
        elif setting_to_change == "4":
            print("What config do you want to change?")
            # The config the user wants to change
            temp = input("1. Headers\n2. Link or text\n3. Give text a class?\n")
            # Changing the headers
            if temp == "1":
                print("Current configs:\n",
                      "h1 ", self.configs["headers"]["headers1"], "\n",
                      "h2 ", self.configs["headers"]["headers2"], "\n",
                      "h3 ", self.configs["headers"]["headers3"], "\n",
                      "h4 ", self.configs["headers"]["headers4"], "\n")
                # Which header option does the user want to change?
                temp1 = input("""Which header do you want to change?
                              1    2    3   4\n""")
                if temp1 == "1":
                    # The state of the first header
                    self.configs["headers"]["headers1"] = \
                        bool((~self.configs["headers"]["headers1"]) + 2)
                    print("Config changed")
                    self.settings()
                elif temp1 == "2":
                    # The state of the second header
                    self.configs["headers"]["headers2"] = \
                        bool((~self.configs["headers"]["headers2"]) + 2)
                    print("Config changed")
                    self.settings()
                elif temp1 == "3":
                    # The state of the third header
                    self.configs["headers"]["headers3"] = \
                        bool((~self.configs["headers"]["headers3"]) + 2)
                    print("Config changed")
                    self.settings()
                elif temp1 == "4":
                    # The state of the fourth header
                    self.configs["headers"]["headers4"] = \
                        bool((~self.configs["headers"]["headers4"]) + 2)
                    print("Config changed")
                    self.settings()
                else:
                    print("I did not understand that.")
                    self.settings()
            # Choosing IF the user wants the urls to be
            # entered in as links or as plain text
            elif temp == "2":
                print("""Enter 'link' or 'text'.
                      Enter e to not change anything.""")
                print("Current config: ", self.configs["linkortext"])
                # Does the user want links or text?
                temp1 = input()
                if temp1.lower() == "e":
                    print("No changes made")
                elif temp1.lower() == "link":
                    # The user's choice of either link or text
                    self.configs["linkortext"] = "link"
                elif temp1.lower() == "text":
                    self.configs["linkortext"] = "text"
                else:
                    print("Bad input.")
                    self.settings()
            # Changing class name for HTML file
            elif temp == "3":
                print("Current class name: ", self.configs["classnames"])
                # The classname
                self.configs["classnames"] = \
                    input("Enter your desired class name." +
                          "Leave blank if you don't want any\n")
            else:
                print("I did not understand that.")
                self.settings()
        # User wants storage warnings
        elif setting_to_change == "5":
            print("Would you like to receive warnings if the " +
                  "site you are crawling is very large?")
            print("Current configs: ", self.configs["warnings"])
            # Does the user want warnings?
            temp1 = input("Please input either yes or no\n")
            if temp1.lower() == "yes":
                # The state of warnings
                self.configs["warnings"] = True
                print("Setting changed")
            elif temp1.lower() == "no":
                self.configs["warnings"] = False
                print("Setting changed")
            else:
                print("I did not understand that.")
                self.settings()
        # If the user wants to change their compression settings
        elif setting_to_change == "6":
            print("Do you want to compress the results file upon completion?")
            print("Current config: ", self.configs["compress"])
            # Does the user want compression?
            temp1 = input("Enter either yes or no\n")
            if temp1.lower() == "yes":
                # The state of compression
                self.configs["compress"] = True
            elif temp1.lower() == "no":
                self.configs["compress"] = False
            else:
                print("Bad input. Skipping.")
                self.settings()
        # If the user wishes to regenerate a broken configs file
        elif setting_to_change == "7":
            print("ARE YOU SURE YOU WANT TO REGENERATE YOUR CONFIG FILE?")
            print("THIS WILL WIPE ALL EXISTING SETTINGS!")
            print("Please enter 'Confirm' exactly to confirm regeneration")
            # Does the user wish to proceed?
            temp1 = input("")
            if temp1 == "Confirm":
                # Vanilla configs
                self.configs = {
                    "threads": 8,
                    "outside_sites": False,
                    "max_links": [False, 99],
                    "warnings": True,
                    "compress": False,
                    "classnames": "",
                    "linkortext": "link",
                    "headers": {
                        "headers1": False,
                        "headers2": False,
                        "headers3": False,
                        "headers4": False
                    }
                }
            else:
                print("Bad input. Skipping.")
                self.settings()
        elif setting_to_change == "8":
            print("Changing nothing.")
        # If the user gives bad input
        else:
            main.clear_screen()
            print("I didn't understand that")
            self.settings()
        # Writing changes to the file
        with open(self.settingsdir, 'w', encoding='utf8') as file:
            file.write(json.dumps(self.configs))
            file.close()
        main.clear_screen()
        self.main()


# Starting the application
# Object that holds the Main class
main = Main("results")
main.main()
