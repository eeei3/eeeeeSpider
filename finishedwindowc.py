from tkinter import *
from tkinter.font import Font
class CrawlerFinished:

    def completedgui():
        root = Tk()

        crawlerfinish  = Label(root, text = "Crawler has finished", font = ("Arial", 18), fg = "black")
        crawlerfinish.pack()

        root.title("Project  SpydrIE")
        root.minsize(200, 120)
        root.iconbitmap("assets/spider.ico")
        root.mainloop()
