__all__ = ['Voice','util','settings','tests']
__author__ = 'Justin Quick and Joe McCall'
__email__ = 'justquick@gmail.com, joe@mcc4ll.us',
__copyright__ = 'Copyright 2009, Justin Quick and Joe McCall'
__credits__ = ['Justin Quick','Joe McCall','Jacob Feisley']
__license__ = 'New BSD'
__version__ = '0.3'
__doc__ = '''
PyGoogleVoice: %(__copyright__)s
Version: %(__version__)s

This project aims to bring the power of the Google Voice API to the Python language in a simple,
easy-to-use manner. Currently it allows you to place calls, send sms,
download voicemails/recorded messages, and search the various folders of your Google Voice Accounts.
You can use the Python API or command line script to schedule calls, check for new received calls/sms,
or even sync your recorded voicemails/calls.
Works for Python 2 and Python 3

Contact: %(__email__)s
''' % locals()

from time import gmtime
from datetime import datetime

from googlevoice import settings
from googlevoice.util import *

class Voice(object):
    '''
    Main voice instance for interacting with the Google Voice service
    Also contains callable methods for each folder (eg inbox,voicemail,sms,etc)
    '''
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
        '''
        Returns special identifier for your session (if logged in)
        '''
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
        '''
        Login to the service using your Google Voice account
        Credentials will be propmpted for if not given
        '''
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
        '''
        Logs out an instance and makes sure it does not still have a session
        '''
        urlopen(settings.LOGOUT)
        del self._special 
        assert self.special == None
    
    def call(self, outgoingNumber, forwardingNumber, subscriberNumber=None):
        '''
        Make a call to an outgoing number using your forwarding number
        '''
        response = loads(self.__do_special_page('call', {
            'outgoingNumber':outgoingNumber,
            'forwardingNumber':forwardingNumber,
            'subscriberNumber':subscriberNumber or 'undefined',
            'remember':'1',
        }).read())
        assert 'ok' in response and response['ok'], \
            'There was a problem with your call: %(error)s' % response
        
    __call__ = call
    
    def cancel(self, outgoingNumber=None, forwardingNumber=None):
        '''
        Cancels a call matching outgoing and forwarding numbers (if given)
        Will raise an error if no matching call is being placed
        '''
        response = loads(self.__do_special_page('cancel', {
            'outgoingNumber':outgoingNumber or 'undefined',
            'forwardingNumber':forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        }).read())
        assert 'ok' in response and response['ok'], \
            'There was a problem with canceling your call: %(error)s' % response
        
    @property
    def phones(self):
        '''
        Returns a dict of your Google Voice phone numbers
        '''
        return self._contacts['phones']
    
    @property
    def settings(self):
        '''
        Returns a dict of current Google Voice settings
        '''
        return self._contacts['settings']
    
    def send_sms(self, phoneNumber, text):
        '''
        Send an SMS message to a given phone number with the given text message
        '''
        response = loads(self.__do_special_page('sms', {
            'phoneNumber': phoneNumber,
            'text': text,
        }).read())
        assert 'ok' in response and response['ok'], \
            'There was a problem with your sms: %(error)s' % response
        
    def search(self, query):
        '''
        Search your Google Voice Account history for calls, voicemails, and sms
        Returns Folder instance containting matching messages
        '''
        return Folder(self, 'search', self.__multiformat('search',
                                    data='?q=%s' % quote(query))())
        
    def download(self, msg, adir=None):
        '''
        Download a voicemail or recorded call MP3 matching the given msg sha1 hash
        Saves files to adir (default current directory)
        Message hashes can be found in self.voicemail().messages
        Returns location of saved file
        '''
        from os import path,getcwd
        if isinstance(msg, Message):
            msg = msg.id
        assert is_sha1(msg), 'Message id not a SHA1 hash'
        if adir is None:
            adir = getcwd()
        try:
            response = self.__do_page('download', msg)
        except:
            raise DownloadError
        fn = path.join(adir, '%s.mp3' % msg)
        fo = open(fn, 'wb')
        fo.write(response.read())
        fo.close()
        return fn

    ######################
    # Experimental methods
    ######################
    def _delete(self, *msgs):
        '''
        Moves any messages indicated by sha1 hash to the Trash
        '''
        self.__messages_post('delete', trash=1, *msgs)
        
    def _star(self, *msgs):
        '''
        Star a list of messages
        '''
        self.__messages_post('star', star=1, *msgs)

    ######################
    # Helper methods
    ######################
    @property
    def _contacts(self):
        '''
        Caches XML contacts page
        '''
        if hasattr(self, '__contacts'):
            return self.__contacts
        self.__contacts = self.__do_xml_page('contacts')[0]
        return self.__contacts
    
    def __do_page(self, page, data=None, headers={}):
        '''
        Loads a page out of the settings and pass it on to urllib Request
        '''
        page = page.upper()
        if isinstance(data, dict) or isinstance(data, tuple):
            data = urlencode(data)
        headers.update({'User-Agent': 'PyGoogleVoice/%s' % __version__})
        if page in ('DOWNLOAD','XML_SEARCH'):
            return urlopen(Request(getattr(settings, page) + data, None, headers))
        if data:
            headers.update({'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'})
        return urlopen(Request(getattr(settings, page), data, headers))

    def __do_special_page(self, page, data=None, headers={}):
        '''
        Add self.special to request data
        '''
        assert self.special, 'You must login before using this page'
        if isinstance(data, tuple):
            data += ('_rnr_se', self.special)
        elif isinstance(data, dict):
            data.update({'_rnr_se': self.special})
        return self.__do_page(page, data, headers)
    
    def __do_xml_page(self, page, data=None, headers={}):
        '''
        Parses XML folder page (eg inbox,voicemail,sms,etc)
        Returns a str tuple (json dict, html string)
        '''
        return XMLParser(self.__do_special_page(
            'XML_%s' % page.upper(), data, headers).read())()
    
    def __multiformat(self, page, format='json', data=None, headers={}):
        '''
        Uses json/simplejson to load given format from folder page
        Returns wrapped function available at self.
        '''
        def inner():
            '''Formatted %s for the %s''' % (format.upper(), page.title())
            if format == 'json':
                return Folder(self, page.lower(),
                        self.__do_xml_page(page, data, headers)[0])
            else:
                return self.__do_xml_page(page, data, headers)[1]
        return inner
  
    def __messages_post(self, page, *msgs, **kwargs):
        '''
        Performs message operations, eg deleting,staring,moving
        '''
        data = kwargs.items()
        for msg in msgs:
            if isinstance(msg, Message):
                msg = msg.id
            assert is_sha1(msg), 'Message id not a SHA1 hash'
            data += ('messages',msg)
        return self.__do_special_page(page, data)

class AttrDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]    
  
class Message(AttrDict):
    '''
    Wrapper for all call/sms message instances stored in Google Voice
    Attributes are:
        id: SHA1 identifier
        isTrash: bool
        displayStartDateTime: datetime
        star: bool
        isSpam: bool
        startTime: gmtime
        labels: list
        displayStartTime: time
        children: str
        note: str
        isRead: bool
        displayNumber: str
        relativeStartTime: str
        phoneNumber: str
        type: int
    '''
    def __init__(self, folder, id, data):
        assert is_sha1(id), 'Message id not a SHA1 hash'
        self.folder = folder
        self.id = id
        super(AttrDict, self).__init__(data)
        self['startTime'] = gmtime(int(self['startTime'])/1000)
        self['displayStartDateTime'] = datetime.strptime(
                self['displayStartDateTime'], '%m/%d/%y %I:%M %p')
        self['displayStartTime'] = self['displayStartDateTime'].time()

    def download(self, adir=None):
        '''
        Download this message to adir
        Same as Voice.download
        '''
        return self.folder.voice.download(self, adir)

    def __str__(self):
        return self.id
    
    def __repr__(self):
        return '<Message #%s (%s)>' % (self.id, self.phoneNumber)

class Folder(AttrDict):
    '''
    Folder wrapper for feeds from Google Voice
    Attributes are:
        totalSize: int (aka __len__)
        unreadCounts: dict
        resultsPerPage: int
        messages: list of Message instances
    '''
    def __init__(self, voice, name, data):
        self.voice = voice
        self.name = name
        super(AttrDict, self).__init__(data)
        
    @property
    def messages(self):
        return [Message(self, *i) for i in self['messages'].items()]
        
    def __len__(self):
        return self['totalSize']

    def __repr__(self):
        return '<Folder %s (%s)>' % (self.name, len(self))