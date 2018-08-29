from __future__ import print_function

import pprint

from six.moves import input

from googlevoice import Voice


def run():
	voice = Voice()
	voice.login()

	folder = voice.search(input('Search query: '))

	print('Found %s messages: ', len(folder))
	pprint.pprint(folder.messages)


__name__ == '__main__' and run()
