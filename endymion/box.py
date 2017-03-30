

import json
import urllib.request
import urllib.error
import urllib.parse


class Box:
    """Downloads and parses metainformation about a Vagrant box"""
    def __init__(self, publisher, name):
        """Extract metainformation for a Vagrant box.

        publisher -- Atlas owner
        name -- Vagrant box name
        """
        json_url = ("https://atlas.hashicorp.com/{0}/boxes/{1}/"
                    .format(publisher, name))
        request = urllib.request.Request(json_url, None,
                                         {'Accept': 'application/json'})
        json_file = urllib.request.urlopen(request)
        self._data = json.loads(json_file.read().decode('utf-8'))

    def versions(self):
        """Return a tuple with all available box versions."""
        return tuple(v['version'] for v in self._data['versions']
                     if v['status'] == 'active')

    def providers(self, version):
        """Return a list of providers for a specific box version."""
        _ver = ([v for v in self._data['versions']
                 if v['version'] == version])[0]
        return [p['name'] for p in _ver['providers']]

    def url(self, version, provider):
        """Return the download URL for a specific box version and provider."""
        _ver = ([v for v in self._data['versions']
                 if v['version'] == version])[0]
        return ([p for p in _ver['providers']
                 if p['name'] == provider])[0]['url']
