from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from inputTextBox import InputTextBox
from logicalNodeWidget import LogicalNodeWidget

class CircuitBuilderWidget(QWidget):
    def __init__(self, parent=None):
        super(CircuitBuilderWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.scrollAreaWidgetContents = QWidget(self.scrollArea)
        self.scrollAreaLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName("Cb Grid")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.vspacer = QSpacerItem(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scrollAreaLayout.addItem(self.vspacer, 20, 0, 1, -1)

        self.hspacer = QSpacerItem(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.scrollAreaLayout.addItem(self.hspacer, 0, 20, -1, 1)
        
        self.layout.addWidget(self.scrollArea)

        self.conds = []

    def delete_cond(self, condition_index):
        if condition_index < 0 or condition_index >= len(self.conds):
            return

        cond = self.conds[condition_index]
        cond.setParent(None)
        cond.deleteLater()
        self.conds.pop(condition_index)

    def clear_cb(self):
        for i in reversed(range(self.scrollAreaLayout.count())): 
            if self.scrollAreaLayout.itemAt(i).widget() is not None :
                self.scrollAreaLayout.itemAt(i).widget().setParent(None)
            
    def delete_all_conds(self):
        for cond in self.conds:
            cond.setParent(None)
            cond.deleteLater()
        self.conds.clear()
        
    def add_cond(self,x):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        cond = LogicalNodeWidget()
        cond.scrollAreaLayout = self.scrollAreaLayout
        cond.deletable = False
        cond.setParent(self)  # Set CircuitBuilderWidget as the parent
        cond.setObjectName(f"{x}_cond")
        self.conds.append(cond)
        self.scrollAreaLayout.addWidget(cond, 0, 0, 1, 1, Qt.AlignTop | Qt.AlignLeft)  # Add widget at index 0 with left alignment
        print(self.scrollAreaLayout.objectName())

    def add_input_box(self, condition_index, input_text):
        condition = self.conds[condition_index]
        condition.add_input_box(input_text)
        
    def get_conditions(self):
        condition_list = []
        for cond in self.conds: 
            cond_info = {
                "cond_type": cond.get_cond_type(),
                "inputs": [child.objectName() for child in cond.findChildren(InputTextBox)]
            }
            condition_list.append(cond_info)
        return condition_list

    def delete_Cond(self):
        self.setParent(None)
        self.deleteLater()