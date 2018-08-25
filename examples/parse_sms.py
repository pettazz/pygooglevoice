#
# SMS test via Google Voice
#
# John Nagle
#   nagle@animats.com
#
from googlevoice import Voice
import BeautifulSoup


def extractsms(htmlsms):
    """
    extractsms  --  extract SMS messages from BeautifulSoup
    tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    # Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div", attrs={"id": True}, recursive=False)
    for conversation in conversations:
        # For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class": "gc-message-sms-row"})
        for row in rows:								# for all rows
            # For each row, which is one message, extract all the fields.
            # tag this message with conversation ID
            msgitem = {"id": conversation["id"]}
            spans = row.findAll("span", attrs={"class": True}, recursive=False)
            for span in spans:							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                # put text in dict
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems


def run():
    voice = Voice()
    voice.login()

    voice.sms()
    for msg in extractsms(voice.sms.html):
        print(msg)


__name__ == '__main__' and run()
