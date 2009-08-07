from googlevoice import Voice

download_dir = '.'

voice = Voice()
voice.login()

for message in voice.voicemail().messages:
    message.download(download_dir)