from __future__ import unicode_literals, print_function
import re


class SHA256Sums(dict):
    def __init__(self, f):
        """Load SHA256 sums from file f"""
        hash_re = re.compile(r'Hash:\s+(\S+)')
        checksum_re = re.compile(r'([0-9a-fA-F]{64})\s+(\S+)')
        for line in f:
            hash_match = hash_re.match(line)
            if hash_match and hash_match.group(1) != 'SHA256':
                raise RuntimeError('Expected SHA256 as hash type')
            checksum_match = checksum_re.match(line)
            if checksum_match:
                self[checksum_match.group(2)] = checksum_match.group(1)
