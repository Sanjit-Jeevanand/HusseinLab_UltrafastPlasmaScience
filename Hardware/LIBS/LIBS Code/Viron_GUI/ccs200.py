from instrumental.drivers import instrument
from instrumental.drivers.spectrometers.thorlabs_ccs import list_instruments
from pyvisa import ResourceManager
import time
import numpy as np
import threading

import sys, os



class ThorlabsSpecThread(threading.Thread):
    
    def __init__(self, exposureTime):
        cwd = os.getcwd()
        sys.path.append(os.path.join(*cwd.split("\\")[:cwd.split("\\").index("HusseinLab_UltrafastPlasmaScience")+1], 'Hardware', "Thorlabs CCS200"))

        # super(ThorlabsSpecThread, self).__init__()
        #Spectrometer initialization
        rm = ResourceManager()
        res = rm.list_resources('?*::?*')
        print(res)
        
        if res:
            paramsets = list_instruments()
            print(paramsets)
            self.spec = instrument(paramsets[0], reopen_policy="reuse") # thorlabs ccs200
            print(self.spec.get_device_info())
            
            # self.running = False
            # self.wave = self.spec._wavelength_array
            # self.spec.set_integration_time(f'{exposureTime} ms')

            # self.spec.start_single_scan()
            # self.intensity = self.spec.get_scan_data()

    # def __del__(self):
    #     self.wait()

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
        
if __name__ == "__main__":
    i = ThorlabsSpecThread(1)
    # print(i.getIntensity())