from instrumental import instrument, list_instruments
from pyvisa import ResourceManager
import time
import numpy as np
import threading

class ThorlabsSpecThread(threading.Thread):
    
    def __init__(self, exposureTime):
        super(ThorlabsSpecThread, self).__init__()
        #Spectrometer initialization
        rm = ResourceManager()
        res = rm.list_resources('?*::?*')
        
        if res:
            paramsets = list_instruments()
            self.spec = instrument(paramsets[0], reopen_policy="reuse") # thorlabs ccs200

            
            # self.running = False
            # self.wave = self.spec._wavelength_array
            # self.spec.set_integration_time(f'{exposureTime} ms')

            # self.spec.start_single_scan()
            # self.intensity = self.spec.get_scan_data()

    def __del__(self):
        self.wait()

    def run(self):
        self.running = True
        self.is_paused = False
        self.spec.start_continuous_scan()
        while self.running:
            if self.spec:
                    self.intensity = np.array(self.spec.get_scan_data())
                    self.acquired.emit(self.intensity)
                    time.sleep(0.001)
            while self.is_paused:
                time.sleep(0.01)
        self.spec.stop_and_clear()

    def stop(self):
        self.running = False
    
    def pause(self):
        self.spec.stop_and_clear()
        self.is_paused = True
    
    def resume(self):
        self.spec.start_continuous_scan()
        self.is_paused = False

    def getWavelength(self):
        return self.wave
    
    def getIntensity(self):
        return self.intensity
    
    def updateThorlabsParameters(self,val,param = None):
        '''Note this function is causing crashing at the moment. Haven't had time to debug it.'''
        self.pause()
        if param == "integrationTime":
            if self.spec:
                self.spec.set_integration_time(f'{val} ms')
                print(self.spec.get_integration_time())
        self.resume()
        
