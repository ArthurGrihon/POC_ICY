from PyQt5.QtWidgets import QComboBox, QCompleter


class AutocompleteComboBox(QComboBox):
    def __init__(self, parent=None):
        super(AutocompleteComboBox, self).__init__(parent)
        self.setEditable(True)
        self.completer = QCompleter(self)
        self.setCompleter(self.completer)

    def setItems(self, items):
        self.clear()
        self.addItems(items)
        self.completer.setModel(self.model())
