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
