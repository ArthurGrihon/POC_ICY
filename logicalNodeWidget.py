from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QGroupBox, QGridLayout, QLabel
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from inputTextBox import InputTextBox

class LogicalNodeWidget(QWidget):
    def __init__(self, parent=None):
        super(LogicalNodeWidget, self).__init__(parent)

        self.layout = QGridLayout(self)
        self.inputGroup = QGroupBox(self)
        self.scrollAreaLayout = None

        self.inputLayout = QGridLayout(self.inputGroup)
        self.inputLayout.setContentsMargins(10,10,10,10)
        self.inputLayout.setSpacing(10)
        self.inputGroup.setMaximumSize(self.inputGroup.sizeHint())
        self.inputGroup.setMinimumSize(self.inputGroup.sizeHint())

        self.conditionCombo = QComboBox()
        self.conditionCombo.addItems(["SIMPLE", "OR", "AND", "NOT", "XOR"]  )
        self.conditionCombo.currentIndexChanged.connect(self.update_input_connections)
        self.inputLayout.addWidget(self.conditionCombo, 0, 0, 1, 2)
        self.layout.addWidget(self.inputGroup, 1, 0, 1, 1)

        self.cond_label = QLabel(self.conditionCombo.currentText())
        self.layout.addWidget(self.cond_label, 0, 0, 1, 1, Qt.AlignCenter)
        self.cond_label.hide()
         
        self.addSCButton = QPushButton("+", self)
        self.addSCButton.setFixedSize(QSize(30, 30))
        self.addSCButton.clicked.connect(self.add_subCond)
        self.inputLayout.addWidget(self.addSCButton, 1, 0, 1, 1) 

        self.deleteButton = QPushButton("X", self)
        self.deleteButton.setFixedSize(QSize(30, 30))
        self.deleteButton.clicked.connect(self.invert_and_suppress_widgets)
        self.inputLayout.addWidget(self.deleteButton, 1, 1, 1, 1)
        if self.parent() == None:
            self.deleteButton.setEnabled(False)

        self.var_type = "HELLO"
        self.var_title = QLabel(self.var_type)
        self.inputLayout.addWidget(self.var_title, 0, 2, 1, 1, Qt.AlignCenter)
        self.child_nodes = []

        self.update_input_connections()

        self.subCond_counter = 0
        self.subConds = []

    def add_subCond(self):
        prow, pcol, _, _ = self.scrollAreaLayout.getItemPosition(self.scrollAreaLayout.indexOf(self))
        subCond = LogicalNodeWidget(self)
        subCond.scrollAreaLayout = self.scrollAreaLayout
        subCond.setObjectName(f"{self.objectName()}_subcond_{self.subCond_counter}")
        self.subConds.append(subCond)
        self.child_nodes.append(subCond)

        i = 0
        while True:
            if self.scrollAreaLayout.itemAtPosition(prow + i, pcol + 1) is None:
                break
            subCond.cond_label.show()
            i += 1

        subCond.cond_label.setText(self.conditionCombo.currentText())  # Set the text of cond_label
        self.scrollAreaLayout.addWidget(subCond, prow + i, pcol + 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)

        self.subCond_counter += 1
        subCond.input_node.valueSelected.connect(self.handle_value_selected)


    def invert_and_suppress_widgets(self):
        # Get the position of the current widget
        prow, pcol, _, _ = self.scrollAreaLayout.getItemPosition(self.scrollAreaLayout.indexOf(self))

        # Find the number of rows and columns in the layout
        rows = self.scrollAreaLayout.rowCount()
        cols = self.scrollAreaLayout.columnCount()

        # Iterate over the next column at the same row and below it
        for row in range(prow, rows):
            widget_item = self.scrollAreaLayout.itemAtPosition(row, pcol + 1)
            if widget_item is not None:
                widget = widget_item.widget()
                if widget is not None:
                    # Remove the widget from the layout and delete it
                    self.scrollAreaLayout.removeWidget(widget)
                    widget.deleteLater()

        # Update the layout to reflect the changes
        self.deleteLater()
        self.scrollAreaLayout.update()
        self.adjustGroupBoxSize()


    def delete_subCond(self):  
        self.deleteLater()
        self.adjustGroupBoxSize()
 
    def update_input_connections(self):
        condition = self.conditionCombo.currentText()

        if condition == "SIMPLE":
            self.add_input_node()
            self.addSCButton.setEnabled(False)
            self.adjustSIMPLE()
        if condition == "OR":
            self.delete_input_nodes()
            self.addSCButton.setEnabled(True)
            self.add_subCond()
            self.add_subCond()
            self.adjustGroupBoxSize()
        if condition == "AND":
            self.delete_input_nodes()
            self.addSCButton.setEnabled(True)
            self.adjustGroupBoxSize()
        if condition == "NOT":
            self.delete_input_nodes()
            self.addSCButton.setEnabled(True)
            self.adjustGroupBoxSize()
        if condition == "XOR":
            self.delete_input_nodes()
            self.addSCButton.setEnabled(True)
            self.adjustGroupBoxSize()

    def adjustSIMPLE(self):
        self.conditionCombo.setMinimumSize(self.conditionCombo.sizeHint())
        self.conditionCombo.setMaximumSize(self.conditionCombo.sizeHint())
        self.inputGroup.setFixedSize(300,80)
        self.inputLayout.setHorizontalSpacing(5)
        self.inputLayout.setVerticalSpacing(5)
        self.inputLayout.setAlignment(Qt.AlignLeft)

    def adjustGroupBoxSize(self):
        self.conditionCombo.setMinimumSize(self.conditionCombo.sizeHint())
        self.conditionCombo.setMaximumSize(self.conditionCombo.sizeHint())
        self.inputLayout.setHorizontalSpacing(5)
        self.inputLayout.setVerticalSpacing(5)
        self.inputGroup.setMinimumSize(self.inputGroup.sizeHint())
        self.inputGroup.setMaximumSize(self.inputGroup.sizeHint())
        self.inputLayout.setAlignment(Qt.AlignLeft)

    def delete_input_nodes(self):
        for input_node in self.child_nodes:
            input_node.setParent(None)
            self.inputLayout.removeWidget(input_node)
            input_node.deleteLater()
        self.child_nodes.clear()

    def add_input_node(self):
        input_node = InputTextBox(self)
        input_node.setFixedSize(QSize(180, 30))
        self.child_nodes.append(input_node)
        self.inputLayout.addWidget(input_node, 1, 2, 1, 1)
        input_node.valueSelected.connect(self.handle_value_selected) 
        
    def get_cond_type(self):
        return self.conditionCombo.currentText()

    def get_input_nodes(self):
        return self.child_nodes
    
    def handle_value_selected(self, selected_var):
        self.var_title.setText(selected_var)