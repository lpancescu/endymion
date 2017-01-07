#!/usr/bin/env python2.7
from __future__ import unicode_literals, print_function

import argparse
import logging
import sys
import httplib
import urllib2
from atlas.box import Box


def check_url(url):
    request = urllib2.Request(url)
    if request.get_type() == 'https':
        conn = httplib.HTTPSConnection(request.get_host())
    elif request.get_type() == 'http':
        conn = httplib.HTTPConnection(request.get_host())
    conn.request('HEAD', request.get_selector())
    response = conn.getresponse()
    if response.status == httplib.OK:
        logging.info('{}: OK'.format(url))
        return True
    elif response.status == httplib.FOUND:
        redirect_url = response.getheader('Location')
        logging.debug('{}: FOUND'.format(url))
        logging.debug('==> {}'.format(redirect_url))
        return check_url(redirect_url)
    else:
        logging.error('{}: {} {}'.format(url, response.status, response.reason))
        return False


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.NOTSET)
    result = True
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', help='check all box versions',
                                 action='store_true')
    parser.add_argument('box', help='name of box to check, e.g. centos/7')
    args = parser.parse_args()
    box = Box(*args.box.split('/', 1))
    versions = list(box.versions())
    if not args.all:
        versions = versions[:1] # only test the latest version
    for version in versions:
        for provider in box.providers(version):
            url = box.url(version, provider)
            if not check_url(url):
                result = False
    if not result:
        sys.exit(1)
