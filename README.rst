==========
Atlas Lint
==========

``atlas-lint`` checks if the specified Vagrant boxes can be downloaded
from Hashicorp's Atlas.

Getting started
===============

First, create a local clone of the repository::

        $ git clone https://github.com/lpancescu/atlas-lint.git

By default, ``atlas-lint`` checks the latest version of the boxes
provided as arguments, displaying any errors::

        $ cd atlas-lint/
        $ python2 main.py centos/6 centos/7

Use ``-v`` to see more details (``-vv`` to also show the redirects)::

        $ python2 main.py -v centos/6
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.Libvirt.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VirtualBox.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VMwareFusion.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VMwareFusion.box: OK

If you want to check all versions available on Atlas, use ``--all`` (not
recommended because of the large number of requests to Atlas, for boxes
with many versions).

Limitations
===========

* ``atlas-lint`` uses the HTTP 1.1 method ``HEAD`` to check the
  availability of the boxes without downloading them. This usually works
  with external boxes like the ones provided by CentOS or Fedora, but it
  will fail with ``405 Method Not Allowed`` for boxes hosted by
  Hashicorp. 
* The CentOS project provides gpg-signed SHA256 checksums, but
  ``atlas-lint`` doesn't try to validate them (this would require
  downloading each variant of a box)
