# eeeeeSpider
This is my CS 20 final assesment. 

![codeql-analysis(3.10)](https://github.com/eeei3/eeeeeSpider/actions/workflows/codeql-analysis.yml/badge.svg)

Table of Contents:
--------------------------------------------------------------------------
1. REQUIRMENTS
2. FAQ
3. How to use
4. Options/Explanations
5. Troubleshooting


REQUIRMENTS:
--------------------------------------------------------------------------
- Python 3.10

FAQ:
--------------------------------------------------------------------------
Q: What do I download? The binary or the source code?
A: You probably want to download the binary. But if you intend to modify the program yourself, get the source code.

Q: I have a problem!
A: First check the troubleshooting section. Second, check your configs folder. Third depends on which version you downloaded. Did you download the binary? Let me know. Did you download the source code? Check your code. Fourth, make sure all of your configs are in order.

How to use:
--------------------------------------------------------------------------
1. Extract the project.
2. Run start.exe. There are no external dependancies that you will have to manually install. To make a no-gui version, simply delete start.py and modify main.py.
3. 
Want to change the settings? Just type in "settings" at the prompt

Want to start the crawler? Just type in "start" at the prompt

Want to quit? Just type in "exit" at the prompt
                                                                                                                                                     
[Main Crawler Configs]
--------------------------------------------------------------------------
1. Threads [Num of threads]
- This will be how many threads the spider will be allowed to access. It will not use any more than you have allowed.
- The more you use, the faster it will be, but the more resource intensive. Set to 8 threads by default.
2. External sites [True or False]
- This will give you the option to crawl a external site. For example, lets say you wanted to crawl your site gamers.ru. But the lets say you had some YouTube and Twitter embeds. Well what would happen if you had this option enabled is that once the spider hits lets say YouTube, it will begin to crawl the actual YouTube site. Not very pretty. Keep this option disabled unless you have a really good reason.
- Set to disabled by default.
3. Max links [True or False, num of pages]
- This is what it sounds like. THe max amount of links the spider will crawl. Useful if you don't want to index a whole site or are limited by some metric. Disabled by default.
4. Warnings [True or False]
- This feature will pause the crawler once it has hit a certain number of sites. Enableing this will cause the crawler to pause and give the user
  a choice with what to do.
- Disabling this feature will cause the crawler to keep parsing without any input from the user.
5. Compress [True or False]
- This gives the user the option if they want the results to be compressed or not. This can be helpful, for when the crawler needs to parse a large site, to save storage space.
                                                                                                                                                                                 

[HTML Configs]
--------------------------------------------------------------------------
1. Classname [Name]
- This gives the user the ability to assign the text a class for easier manipulation
2. Linkortext [Link or Text]
- Gives the user the ability to either choose the a tag or text tag
3. Headers [True or False]
- Gives the user the ability to assign the text a header tag. h1-h4 are supported.



TROUBLESHOOTING:
--------------------------------------------------------------------------
1. Why are there mysterious symbols and letters?
- This is probably because one of the sites your crawled had some funny characters in it's link. Try changing the UTF encoding.
2. My disk is getting filled up with your project!
- Try setting a limit on the amount of links crawled.
3. How can I manipulate the src?
- You need a basic understanding of Python. Check out the graph for how the program runs.
4. Why does the crawler not work properly?
- My first suggestion is that you look into your configs. Make sure that they keep in line with their original cases.
