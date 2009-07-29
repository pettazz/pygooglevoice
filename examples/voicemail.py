from googlevoice import Voice

voice = Voice()
voice.login()

for msg in list(voice.voicemail()['messages']):
    voice.download(msg)