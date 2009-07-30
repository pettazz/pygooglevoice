from googlevoice import settings
from googlevoice.util import *

class Voice(object):
    """
    Main voice instance for interacting with the Google Voice service
    Also contains callable methods for each folder (eg inbox,voicemail,sms,etc)
    """
    def __init__(self):
        install_opener(build_opener(HTTPCookieProcessor(CookieJar())))
        
        for name in settings.FEEDS:
            setattr(self, name, self.__multiformat(name))
            setattr(self, '%s_html' % name, self.__multiformat(name, 'html'))
    
    ######################
    # Some handy methods
    ######################  
    @property
    def special(self):
        """
        Returns special identifier for your session (if logged in)
        """
        if hasattr(self, '_special') and getattr(self, '_special'):
            return self._special
        try:
            try:
                regex = bytes("('_rnr_se':) '(.+)'", 'utf8')
            except TypeError:
                regex = bytes("('_rnr_se':) '(.+)'")
        except NameError:
            regex = r"('_rnr_se':) '(.+)'"
        try:
            sp = re.search(regex, urlopen(settings.INBOX).read()).group(2)
        except AttributeError:
            sp = None
        self._special = sp
        return sp
    
    def login(self, email=None, passwd=None):
        """
        Login to the service using your Google Voice account
        Credentials will be propmpted for if not given
        """
        if email is None:
            email = input('Email address: ')
        
        if passwd is None:
            from getpass import getpass
            passwd = getpass()
        
        self.__do_page('LOGIN', {'Email':email,'Passwd':passwd})
        
        del email,passwd
        
        try:
            assert self.special
        except (AssertionError, AttributeError):
            raise LoginError
        
    def logout(self):
        """
        Logs out an instance and makes sure it does not still have a session
        """
        urlopen(settings.LOGOUT)
        del self._special 
        assert self.special == None
    
    def call(self, outgoingNumber, forwardingNumber, subscriberNumber=None):
        """
        Make a call to an outgoing number using your forwarding number
        """
        self.__do_special_page('call', {
            'outgoingNumber':outgoingNumber,
            'forwardingNumber':forwardingNumber,
            'subscriberNumber':subscriberNumber or 'undefined',
            'remember':'0',
        })
    __call__ = call
    
    def cancel(self, outgoingNumber=None, forwardingNumber=None):
        """
        Cancels a call matching outgoing and forwarding numbers (if given)
        Will raise an error if no matching call is being placed
        """
        self.__do_special_page('cancel', {
            'outgoingNumber':outgoingNumber or 'undefined',
            'forwardingNumber':forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        })
        
    def send_sms(self, phoneNumber, text):
        """
        Send an SMS message to a given phone number with the given text message
        """
        self.__do_special_page('sms', {
            'phoneNumber': phoneNumber,
            'text': text,
        })
        
    def search(self, query):
        """
        Search your Google Voice Account history for calls, voicemails, and sms
        Returns formatted dict of anything matching query
        """
        return self.__multiformat('search', data='?q=%s'%quote(query))()
        
    def download(self, msg, adir=None):
        """
        Download a voicemail or recorded call MP3 matching the given msg sha1 hash
        Saves files to adir (default current directory)
        Message hashes can be found in list(self.voicemail()['messages'])
        Returns location of saved file
        """
        from os import path,getcwd
        assert is_sha1(msg), 'Message id not a SHA1 hash'
        if adir is None:
            adir = getcwd()
        fn = path.join(adir, '%s.mp3' % msg)
        fo = open(fn, 'wb')
        fo.write(self.__do_page('download', msg).read())
        fo.close()
        return fn

    ######################
    # Experimental methods
    ######################
    @property
    def _balance(self):
        """
        Returns current account balance
        """
        if self.special:
            return self.__do_special_page('BALANCE').read()
    
    def _delete(self, *msgs):
        """
        Moves any messages indicated by sha1 hash to the Trash
        """
        self.__messages_post('delete', trash=1, *msgs)
        
    def _star(self, *msgs):
        """
        Star a list of messages
        """
        self.__messages_post('star', star=1, *msgs)

    ######################
    # Helper methods
    ######################
    def __do_page(self, page, data=None, headers={}):
        """
        Loads a page out of the settings and pass it on to urllib Request
        """
        page = page.upper()
        if isinstance(data, dict) or isinstance(data, tuple):
            data = urlencode(data)
        if page in ('DOWNLOAD','XML_SEARCH'):
            return urlopen(Request(getattr(settings, page) + data))
        return urlopen(Request(getattr(settings, page), data, headers))

    def __do_special_page(self, page, data=None, headers={}):
        """
        Add self.special to request data
        """
        if isinstance(data, tuple):
            data += ('_rnr_se', self.special)
        elif isinstance(data, dict):
            data.update({'_rnr_se': self.special})
        return self.__do_page(page, data, headers)
    
    def __do_xml_page(self, page, data=None, headers={}):
        """
        Parses XML folder page (eg inbox,voicemail,sms,etc)
        Returns a str tuple (json format, html format)
        """
        return XMLParser(self.__do_special_page('XML_%s' % page.upper(), data, headers).read())()
    
    def __multiformat(self, page, format='json', data=None, headers={}):
        """
        Uses json/simplejson to load given format from folder page
        Returns wrapped function available at self.
        """
        def inner():
            '''Formatted %s for the %s''' % (format.upper(), page.title())
            if format == 'json':
                return load(StringIO(self.__do_xml_page(page, data, headers)[0]))
            else:
                return self.__do_xml_page(page, data, headers)[1]
        return inner
  
    def __messages_post(self, page, *msgs, **kwargs):
        """
        Performs message operations, eg deleting,staring,moving
        """
        data = kwargs.items()
        for msg in msgs:
            assert is_sha1(msg), 'Message id not a SHA1 hash'
            data += ('messages',msg)
        return self.__do_special_page(page, data)   