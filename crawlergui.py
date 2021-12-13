import os
import threading
import sys
from tkinter import *
from tkinter.font import Font


class CrawlerGUI:

    def __init__(self):
        return

    @staticmethod
    def main(links):
        root = Tk()

        vertical = Scrollbar(root, orient='vertical')
        vertical.pack(side=RIGHT, fill=Y)

        text = Text(root, width=15, height=100, wrap=NONE,
                    yscrollcommand=vertical.set)

        text.pack(side=TOP, fill=X)

        vertical.config(command=text.yview)

        for link in links:
            text.insert(END, link + "\n")

        root.minsize(500, 800)
        root.title("Link Viewer")
        root.mainloop()
