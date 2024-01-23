import sys
from sfsdg645 import DG645
from oscilloscope import scope
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
        
        # ------------------------------------------------------------------------------------------
        # dg645 stuff: 
        # init lists for easier access
        self.channel_trig_list = [self.Channel_trig_select_box_T0, self.Channel_trig_select_box_T1, self.Channel_trig_select_box_A, self.Channel_trig_select_box_B, self.Channel_trig_select_box_C, self.Channel_trig_select_box_D, self.Channel_trig_select_box_E, self.Channel_trig_select_box_F, self.Channel_trig_select_box_G, self.Channel_trig_select_box_H]
        self.channel_delay_entry_list = [self.channel_delay_entry_T0, self.channel_delay_entry_T1, self.channel_delay_entry_A, self.channel_delay_entry_B, self.channel_delay_entry_C, self.channel_delay_entry_D, self.channel_delay_entry_E, self.channel_delay_entry_F, self.channel_delay_entry_G, self.channel_delay_entry_H]
        self.channel_delay_time_unit_list = [self.channel_delay_time_unit_T0, self.channel_delay_time_unit_T1, self.channel_delay_time_unit_A, self.channel_delay_time_unit_B, self.channel_delay_time_unit_C, self.channel_delay_time_unit_D, self.channel_delay_time_unit_E, self.channel_delay_time_unit_F, self.channel_delay_time_unit_G, self.channel_delay_time_unit_H]
        self.amplitude_entry_list = [self.ab_amplitude_entry, self.cd_amplitude_entry, self.ef_amplitude_entry, self.gh_amplitude_entry]
        self.offset_entry_list = [self.ab_offset_entry, self.cd_offset_entry, self.ef_offset_entry, self.gh_offset_entry]
        
        self.Display_delay_T0_button.clicked.connect(lambda: self._dg645_display_delay('t0'))
        self.Display_delay_T1_button.clicked.connect(lambda: self._dg645_display_delay('t1'))
        self.Display_delay_A_button.clicked.connect(lambda: self._dg645_display_delay('a'))
        self.Display_delay_B_button.clicked.connect(lambda: self._dg645_display_delay('b'))
        self.Display_delay_C_button.clicked.connect(lambda: self._dg645_display_delay('c'))
        self.Display_delay_D_button.clicked.connect(lambda: self._dg645_display_delay('d'))
        self.Display_delay_E_button.clicked.connect(lambda: self._dg645_display_delay('e'))
        self.Display_delay_F_button.clicked.connect(lambda: self._dg645_display_delay('f'))
        self.Display_delay_G_button.clicked.connect(lambda: self._dg645_display_delay('g'))
        self.Display_delay_H_button.clicked.connect(lambda: self._dg645_display_delay('h'))
        self.set_delay_button.clicked.connect(self._dg645_set_delays)
        self.Trigger_mode_select.currentIndexChanged.connect(self._dg645_handle_trigger_select)
        self.get_all_values_button.clicked.connect(self._dg645_get_all_values)
        # ----------------------------------------------------------------------------------------------
        
        # ------------------------------------------------------------------------------------------
        # oscilloscope stuff:
        '''
        # self.data_source_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
        self.data_source_line.textChanged.connect(lambda: self.ocilloscope_inp('data_source'))
        # self.trig_source_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
        self.trig_source_line.textChanged.connect(lambda: self.ocilloscope_inp('trig_source'))
        self.rec_length_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
        self.rec_length_line.textChanged.connect(lambda: self.ocilloscope_inp('rec_length'))
        self.v_div_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
        self.v_div_line.textChanged.connect(lambda: self.ocilloscope_inp('v_div'))
        self.t_div_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
        self.t_div_line.textChanged.connect(lambda: self.ocilloscope_inp('t_div'))
        '''
        # ----------------------------------------------------------------------------------------------
        # DIAGNOSTIC INITALIZATION
        # ----------------------------------------------------------------------------------------------
        self._init_dg645()
        self._init_scope()
        
        # ----------------------------------------------------------------------------------------------
    
    
    
    '''
        _______   _______    __    _  _     _____  
        |       \ /  _____|  / /   | || |   | ____| 
        |  .--.  |  |  __   / /_   | || |_  | |__   
        |  |  |  |  | |_ | | '_ \  |__   _| |___ \  
        |  '--'  |  |__| | | (_) |    | |    ___) | 
        |_______/ \______|  \___/     |_|   |____/  
    _________________________________________________________________________________________________                                       
    '''    
    def _init_dg645(self):
        try:
            self.dg645 = DG645("COM4")
        except:
            QMessageBox.critical(self, 'Error', 'Unable to connect to DG645 - Check your com port and ensure it was closed properly before connecting again')
        else:
            self._dg645_get_all_delays()
            self._dg645_get_amplitude_offset()
            self._dg645_get_trigger_source()
            
    def _dg645_display_delay(self, target):
        # display them delays
        self.dg645.display_delay(target)
        
    def _dg645_set_delays(self):
        # set all delays from pertinent input boxes
        for i, x in enumerate(self.channel_trig_list):
            # self.dg645.setDelay(self.channel_trig_list[i].currentText(), self.channel_trig_list[0].currentText(), self.channel_delay_entry_list[i].text(), self.channel_delay_time_unit_list[i].currentText())
            self.dg645.setDelay(i, self.channel_trig_list[i].currentText(), self.channel_delay_entry_list[i].text(), self.channel_delay_time_unit_list[i].currentText())

    def _dg645_get_all_delays(self):
        for i in range(10):
            rtn = self.dg645.get_delay(i)
            # update the input boxes
            self.channel_trig_list[i].setCurrentText(rtn[0].upper())
            self.channel_delay_entry_list[i].setText(rtn[1])
            self.channel_delay_time_unit_list[i].setCurrentText(rtn[2])
            
    def _dg645_get_all_values(self):
            self._dg645_get_all_delays()
            self._dg645_get_amplitude_offset()
            self._dg645_get_trigger_source()
    
    def _dg645_get_amplitude_offset(self):
        for i in range(4):
            amp = self.dg645.get_amplitude(i+1)
            offset = self.dg645.get_offset(i+1)
            self.amplitude_entry_list[i].setText(amp)
            self.offset_entry_list[i].setText(offset)
    
    def _dg645_set_amplitude_offset(self):
        for i in range(4):
            self.dg645.set_amplitude(i+1, self.amplitude_entry_list[i].text())
            self.dg645.set_offset(i+1, self.offset_entry_list[i].text())
            
    def _dg645_get_trigger_source(self):
        src = self.dg645.get_trigger_source()
        self.Trigger_mode_select.setCurrentText(src)
    
    def _dg645_set_trigger_source(self):
        src = self.Trigger_mode_select.currentText()
        self.dg645.set_trigger_source(src)
    
    def _dg645_handle_trigger_select(self):
        src = self.Trigger_mode_select.currentText()
        self.dg645.set_trigger_source(src)
        print(src)
    '''_______________________________________________________________________________________________________'''   
    
    
    '''
            _______.  ______   ______   .______    _______ 
            /       | /      | /  __  \  |   _  \  |   ____|
           |   (----`|  ,----'|  |  |  | |  |_)  | |  |__   
            \   \    |  |     |  |  |  | |   ___/  |   __|  
        .----)   |   |  `----.|  `--'  | |  |      |  |____ 
        |_______/     \______| \______/  | _|      |_______|
        _________________________________________________________________________________________________                                                    
    '''
    # scope methods go here
    def _init_scope(self):
        try:
            self.scope = scope()
        except:
            QMessageBox.critical(self, 'Error', 'Unable to connect to oscilloscope - Check your com port and ensure it was closed properly before connecting again')
        else:
            self._scope_get_all_values()

    '''_______________________________________________________________________________________________________'''

    def _update_clock(self):
        current_date_time = QDate.currentDate().toString() + ' ' + QTime.currentTime().toString()
        self.clock_label.setText(current_date_time)
     
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window()
    win.show()
    sys.exit(app.exec())