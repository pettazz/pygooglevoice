from googlevoice import Voice,util

voice = Voice()
voice.login()

folder = voice.search(util.input('Search query: '))

util.pprint('Found %s messages:' % len(folder))
util.pprint(folder.messages)