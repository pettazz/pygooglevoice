from __future__ import print_function

from googlevoice import Voice, settings


def run():
    voice = Voice()
    voice.login()

    for feed in settings.FEEDS:
        print(feed.title())
        for message in getattr(voice, feed)().messages:
            print('\t', message)


__name__ == '__main__' and run()
