from googlevoice import Voice
from googlevoice.util import input

voice = Voice()
voice.login()

phoneNumber = input('Number to send message to: ')
text = input('Message text: ')

voice.send_sms(phoneNumber, text)