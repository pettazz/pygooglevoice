import pprint

from googlevoice import Voice


def run():
    voice = Voice()
    voice.login()

    pprint.pprint(voice.settings)


__name__ == '__main__' and run()
