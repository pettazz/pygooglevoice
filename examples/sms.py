from six.moves import input
from googlevoice import Voice

voice = Voice()
voice.login()

phoneNumber = input('Number to send message to: ')
text = input('Message text: ')

voice.send_sms(phoneNumber, text)
