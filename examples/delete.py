from googlevoice import Voice


def run():
    voice = Voice()
    voice.login()

    for message in voice.sms().messages:
        if message.isRead:
            message.delete()


__name__ == '__main__' and run()
