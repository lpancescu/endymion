import http.client
import urllib.request
import urllib.error
import urllib.parse


class URLTracker:
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
            request = urllib.request.Request(url)
            if request.type == 'https':
                conn = http.client.HTTPSConnection(request.host)
            else:
                conn = http.client.HTTPConnection(request.host)
            conn.request('HEAD', request.selector)
            response = conn.getresponse()
            self._notify_all(url, response)
            if response.status == http.client.OK:
                return True
            elif response.status == http.client.FOUND:
                url = response.getheader('Location')
            else:
                return False
