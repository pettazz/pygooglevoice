from googlevoice import Voice,util

voice = Voice()
voice.login()

util.pprint(voice._balance())