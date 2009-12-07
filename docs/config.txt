.. _config:


Configuration
=============

When you first install the module, it places an ini configuration 
file in yournamed ``.gvoice`` in your home directory. This runs the ``gvoice``
and other scripts with your personal configuration defined in this file.
Run by default, these parameters are prompted for. 
Edit this file and fill in your personal configuration information.
If you enter your ``password``, it must be raw text so watch the privileges on this file.

    
Settings by Section
---------------------

auth
^^^^

Login credentials for http://google.com/voice

**email**

    The Google email account associated with Voice. Can be a gmail username, or proper email address.

**password**

    Raw password for logging in.

gvoice
^^^^^^^

**forwardingNumber**

    The number that you make your calls on (eg your Google Voice number)

**phoneType**

    The type of device connected to your ``forwardingNumber``. Options are::
        
        1. Home
        2. Mobile
        3. Work
        7. Gizmo
        
    Defaults to ``Mobile``
