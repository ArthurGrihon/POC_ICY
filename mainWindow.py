from PyQt5.QtWidgets import QMainWindow, QFormLayout, QWidget, QSizePolicy, QComboBox, QHBoxLayout, QDockWidget, QFileDialog, QSplitter, QVBoxLayout, QAction, QToolBar, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import xml.etree.ElementTree as ET
from circuitBuilderWidget import CircuitBuilderWidget
from autocompletecombobox import AutocompleteComboBox
from inputTextBox import InputTextBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ICY Condition Authoring")
        
        self._createAction()
        self._createMenuBar()
        self._connectActions()

        self._createDockWidgets()

        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

    def _createDockWidgets(self):
        # Create dock widgets
        self.definitionDock = QDockWidget("Definition", self)
        self.conditionsDock1 = QDockWidget("Condition A -> B", self)
        self.conditionsDock2 = QDockWidget("Condition B -> A", self)

        # Set the dock widget features
        self.definitionDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.conditionsDock1.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.conditionsDock2.setFeatures(QDockWidget.NoDockWidgetFeatures)

        # Create comboboxes for definition dock
        self.comboA = AutocompleteComboBox(self)
        self.comboB = AutocompleteComboBox(self)
        self.comboCode = QComboBox(self)
        self.conditions_im = QLabel(self)
        self.pixmap = QPixmap(r'images\100')

        # Set up items for comboA, comboB, and comboCode
        PrePN = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        ICYCode = ["100", "200", "152", "341", "342", "351", "352"]
        self.comboA.setItems(PrePN)
        self.comboB.setItems(PrePN)
        self.comboCode.addItems(ICYCode)
        self.conditions_im.setPixmap(self.pixmap)

        # Clear the current text of comboA, comboB, and comboCode
        self.comboA.setCurrentText("")
        self.comboB.setCurrentText("")
        self.comboCode.setCurrentText("")

        # Connect Combobox actions
        self.comboCode.currentIndexChanged.connect(self.updateConditionsImage)

        # Adjust the width of the comboboxes
        self.comboA.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboA.setFixedWidth(200)

        self.comboB.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboB.setFixedWidth(200)

        self.comboCode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comboCode.setFixedWidth(100)

        # Create form layout for definition dock
        definitionDock_layout = QHBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow("Pre PN (A) : ", self.comboA)
        form_layout.addRow("Post PN (B) : ", self.comboB)
        form_layout.addRow("ICY Code : ", self.comboCode)
        definitionDock_layout.setSpacing(10)
        definitionDock_layout.addLayout(form_layout)
        definitionDock_layout.addWidget(self.conditions_im, 2)

        # Create widget for definition dock and set widget
        definitionDock_widget = QWidget()
        definitionDock_widget.setLayout(definitionDock_layout)
        self.definitionDock.setWidget(definitionDock_widget)

        # Create CircuitBuilderWidgets for the conditions dock widgets
        self.circuitBuilderWidget1 = CircuitBuilderWidget(self.conditionsDock1.widget())
        self.circuitBuilderWidget2 = CircuitBuilderWidget(self.conditionsDock2.widget())
        self.spacer_removed1 = False
        self.spacer_removed2 = False

        # Set the conditionsTabWidget as the widget for the conditions dock widgets
        self.conditionsDock1.setWidget(self.circuitBuilderWidget1)
        self.conditionsDock2.setWidget(self.circuitBuilderWidget2)

        # Create splitter and add dock widgets
        splitter1 = QSplitter()
        splitter2 = QSplitter()
        splitter1.setOrientation(Qt.Vertical)  # Set the orientation to horizontal
        splitter1.addWidget(self.definitionDock)
        splitter1.addWidget(splitter2)
        splitter2.addWidget(self.conditionsDock1)
        splitter2.addWidget(self.conditionsDock2)  # Add the second conditions dock widget
        splitter1.setSizes([80, 820])  # Adjust the sizes of the dock widgets
        splitter2.setSizes([400,400])
        

        self.setCentralWidget(splitter1)
        self.updateConditionsImage(0)


    def _createMenuBar(self):
        menuBar = self.menuBar()

        # File menu
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

        # View menu
        viewMenu = menuBar.addMenu("&View")
        viewMenu.addAction(self.showDefinitionAction)
        viewMenu.addAction(self.showConditionsAction)

        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)

    def _createAction(self):
        # File Actions
        self.newAction = QAction("New file", self)
        self.openAction = QAction("Open File", self)
        self.saveAction = QAction("Save File", self)

        # View Actions
        self.showDefinitionAction = QAction("Show Definition", self)
        self.showDefinitionAction.setCheckable(True)
        self.showDefinitionAction.setChecked(True)
        self.showDefinitionAction.setShortcut('F1')

        self.showConditionsAction = QAction("Show Conditions", self)
        self.showConditionsAction.setCheckable(True)
        self.showConditionsAction.setChecked(True)
        self.showConditionsAction.setShortcut('F1')

        # Help Actions
        self.aboutAction = QAction("About", self)

    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)

        # Connect Help actions
        self.aboutAction.triggered.connect(self.about)

        # Connect View actions
        self.showDefinitionAction.triggered.connect(self.toggleDefinition)
        self.showConditionsAction.triggered.connect(self.toggleConditions)

    def updateConditionsImage(self, index):
        selected_code = self.comboCode.itemText(index)
       
        # Display the conditions_im QLabel if the selected_code meets the desired condition
        #Change Size
        not_inter = QLabel("Not Interchangeable")
        not_inter.setFont(QFont('Arial', 18))
        inter_wo = QLabel("Interchangeable without condition")
        inter_wo.setFont(QFont('Arial', 18))
        inter_wo1 = QLabel("Interchangeable without condition")
        inter_wo1.setFont(QFont('Arial', 18))
        inter_set = QLabel("Interchangeable as a SET")
        inter_set.setFont(QFont('Arial', 18))
        inter_set1 = QLabel("Interchangeable as a SET")
        inter_set1.setFont(QFont('Arial', 18))
        not_inter_set = QLabel("Not interchangeable as a SET")
        not_inter_set.setFont(QFont('Arial', 18))

        if selected_code == "100":
            self.pixmap = QPixmap(r'images\100.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == False:
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.vspacer)
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.hspacer)
                self.spacer_removed1 = True

            if self.spacer_removed2 == False:
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.vspacer)
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.hspacer)
                self.spacer_removed2 = True

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.scrollAreaLayout.addWidget(inter_wo,0,0,1,1,Qt.AlignCenter)
            self.circuitBuilderWidget2.scrollAreaLayout.addWidget(not_inter,0,0,1,1,Qt.AlignCenter)

        if selected_code == "200":
            self.pixmap = QPixmap(r'images\200.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == False:
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.vspacer)
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.hspacer)
                self.spacer_removed1 = True

            if self.spacer_removed2 == False:
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.vspacer)
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.hspacer)
                self.spacer_removed2 = True

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.scrollAreaLayout.addWidget(inter_wo,0,0,1,1,Qt.AlignCenter)
            self.circuitBuilderWidget2.scrollAreaLayout.addWidget(inter_wo1,0,0,1,1,Qt.AlignCenter)

        if selected_code == "152":
            self.pixmap = QPixmap(r'images\152.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == False:
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.vspacer)
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.hspacer)
                self.spacer_removed1 = True

            if self.spacer_removed2 == True:
                self.circuitBuilderWidget2.scrollAreaLayout.addItem(self.circuitBuilderWidget2.vspacer, 20, 0, 1, -1)
                self.circuitBuilderWidget2.scrollAreaLayout.addItem(self.circuitBuilderWidget2.hspacer, 0, 20, -1, 1)
                self.spacer_removed2 = False

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget2.add_cond(x = "BA")
            self.circuitBuilderWidget1.scrollAreaLayout.addWidget(inter_wo,0,0,1,1,Qt.AlignCenter)

        if selected_code == "341":
            self.pixmap = QPixmap(r'images\341.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == False:
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.vspacer)
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.hspacer)
                self.spacer_removed1 = True

            if self.spacer_removed2 == False:
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.vspacer)
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.hspacer)
                self.spacer_removed2 = True

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.scrollAreaLayout.addWidget(inter_set,0,0,1,1,Qt.AlignCenter)
            self.circuitBuilderWidget2.scrollAreaLayout.addWidget(not_inter_set,0,0,1,1,Qt.AlignCenter)

        if selected_code == "342":
            self.pixmap = QPixmap(r'images\342.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == False:
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.vspacer)
                self.circuitBuilderWidget1.scrollAreaLayout.removeItem(self.circuitBuilderWidget1.hspacer)
                self.spacer_removed1 = True

            if self.spacer_removed2 == False:
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.vspacer)
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.hspacer)
                self.spacer_removed2 = True

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.scrollAreaLayout.addWidget(inter_set,0,0,1,1,Qt.AlignCenter)
            self.circuitBuilderWidget2.scrollAreaLayout.addWidget(inter_set1,0,0,1,1,Qt.AlignCenter)

        if selected_code == "351":
            self.pixmap = QPixmap(r'images\351.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == True:
                self.circuitBuilderWidget1.scrollAreaLayout.addItem(self.circuitBuilderWidget1.vspacer, 20, 0, 1, -1)
                self.circuitBuilderWidget1.scrollAreaLayout.addItem(self.circuitBuilderWidget1.hspacer, 0, 20, -1, 1)
                self.spacer_removed1 = False

            if self.spacer_removed2 == False:
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.vspacer)
                self.circuitBuilderWidget2.scrollAreaLayout.removeItem(self.circuitBuilderWidget2.hspacer)
                self.spacer_removed2 = True

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.add_cond(x = "AB")
            self.circuitBuilderWidget2.scrollAreaLayout.addWidget(not_inter,0,0,1,1,Qt.AlignCenter)

        if selected_code == "352":
            self.pixmap = QPixmap(r'images\352.PNG')
            self.conditions_im.setPixmap(self.pixmap)

            if self.spacer_removed1 == True:
                self.circuitBuilderWidget1.scrollAreaLayout.addItem(self.circuitBuilderWidget1.vspacer, 20, 0, 1, -1)
                self.circuitBuilderWidget1.scrollAreaLayout.addItem(self.circuitBuilderWidget1.hspacer, 0, 20, -1, 1)
                self.spacer_removed1 = False

            if self.spacer_removed2 == True:
                self.circuitBuilderWidget2.scrollAreaLayout.addItem(self.circuitBuilderWidget2.vspacer, 20, 0, 1, -1)
                self.circuitBuilderWidget2.scrollAreaLayout.addItem(self.circuitBuilderWidget2.hspacer, 0, 20, -1, 1)
                self.spacer_removed2 = False

            self.circuitBuilderWidget1.clear_cb()
            self.circuitBuilderWidget2.clear_cb()
            self.circuitBuilderWidget1.add_cond(x = "AB")
            self.circuitBuilderWidget2.add_cond(x = "BA")

    def openFile(self):
        # Prompt the user to choose a file to open
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Circuit", "", "XML Files (*.xml)")

        if file_path:
            try:
                # Clear the existing circuit
                self.clearCircuit()

                # Load the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Iterate over the conditions in the XML and create the circuit
                for condition_elem in root.findall("condition"):
                    cond_type = condition_elem.get("type")
                    self.circuitBuilderWidget.add_cond()

                    inputs = condition_elem.findall("input")
                    condition_index = len(self.circuitBuilderWidget.conds) - 1
                    logical_node_widget = self.circuitBuilderWidget.conds[condition_index]
                    input_boxes = logical_node_widget.findChildren(InputTextBox)

                    for index, input_elem in enumerate(inputs):
                        if index < len(input_boxes):
                            input_text = input_elem.text
                            input_box = input_boxes[index]
                            input_box.setText(input_text)
                        else:
                            break

                # Update the input box of the CircuitBuilderWidget
                circuit_input = root.find("input")
                if circuit_input is not None:
                    circuit_input_text = circuit_input.text
                    circuit_input_box = self.circuitBuilderWidget.findChild(InputTextBox)
                    if circuit_input_box is not None:
                        circuit_input_box.setText(circuit_input_text)

                QMessageBox.information(self, "Message", "File opened successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while opening the file: {str(e)}")
        else:
            QMessageBox.information(self, "Message", "File opening canceled.")


    def saveFile(self):
        # Prompt the user to choose a file path to save the circuit XML file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Circuit", "", "XML Files (*.xml)")

        if file_path:
            try:
                # Create the root element of the XML document
                root = ET.Element("circuit")

                # Iterate over the conditions in the circuit builder widget and create XML elements for each
                for condition in self.circuitBuilderWidget.get_conditions():
                    condition_elem = ET.SubElement(root, "condition")
                    condition_elem.set("type", condition["cond_type"])

                    # Iterate over the input nodes of the condition and create XML elements for each
                    for input_node in condition["inputs"]:
                        input_elem = ET.SubElement(condition_elem, "input")
                        input_elem.text = input_node

                # Create the XML tree
                tree = ET.ElementTree(root)

                # Add the text values of input boxes to the XML structure
                for input_box in self.circuitBuilderWidget.scrollAreaWidgetContents.findChildren(InputTextBox):
                    input_elem = ET.SubElement(root, "input")
                    input_elem.text = input_box.text()

                # Write the XML tree to the file
                tree.write(file_path)

                QMessageBox.information(self, "Message", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {str(e)}")
        else:
            QMessageBox.information(self, "Message", "File saving canceled.")

    def clearCircuit(self):
        self.circuitBuilderWidget.scrollAreaWidgetContents.deleteLater()
        self.circuitBuilderWidget.scrollAreaWidgetContents = QWidget(self.circuitBuilderWidget.scrollArea)
        self.circuitBuilderWidget.scrollAreaLayout = QVBoxLayout(self.circuitBuilderWidget.scrollAreaWidgetContents)
        self.circuitBuilderWidget.scrollArea.setWidget(self.circuitBuilderWidget.scrollAreaWidgetContents)
        self.circuitBuilderWidget.conds = []

    def newFile(self):
        QMessageBox.information(self, "Message", "File > New -> clicked")

    def about(self):
        QMessageBox.information(self, "Message", "File > About -> clicked")

    def toggleDefinition(self):
        self.definitionDock.setVisible(not self.definitionDock.isVisible())

    def toggleConditions(self):
        self.conditionsDock.setVisible(not self.conditionsDock.isVisible())
