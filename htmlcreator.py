from general import write_file


class HTMLCreator:

    def __init__(self, links, path, linkortext, classnames):
        self.links = links
        self.html = ""
        self.path = path
        self.linkortext = linkortext
        self.classnames = classnames
        self.htmlstarttags = """<!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>\n"""
        with open(path, "x") as htmlfile:
            htmlfile.close()

    # /***************************************************************************************
    #  Function that creates the HTML then dumps it
    # ***************************************************************************************\
    def html_generator(self, headers, classname):
        html = self.htmlstarttags
        htmlendtags = "</body>\n</html>"
        # /***************************************************************************************
        #  Checking if the user has provided any class names
        #  CASE: No class name defined
        # ***************************************************************************************\
        if self.classnames in ('', ' '):
            # Does the user want the url in plain text?
            if self.linkortext == "text":
                for link in self.links:
                    if link == "\n":
                        print("Empty line")
                        continue
                    if headers["headers1"]:
                        html = html + "<h1>" + link + "</h1>" + "\n"
                    elif headers["header2"]:
                        html = html + "<h2>" + link + "</h2>" + "\n"
                    elif headers["header3"]:
                        html = html + "<h3>" + link + "</h3>" + "\n"
                    elif headers["header4"]:
                        html = html + "<h4>" + link + "</h4>" + "\n"
                    else:
                        html = html + "<p>" + link + "</p>" + "\n"
            # Does the user want the url as a hyperlink?
            elif self.linkortext == "link":
                for link in self.links:
                    if link == "\n":
                        print("Empty line")
                        continue
                    if headers["headers1"]:
                        html = html + "<h1>" + "<a> href=\"" +\
                               link + "\"</a>" + "</h1>" + "\n"
                    elif headers["headers2"]:
                        html = html + "<h2>" + "<a> href=\"" +\
                               link + "\"</a>" + "</h2>" + "\n"
                    elif headers["headers3"]:
                        html = html + "<h3>" + "<a> href=\"" +\
                               link + "\"</a>" + "</h3>" + "\n"
                    elif headers["headers4"]:
                        html = html + "<h4>" + "<a> href=\"" +\
                               link + "\"</a>" + "</h4>" + "\n"
                    else:
                        html = html + "<p>" + "<a> href=\"" +\
                               link + "\"</a>" + "</p>" + "\n"
            # The user does not know what they are doing.
            else:
                print("How did we get here?")
                raise "Unexpected/InvalidConfig"
        # /***************************************************************************************
        #  Checking if the user has provided any class names
        #  CASE: Class name present
        # ***************************************************************************************\
        else:
            # Does the user want the url in plain text?
            if self.linkortext == "text":
                for link in self.links:
                    if link == "\n":
                        print("Empty line")
                        continue
                    if headers["headers1"]:
                        html = html + "<h1 class=" + self.classnames +\
                               ">" + link + "</h1>" + "\n"
                    elif headers["headers2"]:
                        html = html + "<h2 class=" + self.classnames +\
                               ">" + link + "</h2>" + "\n"
                    elif headers["headers3"]:
                        html = html + "<h3 class=" + self.classnames +\
                               ">" + link + "</h3>" + "\n"
                    elif headers["headers4"]:
                        html = html + "<h4 class=" + self.classnames +\
                               ">" + link + "</h4>" + "\n"
                    else:
                        html = html + "<p class=" + self.classnames +\
                               ">" + link + "</p>" + "\n"
            # Does the user want the url as a hyperlink?
            elif self.linkortext == "link":
                for link in self.links:
                    if link == "\n":
                        print("Empty line")
                        continue
                    if headers["headers1"]:
                        html = html + "<h1 class=" + self.classnames + ">" \
                                    + "<a> href=\"" + link +\
                                    "\"</a>" + "</h1>" + "\n"
                    elif headers["headers2"]:
                        html = html + "<h2 class=" + self.classnames + ">"\
                                    + "<a> href=\"" + link + "\"</a>" +\
                                    "</h2>" + "\n"
                    elif headers["headers3"]:
                        html = html + "<h3 class=" + self.classnames + ">"\
                                    + "<a> href=\"" + link + "\"</a>" +\
                                    "</h3>" + "\n"
                    elif headers["headers4"]:
                        html = html + "<h4 class=" + self.classnames + ">"\
                               + "<a> href=\"" + link + "\"</a>" +\
                               "</h4>" + "\n"
                    else:
                        html = html + "<p class=" + self.classnames + ">"\
                               + "<a> href=\"" + link + "\"</a>" +\
                               "</p>" + "\n"
            # The user does not know what they are doing.
            else:
                print("How did we get here?")
                raise "Unexpected/InvalidConfig"

        # Tying up loose ends
        html = html + htmlendtags
        # Saving the HTML
        write_file(self.path, html)
