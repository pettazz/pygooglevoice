from googlevoice import Voice,util,settings

voice = Voice()
voice.login()

for feed in settings.FEEDS:
    folder = getattr(voice,feed)()
    util.pprint(feed)
    util.pprint(.messages,indent=2)