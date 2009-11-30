from ConfigParser import ConfigParser, NoOptionError
import os


DEFAULT = """
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

class Config(ConfigParser):
    def __init__(self):
        self.fname = os.path.expanduser('~/.gvoice')

        if not os.path.exists(self.fname):
            f = open(self.fname, 'w')
            f.write(DEFAULT)
            f.write()
            
        ConfigParser.__init__(self)
        self.read([self.fname])

    def get(self, option):
        try:
            return ConfigParser.get(self, 'gvoice', option) or None
        except NoOptionError:
            return

    def phoneType(self):
        try:
            return int(self.get('phoneType'))
        except TypeError:
            return
    phoneType = property(phoneType)

    def forwardingNumber(self):
        return self.get('forwardingNumber')
    forwardingNumber = property(forwardingNumber)

config = Config()
