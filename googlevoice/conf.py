from ConfigParser import ConfigParser, NoOptionError
import os
import settings



class Config(ConfigParser):
    def __init__(self):
        self.fname = os.path.expanduser('~/.gvoice')

        if not os.path.exists(self.fname):
            f = open(self.fname, 'w')
            f.write(settings.DEFAULT_CONFIG)
            f.write()
            
        ConfigParser.__init__(self)
        self.read([self.fname])

    def get(self, option, section='gvoice'):
        try:
            return ConfigParser.get(self, section, option).strip() or None
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
