from __future__ import print_function

from googlevoice import Voice

voice = Voice()
voice.login()

for message in voice.voicemail().messages:
    print(message)
