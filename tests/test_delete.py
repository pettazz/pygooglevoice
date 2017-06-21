from googlevoice import Voice

voice = Voice()
voice.login()

for message in voice.sms().messages:
    if message.isRead:
        message.delete()