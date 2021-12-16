# eeeeeSpider
This is my CS 20 final assesment. 

![py_lint(3.10)](https://github.com/eeei3/eeeeeSpider/actions/workflows/pylint.yml/badge.svg)
![python-app(3.10)](https://github.com/eeei3/eeeeeSpider/actions/workflows/python-app.yml/badge.svg)

How to use:
1. Open program
2. Run to your hearts content! There are no external dependancies that you will have to manually install

Options explanations:
1. Threads [Num of threads]
- This will be how many threads the spider will be allowed to access. It will not use any more than you have allowed.
- The more you use, the faster it will be, but the more resource intensive. Set to 8 threads by default.
2. External sites [True or False]
- This will give you the option to crawl a external site. For example, lets say you wanted to crawl your site gamers.ru. But the lets say you had some YouTube and Twitter embeds. Well what would happen if you had this option enabled is that once the spider hits lets say YouTube, it will begin to crawl the actual YouTube site. Not very pretty. Keep this option disabled unless you have a really good reason.
- Set to disabled by default.
3. Max links [True or false, num of pages]
- This is what it sounds like. THe max amount of links the spider will crawl. Useful if you don't want to index a whole site or are limited by some metric. Disabled by default.



TROUBLESHOOTING:
1. Why are there mysterious symbols and letters?
- This is probably because one of the sites your crawled had some funny characters in it's link. Try changing the UTF encoding.
2. My disk is getting filled up with your project!
- Try setting a limit on the amount of links crawled.
3. How can I manipulate the src?
- You need a basic understanding of Python. Check out the graph for how the program runs.
4. Why does the crawler not work properly?
- My first suggestion is that you look into your configs. Make sure that they keep in line with their original cases.
