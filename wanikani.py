# wanikani2anki, import unlocked Kanji and Vocab from WaniKani to a
# deck in desktop Anki 2.0.x.  place this file in your desktop Anki 2
# addons folder, then replace YOUR_API_KEY_HERE below with your
# 32-character API key from wanikani (see
# http://www.wanikani.com/account).  Restart Anki 2, and the Tools
# menu will have two new options, "Show WaniKani API Key" and "Update
# WaniKani Deck".

# "Update WaniKani Deck" will create if it does not already exist, or
# add new cards to if it does exist, a deck called "WaniKani".  It
# will try to add Kanji and Vocabulary that you have stats for so
# far. Subsequent runs of "Update WaniKani Deck" will add new Kanji
# and Vocabulary you've learnt since the last run.

# By default it will add a normal card (that will remind of you of how
# WaniKani shows you normally), and a reversed card.  See MODEL_NAME
# below if you just want one card, the WaniKani style.

# Kanji will be added with the kanji itself on one side, onyomi,
# kunyomi, and meaning on the other.  The important reading per
# WaniKani is bolded.

# Vocab will be added with the vocabulary on one side, reading and
# meaning on the other.

# A span element surrounds each side of each card, with two css
# classes applied, one of kanji and vocab, and one of front and back
# (where front and back are relative to the WaniKani style).  You
# could use these classes to style these differently with Anki 2.

# from https://github.com/nigelkerr/wanikani2anki and in the public
# domain, with no sort of warranty whatsoever.

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.importing.noteimp  import NoteImporter, ForeignNote

import re
import urllib2
import json
import sys

WANIKANI_API_KEY = 'YOUR_API_KEY_HERE'
KANJI_URL = 'http://www.wanikani.com/api/v1.1/user/{}/kanji'.format(WANIKANI_API_KEY)
VOCAB_URL = 'http://www.wanikani.com/api/v1.1/user/{}/vocabulary'.format(WANIKANI_API_KEY)
MODEL_NAME = "Basic (and reversed card)" # also "Basic"

class WaniKaniImporter(NoteImporter):
    def __init__(self, *args):
        NoteImporter.__init__(self, *args)
        self.allowHTML = True # see NoteImporter

    def fields(self):
        return 2 # see NoteImporter

    def foreignNotes(self):
        notes = []
        for item in self.correctPart(): # json structures different
            if item[u'stats']:
                note = self.noteFromJson(item)
                notes.append(note)
        return notes

    def correctPart(self):
        return self.file[u'requested_information']

    def noteFromJson(self,jsonDict):
        return None

class KanjiImporter(WaniKaniImporter):
    def __init(self, *args):
        WaniKaniImporter.__init(self, *args)

    def noteFromJson(self,jsonDict):
        note = ForeignNote()
        tmpl = u"<span class='kanji back'><b>{}</b><br>{}<br>{}</span>"
        if jsonDict[u'important_reading'] == u'kunyomi':
            tmpl = u"<span class='kanji back'>{}<br><b>{}</b><br>{}</span>"
        note.fields.append(u"<span class='kanji front'>{}</span>".format(jsonDict[u'character']))
        note.fields.append(tmpl.format(jsonDict[u'onyomi'], jsonDict[u'kunyomi'], jsonDict[u'meaning']))
        note.tags.append('kanji')
        return note

class VocabImporter(WaniKaniImporter):
    def __init(self, *args):
        WaniKaniImporter.__init(self, *args)

    def correctPart(self):
        return self.file[u'requested_information'][u'general']

    def noteFromJson(self, jsonDict):
        note = ForeignNote()
        note.fields.append(u"<span class='vocab front'>{}</span>".format(jsonDict[u'character']))
        note.fields.append(u"<span class='vocab back'>{}<br>{}</span>".format(jsonDict[u'kana'], jsonDict[u'meaning']))
        note.tags.append('vocab')
        return note


def getjsonbolus(url):
    parsed = None
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        parsed = json.loads(data)
    except Exception as e:
        showInfo('Something unfortunate happened trying to contact WaniKani, as below, please try again later. {}'.format(e))
    return parsed

def getvocab():
    return getjsonbolus(VOCAB_URL)

def getkanji():
    return getjsonbolus(KANJI_URL)

def showApiKey():
    if WANIKANI_API_KEY and re.match('^[a-f0-9]{32}$', WANIKANI_API_KEY):
        showInfo('WaniKani API Key: {}'.format(WANIKANI_API_KEY))
    else:
        showInfo('WaniKani API Key not defined!')

def updateWaniKaniDeck():
    kanjiJson = getkanji()
    vocabJson = getvocab()

    if not kanjiJson and not vocabJson:
        showInfo("WaniKani didn't respond to either request, not updating anything.")
        return

    m = mw.col.models.byName(MODEL_NAME)
    assert m
    mw.col.models.setCurrent(m)
    m['did'] = mw.col.decks.id("WaniKani")
    mw.col.models.save(m)
    if kanjiJson:
        wki = KanjiImporter(mw.col,kanjiJson)
        wki.initMapping()
        wki.run()
    if vocabJson:
        wki = VocabImporter(mw.col,vocabJson)
        wki.initMapping()
        wki.run()
    mw.app.processEvents()
    showInfo('WaniKani deck updated!')
    mw.deckBrowser.show()

apiaction = QAction("Show WaniKani API Key", mw)
mw.connect(apiaction, SIGNAL("triggered()"), showApiKey)
mw.form.menuTools.addAction(apiaction)

if WANIKANI_API_KEY and re.match('^[a-f0-9]{32}$', WANIKANI_API_KEY):
    updateaction = QAction("Update WaniKani Deck", mw)
    mw.connect(updateaction, SIGNAL("triggered()"), updateWaniKaniDeck)
    mw.form.menuTools.addAction(updateaction)
