import stellarnet_driver3 as sn
import threading, time
import usb

# set pauses function?
global spectrometers_running

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
        print('spectrometer has been yeeted')

    def getSpectrum(self, spectrometer, wav, inttime, scansavg, smooth):
        spectrometer['device'].set_config(int_time=inttime, scans_to_avg=scansavg, x_smooth=smooth)
        sn.setTempComp(spectrometer, True) 
        spectrum = sn.array_spectrum(spectrometer, wav)
        return spectrum 
       
    def external_trigger(self, spectrometer,trigger):
        sn.ext_trig(spectrometer,trigger)   


    
if __name__ == '__main__':
    print(sn.version())
    print(sn.find_devices())
    spectrometer0, wav0 = sn.array_get_spec(2)
    spectrometer1, wav1 = sn.array_get_spec(1)
    spectrometer2, wav2 = sn.array_get_spec(0)
    spectrometer3, wav3 = sn.array_get_spec(3)
    spectrometer4, wav4 = sn.array_get_spec(4)
    spectrometer5, wav5 = sn.array_get_spec(5)
    specs = [spectrometer0, spectrometer1, spectrometer2, spectrometer3, spectrometer4, spectrometer5]
    wavs = [wav0, wav1, wav2, wav3, wav4, wav5]
    names = ['1', '2', '3', '4', '5']
    spectrometers_running = True
    # threads = [threading.Thread(target=StellerNetTriggerThread, args=(specs[1], wavs[1], 1, names[1]))]
    threads = []
    for spec, wav, name in zip(specs, wavs, names):
        threads.append(threading.Thread(target=StellerNetTriggerThread, args=(spec, wav, 1, name)))

    for i in threads:
        i.start()
    print("all spectrometers initalized")
    input()

    spectrometers_running = False

    
