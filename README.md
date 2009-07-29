Python Google Voice
=============

Exposing the Google Voice API to the Python language
----------------------------------------------------

Google Voice for Python Allows you to place calls, send sms, download voicemail, and check the various folders of your Google Voice Accounts.
You can use the Python API or command line script to schedule calls, check for new recieved calls/sms, or even sync your recorded voicemails/calls.  
Works for Python 2 and Python 3

INSTALL
-------------------------------

**Download the code from GoogleCode**

    $ hg clone https://pygooglevoice.googlecode.com/hg/ pygooglevoice  

**Install the module**

    $ cd pygooglevoice
    $ sudo python setup.py install

USAGE
-------------------------------

**Running the command line script**

    $ gvoice
    
It will prompt you for your Google Voice Account login credentials. At no point are these credentials saved or distributed to a 3rd party; they are only sent to Google. 
Now try calling someone
    
    gvoice> call
    
Fill in the outgoing number (number you wish to reach) and the forwarding number (the phone to place the call from, usually your Google Voice number). 
This will schedule a call between the two numbers, just wait for the forwarding phone to ring and let Google connect you. 
To find out the other commands, type `help`. 

**Try it out in Python**
    
    from googlevoice import Voice
    
    voice = Voice()
    voice.login(email=None, passwd=None)
    
    # Calling
    voice.call(outgoingNumber, forwardingNumber) # Places call
    voice.cancel(outgoingNumber, forwardingNumber) # Cancels previous call
    
    # SMS
    voice.send_sms(phoneNumber, text) # Sends text message to phoneNumber
    
    # Voicemail
    voice.download(msg) # Download MP3 of voicemail by sha1 hash
    
    # Folders
    print voice.inbox().items() # Prints out dict of vital stats and paginated list of inbox messages
    print voice.inbox('html') # Prints out raw html listing of folder
    
    
**Examples**

Simple examples are located in the `examples` directory

**API Documentation**

HTML format located in the `docs` directory

