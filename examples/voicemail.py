from __future__ import print_function

from googlevoice import Voice


def run():
    voice = Voice()
    voice.login()

    for message in voice.voicemail().messages:
        print(message)


__name__ == '__main__' and run()
