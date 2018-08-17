from __future__ import print_function

from googlevoice import Voice, settings

voice = Voice()
voice.login()

for feed in settings.FEEDS:
    print(feed.title())
    for message in getattr(voice, feed)().messages:
        print('\t', message)
