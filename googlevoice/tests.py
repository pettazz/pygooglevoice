from googlevoice import Voice,util
from os import path,remove
from unittest import TestCase,main

class VoiceTest(TestCase):
    voice = Voice()
    voice.login()
    outgoing = util.input('Outgoing number: ')
    forwarding = util.input('Forwarding number: ')
    
    def test_special(self):
        self.assert_(self.voice.special)
    
    if outgoing and forwarding:
        def test_1call(self):
            self.voice.call(self.outgoing, self.forwarding)

        def test_sms(self):
            self.voice.send_sms(self.outgoing, 'i sms u')

        def test_2cancel(self):
            self.voice.cancel(self.outgoing, self.forwarding)

    def test_inbox(self):
        self.assert_(self.voice.inbox())
    
    def test_balance(self):
        util.pprint(self.voice.balance())
        self.assert_(self.voice.balance())
        
    def test_search(self):
        util.pprint(self.voice.search('joe'))
    
    def test_download(self):
        msg = list(self.voice.voicemail()['messages'])[0]
        if path.isfile('%s.mp3' % msg): remove('%s.mp3' % msg)
        self.voice.download(msg)
        self.assert_(path.isfile('%s.mp3' % msg))
    
    def test_zlogout(self):
        self.voice.logout()
        self.assert_(self.voice.special is None)
        
if __name__ == '__main__': main()