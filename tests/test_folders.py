from googlevoice import Voice,util,settings

def test_folders():
    voice = Voice()
    # voice.login()

    #for feed in settings.FEEDS:
    #    util.print_(feed.title())
    #    for message in getattr(voice, feed)().messages:
    #        util.print_('\t', message)

    assert 1 == 1