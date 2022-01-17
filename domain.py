# pylint: disable=C0116
"""
# /***************************************************************************************
#  Module that is responsible for fetching the domain name and the subdomain name of
#  the URLs that are crawled.
# ***************************************************************************************\
"""
from urllib.parse import urlparse


# Getting the domain name ex. github
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return str(results[-2]) + '.' + str(results[-1])
    except Exception as error:
        print(error)
        return ''


# Getting the sub domain name ex. github.com
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except Exception as error:
        print(error)
        return ''
