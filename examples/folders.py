from googlevoice import Voice,util

voice = Voice()
voice.login()

util.pprint(getattr(voice,util.input('Folder to browse: '))())