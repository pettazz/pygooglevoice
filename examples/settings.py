import pprint

from googlevoice import Voice


voice = Voice()
voice.login()

pprint.pprint(voice.settings)
