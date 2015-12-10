from conf import config
from util import *
import settings
import base64

qpat = re.compile(r'\?')

if settings.DEBUG:
    import logging
    logging.basicConfig()
    log = logging.getLogger('PyGoogleVoice')
    log.setLevel(logging.DEBUG)
else:
    log = None


class Voice(object):
    """
    Main voice instance for interacting with the Google Voice service
    Handles login/logout and most of the baser HTTP methods
    """
    def __init__(self):
        install_opener(build_opener(HTTPCookieProcessor(CookieJar())))

        for name in settings.FEEDS:
            setattr(self, name, self.__get_xml_page(name))

        setattr(self, 'message', self.__get_xml_page('message'))

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

    def login(self, email=None, passwd=None, smsKey=None):
        """
        Login to the service using your Google Voice account
        Credentials will be propmpted for if not given as args or in the ``~/.gvoice`` config file
        """
        if hasattr(self, '_special') and getattr(self, '_special'):
            return self

        if email is None:
            email = config.email
        if email is None:
            email = input('Email address: ')

        if passwd is None:
            passwd = config.password
        if passwd is None:
            from getpass import getpass
            passwd = getpass()

        content = self.__do_page('login').read()
        # holy hackjob
        galx = re.search(r"type=\"hidden\"\s+name=\"GALX\"\s+value=\"(.+)\"", content).group(1)
        result = self.__do_page('login', {'Email': email, 'Passwd': passwd, 'GALX': galx})

        if result.geturl().startswith(getattr(settings, "SMSAUTH")):
            content = self.__smsAuth(smsKey)

            try:
                smsToken = re.search(r"name=\"smsToken\"\s+value=\"([^\"]+)\"", content).group(1)
                galx = re.search(r"name=\"GALX\"\s+value=\"([^\"]+)\"", content).group(1)
                content = self.__do_page('login', {'smsToken': smsToken, 'service': "grandcentral", 'GALX': galx})
            except AttributeError:
                raise LoginError

            del smsKey, smsToken, galx

        del email, passwd

        try:
            assert self.special
        except (AssertionError, AttributeError):
            raise LoginError

        return self

    def __smsAuth(self, smsKey=None):
        if smsKey is None:
            smsKey = config.smsKey

        if smsKey is None:
            from getpass import getpass
            smsPin = getpass("SMS PIN: ")
            content = self.__do_page('smsauth', {'smsUserPin': smsPin}).read()

        else:
            smsKey = base64.b32decode(re.sub(r' ', '', smsKey), casefold=True).encode("hex")
            content = self.__oathtoolAuth(smsKey)

            try_count = 1

            while "The code you entered didn&#39;t verify." in content and try_count < 5:
                sleep_seconds = 10
                try_count += 1
                print('invalid code, retrying after %s seconds (attempt %s)' % (sleep_seconds, try_count))
                import time
                time.sleep(sleep_seconds)
                content = self.__oathtoolAuth(smsKey)

        del smsKey

        return content

    def __oathtoolAuth(self, smsKey):
        import commands
        smsPin = commands.getstatusoutput('oathtool --totp ' + smsKey)[1]
        content = self.__do_page('smsauth', {'smsUserPin': smsPin}).read()
        del smsPin
        return content

    def logout(self):
        """
        Logs out an instance and makes sure it does not still have a session
        """
        self.__do_page('logout')
        del self._special
        assert self.special == None
        return self

    def call(self, outgoingNumber, forwardingNumber=None, phoneType=None, subscriberNumber=None):
        """
        Make a call to an ``outgoingNumber`` from your ``forwardingNumber`` (optional).
        If you pass in your ``forwardingNumber``, please also pass in the correct ``phoneType``
        """
        if forwardingNumber is None:
            forwardingNumber = config.forwardingNumber
        if phoneType is None:
            phoneType = config.phoneType

        self.__validate_special_page('call', {
            'outgoingNumber': outgoingNumber,
            'forwardingNumber': forwardingNumber,
            'subscriberNumber': subscriberNumber or 'undefined',
            'phoneType': phoneType,
            'remember': '1'
        })

    __call__ = call

    def cancel(self, outgoingNumber=None, forwardingNumber=None):
        """
        Cancels a call matching outgoing and forwarding numbers (if given).
        Will raise an error if no matching call is being placed
        """
        self.__validate_special_page('cancel', {
            'outgoingNumber': outgoingNumber or 'undefined',
            'forwardingNumber': forwardingNumber or 'undefined',
            'cancelType': 'C2C',
        })

    def phones(self):
        """
        Returns a list of ``Phone`` instances attached to your account.
        """
        return [Phone(self, data) for data in self.contacts['phones'].values()]
    phones = property(phones)

    def settings(self):
        """
        Dict of current Google Voice settings
        """
        return AttrDict(self.contacts['settings'])
    settings = property(settings)

    def send_sms(self, phoneNumber, text):
        """
        Send an SMS message to a given ``phoneNumber`` with the given ``text`` message
        """
        self.__validate_special_page('sms', {'phoneNumber': phoneNumber, 'text': text})

    def search(self, query):
        """
        Search your Google Voice Account history for calls, voicemails, and sms
        Returns ``Folder`` instance containting matching messages
        """
        return self.__get_xml_page('search', data='?q=%s' % quote(query))()

    def archive(self, msg, archive=1):
        """
        Archive the specified message by removing it from the Inbox.
        """
        if isinstance(msg, Message):
            msg = msg.id
        assert is_sha1(msg), 'Message id not a SHA1 hash'
        self.__messages_post('archive', msg, archive=archive)

    def delete(self, msg, trash=1):
        """
        Moves this message to the Trash. Use ``message.delete(0)`` to move it out of the Trash.
        """
        if isinstance(msg, Message):
            msg = msg.id
        assert is_sha1(msg), 'Message id not a SHA1 hash'
        self.__messages_post('delete', msg, trash=trash)

    def download(self, msg, adir=None):
        """
        Download a voicemail or recorded call MP3 matching the given ``msg``
        which can either be a ``Message`` instance, or a SHA1 identifier.
        Saves files to ``adir`` (defaults to current directory).
        Message hashes can be found in ``self.voicemail().messages`` for example.
        Returns location of saved file.
        """
        from os import path, getcwd
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
        with open(fn, 'wb') as fo:
            fo.write(response.read())
        return fn

    def contacts(self):
        """
        Partial data of your Google Account Contacts related to your Voice account.
        For a more comprehensive suite of APIs, check out http://code.google.com/apis/contacts/docs/1.0/developers_guide_python.html
        """
        if hasattr(self, '_contacts'):
            return self._contacts
        self._contacts = self.__get_xml_page('contacts')()
        return self._contacts
    contacts = property(contacts)

    ######################
    # Helper methods
    ######################

    def __do_page(self, page, data=None, headers={}, terms={}):
        """
        Loads a page out of the settings and pass it on to urllib Request
        """
        page = page.upper()
        if isinstance(data, dict) or isinstance(data, tuple):
            data = urlencode(data)
        headers.update({'User-Agent': 'PyGoogleVoice/0.5'})
        if log:
            log.debug('%s?%s - %s' % (getattr(settings, page)[22:], data or '', headers))
        if page in ('DOWNLOAD', 'XML_SEARCH'):
            return urlopen(Request(getattr(settings, page) + data, None, headers))
        if data:
            headers.update({'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'})
        pageuri = getattr(settings, page)
        if len(terms) > 0:
            m = qpat.match(page)
            if m:
                pageuri += '&'
            else:
                pageuri += '?'
            for i, k in enumerate(terms.keys()):
                pageuri += k + '=' + terms[k]
                if i < len(terms) - 1:
                    pageuri += '&'
        return urlopen(Request(pageuri, data, headers))

    def __validate_special_page(self, page, data={}, **kwargs):
        """
        Validates a given special page for an 'ok' response
        """
        data.update(kwargs)
        load_and_validate(self.__do_special_page(page, data))

    _Phone__validate_special_page = __validate_special_page

    def __do_special_page(self, page, data=None, headers={}, terms={}):
        """
        Add self.special to request data
        """
        assert self.special, 'You must login before using this page'
        if isinstance(data, tuple):
            data += ('_rnr_se', self.special)
        elif isinstance(data, dict):
            data.update({'_rnr_se': self.special})
        return self.__do_page(page, data, headers, terms)

    _Phone__do_special_page = __do_special_page

    def __get_xml_page(self, page, data=None, headers={}):
        """
        Return XMLParser instance generated from given page
        """
        return XMLParser(self, page, lambda terms={}: self.__do_special_page('XML_%s' % page.upper(), data, headers, terms).read())

    def __messages_post(self, page, *msgs, **kwargs):
        """
        Performs message operations, eg deleting,staring,moving
        """
        data = kwargs.items()
        for msg in msgs:
            if isinstance(msg, Message):
                msg = msg.id
            assert is_sha1(msg), 'Message id not a SHA1 hash'
            data += (('messages', msg),)
        return self.__do_special_page(page, dict(data))

    _Message__messages_post = __messages_post
