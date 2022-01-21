# pylint: disable=C0116
"""
# /***************************************************************************************
#  This module is responsible for generating an HTML file from the given links.
# ***************************************************************************************\
"""
from general import write_file


class BadConfig(Exception):
    """
    /***************************************************************************************
    Exception for when the user has a invalid configuration
    ***************************************************************************************\
    """
    pass


class HTMLCreator:

    def __init__(self, links, path, linkortext, classnames):
        # The URL's to be added to the HTML
        self.links = links
        # The string holding the HTML
        self.html = ""
        # The location of the html file
        self.path = path
        # Whether the user wants links or text
        self.linkortext = linkortext
        # Class name for the elements
        self.classnames = classnames
        # The HTML start tags
        self.htmlstarttags = """<!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>\n"""
        with open(path, "x", encoding='utf8') as htmlfile:
            htmlfile.close()

    # /***************************************************************************************
    #  Function that creates the HTML then dumps it
    # ***************************************************************************************\
    def html_generator(self, headers, classname):
        # The HTML end tags
        htmlendtags = "</body>\n</html>"
        # /***************************************************************************************
        #  Checking if the user has provided any class names
        #  CASE: No class name defined
        # ***************************************************************************************\
        if self.classnames in ('', ' '):
            # Does the user want the url in plain text?
            html = self.htmlstarttags
            if self.linkortext == "text":
                for link in self.links:
                    if link == "\n":
                        # Is the element empty? Skip it!
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
                        # Is the element empty? Skip it!
                        continue
                    if headers["headers1"]:
                        html = html + "<h1>" + "<a href=\"" +\
                               link + "\">" + link + "</a>" + "</h1>" + "\n"
                    elif headers["headers2"]:
                        html = html + "<h2>" + "<a href=\"" +\
                               link + "\">" + link + "</a>" + "</h2>" + "\n"
                    elif headers["headers3"]:
                        html = html + "<h3>" + "<a href=\"" +\
                               link + "\">" + link + "</a>" + "</h3>" + "\n"
                    elif headers["headers4"]:
                        html = html + "<h4>" + "<a href=\"" +\
                               link + "\">" + link + "</a>" + "</h4>" + "\n"
                    else:
                        html = html + "<p>" + "<a href=\"" +\
                               link + "\">" + link + "</a>" + "</p>" + "\n"
            # The user does not know what they are doing.
            else:
                print("How did we get here?")
                raise BadConfig
        # /***************************************************************************************
        #  Checking if the user has provided any class names
        #  CASE: Class name present
        # ***************************************************************************************\
        else:
            html = self.htmlstarttags
            # Does the user want the url in plain text?
            if self.linkortext == "text":
                for link in self.links:
                    # Is the element empty? Skip it!
                    if link == "\n":
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
                    # Is the element empty? Skip it!
                    if link == "\n":
                        continue
                    if headers["headers1"]:
                        html = html + "<h1 class=" + self.classnames + ">" \
                               + "<a href=\"" + link + "\">" + link + "</a>" + "</h1>" + "\n"
                    elif headers["headers2"]:
                        html = html + "<h2 class=" + self.classnames + ">"\
                                    + "<a href=\"" + link + "\">" + link + "</a>" + "</h2>" + "\n"
                    elif headers["headers3"]:
                        html = html + "<h3 class=" + self.classnames + ">"\
                                    + "<a href=\"" + link + "\">" + link + "</a>" + "</h3>" + "\n"
                    elif headers["headers4"]:
                        html = html + "<h4 class=" + self.classnames + ">"\
                               + "<a href=\"" + link + "\">" + link + "</a>" + "</h4>" + "\n"
                    else:
                        html = html + "<p class=" + self.classnames + ">"\
                               + "<a href=\"" + link + "\">" + link + "</a>" + "</p>" + "\n"
            # The user does not know what they are doing.
            else:
                print("How did we get here?")
                raise BadConfig

        # Tying up loose ends
        html = html + htmlendtags
        # Saving the HTML
        write_file(self.path, html)
