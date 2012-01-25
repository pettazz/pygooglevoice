from distutils.core import setup


README = """Python Google Voice
====================

Joe McCall & Justin Quick

Exposing the Google Voice "API" to the Python language
-------------------------------------------------------

Google Voice for Python Allows you to place calls, send sms, download voicemail, and check the various folders of your Google Voice Accounts.
You can use the Python API or command line script to schedule calls, check for new recieved calls/sms, or even sync your recorded voicemails/calls.  
Works for Python 2 and Python 3

Full documentation is available up at http://sphinxdoc.github.com/pygooglevoice/
"""

setup(
    name = "pygooglevoice",
    version = '0.5',
    url = 'http://code.google.com/p/pygooglevoice',
    author = 'Justin Quick and Joe McCall',
    author_email='justquick@gmail.com, joe@mcc4ll.us',
    description = 'Python 2/3 Interface for Google Voice',
    long_description = README,
    packages = ['googlevoice'],
    scripts = ['bin/gvoice','bin/asterisk-gvoice-setup', 'bin/gvi']
)