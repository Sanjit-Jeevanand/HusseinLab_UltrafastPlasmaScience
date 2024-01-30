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
from pyqtgraph import PlotWidget
from telnetGUI import TelnetSessionGUI
from Viron import VironLaser
from XPS import XPS, XPSnotFound

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # set up timer for the clock
        self.clock_timer = QTimer(self, interval=1000, timeout=self._update_clock)
        self.clock_timer.start()
        
        # init variables for if stuff is connected:
        self.is_dg645_connected = False
        self.is_scope_connected = False
        self.is_xps_connected = False
        
        
        # ----------------------------------------------------------------------------------------------
        # DIAGNOSTIC INITALIZATION
        # ----------------------------------------------------------------------------------------------
        if self._init_dg645():
            self.is_dg645_connected = True
            self.dg645_isconnected_label.setText("Connected")
            self.dg645_isconnected_label.setStyleSheet("color: green")
        if self._init_scope():
            self.is_scope_connected = True
            self.scope_isconnected_label.setText("Connected")
            self.scope_isconnected_label.setStyleSheet("color: green")
        self._init_viron()
        
        
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
        self.scope_datasource_select.currentIndexChanged.connect(lambda: self._scope_set_data_source(self.scope_datasource_select.currentText()))
        self.scope_triggersource_select.currentIndexChanged.connect(lambda: self._scope_set_trigger_source(self.scope_triggersource_select.currentText()))
        self.set_scope_params_button.clicked.connect(self._scope_set_all_params)
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


        # connect button
        self.viron_connect_button.clicked.connect(self.handle_connect_to_laser)
        # standby button
        self.viron_standby_button.clicked.connect(self.toggle_standby)
        # stop button
        self.viron_stop_button.clicked.connect(self.toggle_stop)
        # auto fire button
        self.viron_autofire_button.clicked.connect(self.toggle_autofire)
        # single shot button
        self.viron_singlefire_button.clicked.connect(self.toggle_singlefire)
        # set rep rate
        self.viron_set_reprate_button.clicked.connect(self.handle_set_rep_rate)
        # set qs delay
        self.viron_set_qsdelay_button.clicked.connect(self.handle_set_qs_delay)
        # set qs pre
        self.viron_qspre_set_button.clicked.connect(self.handle_set_qs_pre)
        # init tngui layout
        self.tngui_box.addWidget(self.tngui)
        # init statuses
        self.handle_get_status(status_hex="0x000000000000")
        # ----------------------------------------------------------------------------------------------
        
        
        # XPS Stuff
        # ------------------------------------------------------------------------------------------
        # init xpses
        try:
            self.x_xps = XPS()
            self.y_xps = XPS()
        except XPSnotFound:
            QMessageBox.critical(self, 'Error', 'Unable to connect to XPS. Motion control will be unavailable.')
            self.xps_enable_button.setEnabled(False)
            self.xps_init_button.setEnabled(False)
            self.xps_kill_button.setEnabled(False)
        else:
            # max and min values for the stage
            self.abs_min = [0, 0]
            self.abs_max = [50, 50]

            # X-Axis Combo Box
            self.xps_groups = self.x_xps.getXPSStatus()
            self.x_axis_select_box.clear()
            self.x_axis_select_box.addItems(list(self.xps_groups.keys()))
            self.x_axis = str(self.x_axis_select_box.currentText())
            self.x_xps.setGroup(self.x_axis)
            self.stageStatus = self.x_xps.getStageStatus(self.x_axis)
            self.xps_update_group("X")
            self.x_axis_select_box.activated.connect(lambda: self.xps_update_group("X"))

            # Y-Axis Combo Box
            self.y_axis_select_box.clear()
            self.y_axis_select_box.addItems(list(self.xps_groups.keys()))
            self.y_axis_select_box.setCurrentIndex(1)
            self.y_axis = str(self.y_axis_select_box.currentText())
            self.y_xps.setGroup(self.y_axis)
            self.stageStatus = self.y_xps.getStageStatus(self.y_axis)
            self.xps_update_group("Y")
            self.y_axis_select_box.activated.connect(lambda: self.xps_update_group("Y"))
            
            # # Status Buttons
            self.xps_init_button.clicked.connect(self.xps_initialize)
            self.xps_kill_button.clicked.connect(self.xps_kill)
            self.xps_enable_button.clicked.connect(self.xps_enable_disable)
            
            # Travel Limits
            self.set_motion_bounds_button.clicked.connect(self.xps_set_minmax)
            # self.x_min_travel_entry.textChanged.connect(lambda: self.set_minmax("x", "min", self.x_min_travel_entry.text()))
            # self.x_max_travel_entry.textChanged.connect(lambda: self.set_minmax("x", "max", self.x_max_travel_entry.text()))
            # self.y_min_travel_entry.textChanged.connect(lambda: self.set_minmax("y", "min", self.y_min_travel_entry.text()))
            # self.y_max_travel_entry.textChanged.connect(lambda: self.set_minmax("y", "max", self.y_max_travel_entry.text()))
            
            # # Relative Motion Controls
            # # self.rel_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.left_btn.clicked.connect(lambda: self.relative('left'))
            # self.right_btn.clicked.connect(lambda: self.relative('right'))
            # self.down_btn.clicked.connect(lambda: self.relative('down'))
            # self.up_btn.clicked.connect(lambda: self.relative('up'))

            # # Absolute Motion Controls
            # self.abs_x_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.abs_y_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.abs_move_btn.clicked.connect(self.absolute)

            # # Reference Point Commands
            # self.ref = [0, 0]
            # self.set_btn.clicked.connect(lambda: self.ref_commands('set'))
            # self.return_btn.clicked.connect(lambda: self.ref_commands('return'))
            
            # # Raster Input Boxes
            # self.step_length_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.step_length_line.textChanged.connect(lambda: self.raster_inp('step_length'))
            # self.sample_length_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.sample_length_line.textChanged.connect(lambda: self.raster_inp('sample_length'))
            # self.sample_width_line.setValidator(QtGui.QDoubleValidator(0.10, 50.00, 2))
            # self.sample_width_line.textChanged.connect(lambda: self.raster_inp('sample_width'))
            # self.set_x_btn.clicked.connect(lambda: self.raster_inp('set_bound_x'))
            # self.set_y_btn.clicked.connect(lambda: self.raster_inp('set_bound_y'))
            # self.num_shots_line.setEnabled(False)
            # self.num_shots_line.textChanged.connect(lambda: self.raster_inp('num_shots'))
            
            # # Raster Controls
            # self.raster_btn.setEnabled(False)
            # self.raster_btn.clicked.connect(self.start_timer)
            # self.stop_btn_2.clicked.connect(self.end_timer)
            
            # # Timer and Printing of Stage Location
            # self.print_timer = QtCore.QTimer(self, interval = 1000, timeout = self.print_location)
            # self.print_timer.start()
            # self.print_location()
            
            # ------------------------------------------------------------------------------------------
        
        

        # ----------------------------------------------------------------------------------------------
    
    
    '''
        __  ______  ____  
        \ \/ /  _ \/ ___| 
         \  /| |_) \___ \ 
         /  \|  __/ ___) |
        /_/\_\_|   |____/ 
     _________________________________________________________________________________________________              
    '''
    def xps_update_group(self, axis):
        '''
        Sets and gets the status of a new actuator group after changing actuators.
        
        Parameters
        ----------
        axis (string) : The axis of travel that the actuator will be moving along. Either "X" for 
                        x-axis or "Y" for y-axis
        '''
        self.xps_groups = self.x_xps.getXPSStatus()
        if axis == "X": 
            self.x_axis = str(self.x_axis_select_box.currentText())
            self.x_xps.setGroup(self.x_axis)
            self.update_status(self.x_xps.getStageStatus(self.x_axis))
            
        elif axis == "Y":
            self.y_axis = str(self.y_axis_select_box.currentText())
            self.y_xps.setGroup(self.y_axis)
            self.update_status(self.y_xps.getStageStatus(self.y_axis))
    
    def xps_initialize(self):
        '''
        Initializes and homes both selected actuators.
        '''
        self.x_xps.initializeStage(self.x_axis)
        self.x_xps.homeStage(self.x_axis)
        self.y_xps.initializeStage(self.y_axis)
        self.y_xps.homeStage(self.y_axis)
        
        self.update_status(self.x_xps.getStageStatus(self.x_axis))
        self.update_status(self.y_xps.getStageStatus(self.y_axis))
        
    def xps_kill(self):
        '''
        Kills both selected actuators.
        '''
        self.x_xps.killAll(self.x_axis)
        self.y_xps.killAll(self.y_axis)
        
        self.update_status(self.x_xps.getStageStatus(self.x_axis))
        self.update_status(self.y_xps.getStageStatus(self.y_axis))

    def xps_enable_disable(self):
        '''
        Enables or disables both selected actuators depending on its status.
        '''
        if self.x_xps.getStageStatus(self.x_axis).upper() == "Disabled state".upper() \
            or self.y_xps.getStageStatus(self.y_axis).upper() == "Disabled state".upper():
            self.x_xps.enableGroup(self.x_axis)
            self.y_xps.enableGroup(self.y_axis)
        elif self.x_xps.getStageStatus(self.x_axis)[:11].upper() == "Ready state".upper() \
            or self.y_xps.getStageStatus(self.y_axis)[:11].upper() == "Ready state".upper():
            self.x_xps.disableGroup(self.x_axis)
            self.y_xps.disableGroup(self.y_axis)
            
        self.update_status(self.x_xps.getStageStatus(self.x_axis))
        self.update_status(self.y_xps.getStageStatus(self.y_axis))
        
    def xps_set_minmax(self, axis, setting, val):
        '''
        Sets the minimum and maximum points of travel.
        
        Parameters
        ----------
        axis (string) : The axis of travel that the actuator will be moving along. Either "x" for 
                        x-axis or "y" for y-axis
        setting (string) : Setting of whether to set a minimum or maximum. "min" for minimum, 
                           "max" for maximum.
        val (string) : The value to set the minimum or maximum point as. Defaults to 0 for minumum 
                       and 50 for maximum if nothing is inputted.
        '''
        xmin = self.x_min_travel_entry.text()
        xmax = self.x_max_travel_entry.text()
        ymin = self.y_min_travel_entry.text()
        ymax = self.y_max_travel_entry.text()
        
        if float(xmin) < 0 or xmin == '' or float(xmin) > float(xmax):
            xmin = 0
        if float(xmax) > 50 or xmax == '' or float(xmax) < float(xmin):
            xmax = 50
        if float(ymin) < 0 or ymin == '' or float(ymin) > float(ymax):
            ymin = 0
        if float(ymax) > 50 or ymax == '' or float(ymax) < float(ymin):
            ymax = 50
        
        self.x_xps.setminLimit(self.x_axis, float(xmin))
        self.x_xps.setmaxLimit(self.x_axis, float(xmax))
        self.y_xps.setminLimit(self.y_axis, float(ymin))
        self.y_xps.setmaxLimit(self.y_axis, float(ymax))        
        
    
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
            return False
        else:
            self._dg645_get_all_delays()
            self._dg645_get_amplitude_offset()
            self._dg645_get_trigger_source()
            return True
        
    def _dg645_display_delay(self, target):
        # display them delays
        self.dg645.display_delay(target)
        
    def _dg645_set_delays(self):
        # set all delays from pertinent input boxes
        for i, x in enumerate(self.channel_trig_list):
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
            return False
        else:
            self._scope_get_all_values()
            return True
    def _scope_set_data_source(self, source):
        self.scope.set_data_source(source)
        
    def _scope_set_trigger_source(self, source):
        self.scope.set_trigger_source(source)
        
    def _scope_set_all_params(self):
        source = self.scope_datasource_select.currentText()
        trig = self.scope_triggersource_select.currentText()
        vdiv = self.scope_voltsperdiv_entry.text()
        tdiv = self.scope_timeperdiv_entry.text()
        reclen = self.scope_record_length_entry.text()
        if self._is_float(vdiv) and self._is_float(tdiv) and self._is_float(reclen):
            self.scope.set_params(source, trig, vdiv, tdiv, reclen)
        else:
            QMessageBox.critical(self, 'Error', 'Error: Invalid scope parameters')

    '''_______________________________________________________________________________________________________'''
    
    
    '''_______________________________________________________________________________________________________'''
    '''
        __     _____ ____   ___  _   _ 
        \ \   / /_ _|  _ \ / _ \| \ | |
         \ \ / / | || |_) | | | |  \| |
          \ V /  | ||  _ <| |_| | |\  |
           \_/  |___|_| \_\\___/|_| \_|
        _________________________________________________________________________________________________'''
        
    def _init_viron(self):
        self.host = "192.168.103.103"
        self.port = 23
        self.password = "VR6BE4EE"
        try:
            self.tngui = TelnetSessionGUI()
            self.laser = VironLaser(self.host, self.port, self.password, telnetgui=self.tngui)
            self.tngui.set_laser(self.laser)
        except:
            print("failure initalizing Viron")
            return False

        else:
            self.viron_connected = False
            self.currentstate = None
            self.states = ['standby', 'stop', 'fire', 'single_shot']
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.handle_get_status)
            self.status_timer.setInterval(5000)
            return True
        
        
    def handle_get_status(self, status_hex=None):
        """
        Handles the action when the "Get Status" button is clicked.
        Retrieves the laser status hex value and parses it into a status dictionary.
        Then, it displays the status on the GUI.

        Returns:
            None
        """
        if status_hex is None:
            if self.viron_connected:
                status_hex = self.laser.get_status()
            else:
                return
        if status_hex is not None:   
            status = self._parse_status(status_hex)
            
        self.display_status(status)
        self.display_critical_info(status)
        if self.viron_connected:
            self._get_values()
        
    def _get_values(self):
        qs_delay = self.laser.send_command('$QSDELAY ?', response=True)
        qs_pre = self.laser.send_command('$QSPRE ?', response=True)
        reprate = self.laser.send_command('$DFREQ ?', response=True)
        
       
        if qs_delay:
            self.viron_qsdelay_entry.setText(str(qs_delay.split()[1]))
        if qs_pre:
            self.viron_qspre_entry.setText(str(qs_pre).split()[1])
        if reprate:
            self.viron_reprate_entry.setText(str(reprate).split()[1])   
            
    def _parse_status(self, hex_value):
        """
        Parses the status hex value into a dictionary containing the status information.
        
        input:
        - hex_value (str): The status hex value.
        
        return:
        - status (dict): The status dictionary containing key-value pairs.
        """
        
        
        # Convert hex value to binary string
        binary_string = bin(int(hex_value, 16))[2:].zfill(48)

        # Extract individual status based on byte and bit positions
        status = {}

        # Byte 1
        status['Fire Mode'] = 'Disabled' if binary_string[0] == '0' else 'Fire'
        status['Standby Mode'] = 'Stop' if binary_string[1] == '0' else 'Standby'
        status['Diode Trigger Mode'] = 'Internal' if binary_string[2] == '0' else 'External'
        status['Q-Switch Mode'] = 'Internal' if binary_string[3] == '0' else 'External'
        status['Divide By Mode'] = 'Normal' if binary_string[4] == '0' else 'Divide By'
        status['Burst Mode'] = 'Continuous' if binary_string[5] == '0' else 'Burst'
        status['Q-Switch'] = 'Disabled' if binary_string[6] == '0' else 'Enabled'
        status['Ready'] = "Ready" if binary_string[7] == '0' else 'Not Ready'

        # Byte 2
        status['UV Illumination'] = 'Disabled' if binary_string[8] == '0' else 'Enabled'
        status['Remote Q-Switch'] = 'Normal Q-Switch' if binary_string[9] == '0' else 'Q-Switch off'
        status['50 Ohm Trigger Termination'] = 'Laser Disabled' if binary_string[10] == '0' else 'Enabled'
        status['BLE Session Temp'] = 'No Session' if binary_string[11] == '0' else 'Session'
        status['Diode TEC Running Temp'] = 'Off' if binary_string[12] == '0' else 'Run'
        status['LAN Session Temp'] = 'No Session' if binary_string[13] == '0' else 'Session'
        status['NLO Oven 2 Running Temp'] = 'Off' if binary_string[14] == '0' else 'Run'
        status['NLO Oven 1 Running Temp'] = 'Off' if binary_string[15] == '0' else 'Run'

        # Byte 3
        status['Remote Interlock Laser'] = 'No' if binary_string[16] == '0' else 'Yes'
        status['Laser Temperature Range'] = 'OK' if binary_string[17] == '0' else 'Fault'
        status['Charge Fault'] = 'OK' if binary_string[18] == '0' else 'Fault'
        status['Diode Current Fault'] = 'OK' if binary_string[19] == '0' else 'Fault'
        status['Diode Temperature High or Low'] = 'OK' if binary_string[20] == '0' else 'Fault'
        status['Diode Temperature Control Fault'] = 'OK' if binary_string[21] == '0' else 'Fault'
        status['System Interlock System/TEC Temp/Sys OK'] = 'OK' if binary_string[22] == '0' else 'Fault'
        status['System Interlock Laser Node'] = 'OK' if binary_string[23] == '0' else 'Fault'

        # Byte 4
        status['Reserved for BLE'] = 'No Action' if binary_string[24] == '0' else 'No Action'
        status['Reserved'] = 'No Action' if binary_string[25] == '0' else 'No Action'
        status['Operations Config Checksum'] = 'OK' if binary_string[26] == '0' else 'Fault'
        status['Factory Config Checksum'] = 'Ok' if binary_string[27] == '0' else 'Fault'
        status['CAN bus fault'] = 'OK' if binary_string[28] == '0' else 'Fault'
        status['Run time fault'] = 'OK' if binary_string[29] == '0' else 'Fault'
        status['RAM test fault'] = 'OK' if binary_string[30] == '0' else 'Fault'
        status['Watchdog Timeout'] = 'OK' if binary_string[31] == '0' else 'Fault'

        # Byte 5
        status['External Lamp PRF'] = 'OK' if binary_string[32] == '0' else 'PRF High'
        status['Laser Temperature Warning'] = 'OK' if binary_string[33] == '0' else 'Warning'
        status['Pre-Lase Detect/Q-Switch inhibited'] = 'OK' if binary_string[34] == '0' else 'Inhibited'
        status['CAN Bus Illegal ID or data'] = 'No' if binary_string[35] == '0' else 'Yes'
        status['CAN Bus Overrun'] = 'No' if binary_string[36] == '0' else 'Yes'
        status['Diode Current Limit'] = 'OK' if binary_string[37] == '0' else 'Warning'
        status['Reserved for Log Only - Temp Laser'] = 'Temp' if binary_string[38] == '0' else 'Laser'
        status['Diode/TEC Temp. Warning'] = 'OK' if binary_string[39] == '0' else 'Warning'

        # Byte 6
        status['NLO Oven 2 out of tolerance'] = 'No' if binary_string[40] == '0' else 'Yes'
        status['NLO Oven 2 timeout, oven 2 off'] = 'OK' if binary_string[41] == '0' else 'Warning'
        status['NLO Oven 2 over temp, oven 2 off'] = 'OK' if binary_string[42] == '0' else 'Warning'
        status['NLO Oven 2 open sensor, oven 2 off'] = 'OK' if binary_string[43] == '0' else 'Warning'
        status['NLO Oven 1 out of tolerance'] = 'No' if binary_string[44] == '0' else 'Yes'
        status['NLO Oven 1 timeout, oven 1 off'] = 'OK' if binary_string[45] == '0' else 'Warning'
        status['NLO Oven 1 over temp, oven 1 off'] = 'OK' if binary_string[46] == '0' else 'Warning'
        status['NLO Oven 1 open sensor, oven 1 off'] = 'OK' if binary_string[47] == '0' else 'Warning'

        return status
    

    def display_critical_info(self, status):
        """
        Displays the critical status information on the GUI.
        
        Input:
        - status (dict): The status dictionary containing key-value pairs.
        """
        status_text = "Modes:\n"
        status_text += f"  Fire Mode: {status['Fire Mode']}\n"
        status_text += f"  Standby Mode: {status['Standby Mode']}\n"
        status_text += f"  Status: {status['Ready']}\n"
        status_text += f"  Q-Switch: {status['Q-Switch']}\n"
        status_text += "Interlocks:\n"
        status_text += f"  Remote interlock: {status['Remote Interlock Laser']}\n"
        status_text += f"  System Interlock: {status['System Interlock System/TEC Temp/Sys OK']}\n"
        status_text += f"  Laser Node Interlock: {status['System Interlock Laser Node']}\n"
        temps = self.laser.get_temps()
        status_text += "Temperatures:\n"
        status_text += f"  Laser Temp: {temps['Laser Temp']} C\n"
        status_text += f"  Diode Temp: {temps['Diode Temp']} C\n"
        self.critical_status_label.setText(status_text)
        
        
    def display_status(self, status):
        # Define the headers for each bundle of 8 lines
        headers = ["Status Byte 1", "Status Byte 2", "Fault Byte 1", "Fault Byte 2", "Warning Byte 1", "Warning Byte 2"]

        # ToDo: Color code status based on fault/warning
        status_text_1 = ""
        status_text_2 = ""
        i = 0
        j = 0
        for key, value in status.items():
            if i % 8 == 0:
                # Add the header for the current bundle of 8 lines
                header_index = i // 8
                if j > 2:
                    status_text_2 += f"\n{headers[header_index]}:\n"
                else:
                    status_text_1 += f"\n{headers[header_index]}:\n"
                j += 1
            if j > 3:
                status_text_2 += f"  {key}: {value}\n"
            else:
                status_text_1 += f"  {key}: {value}\n"
            i += 1

        self.status_label_left.setText(status_text_1)
        self.status_label_right.setText(status_text_2)
        
    def handle_connect_to_laser(self):
        """
        Handles the action when the "Connect" button is clicked.
        Attempts to connect to the laser using the provided host, port, and password.
        Updates the GUI with the connection status.

        Returns:
            None
        """
        if self.laser.connect_to_laser():
            self.viron_connect_button.setStyleSheet("background-color: green")
            self.viron_isconnected_label.setText("Connected")
            self.viron_isconnected_label.setStyleSheet("color: green")
            self.status_timer.start()
            self.viron_connected = True

        else:
            self.viron_connect_button.setStyleSheet("background-color: red")
            self.viron_isconnected_label.setText("Not Connected")
            self.viron_isconnected_label.setStyleSheet("color: red")
            self.viron_connected = False

    def toggle_standby(self):
        """
        Handles the action when the "Standby" button is clicked.
        Sets the laser in standby mode and updates the GUI accordingly.

        Returns:
            None
        """
        if self.currentstate == 'standby':
            return True
        if self.laser.set_standby():
            self.currentstate = 'standby'
            self.viron_autofire_button.setChecked(False)
            self.viron_stop_button.setChecked(False)
            self.viron_singlefire_button.setChecked(False)
            self.viron_singlefire_button.setStyleSheet("background-color : darkgrey")
            self.viron_standby_button.setStyleSheet("background-color : darkgreen")
            self.viron_stop_button.setStyleSheet("background-color : darkgrey")
            self.viron_autofire_button.setStyleSheet("background-color : darkgrey")
            return True
        print("Failed to set laser to standby")
        return False



    def toggle_stop(self):
        """
        Handles the action when the "Stop" button is clicked.
        Sets the laser in stop mode and updates the GUI accordingly.

        Returns:
            None
        """
        if self.currentstate == 'stop' and self.viron_stop_button.isChecked():
            return True
        
        if self.laser.set_stop():
            self.currentstate = 'stop'
            self.viron_standby_button.setChecked(False)
            self.viron_autofire_button.setChecked(False)
            self.viron_singlefire_button.setChecked(False)
            self.viron_singlefire_button.setStyleSheet("background-color : darkgrey")
            self.viron_standby_button.setStyleSheet("background-color : darkgrey")
            self.viron_stop_button.setStyleSheet("background-color : darkgreen")
            self.viron_autofire_button.setStyleSheet("background-color : darkgrey")
            return True
        else:
            print("failed to set stop")
            return False


    def toggle_autofire(self):
        """
        Handles the action when the "Fire Placeholder" button is clicked.
        Sets the laser in fire mode and updates the GUI accordingly.

        Returns:
            None
        """
        if self.currentstate != 'fire':
            # set to internal trigger
            self.laser.send_command("$QSON 1")
            
        if self.laser.set_fire():
            self.currentstate = 'fire'
        else:
            print("failed to set fire")
            return
        
        self.viron_standby_button.setChecked(False)
        self.viron_stop_button.setChecked(False)
        self.viron_singlefire_button.setChecked(False)
        self.viron_singlefire_button.setStyleSheet("background-color : darkgrey")
        self.viron_standby_button.setStyleSheet("background-color : darkgrey")
        self.viron_stop_button.setStyleSheet("background-color : darkgrey")
        self.viron_autofire_button.setStyleSheet("background-color : red")

    def toggle_singlefire(self):
        """
        Handles the action when the "Set Single Shot" button is clicked.
        Sets the laser in single shot mode and updates the GUI accordingly.

        Returns:
            None
        """
        if self.currentstate != 'single_shot':
            if self.laser.set_single_shot():
                self.currentstate = 'single_shot'
            else:
                print("Single Shot Not Set")
                return

            self.viron_standby_button.setChecked(False)
            self.viron_stop_button.setChecked(False)
            self.viron_autofire_button.setChecked(False)
            self.viron_standby_button.setStyleSheet("background-color : darkgrey")
            self.viron_stop_button.setStyleSheet("background-color : darkgrey")
            self.viron_autofire_button.setStyleSheet("background-color : darkgrey")
            self.viron_singlefire_button.setStyleSheet("background-color : red")
            
        if self.laser.fire_single_shot():
            print("fired mah lazor")  
            
            
    def handle_set_rep_rate(self):
        """
        Handles the action when the "Set Rep Rate" button is clicked.
        Retrieves the repetition rate value from the text entry and sets it on the laser.

        Returns:
            None
        """
        rate = self.viron_reprate_entry.text()
        if rate.isdigit():
            self.laser.set_rep_rate(int(rate))
            
    def handle_set_qs_delay(self):
        '''
        Handles the action when the "Set Q-Switch Delay" button is clicked.
        '''
        delay = self.viron_qsdelay_entry.text()
        if delay.isdigit():
            if self.laser.set_qs_delay(int(delay)):
                print('Q-Switch Delay Set to ', delay)
                return True
        return False
    
    def handle_set_qs_pre(self):
        '''
        Handles the action when the "Set Q-Switch pre" button is clicked.
        '''
        delay = self.viron_qspre_entry.text()
        if delay.isdigit():
            if self.laser.set_qs_pre(int(delay)):
                print('Q-Switch Pre Set to ', delay)
                return True
        return False
             
    def _update_clock(self):
        current_date_time = QDate.currentDate().toString() + ' ' + QTime.currentTime().toString()
        self.clock_label.setText(current_date_time)
     
    def _is_float(self, string):
        if string.replace(".", "").isnumeric():
            return True
        else:
            return False
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window()
    win.show()
    sys.exit(app.exec())