"""Check links to external Vagrant boxes listed on Atlas."""
from __future__ import unicode_literals

import argparse
import logging
import sys
import pkg_resources

from endymion.box import Box
import endymion.policy
import endymion.urlutil
from endymion.checksums import SHA256Sums


# The module version is defined in setup.py; ask setuptools
__version__ = pkg_resources.get_distribution(__name__).version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('-a', '--all', action='store_true',
                        help='check all box versions')
    parser.add_argument('--export', action='store_true',
                        help='export JSON data for self-hosting')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase log verbosity')
    parser.add_argument('boxes', nargs='+', metavar='box',
                        help='name of a box to check, e.g. centos/7')
    args = parser.parse_args()

    if args.verbose >= 2:
        logging.getLogger().setLevel(logging.NOTSET)
    elif args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)

    success = True
    for box_name in args.boxes:
        os_family, major_version = box_name.split('/', 1)
        with open('{}_{}.sha256sum.txt'.format(os_family,
                                               major_version)) as f:
            checksums = SHA256Sums(f)
        box = Box(os_family, major_version)
        versions = list(box.versions())
        if not (args.all or args.export):
            versions = versions[:1]
        for version in versions:
            for provider in box.providers(version):
                url = box.url(version, provider)
                rlp = policy.RedirectLimitPolicy(20)
                vcp = policy.VersionCheckPolicy(os_family, version)
                asp = policy.AlwaysSSLPolicy()
                lp = policy.LogPolicy()
                cw = policy.ChecksumWriter(box, version, provider, checksums)
                if args.export:
                    tracker = urlutil.URLTracker([cw, lp, rlp])
                else:
                    tracker = urlutil.URLTracker([lp, rlp, asp, vcp])
                try:
                    if not tracker.follow(url):
                        success = False
                except policy.FatalError as pe:
                    fmt = '{version}/{provider}: {pe.message} ({pe.url})'
                    print(fmt.format(**locals()))
                    success = False
        if args.export:
            with open('{}_{}.json'.format(os_family,
                                          major_version), 'w') as f:
                f.write(box.json())
    if not success:
        sys.exit(1)
