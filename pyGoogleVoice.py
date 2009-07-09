###
#    Copyright 2009 Joseph McCall
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

import cookielib
import re
import urllib
import urllib2

loginURL="https://www.google.com/accounts/ServiceLoginAuth?service=grandcentral"
logoutURL="https://www.google.com/voice/account/signout"
inboxURL="https://www.google.com/voice/#inbox"
usernameField="Email"
passwordField="Passwd"

cj=cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def login(Email, Passwd):
    url = loginURL
    values = {'Email':Email,
              'Passwd':Passwd}
    headers = {'Content-Type':'application/x-www-form-urlencoded'}

    data = urllib.urlencode(values)
    loginRequest = urllib2.Request(url, data, headers)
    loginResponse = urllib2.urlopen(loginRequest)

def getSpecialKey():
    inboxResponse = urllib2.urlopen(inboxURL)
    responseText = inboxResponse.read()
    global specialKey
    match = re.search("('_rnr_se':) '(.+)'", responseText)
    specialKey = match.group(2)

def logout():
    logoutResponse = urllib2.urlopen(logoutURL)

def placeCall(toNumber, fromNumber):
    """
    POST /voice/call/connect/ outgoingNumber=[number to call]&forwardingNumber=[forwarding number]&subscriberNumber=undefined&remember=0&_rnr_se=[pull from page]
    """
    getSpecialKey()
    url = "https://www.google.com/voice/call/connect/"
    values = {'outgoingNumber':toNumber,
              'forwardingNumber':fromNumber,
              'subscriberNumber':'undefined',
              'remember':'0',
              '_rnr_se':specialKey}
              
    data = urllib.urlencode(values)
    placeCallRequest = urllib2.Request(url, data)
    placeCallResponse = urllib2.urlopen(placeCallRequest)
              
              
