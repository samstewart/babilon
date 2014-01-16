#!/bin/python
# -*- coding: utf-8 -*- 

# Simple script to download pronunciation guides for words
# Reference for Anki media: http://www.martinogg.com/2013/01/create-anki-deck-tutorial-part3/
# TODO: Package as greesemonkey script for quizlet?

import csv
import urllib2
import urllib
import hashlib
from os.path import expanduser

MEDIA_LIB_PREFIX = expanduser('~/Documents/Anki/User 1/collection.media/')

print MEDIA_LIB_PREFIX

def addPronunciations(fname):
	with open(fname, 'rb') as infile:
		reader = csv.reader(infile, delimiter="\t")
		
		with open('with_pronunciations_' + fname, 'w') as outfile:
			writer = csv.writer(outfile, delimiter="\t")

			for r in reader:

				fname = downloadPronunciation('hu', r[0].decode('utf-8'))
				r[0] = "%s [sound:%s]" % (r[0], fname)

				writer.writerow(r)


# downloads the word pronunciation and returns the new file output (relative to the media folder)
def downloadPronunciation(language, word):

	language = language.lower()
	word = urllib.quote(word.encode('utf-8'))

	headers = { 'User-Agent': 'Mozilla/5.0' }

	url = 'http://translate.google.com/translate_tts?ie=UTF-8&tl=%s&q=%s' % (language, word)
	
	mp3 = urllib2.Request(url, None, headers)

	mp3 = urllib2.urlopen(mp3)

	fname = hashlib.md5()
	fname.update(word)

	slug = fname.hexdigest() + ".mp3"

	fname = MEDIA_LIB_PREFIX + slug

	f = open(fname, 'wb')
	f.write(mp3.read())
	f.close()

	return slug

# downloadPronunciation('hu', u'Van egy kérdésem')

# TODO: hook into Quizlet api
def downloadFlashcards(name):
	pass


addPronunciations("hungarian_1.csv")