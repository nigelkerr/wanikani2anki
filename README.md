wanikani2anki
=============

Import unlocked Kanji and Vocab from WaniKani to a deck in desktop Anki 2.0.x.

Tested on Mac Anki 2.0.8, various WaniKani users/versions/osen.

Now mo' bettah, with a niftier model (contributed by aina @WaniKani)
and a configuration dialog (your truly) such that you don't have to
edit files to set the api key.

UPDATING FROM PREVIOUS VERSION
==============================

Just follow the INSTALL directions here, over-writing any older files.

INSTALL
=======

Easiest way: download the zip from https://github.com/nigelkerr/wanikani2anki/archive/master.zip which will unpack a folder called "wanikani2anki-master".  There should be some things in the folder.  Drag the items inside the folder to your Anki/addons directory (don't drag the wanikani2anki-master folder itself...).

USING
=====

After you install, there will be a Tools menu entry for "WaniKani 2 Anki".  This will bring up a dialog box.

There is a field for your WaniKani API Key, enter it here.
Choose to have just Kanji, or just Vocab, or both.
Choose to have just the WaniKani direction, just the reverse of that, or both.
Choose to have a Tangorin (http://tangorin.com/) link to the relevant entry inserted below the answer portion of each ard.

These last to preferences get backed into the templates for the "Note Types", meaning that presently you have to throw away the decks and those note types to change them.  Ought to be a way around that.  Tangorin wasn't doing it for me, nor was having both directions of the cards.  I may be a Special Case.

Once you've set it the way you want, press the Update WaniKani Decks button here.  Once it updates, you can press OK to return to Anki.

The options you choose will be saved to a preferences file in the addons directory named ".wanikani.conf".


