========
Endymion
========

*Endymion* is a command-line tool that checks if the specified Vagrant
boxes can be downloaded from Hashicorp's Atlas_. In the case of the
official `CentOS Linux images for Vagrant`_, it will also check if the
images correspond to the version listed on Atlas.

.. _Atlas: https://atlas.hashicorp.com
.. _CentOS Linux images for Vagrant: https://atlas.hashicorp.com/centos/

Installation
============

*Endymion* doesn't have any external dependencies outside of the Python
standard library, so it shouldn't pose any problems to install it
directly. You can also install it in a virtualenv if you prefer.

If you only plan to use *Endymion*, the simplest way is to install it
from PyPI::

        $ pip install endymion

Developers can also run the development version::

        $ git clone https://github.com/lpancescu/endymion.git
        $ git checkout python3 # only if you use Python 3.x
        $ pip install -e .

Usage
=====

By default, ``endymion`` checks the latest version of the boxes
provided as arguments, displaying any errors::

        $ endymion centos/6 centos/7

Use ``-v`` to see more details (``-vv`` to also show the redirects)::

        $ endymion -v centos/6
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.Libvirt.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VirtualBox.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VMwareFusion.box: OK
        INFO:root:http://cloud.centos.org/centos/6/vagrant/x86_64/images/CentOS-6-x86_64-Vagrant-1611_01.VMwareFusion.box: OK

If you want to check all versions available on Atlas, use ``--all`` (not
recommended for day-to-day use because of the large number of requests
to Atlas, for boxes with many versions).

The return code will be 0 if no errors were found, and non-zero
otherwise.

Limitations
===========

* ``endymion`` uses the ``HEAD`` method of HTTP 1.1 to check the
  availability of the boxes without downloading them. This usually works
  with external boxes like the ones provided by CentOS or Fedora, but it
  will fail with ``405 Method Not Allowed`` for boxes hosted by
  Hashicorp; using ``GET`` with a ``Content-range`` header produces the
  same response.
* The CentOS project provides GnuPG-signed SHA256 checksums, but
  ``endymion`` doesn't try to validate them (this would require
  downloading each variant of a box)

Supported Python versions
=========================

Both Python 2.7 and Python 3.x are supported, although they have
different codebases:

* The ``master`` branch contains the Python 2.7 source code
* The ``python3`` branch, unsurprisingly, only runs under Python 3.x
  (instead of unifying the two code bases, I decided to convert the
  Python 2.7 code to Python 3, to avoid needlessly complicating the code
  to support both versions in the long term; if CentOS Linux 8 will
  default to Python 3, I can just move the Python 3 code to ``master``).

If you are a regular user, this doesn't matter: ``pip install endymion``
will always install the right package for your Python version.
