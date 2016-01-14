#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import urllib, urllib2
import traceback, time, random, datetime
from urlparse import urlparse, parse_qs
from urllib import urlencode
from os import getenv
import sys

randomSleep = 0

while True:
	try:
		# Get username and password from shell environment passwords
		FON_USERNAME = getenv('FON_USERNAME')
		FON_PASSWORD = getenv('FON_PASSWORD')
		
		print datetime.date.today(), " sleeping time ", randomSleep, "... "
		if randomSleep > 10:
			randomSleep = random.randint(4,10)
		time.sleep(randomSleep)
		#Pass arguments option
		if len(sys.argv) < 2 and (not FON_USERNAME or not FON_PASSWORD):
			print "Command: python zon_fon_authenticate.py <LOGIN> <PASSWORD>";
			continue
		
		FON_USERNAME = sys.argv[1]
		FON_PASSWORD = sys.argv[2]
		
		# Attempt to fetch the START_URL in order to be redirected
		# to the Zon@Fon authetincation page
		START_URL = 'http://www.sapo.pt'
		
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		urllib2.install_opener(opener)
		data = urllib2.urlopen(START_URL,timeout=10)
		
		auth_url = data.geturl()
		if not auth_url.startswith('https://zon.portal.fon.com/') and not auth_url.startswith('https://nos.portal.fon.com'):
			print "Zon fon authentication was not requested. Already authenticated?"
			randomSleep = random.randint(4,10)
			continue
		
		# Build the POST URL from the redirect location
		url_data = parse_qs(urlparse(auth_url).query, keep_blank_values=True)
		fields = [ 'nasid', 'uamip', 'uamport', 'mac', 'challenge' ]
		str_data = 'res=login'
		for f in fields:
			str_data += '&%s=%s' % (f, url_data[f][0])
		str_data += '&tab=2'
		url = "%s://%s%s?%s" % (urlparse(auth_url).scheme, urlparse(auth_url).netloc, urlparse(auth_url).path, str_data)
		
		html = urllib2.urlopen(url,
		 data=urllib.urlencode({'USERNAME': FON_USERNAME, 'PASSWORD': FON_PASSWORD}),timeout=10)
		html_data = html.read()
		
		# Check the result
		if 'Incorrect username or password' in html_data:
			print "Login failed, check username/password!"
			randomSleep = 10
			continue
		elif "'You're connected!":
			print "You are now connected"
			randomSleep = random.randint(4,10)
			continue
		else:
			print "Something failed"
			randomSleep = 0
			continue
	except Exception:
		print "Without internet?"
		print(traceback.format_exc())
		randomSleep = 0