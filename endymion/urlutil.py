import httplib
import urllib2


class URLTracker(object):
    """Follow redirected URLs to their final destination."""
    def __init__(self, observers=None):
        """Create an URLTracker object

        observers -- iterable containing observers to be notified of each URL
        """
        self.observers = []
        if observers is not None:
            self.observers.extend(observers)

    def _notify_all(self, url, response):
        """Notify observers about an URL and the received HTTP response.
        """
        for observer in self.observers:
            observer.notify(url, response)

    def register(self, observer):
        """Add an observer to be notified about followed URLs.

        If the observer is already in the list, no action is taken.
        """
        if observer not in observers:
            observers.append(observer)

    def unregister(self, observer):
        """Remove an observer from the list of observers.

        A ValueError is raised if he observer is not in the list.
        """
        observers.remove(observer)

    def follow(self, url):
        """Follow HTTP redirects and notify observers about each URL."""
        while True:
            request = urllib2.Request(url)
            if request.get_type() == 'https':
                conn = httplib.HTTPSConnection(request.get_host())
            else:
                conn = httplib.HTTPConnection(request.get_host())
            conn.request('HEAD', request.get_selector())
            response = conn.getresponse()
            self._notify_all(url, response)
            if response.status == httplib.OK:
                return True
            elif response.status == httplib.FOUND:
                url = response.getheader('Location')
            else:
                return False
