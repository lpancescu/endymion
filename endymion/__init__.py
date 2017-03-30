"""Check links to external Vagrant boxes listed on Atlas."""


import argparse
import logging
import sys
import pkg_resources

from endymion.box import Box
import endymion.policy
import endymion.urlutil


# The module version is defined in setup.py; ask setuptools
__version__ = pkg_resources.get_distribution(__name__).version


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
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

    success = True
    for box_name in args.boxes:
        os_family, major_version = box_name.split('/', 1)
        box = Box(os_family, major_version)
        versions = list(box.versions())
        # only test the latest version by default
        if not args.all:
            versions = versions[:1]
        for version in versions:
            for provider in box.providers(version):
                url = box.url(version, provider)
                rlp = policy.RedirectLimitPolicy(20)
                vcp = policy.VersionCheckPolicy(os_family, version)
                asp = policy.AlwaysSSLPolicy()
                lp = policy.LogPolicy()
                tracker = urlutil.URLTracker([lp, rlp, asp, vcp])
                try:
                    if not tracker.follow(url):
                        success = False
                except policy.FatalError as pe:
                    fmt = '{version}/{provider}: {pe.message} ({pe.url})'
                    print(fmt.format(**locals()))
                    success = False
    if not success:
        sys.exit(1)
