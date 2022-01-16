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
    # /***************************************************************************************
    #  Main function of the program. Houses all functions.
    # ***************************************************************************************\
    """
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
                "headers1": False,
                "headers2": False,
                "headers3": False,
                "headers4": False
            }
        }
        if not os.path.exists(directory):
            os.mkdir(directory)
            with open(self.queue, 'x', encoding='utf8') as file:
                file.close()
            with open(self.crawled, 'x', encoding='utf8') as file:
                file.close()
            with open(self.settingsdir, 'x', encoding='utf8') as file:
                file.write(json.dumps(self.configs))
                file.close()
        else:
            # Making sure the crawled file is present and now empty
            with open(self.crawled, 'w', encoding='utf8') as file:
                file.write("")
                file.close()
            # Making sure the queue file is present
            try:
                with open(self.queue, 'x', encoding='utf8') as file:
                    file.close()
            except FileExistsError:
                pass
            # Making sure the configs file is present
            try:
                with open(self.settingsdir, 'r', encoding='utf8') as file:
                    self.configs = json.loads(file.read())
            except FileNotFoundError:
                print("""Panic! Configs folder not found!
                         Loading in default values.""")
                with open(self.settingsdir, 'w', encoding='utf8') as file:
                    file.write(self.configs)
            # Removing superfluous data
            try:
                os.remove(directory + "/crawled.csv")
            except os.error:
                pass
            try:
                os.remove(directory + "/results.html")
            except os.error:
                pass

    # /***************************************************************************************
    #  Function that clears the window
    # ***************************************************************************************\
    @staticmethod
    def clear_screen():
        if sys.platform == "linux":
            _ = system('clear')
        elif sys.platform == "win32":
            _ = system('cls')
        else:
            print("Unsupported platform!")

    """
    /***************************************************************************************
    Function that creates a gui using Tkinter. Then it creates a scrollbar object
    and the text element that is created gets populated with the links.
    ***************************************************************************************\
    """
    @staticmethod
    def create_viewing_gui(links):
        y_height = 0
        # Setting a appropriate height
        for link in links:
            y_height = y_height + 1
        # Creating root window
        root = Tk()
        # Creating the scrollbar
        vertical = Scrollbar(root, orient='vertical')
        vertical.pack(side=RIGHT, fill=Y)

        text = Text(root, width=15, height=y_height, wrap=NONE,
                    yscrollcommand=vertical.set)

        text.pack(side=TOP, fill=X)

        vertical.config(command=text.yview)
        # Populating text widget
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
                with open(self.directory + "/crawled.txt", "r") as result_file:
                    craweld_url_list = result_file.read()
                    craweld_url_list = craweld_url_list.split("\n")
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
            html_obj = HTMLCreator(url_list, self.directory + "/results.html",
                               self.configs["linkortext"],
                               self.configs["classnames"])
            html_obj.html_generator(self.configs["headers"],
                                self.configs["classnames"])
            return 0
        # Checking if the user wanted to compress their file or not
        # and then using the deflated algorithm to compress it
        if self.configs["compress"]:
            compressedfile = zipfile.ZipFile(self.directory +
                                             '/crawled.zip', 'w',
                                             zipfile.ZIP_DEFLATED)
            compressedfile.write(self.directory + '/crawled.txt')
            compressedfile.close()

        main.clear_screen()
        print("""
/***************************************************************************
Crawler has finished!
***************************************************************************\\
    """)
        print("""You can either view the URL's in the CLI,
              export the file to a CSV format""")
        print("or exit the program right now")
        print("V to view, E to export and Q to quit")
        choice = input("")
        if choice == "V" or choice == "view" or choice == "v":
            with open(self.directory + "/crawled.txt", "r", encoding='utf8') as file:
                url_list = file.read()
                url_list = url_list.split("\n")
            Main.create_viewing_gui(url_list)

        elif choice == "E" or choice == "export" or choice == "e":
            with open(self.directory + "/crawled.txt", "r", encoding='utf8') as file:
                url_list = file.read()
                url_list = url_list.split("\n")
                
            print("Export to CSV or to HTML?")
            print("Exports are wiped on start of program! Remember to backup!")
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
        url = input("Url to crawl:\n")
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
        print("Please input your choice.\nChoices\n-------------------")
        print("1.Start crawling\n2.Change Settings\n3.Exit\n4.Help")
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
            sys.exit()

        elif choice == "4" or choice == "help":
            print("Help is on the way!")
        else:
            pass

    # /***************************************************************************************
    #  Function that gives the user options to change the program settings
    # ***************************************************************************************\
    def settings(self):
        main.clear_screen()
        print("Which element do you want to change?\n1.Threads")
        print("2.Crawl outside sides\n3.Max amount to crawl")
        print("\n4.HTML configs\n5.Storage Warnings\n6.Compression")
        print("7.Regenerate config file\n8.Nothing and return")
        setting_to_change = input("Type in the number\n")
        # Changing number of threads used
        if setting_to_change == "1":
            print("How many threads do you want?")
            print("Current amount of threads: " + str(self.configs["threads"]))
            try:
                self.configs["threads"] = int(input(""))
            except ValueError:
                print("Bad value detected!")
                self.settings()
        # Changing if the user wants to crawl outside sites
        elif setting_to_change == "2":
            print("Do you want the spider to crawl external sides?")
            print("Enter 'yes' or 'no'")
            temp = input("")
            temp = temp.lower()
            if temp == "yes":
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
            temp = input("")
            temp = temp.lower()
            if temp == "yes":
                self.configs["max_links"][0] = True
                print("What do you want the limit to be?\n")
                temp = int(input(""))
                self.configs["max_links"][1] = temp
            elif temp == "no":
                self.configs["max_links"][0] = False
            else:
                print("Bad input. Skipping")
                self.settings()
        # User wishes to change HTML settings
        elif setting_to_change == "4":
            print("What config do you want to change?")
            temp = input("1. Headers\n2. Link or text\n3. Give text a class?\n")
            # Changing the headers
            if temp == "1":
                print("Current configs:\n",
                      "h1 ", self.configs["headers"]["headers1"], "\n",
                      "h2 ", self.configs["headers"]["headers2"], "\n",
                      "h3 ", self.configs["headers"]["headers3"], "\n",
                      "h4 ", self.configs["headers"]["headers4"], "\n")
                temp1 = input("""Which header do you want to change?
                              1    2    3   4\n""")
                if temp1 == "1":
                    self.configs["headers"]["headers1"] = \
                        bool((~self.configs["headers"]["headers1"]) + 2)
                    print("Config changed")
                elif temp1 == "2":
                    self.configs["headers"]["headers2"] = \
                        bool((~self.configs["headers"]["headers2"]) + 2)
                    print("Config changed")
                elif temp1 == "3":
                    self.configs["headers"]["headers3"] = \
                        bool((~self.configs["headers"]["headers3"]) + 2)
                    print("Config changed")
                elif temp1 == "4":
                    self.configs["headers"]["headers4"] = \
                        bool((~self.configs["headers"]["headers4"]) + 2)
                    print("Config changed")
                else:
                    print("I did not understand that.")
                    self.settings()
            # Choosing IF the user wants the urls to be
            # entered in as links or as plain text
            elif temp == "2":
                print("""Enter 'link' or 'text'.
                      Enter e to not change anything.""")
                print("Current config: ", self.configs["linkortext"])
                temp1 = input()
                if temp1.lower() == "e":
                    print("No changes made")
                elif temp1.lower() == "link":
                    self.configs["linkortext"] = "link"
                elif temp1.lower() == "text":
                    self.configs["linkortext"] = "text"
                else:
                    print("Bad input.")
                    self.settings()
            # Changing class name for HTML file
            elif temp == "3":
                print("Current class name: ", self.configs["classnames"])
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
            temp1 = input("Please input either yes or no\n")
            if temp1.lower() == "yes":
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
            temp1 = input("Enter either yes or no\n")
            if temp1.lower() == "yes":
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
            temp1 = input("")
            if temp1 == "Confirm":
                self.configs = {
                    "threads": 8,
                    "outside_sites": False,
                    "max_links": [False, 0],
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
        with open(self.settingsdir, 'w') as file:
            file.write(json.dumps(self.configs))
            file.close()
        main.clear_screen()
        self.main()


# Starting the application
main = Main("results")
main.main()
