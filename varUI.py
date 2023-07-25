from PyQt5.QtWidgets import QDialog, QFormLayout, QGridLayout, QComboBox, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtCore import Qt
from autocompletecombobox import AutocompleteComboBox

class VarUI(QDialog):
    def __init__(self, parent=None):
        super(VarUI, self).__init__(parent)
        self.setWindowTitle("Add Item")
        self.setFixedSize(400, 200)
        self.selected_data = None
        self.var_type = ""

        FIN_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        PN_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        MPM_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        SB_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        CMM_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        MP_list = ["Option 1", "Option 2", "Option 3","Option 4", "Option 5", "Option 6","Option 7", "Option 8", "Option 9","Option 10", "Option 11", "Option 12"]
        layout = QGridLayout(self)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Installed Part", "Installed MPM",
                          "Embodied SB", "CMM Procedure", "MP Procedure",
                          "Freetext"])
        self.combo_box.currentIndexChanged.connect(self.display_gb)
        layout.addWidget(self.combo_box, 0, 0, 1, 1, Qt.AlignTop)

        self.IP_gp = QGroupBox(self)
        IP_gp_layout = QFormLayout(self.IP_gp)
        self.FIN_cb = AutocompleteComboBox(self.IP_gp)
        self.FIN_cb.setItems(FIN_list)
        IP_gp_layout.addRow("FIN : ",self.FIN_cb)
        self.FIN_cb.setCurrentText("")
        self.PN_cb = AutocompleteComboBox(self.IP_gp)
        self.PN_cb.setItems(PN_list)
        IP_gp_layout.addRow("PN : ",self.PN_cb)
        self.PN_cb.setCurrentText("")
        layout.addWidget(self.IP_gp, 1, 0, 1, 1)
        # self.IP_gp.hide()

        self.IMPM_gp = QGroupBox(self)
        IMPM_gp_layout = QFormLayout(self.IMPM_gp)
        self.MPM_cb = AutocompleteComboBox(self.IMPM_gp)
        self.MPM_cb.setItems(MPM_list)
        IMPM_gp_layout.addRow("MPM NUMBER: ", self.MPM_cb)
        self.MPM_cb.setCurrentText("")
        layout.addWidget(self.IMPM_gp, 1, 0, 1, 1)
        self.IMPM_gp.hide()

        self.ESB_gp = QGroupBox(self)
        ESB_gp_layout = QFormLayout(self.ESB_gp)
        self.SB_cb = AutocompleteComboBox(self.ESB_gp)
        self.SB_cb.setItems(SB_list)
        ESB_gp_layout.addRow("SB NUMBER: ", self.SB_cb)
        self.SB_cb.setCurrentText("")
        layout.addWidget(self.ESB_gp, 1, 0, 1, 1)
        self.ESB_gp.hide()

        self.CMMP_gp = QGroupBox(self)
        CMMP_gp_layout = QFormLayout(self.CMMP_gp)
        self.CMM_cb = AutocompleteComboBox(self.CMMP_gp)
        self.CMM_cb.setItems(CMM_list)
        CMMP_gp_layout.addRow("CMM REF: ", self.CMM_cb)
        self.CMM_cb.setCurrentText("")
        layout.addWidget(self.CMMP_gp, 1, 0, 1, 1)
        self.CMMP_gp.hide()

        self.MPP_gp = QGroupBox(self)
        MPP_gp_layout = QFormLayout(self.MPP_gp)
        self.MPP_cb = AutocompleteComboBox(self.MPP_gp)
        self.MPP_cb.setItems(MP_list)
        MPP_gp_layout.addRow("MP REF: ", self.MPP_cb)
        self.MPP_cb.setCurrentText("")
        layout.addWidget(self.MPP_gp, 1, 0, 1, 1)
        self.MPP_gp.hide()

        # self.FT_gp = QGroupBox(self)
        self.FT = QTextEdit()    
        layout.addWidget(self.FT, 1, 0, 1, 1) 
        self.FT.hide()        

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_text_to_input)
        layout.addWidget(self.add_button, 2, 0, 1, 1, Qt.AlignBottom)

    def display_gb(self, index):
        selected_var = self.combo_box.itemText(index)
        if selected_var == "Installed Part":
            self.IP_gp.show()
            self.IMPM_gp.hide()
            self.ESB_gp.hide()
            self.CMMP_gp.hide()
            self.MPP_gp.hide()
            self.FT.hide()

        if selected_var == "Installed MPM":
            self.IMPM_gp.show()
            self.IP_gp.hide()
            self.ESB_gp.hide()
            self.CMMP_gp.hide()
            self.MPP_gp.hide()
            self.FT.hide()

        if selected_var == "Embodied SB":
            self.ESB_gp.show()
            self.IMPM_gp.hide()
            self.IP_gp.hide()
            self.CMMP_gp.hide()
            self.MPP_gp.hide()
            self.FT.hide()

        if selected_var == "CMM Procedure":
            self.CMMP_gp.show()
            self.IMPM_gp.hide()
            self.ESB_gp.hide()
            self.IP_gp.hide()
            self.MPP_gp.hide()
            self.FT.hide()

        if selected_var == "MP Procedure":
            self.MPP_gp.show()
            self.IMPM_gp.hide()
            self.ESB_gp.hide()
            self.CMMP_gp.hide()
            self.IP_gp.hide()
            self.FT.hide()

        if selected_var == "Freetext":
            self.FT.show()
            self.IMPM_gp.hide()
            self.ESB_gp.hide()
            self.CMMP_gp.hide()
            self.MPP_gp.hide()
            self.IP_gp.hide()

    def add_text_to_input(self):
        selected_var = self.combo_box.currentText()
        if selected_var == "Installed Part":
            self.selected_data = {
                "selected_var": selected_var,
                "selected_id1": self.FIN_cb.currentText(),
                "selected_id2": self.PN_cb.currentText()
            }
            self.var_type = selected_var
        elif selected_var == "Installed MPM":
            self.selected_data = {
                "selected_var": selected_var,
                "selected_id1": self.MPM_cb.currentText()
            }
            self.var_type = selected_var
        elif selected_var == "Embodied SB":
            self.selected_data = {
                "selected_var": selected_var,
                "selected_id1": self.SB_cb.currentText()
            }
            self.var_type = selected_var
        elif selected_var == "CMM Procedure":
            self.selected_data = {
                "selected_var": selected_var,
                "selected_id1": self.CMM_cb.currentText()
            }
            self.var_type = selected_var
        elif selected_var == "MP Procedure":
            self.selected_data = {
                "selected_var": selected_var,
                "selected_id1": self.MPP_cb.currentText()
            }
            self.var_type = selected_var
        elif selected_var == "Freetext":
            self.selected_data = {
                "selected_var": selected_var,
                "freetext": self.FT.toPlainText()
            }
        self.accept()
        



