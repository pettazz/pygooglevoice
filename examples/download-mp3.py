from googlevoice import Voice


def run():
    download_dir = '.'

    voice = Voice()
    voice.login()

    for message in voice.voicemail().messages:
        message.download(download_dir)


__name__ == '__main__' and run()
