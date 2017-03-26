========
Endymion
========

Endymion is a command-line tool that checks if the specified Vagrant
boxes can be downloaded from Hashicorp's Atlas_. In the case of the
official `CentOS Linux images for Vagrant`_, it will also check if the
images correspond to the version listed on Atlas.

.. _Atlas: https://atlas.hashicorp.com
.. _CentOS Linux images for Vagrant: https://atlas.hashicorp.com/centos/


Getting started
===============

First, create a local clone of the repository::

        $ git clone https://github.com/lpancescu/endymion.git

By default, ``endymion`` checks the latest version of the boxes
provided as arguments, displaying any errors::

        $ cd endymion/
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

* ``endymion`` uses the ``HEAD`` method of HTTP 1.1 to check the
  availability of the boxes without downloading them. This usually works
  with external boxes like the ones provided by CentOS or Fedora, but it
  will fail with ``405 Method Not Allowed`` for boxes hosted by
  Hashicorp; using ``GET`` with a ``Content-range`` header produces the
  same response.
* The CentOS project provides gpg-signed SHA256 checksums, but
  ``endymion`` doesn't try to validate them (this would require
  downloading each variant of a box)
