import sys
from sfsdg645 import DG645
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from gui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # dg645 stuff: 
        self._init_dg645
        self.Display_delay_A_button.clicked.connect(lambda: self._dg645_display_delay('a', self.Channel_trig_select_box_A.currentText(), self.channel_delay_entry_A.currentText(), self.channel_delay_time_unit_A.value()))   
        self.Display_delay_B_button.clicked.connect(lambda: self._dg645_display_delay('b', self.Channel_trig_select_box_B.currentText(), self.channel_delay_entry_B.currentText(), self.channel_delay_time_unit_B.value()))
        self.Display_delay_C_button.clicked.connect(lambda: self._dg645_display_delay('c', self.Channel_trig_select_box_C.currentText(), self.channel_delay_entry_C.currentText(), self.channel_delay_time_unit_C.value()))
        self.Display_delay_D_button.clicked.connect(lambda: self._dg645_display_delay('d', self.Channel_trig_select_box_D.currentText(), self.channel_delay_entry_D.currentText(), self.channel_delay_time_unit_D.value()))
        self.Display_delay_E_button.clicked.connect(lambda: self._dg645_display_delay('e', self.Channel_trig_select_box_E.currentText(), self.channel_delay_entry_E.currentText(), self.channel_delay_time_unit_E.value()))
        self.Display_delay_F_button.clicked.connect(lambda: self._dg645_display_delay('f', self.Channel_trig_select_box_F.currentText(), self.channel_delay_entry_F.currentText(), self.channel_delay_time_unit_F.value()))
        self.Display_delay_G_button.clicked.connect(lambda: self._dg645_display_delay('g', self.Channel_trig_select_box_G.currentText(), self.channel_delay_entry_G.currentText(), self.channel_delay_time_unit_G.value()))
        self.Display_delay_H_button.clicked.connect(lambda: self._dg645_display_delay('h', self.Channel_trig_select_box_H.currentText(), self.channel_delay_entry_H.currentText(), self.channel_delay_time_unit_H.value()))
        
    def _init_dg645(self):
        try:
            self.dg645 = DG645("serial://COM3")
        except:
            QMessageBox.critical(self, 'Error', 'Unable to connect to DG645 - Check your com port and ensure it was closed properly before connecting again')
        else:
            self.dg645.get_all_delays()
            
    def _dg645_display_delay(self, target, link, unit, delay):
        self.dg645.display_delay(target, link, unit, delay)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())