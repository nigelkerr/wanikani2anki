# wanikani2anki, import unlocked Kanji and Vocab from WaniKani to a
# deck in desktop Anki 2.0.x.  place this file in your desktop Anki 2
# addons folder.

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

WANIKANI_API_KEY = '7cabb1e2050da36761ad124d447ad5e0'
KANJI_URL = 'https://www.wanikani.com/api/v1.1/user/{}/kanji'
VOCAB_URL = 'https://www.wanikani.com/api/v1.1/user/{}/vocabulary'
KANJI_DECK = "WaniKani Kanji"
VOCAB_DECK = "WaniKani Vocab"
KANJI_MODEL = "WaniKani Kanji Model"
VOCAB_MODEL = "WaniKani Vocab Model"

wkconf = { 'key': '', 'deck_separation': 'bothSeparately', 'card_direction': 'wanikaniDirection', 'include_tangorin_link': False }

class WaniKaniImporter(NoteImporter):
    def __init__(self, *args):
        NoteImporter.__init__(self, *args)
        self.allowHTML = True # see NoteImporter

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

    def fields(self):
        return 5 # see NoteImporter

    def noteFromJson(self,jsonDict):
        note = ForeignNote()
        note.fields.append(jsonDict[u'character'])
        
        onyomi = jsonDict[u'onyomi'] if jsonDict[u'onyomi']  else u'none'
        kunyomi = jsonDict[u'kunyomi'] if jsonDict[u'kunyomi'] else u'none'

        if jsonDict[u'important_reading'] == u'onyomi':
            note.fields.append(onyomi)
        else:
            note.fields.append(kunyomi)

        note.fields.append(onyomi)
        note.fields.append(kunyomi)
        note.fields.append(jsonDict[u'meaning'])
        note.tags.append("wk{0:s}".format(str(jsonDict[u'level'])))
        return note

class VocabImporter(WaniKaniImporter):
    def __init(self, *args):
        WaniKaniImporter.__init(self, *args)

    def fields(self):
        return 3  # see NoteImporter

    def correctPart(self):
        return self.file[u'requested_information'][u'general']

    def noteFromJson(self, jsonDict):
        note = ForeignNote()
        note.fields.append(jsonDict[u'character'])
        note.fields.append(jsonDict[u'kana'])
        note.fields.append(jsonDict[u'meaning'])
        note.tags.append("wk{0:s}".format(str(jsonDict[u'level'])))
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

def showApiKey():
    if WANIKANI_API_KEY and re.match('^[a-f0-9]{32}$', WANIKANI_API_KEY):
        showInfo('WaniKani API Key: {}'.format(WANIKANI_API_KEY))
    else:
        showInfo('WaniKani API Key not defined!')

def updateWaniKaniDeck():
    kanjiJson = None
    vocabJson = None

    if wkconf['deck_separation'] != 'vocabOnly':
        kanjiJson = getkanji()
    if wkconf['deck_separation'] != 'kanjiOnly':
        vocabJson = getvocab()

    if not kanjiJson and not vocabJson:
        showInfo("WaniKani didn't respond to either request, not updating anything.")
        return

    mm = mw.col.models

    tangorin = ""
    if wkconf['include_tangorin_link']:
        tangorin = "<br/><a href=\"http://www.tangorin.com/kanji/{{Kanji}}\">Tangorin</a>"

    if kanjiJson:
         wk_model = mm.byName(KANJI_MODEL)
         if not wk_model:
             wk_model = mm.new(KANJI_MODEL)
             mm.addField(wk_model, mm.newField("Kanji"))
             mm.addField(wk_model, mm.newField("Reading"))
             mm.addField(wk_model, mm.newField("Onyomi"))
             mm.addField(wk_model, mm.newField("Kunyomi"))
             mm.addField(wk_model, mm.newField("Meaning"))
             if wkconf['card_direction'] != 'reverseDirection':
                 tmpl = mm.newTemplate("WaniKani Kanji Meaning")
                 tmpl['qfmt'] = "<span style=\"font-size:100px;\">{{Kanji}}</span><br/>What is the <b>meaning</b>?"
                 tmpl['afmt'] = "{{FrontSide}}\n\n<hr id='answer'>\n\n"\
                     "<span style=\"font-size:30px;\">{{Meaning}}</span>"+tangorin
                 mm.addTemplate(wk_model, tmpl)
             if wkconf['card_direction'] != 'wanikaniDirection':
                 tmpl = mm.newTemplate("WaniKani Kanji (Reading)")
                 tmpl['qfmt'] = "<span style=\"font-size:100px;\">{{Kanji}}</span><br/>What is the <b>reading</b>?"
                 tmpl['afmt'] = "{{FrontSide}}\n\n<hr id='answer'>\n\n"\
                     "<span style=\"font-size:40px;\">"\
                     "{{Reading}}</span><br/>"\
                     "<div style=\"width:50%;float:left;\">"\
                     "On'yomi:&nbsp;{{Onyomi}}"\
                     "</div><div style=\"width:50%;float:left;\">"\
                     "Kun'yomi:&nbsp;{{Kunyomi}}"\
                     "</div><div style=\"clear:left;\"></div>"+tangorin
                 mm.addTemplate(wk_model, tmpl)
             mm.add(wk_model)
         mm.setCurrent(wk_model)
         wk_model['did'] = mw.col.decks.id(KANJI_DECK)
         mm.save(wk_model)
         wki = KanjiImporter(mw.col,kanjiJson)
         wki.initMapping()
         wki.run()
    if vocabJson:
         wk_model = mm.byName(VOCAB_MODEL)
         if not wk_model:
             wk_model = mm.new(VOCAB_MODEL)
             mm.addField(wk_model, mm.newField("Expression"))
             mm.addField(wk_model, mm.newField("Reading"))
             mm.addField(wk_model, mm.newField("Meaning"))
             if wkconf['card_direction'] != 'reverseDirection':
                 tmpl = mm.newTemplate("WaniKani Vocab")
                 tmpl['qfmt'] = "<span style=\"font-size:40px;\">"\
                     "{{Expression}}</span>"
                 tmpl['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n"\
                     "<span style=\"font-size:25px;\">{{Reading}}</span>"\
                     "<br/><span style=\"font-size:30px;\">{{Meaning}}</span>"+tangorin
                 mm.addTemplate(wk_model, tmpl)
             if wkconf['card_direction'] != 'wanikaniDirection':
                 tmpl = mm.newTemplate("WaniKanii Vocab (flipped)")
                 tmpl['qfmt'] = "<span style=\"font-size:30px;\">{{Meaning}}</span>"
                 tmpl['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n"\
                     "<span style=\"font-size:25px;\">{{Reading}}</span>"\
                     "<br/><span style=\"font-size:40px;\">"\
                     "{{Expression}}</span>"+tangorin
                 mm.addTemplate(wk_model, tmpl)
             mm.add(wk_model)
         mm.setCurrent(wk_model)
         wk_model['did'] = mw.col.decks.id(VOCAB_DECK)
         mm.save(wk_model)
         wki = VocabImporter(mw.col,vocabJson)
         wki.initMapping()
         wki.run()

    mw.app.processEvents()
    showInfo('Decks updated!')
    mw.deckBrowser.show()

def readConf():
    global wkconf
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
    global wkconf
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

    button = d.findChild(QCheckBox,'includeTangorinLink')
    button.setChecked(wkconf.get('include_tangorin_link', False))

    button = d.findChild(QPushButton,'updateWaniKaniDecks')
    button.clicked.connect(updateWaniKaniDeck)

    d.setWindowModality(Qt.WindowModal)

    if d.exec_():
        wkconf['key'] = form.key.text()
        wkconf['deck_separation'] = form.deckSeparation.checkedButton().objectName()
        wkconf['card_direction'] = form.cardDirection.checkedButton().objectName()
        wkconf['include_tangorin_link'] = form.includeTangorinLink.isChecked()
        writeConf();

    mw.app.processEvents()
    mw.reset()
    mw.deckBrowser.show()

readConf()

confaction = QAction("WaniKani 2 Anki", mw)
mw.connect(confaction, SIGNAL("triggered()"), showConfDialog)
mw.form.menuTools.addAction(confaction)
