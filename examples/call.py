from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

outgoingNumber = input('Number to call: ')
forwardingNumber = input('Number to call from [optional]: ') or None

voice.call(outgoingNumber, forwardingNumber)

if input('Calling now... cancel?[y/N] ').lower() == 'y':
    voice.cancel(outgoingNumber, forwardingNumber)