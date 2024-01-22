import sys
from sfsdg645 import DG645
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.QtCore import QTimer, QTime
from PyQt5.uic import loadUi
import qdarktheme
from gui import Ui_MainWindow
from PyQt5.QtCore import QDate

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # set up timer for the clock
        self.clock_timer = QTimer(self, interval=1000, timeout=self._update_clock)
        self.clock_timer.start()
        
        # dg645 stuff: 
        self._init_dg645()
        
        # init lists for easier access
        self.channel_trig_list = [self.Channel_trig_select_box_A, self.Channel_trig_select_box_B, self.Channel_trig_select_box_C, self.Channel_trig_select_box_D, self.Channel_trig_select_box_E, self.Channel_trig_select_box_F, self.Channel_trig_select_box_G, self.Channel_trig_select_box_H]
        self.channel_delay_entry_list = [self.channel_delay_entry_A, self.channel_delay_entry_B, self.channel_delay_entry_C, self.channel_delay_entry_D, self.channel_delay_entry_E, self.channel_delay_entry_F, self.channel_delay_entry_G, self.channel_delay_entry_H]
        self.channel_delay_time_unit_list = [self.channel_delay_time_unit_A, self.channel_delay_time_unit_B, self.channel_delay_time_unit_C, self.channel_delay_time_unit_D, self.channel_delay_time_unit_E, self.channel_delay_time_unit_F, self.channel_delay_time_unit_G, self.channel_delay_time_unit_H]
        
        self.Display_delay_T0_button.clicked.connect(lambda: self._dg645_display_delay('t0', self.Channel_trig_select_box_T0.currentText(), self.channel_delay_entry_T0.text(), self.channel_delay_time_unit_T0.currentText()))
        self.Display_delay_T1_button.clicked.connect(lambda: self._dg645_display_delay('t1', self.Channel_trig_select_box_T1.currentText(), self.channel_delay_entry_T1.text(), self.channel_delay_time_unit_T1.currentText()))
        self.Display_delay_A_button.clicked.connect(lambda: self._dg645_display_delay('a', self.Channel_trig_select_box_A.currentText(), self.channel_delay_entry_A.text(), self.channel_delay_time_unit_A.currentText()))   
        self.Display_delay_B_button.clicked.connect(lambda: self._dg645_display_delay('b', self.Channel_trig_select_box_B.currentText(), self.channel_delay_entry_B.text(), self.channel_delay_time_unit_B.currentText()))
        self.Display_delay_C_button.clicked.connect(lambda: self._dg645_display_delay('c', self.Channel_trig_select_box_C.currentText(), self.channel_delay_entry_C.text(), self.channel_delay_time_unit_C.currentText()))
        self.Display_delay_D_button.clicked.connect(lambda: self._dg645_display_delay('d', self.Channel_trig_select_box_D.currentText(), self.channel_delay_entry_D.text(), self.channel_delay_time_unit_D.currentText()))
        self.Display_delay_E_button.clicked.connect(lambda: self._dg645_display_delay('e', self.Channel_trig_select_box_E.currentText(), self.channel_delay_entry_E.text(), self.channel_delay_time_unit_E.currentText()))
        self.Display_delay_F_button.clicked.connect(lambda: self._dg645_display_delay('f', self.Channel_trig_select_box_F.currentText(), self.channel_delay_entry_F.text(), self.channel_delay_time_unit_F.currentText()))
        self.Display_delay_G_button.clicked.connect(lambda: self._dg645_display_delay('g', self.Channel_trig_select_box_G.currentText(), self.channel_delay_entry_G.text(), self.channel_delay_time_unit_G.currentText()))
        self.Display_delay_H_button.clicked.connect(lambda: self._dg645_display_delay('h', self.Channel_trig_select_box_H.currentText(), self.channel_delay_entry_H.text(), self.channel_delay_time_unit_H.currentText()))
        
        self.set_delay_button.clicked.connect(self._dg645_set_delays)
             
    def _init_dg645(self):
        try:
            self.dg645 = DG645("serial://COM3")
        except:
            QMessageBox.critical(self, 'Error', 'Unable to connect to DG645 - Check your com port and ensure it was closed properly before connecting again')
        else:
            pass #self._dg645_get_all_delays()
            
    def _dg645_display_delay(self, target, link, unit, delay):
        # display them delays
        self.dg645.display_delay(target, link, unit, delay)
        
    def _dg645_set_delays(self):
        # set all delays from pertinent input boxes
        for i, x in enumerate(self.channel_trig_list):
            self.dg645.setDelay(self.channel_trig_list[i].currentText(), self.channel_trig_list[0].currentText(), self.channel_delay_entry_list[i].text(), self.channel_delay_time_unit_list[i].currentText())
            
    def _dg645_get_all_delays(self):
        for i in range(10):
            rtn = self.dg645.get_delay(i)
            # update the input boxes
            self.channel_trig_list[i].setCurrentText(rtn[0].upper())
            self.channel_delay_entry_list[i].setText(rtn[1])
            self.channel_delay_time_unit_list[i].setCurrentText(rtn[2])
            
    def _update_clock(self):
        current_date_time = QDate.currentDate().toString() + ' ' + QTime.currentTime().toString()
        self.clock_label.setText(current_date_time)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window()
    win.show()
    sys.exit(app.exec())