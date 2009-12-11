from ConfigParser import ConfigParser, NoOptionError
import os
import settings


class Config(ConfigParser):
    """
    ``ConfigParser`` subclass that looks into your home folder for a file named
    ``.gvoice`` and parses configuration data from it.
    """
    def __init__(self):
        self.fname = os.path.expanduser('~/.gvoice')

        if not os.path.exists(self.fname):
            try:
                f = open(self.fname, 'w')
            except IOError:
                return
            f.write(settings.DEFAULT_CONFIG)
            f.close()
            
        ConfigParser.__init__(self)
        try:
            self.read([self.fname])
        except IOError:
            return

    def get(self, option, section='gvoice'):
        try:
            return ConfigParser.get(self, section, option).strip() or None
        except NoOptionError:
            return
        
    def set(self, option, value, section='gvoice'):
        return ConfigParser.set(self, section, option, value)

    def phoneType(self):
        try:
            return int(self.get('phoneType'))
        except TypeError:
            return
        
    def save(self):
        f = open(self.fname, 'w')
        self.write(f)
        f.close()
        

    phoneType = property(phoneType)
    forwardingNumber = property(lambda self: self.get('forwardingNumber'))
    email = property(lambda self: self.get('email','auth'))
    password = property(lambda self: self.get('password','auth'))
    secret = property(lambda self: self.get('secret'))
    
config = Config()
