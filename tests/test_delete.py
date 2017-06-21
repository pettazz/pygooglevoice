from googlevoice import Voice

def test_delete:
    voice = Voice()
    # voice.login()

    for message in voice.sms().messages:
        if message.isRead:
            message.delete()

    assert 1 == 1