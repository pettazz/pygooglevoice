import re
from sys import stdout
from xml.parsers.expat import ParserCreate
from pprint import pprint
try:
    from urllib2 import build_opener,install_opener, \
        HTTPCookieProcessor,Request,urlopen
    from urllib import urlencode,quote
except ImportError:
    from urllib.request import build_opener,install_opener, \
        HTTPCookieProcessor,Request,urlopen
    from urllib.parse import urlencode,quote
try:
    from http.cookiejar import LWPCookieJar as CookieJar
except ImportError:
    from cookielib import LWPCookieJar as CookieJar
try:
    from json import loads
except ImportError:
    from simplejson import loads
try:
    input = raw_input
except NameError:
    input = input

sha1_re = re.compile(r'^[a-fA-F0-9]{40}$')

def print_(*values, **kwargs):
    """
    Implementation of Python3's print function
    
    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file: a file-like object (stream); defaults to the current sys.stdout.
    sep:  string inserted between values, default a space.
    end:  string appended after the last value, default a newline.
    """
    fo = kwargs.pop('file', stdout)
    fo.write(kwargs.pop('sep', ' ').join(map(str, values)))
    fo.write(kwargs.pop('end', '\n'))
    fo.flush()

def is_sha1(s):
    """
    Returns True if the string is a SHA1 hash
    """
    return bool(sha1_re.match(s))

def validate_response(response):
    """
    Validates that the JSON response is A-OK
    """
    try:
        assert 'ok' in response and response['ok']
    except AssertionError:
        raise ValidationError('There was a problem with GV: %s' % response)

def load_and_validate(response):
    """
    Loads JSON data from http response then validates
    """
    validate_response(loads(response.read()))

class ValidationError(Exception):
    """
    Bombs when response code back from Voice 500s
    """

class LoginError(Exception):
    """
    Occurs when login credentials are incorrect
    """
    
class ParsingError(Exception):
    """
    Happens when XML feed parsing fails
    """
    
class JSONError(Exception):
    """
    Failed JSON deserialization
    """
    
class DownloadError(Exception):
    """
    Cannot download message, probably not in voicemail/recorded
    """
    
class ForwardingError(Exception):
    """
    Forwarding number given was incorrect
    """
    
class XMLParser(dict):
    """
    XML Parser helper that can dig json and html out of the feeds
    Calling the parser returns a tuple of (data_dict, html_content)
    """
    attr = None
        
    def start_element(self, name, attrs):
        if name in ('json','html'):
            self.attr = name
    def end_element(self, name): self.attr = None
    def char_data(self, data):
        if self.attr and data:
            self[self.attr] += data

    def __init__(self, data):
        dict.__init__(self, {'json':'', 'html':''})
        p = ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        try:
            p.Parse(data, 1)
        except:
            raise ParsingError

    def __call__(self):
        try:
            return loads(self['json']), self['html']
        except Exception:
            raise JSONError