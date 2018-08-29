from six.moves import input

from googlevoice import Voice


def run():
    voice = Voice()
    voice.login()

    outgoingNumber = input('Number to call: ')
    forwardingNumber = input('Number to call from [optional]: ') or None

    voice.call(outgoingNumber, forwardingNumber)

    if input('Calling now... cancel?[y/N] ').lower() == 'y':
        voice.cancel(outgoingNumber, forwardingNumber)


__name__ == '__main__' and run()
