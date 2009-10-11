from time import gmtime
from datetime import datetime
from util import *
import settings


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
    special = property(special)
    
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

        content = self.__do_page('login').read()
        galx = re.search(r"name=\"GALX\"\s+value=\"(.+)\"", content).group(1)
        self.__do_page('login', {'Email':email,'Passwd':passwd, 'GALX': galx})
        
        del email,passwd
        
        try:
            assert self.special
        except (AssertionError, AttributeError):
            raise LoginError
        
        return self
        
    def logout(self):
        """
        Logs out an instance and makes sure it does not still have a session
        """
        self.__do_page('logout')
        del self._special 
        assert self.special == None
        return self
    
    def call(self, outgoingNumber, forwardingNumber, subscriberNumber=None):
        """
        Make a call to an outgoing number using your forwarding number
        """
        self.__validate_special_page('call', {
            'outgoingNumber': outgoingNumber,
            'forwardingNumber': forwardingNumber,
            'subscriberNumber': subscriberNumber or 'undefined',
            'remember': '1'
        })
        
    __call__ = call
    
    def cancel(self, outgoingNumber=None, forwardingNumber=None):
        """
        Cancels a call matching outgoing and forwarding numbers (if given)
        Will raise an error if no matching call is being placed
        """
        self.__validate_special_page('cancel', {
            'outgoingNumber': outgoingNumber or 'undefined',
            'forwardingNumber': forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        })

    def phones(self):
        """
        Returns a dict of your Google Voice phone numbers
        """
        return [Phone(self, data) for data in self._contacts['phones'].values()]
    phones = property(phones)

    def settings(self):
        """
        Returns a dict of current Google Voice settings
        """
        return AttrDict(self._contacts['settings'])
    settings = property(settings)
    
    def send_sms(self, phoneNumber, text):
        """
        Send an SMS message to a given phone number with the given text message
        """
        self.__validate_special_page('sms',
            {'phoneNumber': phoneNumber, 'text': text}
        )

    def search(self, query):
        """
        Search your Google Voice Account history for calls, voicemails, and sms
        Returns Folder instance containting matching messages
        """
        return Folder(self, 'search', self.__multiformat('search',
                                    data='?q=%s' % quote(query))())
        
    def download(self, msg, adir=None):
        """
        Download a voicemail or recorded call MP3 matching the given msg sha1 hash
        Saves files to adir (default current directory)
        Message hashes can be found in self.voicemail().messages
        Returns location of saved file
        """
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


    ######################
    # Helper methods
    ######################
    def _contacts(self):
        """
        Caches XML contacts page
        """
        if hasattr(self, '__contacts'):
            return self.__contacts
        self.__contacts = self.__do_xml_page('contacts')[0]
        return self.__contacts
    _contacts = property(_contacts)
    
    def __do_page(self, page, data=None, headers={}):
        """
        Loads a page out of the settings and pass it on to urllib Request
        """
        page = page.upper()
        if isinstance(data, dict) or isinstance(data, tuple):
            data = urlencode(data)
        headers.update({'User-Agent': 'PyGoogleVoice'})
        if page in ('DOWNLOAD','XML_SEARCH'):
            return urlopen(Request(getattr(settings, page) + data, None, headers))
        if data:
            headers.update({'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'})
        return urlopen(Request(getattr(settings, page), data, headers))

    def __validate_special_page(self, page, data={}, **kwargs):
        """
        Validates a given special page for an 'ok' response
        """
        data.update(kwargs)
        load_and_validate(self.__do_special_page(page, data))

    _Phone__validate_special_page = __validate_special_page
    
    def __do_special_page(self, page, data=None, headers={}):
        """
        Add self.special to request data
        """
        assert self.special, 'You must login before using this page'
        if isinstance(data, tuple):
            data += ('_rnr_se', self.special)
        elif isinstance(data, dict):
            data.update({'_rnr_se': self.special})
        return self.__do_page(page, data, headers)
        
    _Phone__do_special_page = __do_special_page
    
    def __do_xml_page(self, page, data=None, headers={}):
        """
        Parses XML folder page (eg inbox,voicemail,sms,etc)
        Returns a str tuple (json dict, html string)
        """
        return XMLParser(self.__do_special_page(
            'XML_%s' % page.upper(), data, headers).read())()
    
    def __multiformat(self, page, format='json', data=None, headers={}):
        """
        Uses json/simplejson to load given format from folder page
        Returns wrapped function available at self.
        """
        def inner():
            """Formatted %s for the %s""" % (format.upper(), page.title())
            if format == 'json':
                return Folder(self, page.lower(),
                        self.__do_xml_page(page, data, headers)[0])
            else:
                return self.__do_xml_page(page, data, headers)[1]
        return inner
  
    def __messages_post(self, page, *msgs, **kwargs):
        """
        Performs message operations, eg deleting,staring,moving
        """
        data = kwargs.items()
        for msg in msgs:
            if isinstance(msg, Message):
                msg = msg.id
            assert is_sha1(msg), 'Message id not a SHA1 hash'
            data += (('messages',msg),)
        return self.__do_special_page(page, dict(data))
    
    _Message__messages_post = __messages_post
    
class AttrDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]

class Phone(AttrDict):
    """
    Wrapper for phone objects used for phone specific methods
    Attributes are:
        id: int
        phoneNumber: i18n phone number
        formattedNumber: humanized phone number string
        we: data dict
        wd: data dict
        verified: bool
        name: strign label
        smsEnabled: bool
        scheduleSet: bool
        policyBitmask: int
        weekdayTimes: list
        dEPRECATEDDisabled: bool
        weekdayAllDay: bool
        telephonyVerified
        weekendTimes: list
        active: bool
        weekendAllDay: bool
        type: int
        enabledForOthers: bool
    """
    def __init__(self, voice, data):
        self.voice = voice
        super(Phone, self).__init__(data)
    
    def enable(self,):
        """
        Enables forwarding to the given phoneNumber
        """
        return self.__call_forwarding()

    def disable(self):
        """
        Disables forwarding to the given phoneNumber
        """
        return self.__call_forwarding('0')
        
    def __call_forwarding(self, enabled='1'):
        """
        Enables or disables your forwarding call numbers
        """
        self.voice.__validate_special_page('default_forward',
            {'enabled':enabled, 'phoneId': self.id}
        )
        
    def __str__(self):
        return self.phoneNumber
    
    def __repr__(self):
        return '<Phone %s>' % self.phoneNumber
        
class Message(AttrDict):
    """
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
    """
    def __init__(self, folder, id, data):
        assert is_sha1(id), 'Message id not a SHA1 hash'
        self.folder = folder
        self.id = id
        super(AttrDict, self).__init__(data)
        self['startTime'] = gmtime(int(self['startTime'])/1000)
        self['displayStartDateTime'] = datetime.strptime(
                self['displayStartDateTime'], '%m/%d/%y %I:%M %p')
        self['displayStartTime'] = self['displayStartDateTime'].time()
    
    def delete(self, trash=1):
        """
        Moves this message to the Trash
        """
        self.folder.voice.__messages_post('delete', self.id, trash=trash)

        
    def star(self, star=1):
        """
        Star this message
        """
        self.folder.voice.__messages_post('star', self.id, star=star)
        
    def mark(self, read=1):
        """
        Mark this message as read or not
        """
        self.folder.voice.__messages_post('mark', self.id, read=read)

        
    def download(self, adir=None):
        """
        Download this message to adir
        """
        return self.folder.voice.download(self, adir)

    def __str__(self):
        return self.id
    
    def __repr__(self):
        return '<Message #%s (%s)>' % (self.id, self.phoneNumber)

class Folder(AttrDict):
    """
    Folder wrapper for feeds from Google Voice
    Attributes are:
        totalSize: int (aka __len__)
        unreadCounts: dict
        resultsPerPage: int
        messages: list of Message instances
    """
    def __init__(self, voice, name, data):
        self.voice = voice
        self.name = name
        super(AttrDict, self).__init__(data)
        
    def messages(self):
        return [Message(self, *i) for i in self['messages'].items()]
    messages = property(messages)
    
    def __len__(self):
        return self['totalSize']

    def __repr__(self):
        return '<Folder %s (%s)>' % (self.name, len(self))