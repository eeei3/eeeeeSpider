from urllib.parse import urlparse


"""
# /***************************************************************************************
#  Module that is responsible for fetching the domain name and the sub domain name of
#  the URL's that are crawled.
# ***************************************************************************************\
"""
def get_domain_name(url):
    # Getting the domain name ex. github
    try:
        results = get_sub_domain_name(url).split('.')
        return str(results[-2]) + '.' + str(results[-1])
    except Exception:
        return ''


def get_sub_domain_name(url):
    # Getting the sub domain name ex. github.com
    try:
        return urlparse(url).netloc
    except Exception:
        return ''
