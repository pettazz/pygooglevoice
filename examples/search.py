from __future__ import print_function

import pprint

from six.moves import input

from googlevoice import Voice

voice = Voice()
voice.login()

folder = voice.search(input('Search query: '))

print('Found %s messages: ', len(folder))
pprint.pprint(folder.messages)
