from tkinter import Tk, Scrollbar, RIGHT, TOP, Y, Text, NONE, X, END


class CrawlerGUI:

    def __init__(self):
        return

    # /***************************************************************************************
    #  Function that creates a gui using Tkinter. Then it creates a scrollbar object
    #  and the text element that is created gets populated with the links.
    # ***************************************************************************************\

    def main(self, links):
        y_height = 0
        # Setting a appropriate height
        for link in links:
            y_height = y_height + 1

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
