from googlevoice import Voice
from googlevoice.util import input


def test_call():
    # assert inc(3) == 5

    voice = Voice()
    # voice.login()

    outgoingNumber = "18005551212" # input('Number to call: ')
    forwardingNumber = None # input('Number to call from [optional]: ') or None

    voice.call(outgoingNumber, forwardingNumber)

    """
    if input('Calling now... cancel?[y/N] ').lower() == 'y':
        voice.cancel(outgoingNumber, forwardingNumber)
    """

    assert 1 == 1
