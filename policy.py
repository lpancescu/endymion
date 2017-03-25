from __future__ import unicode_literals

class PolicyError(RuntimeError):
    def __init__(self, message, url):
        self.message = message
        self.url = url

    def __str__(self):
        return "{}: {}".format(self.message, self.url)


class RedirectLimitPolicy(object):
    def __init__(self, max_redirects):
        self.max_redirects = max_redirects
        self.redirects = 0

    def __call__(self, url):
        if self.redirects >= self.max_redirects:
            raise PolicyError('too many redirects', url)
        self.redirects += 1


class VersionCheckPolicy(object):
    def __init__(self, os_family, version_string):
        self.version_string = version_string
        self.os_family = os_family
        self.url_version_string = self._version_transform(version_string)

    def _version_transform(self, version):
        if self.os_family == 'centos':
            return version[:version.rindex('.')]
        return version

    def __call__(self, url):
        if self.os_family == 'centos':
            ver = self.url_version_string
            if ver not in url:
                message = 'version "{}" not found in url'.format(ver)
                raise PolicyError(message, url)
