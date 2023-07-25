from PyQt5.QtWidgets import QLineEdit, QDialog
from PyQt5.QtCore import QEvent, pyqtSignal
from varUI import VarUI


class InputTextBox(QLineEdit):
    valueSelected = pyqtSignal(str)
    def __init__(self, parent=None):
        super(InputTextBox, self).__init__(parent)
        self.setReadOnly(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            self.open_ui()  # Open the desired UI
        return super().eventFilter(obj, event)

    def open_ui(self):
        ui = VarUI()
        if self.text() != "":
            # Si des données sont déjà présentes, les transmettre à la boîte de dialogue
            selected_var = self.text().split(":")[0].strip()
            if selected_var == "FIN":
                ui.combo_box.setCurrentText("Installed Part")
                a = self.text().split(":")[1].strip()
                b = a.split(" ; PN")[0].strip()
                ui.FIN_cb.setCurrentText(b)
                ui.PN_cb.setCurrentText(self.text().split(":")[2].strip())
            elif selected_var == "MPM":
                ui.combo_box.setCurrentText("Installed MPM")
                ui.MPM_cb.setCurrentText(self.text().split(":")[1].strip())
            elif selected_var == "SB":
                ui.combo_box.setCurrentText("Embodied SB")
                ui.SB_cb.setCurrentText(self.text().split(":")[1].strip())
            elif selected_var == "CMM":
                ui.combo_box.setCurrentText("CMM Procedure")
                ui.CMM_cb.setCurrentText(self.text().split(":")[1].strip())
            elif selected_var == "MP":
                ui.combo_box.setCurrentText("MP Procedure")
                ui.MPP_cb.setCurrentText(self.text().split(":")[1].strip())
            elif selected_var == "Freetext":
                ui.combo_box.setCurrentText("Freetext")
                ui.FT.setPlainText(self.text().split(":")[1].strip())
                
        if ui.exec_() == QDialog.Accepted:
            selected_var = ui.combo_box.currentText()
            if selected_var == "Installed Part":
                selected_id1 = ui.FIN_cb.currentText()
                selected_id2 = ui.PN_cb.currentText()
                self.setText(f"FIN : {selected_id1} ; PN : {selected_id2}")
            elif selected_var == "Installed MPM":
                selected_id1 = ui.MPM_cb.currentText()
                self.setText(f"MPM : {selected_id1}")
            elif selected_var == "Embodied SB":
                selected_id1 = ui.SB_cb.currentText()
                self.setText(f"SB : {selected_id1}")
            elif selected_var == "CMM Procedure":
                selected_id1 = ui.CMM_cb.currentText()
                self.setText(f"CMM : {selected_id1}")
            elif selected_var == "MP Procedure":
                selected_id1 = ui.MPP_cb.currentText()
                self.setText(f"MP : {selected_id1}")
            elif selected_var == "Freetext":
                freetext = ui.FT.toPlainText()
                self.setText(f"Freetext : {freetext}")
                
            self.valueSelected.emit(selected_var)

