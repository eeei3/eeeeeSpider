# eeeeeSpider
This is my CS 20 final assesment. 

How to use:
1. Open program
2. Run to your hearts content! There are no external dependancies that you will have to manually install

Options explanations:
1. Threads
- This will be how many threads the spider will be allowed to access. It will not use any more than you have allowed.
- The more you use, the faster it will be, but the more resource intensive. Set to 8 threads by default.
2. External sites
- This will give you the option to crawl a external site. For example, lets say you wanted to crawl your site gamers.ru. But the lets say you had some YouTube and Twitter embeds. Well what would happen if you had this option enabled is that once the spider hits lets say YouTube, it will begin to crawl the actual YouTube site. Not very pretty. Keep this option disabled unless you have a really good reason.
- Set to disabled by default.
3. Max links
- This is what it sounds like. THe max amount of links the spider will crawl. Useful if you don't want to index a whole site or are limited by some metric. Disabled by default.
