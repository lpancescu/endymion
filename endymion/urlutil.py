import logging
import http.client
import urllib.request
import urllib.error
import urllib.parse

from .policy import PolicyError


def check_url(url, policies):
    try:
        while True:
            request = urllib.request.Request(url)
            class_map = {'https': http.client.HTTPSConnection,
                         'http': http.client.HTTPConnection}
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
                logging.error('{}: {} {}'.format(url,
                                                 response.status,
                                                 response.reason))
                return False
    except PolicyError as e:
        logging.error(e)
        return False
