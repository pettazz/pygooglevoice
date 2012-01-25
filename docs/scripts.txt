.. _scripts:


Command Line Script
===================

The module also comes with a script called ``gvoice`` which can do all the wonderful stuff that the 
Python module can do easily on the command line. 


Usage
-----

::

    Usage: gvoice [options] commands
        Where commands are
        
        login (li) - log into the voice service
        logout (lo) - log out of the service and make sure session is deleted
        help
    
        Voice Commands
            call (c) - call an outgoing number from a forwarding number
            cancel (cc) - cancel a particular call
            download (d) - download mp3 message given id hash
            send_sms (s) - send sms messages
                
        Folder Views
            search (se)
            inbox (i)
            voicemail (v)
            starred (st)
            all (a)
            spam (sp)
            trash (t)
            voicemail (v)
            sms (sm)
            recorded (r)
            placed (p)
            recieved (re)
            missed (m)
    
    Options:
      -h, --help            show this help message and exit
      -e EMAIL, --email=EMAIL
                            Google Voice Account Email
      -p PASSWD, --password=PASSWD
                            Your account password (prompted if blank)
      -b, --batch           Batch operations, asking for no interactive input


Example
-------

::

    $ gvoice -e myusername@gmail.com
    Password:
    gvoice> call
    Outgoing number: 18004664411
    Forwarding number: 14075551234
    Calling...