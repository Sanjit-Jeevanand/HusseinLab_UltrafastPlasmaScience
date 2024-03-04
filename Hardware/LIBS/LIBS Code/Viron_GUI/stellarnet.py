import threading, time
import numpy as np
import usb
try:
    import stellarnet_driver3 as sn
except:
    raise("Stellarnet Driver failed to load :(")
else:
    
    # set pauses function?
    global spectrometers_running

    def init_spectrometers():
        num_connected = len(sn.find_devices())
        devices = [sn.array_get_spec(i) for i in range(num_connected)]
        devices = sorted(devices, key=lambda x: x[1][0])
        spectrometers = [x[0] for x in devices]
        waves = [x[1] for x in devices]
        
        return spectrometers, waves
                    
    def wavelengthCalibration(coeffs):
        pixels = np.arange(2048)#.reshape(-1, 1)
        wave = coeffs[2]+coeffs[0]*pixels/2+coeffs[1]*(pixels/2)**2+coeffs[3]*(pixels/2)**3
        return wave

    class StellerNetTriggerThread(threading.Thread):
        def __init__(self, spec, wav, inttime, name):
            global spectrometers_running
            super(StellerNetTriggerThread,self).__init__()
            self.inttime = inttime
            self.spec = spec
            self.wav = wav
            self.name = name
            self.st = time.time()
            self.last = time.time()
            self.now = time.time()
            self.do_stuff()

        def do_stuff(self):
            while spectrometers_running:
                self.external_trigger(self.spec, True)
                data_stellar0 = self.getSpectrum(self.spec, self.wav, self.inttime, 1, 1)
                self.now = time.time() - self.st
                print(str(self.now)[:6] + ' ' + str(self.name) + " fired at " + str(1 / (self.now - self.last))[:4] + ' Hz')
                self.last = self.now
            sn.reset(self.spec)
            print('spectrometer has been yeeted')

        def getSpectrum(self, spectrometer, wav, inttime, scansavg, smooth):
            spectrometer['device'].set_config(int_time=inttime, scans_to_avg=scansavg, x_smooth=smooth)
            sn.setTempComp(spectrometer, True) 
            spectrum = sn.array_spectrum(spectrometer, wav)
            return spectrum 
        
        def external_trigger(self, spectrometer,trigger):
            sn.ext_trig(spectrometer,trigger)   


        
    if __name__ == '__main__':
        specs, wavs = init_spectrometers()
        names = [str(i) for i in range(len(specs))]
        print(len(specs), len(wavs))
        for i in range(len(specs)):
            print(specs[i]['device'].get_device_id(), wavs[i][0], wavs[i][-1])
        
        spectrometers_running = True
        threads = []
        for spec, wav, name in zip(specs, wavs, names):
            threads.append(threading.Thread(target=StellerNetTriggerThread, args=(spec, wav, 1, name)))

        for i in threads:
            i.start()
        print("all spectrometers initalized")
        input()

        spectrometers_running = False
