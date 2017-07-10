

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
        json_url = ("https://app.vagrantup.com/{0}/boxes/{1}/"
                    .format(publisher, name))
        request = urllib.request.Request(json_url, None,
                                         {'Accept': 'application/json'})
        json_file = urllib.request.urlopen(request)
        self._data = json.loads(json_file.read())
        # We need to preserve the order of the versions
        self._versions = tuple(v['version'] for v in self._data['versions'])
        # Prepare a data structure for quick lookups
        self._boxes = {}
        for v in self._data['versions']:
            _version = v['version']
            self._boxes[_version] = {}
            for p in v['providers']:
                _provider = p['name']
                self._boxes[_version][_provider] = {}
                self._boxes[_version][_provider]['url'] = p['url']

    def versions(self):
        """Return a tuple with all available box versions."""
        return self._versions

    def providers(self, version):
        """Return a list of providers for a specific box version."""
        return self._boxes[version].keys()

    def url(self, version, provider):
        """Return the download URL for a specific box version and provider."""
        return self._boxes[version][provider]['url']

    def checksum(self, version, provider, checksum, checksum_type='sha256'):
        self._boxes[version][provider]['checksum_type'] = checksum_type
        self._boxes[version][provider]['checksum'] = checksum

    def json(self):
        _data = self._data
        for v in _data['versions']:
            _version = v['version']
            for p in v['providers']:
                _provider = p['name']
                _box_data = self._boxes[_version][_provider]
                if 'checksum' in _box_data:
                    p['checksum_type'] = _box_data['checksum_type']
                    p['checksum'] = _box_data['checksum']
        return json.dumps(_data)
