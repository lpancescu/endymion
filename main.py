#!/usr/bin/env python2.7


import argparse
import logging
import sys
import http.client
import urllib.request, urllib.error, urllib.parse
from endymion.box import Box
from policy import RedirectLimitPolicy
from policy import VersionCheckPolicy
from policy import PolicyError


def check_url(url, policies):
    try:
        while True:
            request = urllib.request.Request(url)
            class_map = { 'https': http.client.HTTPSConnection,
                          'http' : http.client.HTTPConnection }
            _conn_class = class_map[request.type]
            conn = _conn_class(request.host)
            conn.request('HEAD', request.selector)
            response = conn.getresponse()
            if response.status == http.client.OK:
                for policy in policies:
                    policy(url)
                logging.info('{}: OK'.format(url))
                return True
            elif response.status == http.client.FOUND:
                logging.debug('{}: FOUND'.format(url))
                url = response.getheader('Location')
                logging.debug('==> {}'.format(url))
                for policy in policies:
                    policy(url)
            else:
                logging.error('{}: {} {}'.format(url, response.status, response.reason))
                return False
    except PolicyError as e:
        logging.error(e)
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
        os_family, major_version = box_name.split('/', 1)
        box = Box(os_family, major_version)
        versions = list(box.versions())
        if not args.all:
            versions = versions[:1] # only test the latest version
        for version in versions:
            for provider in box.providers(version):
                url = box.url(version, provider)
                rlp = RedirectLimitPolicy(20)
                vcp = VersionCheckPolicy(os_family, version)
                if not check_url(url, [rlp, vcp]):
                    result = False
    if not result:
        sys.exit(1)
