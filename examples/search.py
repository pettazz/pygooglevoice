from googlevoice import Voice,util


voice = Voice()
voice.login()

folder = voice.search(util.input('Search query: '))

util.print_('Found %s messages: ', len(folder))
util.pprint(folder.messages)