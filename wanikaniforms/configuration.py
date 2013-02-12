# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './configuration.ui'
#
# Created: Sun Feb 10 21:33:03 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 401, 301))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.key = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.key.setText(_fromUtf8(""))
        self.key.setMaxLength(32)
        self.key.setObjectName(_fromUtf8("key"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.key)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.kanjiOnly = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.kanjiOnly.setObjectName(_fromUtf8("kanjiOnly"))
        self.deckSeparation = QtGui.QButtonGroup(Dialog)
        self.deckSeparation.setObjectName(_fromUtf8("deckSeparation"))
        self.deckSeparation.addButton(self.kanjiOnly)
        self.verticalLayout_2.addWidget(self.kanjiOnly)
        self.vocabOnly = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.vocabOnly.setObjectName(_fromUtf8("vocabOnly"))
        self.deckSeparation.addButton(self.vocabOnly)
        self.verticalLayout_2.addWidget(self.vocabOnly)
        self.bothTogether = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.bothTogether.setObjectName(_fromUtf8("bothTogether"))
        self.deckSeparation.addButton(self.bothTogether)
        self.verticalLayout_2.addWidget(self.bothTogether)
        self.bothSeparately = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.bothSeparately.setObjectName(_fromUtf8("bothSeparately"))
        self.deckSeparation.addButton(self.bothSeparately)
        self.verticalLayout_2.addWidget(self.bothSeparately)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.verticalLayout_2)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.wanikaniDirection = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.wanikaniDirection.setObjectName(_fromUtf8("wanikaniDirection"))
        self.cardDirection = QtGui.QButtonGroup(Dialog)
        self.cardDirection.setObjectName(_fromUtf8("cardDirection"))
        self.cardDirection.addButton(self.wanikaniDirection)
        self.verticalLayout_3.addWidget(self.wanikaniDirection)
        self.reverseDirection = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.reverseDirection.setObjectName(_fromUtf8("reverseDirection"))
        self.cardDirection.addButton(self.reverseDirection)
        self.verticalLayout_3.addWidget(self.reverseDirection)
        self.bothDirection = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.bothDirection.setObjectName(_fromUtf8("bothDirection"))
        self.cardDirection.addButton(self.bothDirection)
        self.verticalLayout_3.addWidget(self.bothDirection)
        self.formLayout_2.setLayout(2, QtGui.QFormLayout.FieldRole, self.verticalLayout_3)
        self.verticalLayout.addLayout(self.formLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "WaniKani 2 Anki Configuration", None))
        self.label_2.setText(_translate("Dialog", "WaniKani API Key", None))
        self.label_3.setText(_translate("Dialog", "Deck Separation", None))
        self.kanjiOnly.setText(_translate("Dialog", "Kanji Only", None))
        self.vocabOnly.setText(_translate("Dialog", "Vocab Only", None))
        self.bothTogether.setText(_translate("Dialog", "Both Together", None))
        self.bothSeparately.setText(_translate("Dialog", "Both Separately", None))
        self.label_4.setText(_translate("Dialog", "Card Direction", None))
        self.wanikaniDirection.setText(_translate("Dialog", "WaniKani Direction", None))
        self.reverseDirection.setText(_translate("Dialog", "Reverse Direction", None))
        self.bothDirection.setText(_translate("Dialog", "Both Directions (two cards)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

