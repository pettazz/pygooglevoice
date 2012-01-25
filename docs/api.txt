.. _api:


API Reference
=============

.. automodule:: googlevoice

Voice
------

In addition to the methods below, ``Voice`` instances have several special methods for
gathering information from folders in the Google Voice service. These methods are:

  * ``inbox`` - Recent, unread messages
  * ``starred`` - Starred messages
  * ``all`` - All messages
  * ``spam`` - Messages likely to be spam
  * ``trash`` - Deleted messages
  * ``voicemail`` - Voicemail messages
  * ``sms`` - Text messages
  * ``recorded`` - Recorced messages
  * ``placed`` - Outgoing messages
  * ``received`` - Incoming messages
  * ``missed`` - Messages not received
  
All of these special methods operate the same way. When they are called,
they parse the feed from the Google Voice service and return a ``Folder`` instance.
After they have been called, you can grab the JSON and HTML data directly.

Usage::

   >>> voice.inbox()       # Parses feed and returns Folder instance
   ... <Folder inbox (9)>
   >>> voice.inbox.json    # Raw JSON data
   ... u'{"messages":{"14ef89...'
   >>> voice.inbox.html    # Raw HTML data
   ... u'\n\n  \n<div id="14fe89...'
   >>> voice.inbox.folder  # Just returns Folder instance
   ... <Folder inbox (9)>

.. autoclass:: Voice
   :members:

Folder
---------------

.. automodule:: googlevoice.util

.. autoclass:: Folder
   :members:

Phone
---------------
   
.. autoclass:: Phone
   :members:
   
Message
---------------

.. autoclass:: Message
   :members:

XMLParser
---------------

.. autoclass:: XMLParser
   :members: