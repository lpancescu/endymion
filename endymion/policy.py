

import logging
import http.client
from urllib.parse import urlparse


class FatalError(RuntimeError):
    """Exception class to be raised to stop following further links."""
    def __init__(self, message, url):
        self.message = message
        self.url = url

    def __str__(self):
        return "{}: {}".format(self.message, self.url)


class RedirectLimitPolicy:
    """Ensure only a maximum number of redirects are followed."""
    def __init__(self, max_redirects):
        self.max_redirects = max_redirects
        self.redirect_count = 0
        self.redirects = set()

    def notify(self, url, response):
        if response.status == http.client.FOUND:
            if url in self.redirects:
                raise FatalError('circular redirect', url)
            if self.redirect_count >= self.max_redirects:
                raise FatalError('too many redirects', url)
            self.redirect_count += 1
            self.redirects.add(url)


class VersionCheckPolicy:
    """Ensure the URL corresponds to the box version.

    Currently, only support for CentOS boxes is implemented.
    """
    def __init__(self, os_family, version_string):
        self.version_string = version_string
        self.os_family = os_family
        self.url_version_string = self._version_transform(version_string)

    def _version_transform(self, version):
        if self.os_family == 'centos':
            return version[:version.rindex('.')]
        return version

    def notify(self, url, response):
        if self.os_family == 'centos':
            ver = self.url_version_string
            if ver not in url:
                message = 'version "{}" not found in url'.format(ver)
                raise FatalError(message, url)


class AlwaysSSLPolicy:
    """Ensure all URLs are served via https."""
    def _validate_scheme(self, url):
        scheme = urlparse(url).scheme
        if scheme != 'https':
            raise FatalError('insecure scheme {}'.format(scheme), url)

    def notify(self, url, response):
        self._validate_scheme(url)
        # if this is a redirect, also check the new URL
        if response.status == http.client.FOUND:
            url = response.getheader('Location')
            self._validate_scheme(url)


class LogPolicy:
    """Log every URL being followed."""
    def notify(self, url, response):
        if response.status == http.client.OK:
            logging.info('{}: {} {}'.format(url,
                                            response.status,
                                            response.reason))
        elif response.status == http.client.FOUND:
            logging.debug('{}: {} {}'.format(url,
                                             response.status,
                                             response.reason))
        else:
            logging.error('{}: {} {}'.format(url,
                                             response.status,
                                             response.reason))


class ChecksumWriter:
    def __init__(self, box, version, provider, checksums):
        self.box = box
        self.version = version
        self.provider = provider
        self.checksums = checksums

    def notify(self, url, response):
        if response.status == http.client.OK:
            self.box.checksum(self.version,
                              self.provider,
                              self.checksums[url[url.rindex('/')+1:]])
