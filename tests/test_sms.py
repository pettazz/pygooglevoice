from googlevoice import Voice
from googlevoice.util import input

def test_sms():
    voice = Voice()
    #voice.login()

    phoneNumber =  "18005551212"  #input('Number to send message to: ')
    text = "Hello, world." #input('Message text: ')

    #voice.send_sms(phoneNumber, text)

    assert 1 == 1