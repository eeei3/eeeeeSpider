import os
import sys
from tkinter import *
from tkinter.font import Font
from html.parser import HTMLParser
import urllib.request
from bs4 import BeautifulSoup
import pgeneral
from concurrent import futures
import threading
import zlib, base64


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)


class ParserGUI:


    def __init__(self, ignorevar, ignorevar2, tags, words, base_url, ignorestr, project_name, parsed, parsed_file, total_data, grab_html, timerun, compress):
        ParserGUI.ignorevar = ignorevar
        ParserGUI.ignorevar2 = ignorevar2
        ParserGUI.tags = tags
        ParserGUI.words = words
        ParserGUI.base_url = base_url
        ParserGUI.ignorestr = ignorestr
        ParserGUI.project_name = project_name
        ParserGUI.parsed = parsed
        ParserGUI.parsed_file = parsed_file
        ParserGUI.total_data = total_data
        ParserGUI.grab_html = grab_html
        ParserGUI.compress = compress
        

    def parserwindow():
        
        """def destr():
            root.destroy()

        def on_exit():
            root = Toplevel()

            titlelabel = Label(root, text = "Are you sure you want to quit?", font = ("Arial", 10), fg = "black")

            titlelabel.pack()
        
            confirmation = Button(root, text = "I am sure", command = destr, height =  2, width = 15)

            confirmation.pack()

            root.title("Project SpydrIE")
            root.iconbitmap("assets/spider.ico")
            root.mainloop()"""
            
        try:
            y = open("parseroptions.conf", "r")
            ParserGUI.compress = y.read()
        except Exception as e:
            print(e)
        root = Tk()
        ParserGUI.ignorevar = IntVar(root)
        ParserGUI.ignorevar2 = IntVar(root)
        ParserGUI.words = StringVar(root)
        ParserGUI.tags = StringVar(root)
        titleLabel = Label(root, text = "Site Content Parser", font = ("Arial", 18), fg = "black")
        titleLabel.pack()
        tagstoinclude = Label(root, text = "Tags to exclude", font = ("Arial", 10), fg = "black")
        tagstoinclude.place(relx = 0.09, rely = 0.14, anchor = 'sw')
        tagsinclude = Entry(root, textvariable = ParserGUI.tags, width =14, font=("Arial", 12), fg = "black")
        tagsinclude.place(relx=0.45, rely=0.14, anchor='sw')
        firstbox = Checkbutton(root, text="Grab full HTML?", variable=ParserGUI.ignorevar, onvalue=1, offvalue=0)
        firstbox.place(relx=0.45, rely=0.20, anchor='sw')
        wordlabel = Label(root, text = "Keyword(s):", font = ("Arial", 10), fg = "black")
        wordlabel.place(relx=0.10, rely=0.32, anchor='sw')
        lookforwords = Entry(root, textvariable = ParserGUI.words, width=18, font=("Arial", 12), fg = "black")
        lookforwords.place(relx=0.35, rely=0.32, anchor='sw')
        advancedoptions = Button(root, text = "Advanced Options", command = ParserGUI.advanced_options, height = 2, width = 32)
        advancedoptions.place(relx=0.10, rely=0.58, anchor='sw')
        start = Button(root, text = "Start", command = ParserGUI.Start, height = 2, width =32)
        start.place(relx=0.10, rely=0.70, anchor='sw')
        abortbutton = Button(root, text = "Abort", command = ParserGUI.abortoperation, height = 2, width = 32)
        abortbutton.place(relx=0.10, rely = 0.82, anchor = 'sw')

        root.title("Project SpydrIE")
        root.minsize(300, 500)
        root.iconbitmap("assets/spider.ico")
        root.protocol("WM_DELETE_WINDOW", on_exit)
        root.mainloop()
        
    

    def advanced_options():
        def saving():
            print("Saving")
            zipsetting = putintozip.get()
            t = open("parseroptions.conf", "w")
            t.write(str(zipsetting))
            t.close()
            root.destroy()
            

        root = Toplevel()
        putintozip = IntVar()
        title = Label(root, text = "Advanced Options", font = ("Arial", 20), fg = "black")
        title.pack()
        packintozip = Checkbutton(root, text = "Compress final file?", variable = putintozip, onvalue = 1, offvalue = 0)
        packintozip.place(relx = 0.05, rely = 0.20, anchor = 'sw')
        reminder = Label(root, text = "You will need to restart the application for settings to take effect", font = ("Arial", 7), fg = "black")
        reminder.place(relx = 0.055, rely = 0.70, anchor = 'sw')
        exitbutton = Button(root, text = "Exit & Save", command = saving, height = 2, width = 15)
        exitbutton.place(relx = 0.3, rely = 0.60, anchor = 'sw')
        root.mainloop
        root.title("Project SpydrIE")
        root.minsize(300, 500)
        root.iconbitmap("assets/spider.ico")
        root.mainloop()
        
    def abortoperation():
        thread_pool_executor.submit(ParserGUI.secondabortoperation)
        
    def secondabortoperation():
        quit()
        
    def Start():
        thread_pool_executor.submit(ParserGUI.parser_Start)
        
    def parser_Start():
        a = open("webfile.rac", "r")
        ParserGUI.base_url = (a.read())

        project_name = 'projecteleparser'

        ParserGUI.parsed_file = project_name + '/parsed.txt'

        ParserGUI.grab_html = (ParserGUI.ignorevar.get())
        print(ParserGUI.grab_html)
        
        pgeneral.create_data_dir(project_name)
        pgeneral.create_data_files(project_name, ParserGUI.base_url)
        if ParserGUI.grab_html == 1:
                thread_pool_executor.submit(ParserGUI.warning_html_size)
        else:
            ParserGUI.parser()
        
    def parser():
        thread_pool_executor.submit(ParserGUI.actualparser)

    def update_files():
        print(ParserGUI.parsed_file)
        try:
            pgeneral.set_to_file(ParserGUI.parsed, ParserGUI.parsed_file)
            ParserGUI.finished_window()
        except Exception as e:
            print(e)
        

    def update_files_html_edition():
        try:
            pgeneral.set_to_file(str(ParserGUI.total_data), ParserGUI.parsed_file)
            ParserGUI.finished_window()
        except Exception as e:
            print(e)

    def search_for_data():
        soup1 = BeautifulSoup(ParserGUI.total_data, features="lxml")
        ParserGUI.parsed = (soup1.get_text())
        ParserGUI.update_files()

    def actualparser():
        url_open = urllib.request.urlopen(ParserGUI.base_url)
        soup = BeautifulSoup(url_open, features="lxml")
        ParserGUI.total_data = (soup.prettify())
        if ParserGUI.grab_html == 1:
            ParserGUI.update_files_html_edition()
        else:
            ParserGUI.search_for_data()

    def finished_window():
        if int(ParserGUI.compress) == 1:
            try:
                mork = open(ParserGUI.parsed_file, 'rb').read()
            except Exception as e:
                print(e)
            bork = zlib.compress(mork, 9)
            g = open(ParserGUI.parsed_file, 'wb')
            g.write(bork) 
            g.close()
        else:
            pass
        
            
        root = Toplevel()
        title = Label(root, text = "Parser has finished", font = ("Arial", 20), fg = "black")
        title.pack()
        root.title("Projectele")
        root.iconbitmap("assets/spider.ico")
        root.mainloop()

    def cancel_operation():
        thread_pool_executor.submit(ParserGUI.cancel__operation)
        
    def cancel__operation():
        quit()

    def warning_html_size():
        
        def parser():
            try:
                root.destroy()
            except Exception as e:
                print(e)
            thread_pool_executor.submit(ParserGUI.actualparser)
        root = Toplevel()
        warning = Label(root, text = "Are you sure you want to parse", font = ("Arial", 15), fg = "black")
        warning.pack()
        warning1 = Label(root, text="ALL of this website's HTML?", font = ("Arial", 15), fg = "black")
        warning1.pack()
        warning2 = Label(root, text = "File size can exceed 4 GB", font = ("Arial", 15), fg = "black")
        warning2.pack()
        warning3 = Label(root, text = "This is beyond some text editors capabillity to display", font = ("Arial", 15), fg = "black")
        warning3.pack()
        areyousure = Button(root, text = "Yes I am sure", command = parser, height = 2, width = 10)
        areyousure.place(relx = 0.30, rely = 0.70, anchor = 'sw')
        notsure = Button(root, text = "Cancel Operation", command = root.destroy, height = 2, width = 13)
        notsure.place(relx = 0.60, rely = 0.70, anchor = 'sw')
        root.title("Project SpydrIE")
        root.minsize(400, 300)
        root.iconbitmap("assets/spider.ico")
        root.mainloop()

        
        


        
    
        
                

            
            
        



        



