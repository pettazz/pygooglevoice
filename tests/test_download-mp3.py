from googlevoice import Voice

def test_download_mp3():
    download_dir = '.'

    voice = Voice()
    # voice.login()

    #for message in voice.voicemail().messages:
    #    message.download(download_dir)

    assert 1 == 1