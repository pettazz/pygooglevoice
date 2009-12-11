DEFAULT_CONFIG = """
[auth]
# Google Account email address (one associated w/ your Voice account)
email=

# Raw password used or login
password=

[gvoice]
# Number to place calls from (eg, your google voice number)
forwardingNumber=

# Default phoneType for your forwardingNumber as defined below
#  1 - Home
#  2 - Mobile
#  3 - Work
#  7 - Gizmo
phoneType=2
"""

DEBUG = False
LOGIN = 'https://www.google.com/accounts/ServiceLoginAuth?service=grandcentral'
FEEDS = ('inbox', 'starred', 'all', 'spam', 'trash', 'voicemail', 'sms',
        'recorded', 'placed', 'received', 'missed')

BASE = 'https://www.google.com/voice/'
LOGOUT = BASE + 'account/signout'
INBOX = BASE + '#inbox'
CALL = BASE + 'call/connect/'
CANCEL = BASE + 'call/cancel/'
DEFAULT_FORWARD = BASE + 'settings/editDefaultForwarding/'
FORWARD = BASE + 'settings/editForwarding/'
DELETE = BASE + 'inbox/deleteMessages/'
MARK = BASE + 'inbox/mark/'
STAR = BASE + 'inbox/star/'
SMS = BASE + 'sms/send/'
DOWNLOAD = BASE + 'media/send_voicemail/'
BALANCE = BASE + 'settings/billingcredit/'

XML_SEARCH = BASE + 'inbox/search/'
XML_CONTACTS = BASE + 'contacts/'
XML_RECENT = BASE + 'inbox/recent/'
XML_INBOX = XML_RECENT + 'inbox/'
XML_STARRED = XML_RECENT + 'starred/'
XML_ALL = XML_RECENT + 'all/'
XML_SPAM = XML_RECENT + 'spam/'
XML_TRASH = XML_RECENT + 'trash/'
XML_VOICEMAIL = XML_RECENT + 'voicemail/'
XML_SMS = XML_RECENT + 'sms/'
XML_RECORDED = XML_RECENT + 'recorded/'
XML_PLACED = XML_RECENT + 'placed/'
XML_RECEIVED = XML_RECENT + 'received/'
XML_MISSED = XML_RECENT + 'missed/'