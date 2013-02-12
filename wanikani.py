# wanikani2anki, import unlocked Kanji and Vocab from WaniKani to a
# deck in desktop Anki 2.0.x.  

# from https://github.com/nigelkerr/wanikani2anki and in the public
# domain, with no sort of warranty whatsoever.

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.importing.noteimp  import NoteImporter, ForeignNote

import wanikaniforms as forms

import re
import urllib2
import json
import sys
import os
import pickle

KANJI_URL = 'http://www.wanikani.com/api/v1.1/user/{}/kanji'
VOCAB_URL = 'http://www.wanikani.com/api/v1.1/user/{}/vocabulary'

wkconf = { 'key': '', 'model_name': 'Basic', 'deck_separation': 'bothSeparately', 'card_direction': 'wanikaniDirection' }

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
    return getjsonbolus(VOCAB_URL.format(wkconf['key']))

def getkanji():
    return getjsonbolus(KANJI_URL.format(wkconf['key']))

def updateWaniKaniDeck():
    if not keyValid():
        showInfo("We don't seem to have a valid WaniKani API Key, please try to configure it!")
        return

    if wkconf['deck_separation'] != 'vocabOnly':
        kanjiJson = getkanji()
    if wkconf['deck_separation'] != 'kanjiOnly':
        vocabJson = getvocab()

    if not kanjiJson and not vocabJson:
        showInfo("WaniKani didn't respond to either request, not updating anything.")
        return

    m = mw.col.models.byName(wkconf['model_name'])
    assert m
    mw.col.models.setCurrent(m)

    name1 = "WaniKani Kanji"
    name2 = "WaniKani Vocab"
    if wkconf['deck_separation'] == 'bothTogether':
        name1 = "WaniKani"
        name2 = "WaniKani"

    if kanjiJson:
        m['did'] = mw.col.decks.id(name1)
        mw.col.models.save(m)
        wki = KanjiImporter(mw.col,kanjiJson)
        wki.initMapping()
        wki.run()
    if vocabJson:
        m['did'] = mw.col.decks.id(name2)
        mw.col.models.save(m)
        wki = VocabImporter(mw.col,vocabJson)
        wki.initMapping()
        wki.run()

    mw.app.processEvents()
    showInfo('WaniKani deck(s) updated!')
    mw.deckBrowser.show()

def readConf():
    conffile = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".wanikani.conf")
    if ( os.path.exists( conffile ) ):
        conffile = conffile.decode(sys.getfilesystemencoding())
        tmpconf = json.load(open(conffile, 'r'))
        wkconf = tmpconf

def writeConf():
    conffile = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".wanikani.conf")
    conffile = conffile.decode(sys.getfilesystemencoding())
    json.dump( wkconf, open( conffile, 'w' ) )

def keyValid():
    return ( wkconf['key'] and re.match('^[a-f0-9]{32}$', wkconf['key']) )

def showConfDialog():
    d = QDialog()
    form = forms.configuration.Ui_Dialog()
    form.setupUi(d)

    form.key.setText(wkconf['key'])
    
    button = d.findChild(QRadioButton,wkconf['deck_separation'])
    if button:
        button.setChecked(True)
    button = d.findChild(QRadioButton,wkconf['card_direction'])
    if button:
        button.setChecked(True)

    d.setWindowModality(Qt.WindowModal)

    if d.exec_():
        wkconf['key'] = form.key.text()
        wkconf['model_name'] = 'Basic'
        wkconf['deck_separation'] = form.deckSeparation.checkedButton().objectName()
        wkconf['card_direction'] = form.cardDirection.checkedButton().objectName()
        writeConf();

readConf()

confaction = QAction("Configure WaniKani 2 Anki", mw)
mw.connect(confaction, SIGNAL("triggered()"), showConfDialog)
mw.form.menuTools.addAction(confaction)

updateaction = QAction("Update WaniKani Deck", mw)
mw.connect(updateaction, SIGNAL("triggered()"), updateWaniKaniDeck)
mw.form.menuTools.addAction(updateaction)
