import logging
import httplib
import urllib2

from .policy import PolicyError


def check_url(url, policies):
    try:
        while True:
            request = urllib2.Request(url)
            class_map = {'https': httplib.HTTPSConnection,
                         'http': httplib.HTTPConnection}
            _conn_class = class_map[request.get_type()]
            conn = _conn_class(request.get_host())
            conn.request('HEAD', request.get_selector())
            response = conn.getresponse()
            if response.status == httplib.OK:
                for policy in policies:
                    policy(url)
                logging.info('{}: OK'.format(url))
                return True
            elif response.status == httplib.FOUND:
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
