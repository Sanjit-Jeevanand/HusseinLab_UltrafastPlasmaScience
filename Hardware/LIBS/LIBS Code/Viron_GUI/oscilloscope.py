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
        self.set_data_source(data_source)
        self.scope.write('DATa:ENCdg RIBinary')   # Set binary data encoding
        self.scope.write('WFMPre:XINcr?')   # Query the x-axis increment
        self.xincr = float(scope.read())   # Convert the string response to a float  
        self.scope.write('WFMPre:YMUlt?')   # Query the y-axis scale
        self.yscale = float(scope.read())   # Convert the string response to a float
        self.set_trigger_source(trig_source)
        self.scope.write('TRIGger:EDGE:SLOPe POSitive')   # Set the trigger slope to positive
        self.set_rec_len(rec_length)
        self.set_t_div(t_div)
        self.set_v_div(v_div)

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

    def set_data_source(self, data_source):
        self.scope.write('DATa:SOUrce '+ str(data_source))
    
    def set_trigger_source(self, trig_source):
        self.scope.write('TRIGger:EDGE:SOURce '+ str(trig_source))
        
    def set_v_div(self, v_div):
        self.scope.write('CH1:SCALE '+ str(v_div))
    
    def set_t_div(self, t_div):
        self.scope.write('HOR:SCALE '+ str(t_div))
        
    def set_rec_len(self, len):
        self.scope.write('DAT:STAR 1')
        self.scope.write('DAT:STOP '+ len)
