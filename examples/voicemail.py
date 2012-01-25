from googlevoice import Voice,util

voice = Voice()
voice.login()

for message in voice.voicemail().messages:
    util.print_(message)