.. _install:


Installation
=============

Requirements, setup instructions, and how to get it running with a PBX

Requirements
-------------------

  * `Python >= 2.3 <http://www.python.org/download/>`_
  * For Python < 2.6, gvoice requires `simplejson <http://code.google.com/p/simplejson/>`_
    
Setups
-------------------

Stable distribution setup::

    $ yum install python python-setuptools
    $ sudo easy_install simplejson
    $ sudo easy_install -U pygooglevoice

Bleeding edge source code setup::

    $ yum install python python-setuptools mercurial
    $ sudo easy_install simplejson
    $ hg clone https://pygooglevoice.googlecode.com/hg/ pygooglevoice
    $ cd pygooglevoice
    $ sudo python setup.py install

Asterisk Setup
-------------------

Here is how to integrate Google Voice with a PBX. This guide was designed for `PBX in a flash <http://pbxinaflash.net/>`_, which is built upon `Asterisk <http://www.asterisk.org/>`_

The first steps are to install `PBX in a flash <http://pbxinaflash.net/>`_. Here is a good guide for doing so http://knol.google.com/k/ward-mundy/pbx-in-a-flash/

Running the setup above copies over a setup script to integrate into your Asterisk configuration setup. Simply run ``$ asterisk-gvoice-setup`` answer a couple questions, then restart your PBX instance.