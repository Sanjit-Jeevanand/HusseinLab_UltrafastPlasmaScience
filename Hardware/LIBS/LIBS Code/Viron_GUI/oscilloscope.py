import pyvisa as visa
import numpy as np
class scope:
    def __init__(self):
        # Connect to the oscilloscope
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource('USB0::0x0699::0x03C7::C020817::INSTR')
        self.yscale = 1
        self.xincr = 1
        
    def set_params(self, data_source, trig_source, v_div, t_div, rec_length):
        # Set up acquisition parameters
        self.scope.write('DATa:SOUrce '+ data_source)   # Select channel 4 as data source
        self.scope.write('DATa:ENCdg RIBinary')   # Set binary data encoding
        self.scope.write('WFMPre:XINcr?')   # Query the x-axis increment
        self.xincr = float(scope.read())   # Convert the string response to a float  
        self.scope.write('WFMPre:YMUlt?')   # Query the y-axis scale
        self.yscale = float(scope.read())   # Convert the string response to a float
        self.scope.write('TRIGger:EDGE:SOURce '+ trig_source)   # Set the trigger source to channel 4
        self.scope.write('TRIGger:EDGE:SLOPe POSitive')   # Set the trigger slope to positive
        # scope.write('TRIGger:LEVel CH1,0')   # Set the trigger level to 0V
        self.scope.write('DAT:STAR 1')
        self.scope.write('DAT:STOP '+ rec_length)
        self.scope.write('DAT:STOP '+ data_source)
        self.scope.write('CH1:SCALE '+ v_div)  # Set the vertical scale of channel 4 to 1V/div
        self.scope.write('HOR:SCALE '+ t_div) # Set the horizontal scale to 1ms/div

    def wait_for_trigger_and_get_data(self):
        # This will wait for the trigger and then get the data. The data will
        # be returned for further async processing in a thread or something.
        
        # Arm the scope and wait for trigger
        scope.write('ACQuire:STOPAfter SEQuence')   # Stop acquisition after one sequence
        scope.write('ACQuire:STATE ON')   # Start acquisition
        scope.query('*OPC?')   # Wait for acquisition to complete
        # Read the acquired data
        scope.write('CURVE?')   # Query the waveform data
        data = scope.read_raw()   # Read the raw binary data
        return data
        
    def handle_data(self, data):
        # takes in data from the scope and returns a numpy array of the data. 
        # meant for use in a thread asynchroneously after wait_for_trigger_and_get_data
        
        headerlen = 2 + int(data[1])   # Determine the length of the header
        # header = data[:headerlen]   # Extract the header
        ADC_wave = data[headerlen:-1]   # Extract the ADC waveform data
        ADC_wave = np.frombuffer(ADC_wave, 'B')   # Convert the binary data to integers
        ADC_wave = ADC_wave - 127   # Convert the ADC values to signed integers
        Volts_wave = self.yscale * ADC_wave   # Convert the ADC values to volts
        Volts_wave = Volts_wave - np.mean(Volts_wave)
        
        # Extract the x-axis data
        xzero = float(scope.query('WFMPre:XZEro?'))
        Time_wave = np.arange(len(Volts_wave)) * self.xincr + xzero
        
        # Time_wave = np.arange(0, xincr * len(Volts_wave), xincr)   # Generate the time axis
        # Time_wave = np.linspace(0, xincr * len(Volts_wave), len(Volts_wave))   # Generate the time axis
        data_oci = np.array([Time_wave, Volts_wave])
        data_oci = data_oci.T
        
        return data_oci
'''
class ocilloscopeThread(threading.Thread):
    def __init__(self, data_source, trig_source, v_div, t_div, rec_length):
        super(ocilloscopeThread,self).__init__()
        # self.start = start
        global data_oci
        data_oci=self.ocilloscope(data_source, trig_source, v_div, t_div, rec_length)
    def ocilloscope(self, data_source, trig_source, v_div, t_div, rec_length):
        # Set up acquisition parameters
        scope.write('DATa:SOUrce '+ data_source)   # Select channel 4 as data source
        scope.write('DATa:ENCdg RIBinary')   # Set binary data encoding
        scope.write('WFMPre:XINcr?')   # Query the x-axis increment
        xincr = float(scope.read())   # Convert the string response to a float  
        scope.write('WFMPre:YMUlt?')   # Query the y-axis scale
        yscale = float(scope.read())   # Convert the string response to a float
        scope.write('TRIGger:EDGE:SOURce '+ trig_source)   # Set the trigger source to channel 4
        scope.write('TRIGger:EDGE:SLOPe POSitive')   # Set the trigger slope to positive
        # scope.write('TRIGger:LEVel CH1,0')   # Set the trigger level to 0V
        scope.write('DAT:STAR 1')
        scope.write('DAT:STOP '+ rec_length)
        scope.write('DAT:STOP '+ data_source)
        scope.write('CH1:SCALE '+ v_div)  # Set the vertical scale of channel 4 to 1V/div
        scope.write('HOR:SCALE '+ t_div) # Set the horizontal scale to 1ms/div
        
        # Arm the scope and wait for trigger
        scope.write('ACQuire:STOPAfter SEQuence')   # Stop acquisition after one sequence
        scope.write('ACQuire:STATE ON')   # Start acquisition
        scope.query('*OPC?')   # Wait for acquisition to complete

        # Read the acquired data
        scope.write('CURVE?')   # Query the waveform data
        data = scope.read_raw()   # Read the raw binary data
        headerlen = 2 + int(data[1])   # Determine the length of the header
        header = data[:headerlen]   # Extract the header
        ADC_wave = data[headerlen:-1]   # Extract the ADC waveform data
        ADC_wave = np.frombuffer(ADC_wave, 'B')   # Convert the binary data to integers
        ADC_wave = ADC_wave - 127   # Convert the ADC values to signed integers
        Volts_wave = yscale * ADC_wave   # Convert the ADC values to volts
        Volts_wave = Volts_wave - np.mean(Volts_wave)
        
        # Extract the x-axis data
        xzero = float(scope.query('WFMPre:XZEro?'))
        Time_wave = np.arange(len(Volts_wave)) * xincr + xzero
        
        # Time_wave = np.arange(0, xincr * len(Volts_wave), xincr)   # Generate the time axis
        # Time_wave = np.linspace(0, xincr * len(Volts_wave), len(Volts_wave))   # Generate the time axis
        data_oci = np.array([Time_wave, Volts_wave])
        data_oci = data_oci.T
        
        return data_oci
        
        # self.plot_graph_10.clear()
        # self.plot_graph_10.plot(Time_wave, Volts_wave, pen='r')
'''