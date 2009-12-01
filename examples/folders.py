from googlevoice import Voice,util,settings

voice = Voice()
voice.login()

for feed in settings.FEEDS:
    util.print_(feed.title())
    for message in getattr(voice, feed)().messages:
        util.print_('\t', message)