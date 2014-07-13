# Scrapy settings for scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrape'

SPIDER_MODULES = ['scrape.spiders']

NEWSPIDER_MODULE = 'scrape.spiders'


DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrape (+http://www.yourdomain.com)'
