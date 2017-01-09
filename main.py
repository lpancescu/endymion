#!/usr/bin/env python2.7
from __future__ import unicode_literals, print_function

import argparse
import logging
import sys
import httplib
import urllib2
from atlas.box import Box


REDIRECT_LIMIT = 100


def check_url(url):
    redirects = 0
    while redirects < REDIRECT_LIMIT:
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
            redirects += 1
            logging.debug('{}: FOUND'.format(url))
            url = response.getheader('Location')
            logging.debug('==> {}'.format(url))
        else:
            logging.error('{}: {} {}'.format(url, response.status, response.reason))
            return False
    else:
        logging.error('redirection limit exceeded')
        return False


if __name__ == '__main__':
    result = True
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', action='store_true',
                        help='check all box versions')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase log verbosity')
    parser.add_argument('boxes', nargs='+', metavar='box',
                        help='name of a box to check, e.g. centos/7')
    args = parser.parse_args()

    if args.verbose >= 2:
        logging.getLogger().setLevel(logging.NOTSET)
    elif args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)

    for box_name in args.boxes:
        box = Box(*box_name.split('/', 1))
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
