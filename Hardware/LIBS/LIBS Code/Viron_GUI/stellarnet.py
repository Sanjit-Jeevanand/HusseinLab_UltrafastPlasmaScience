import threading, time
import numpy as np
import matplotlib.pyplot as plt
import usb

class StellarnetDriverNotFound(Exception):
    pass

try:
    import stellarnet_driver3 as sn
except:
    raise StellarnetDriverNotFound("Stellarnet Driver failed to load :(")
else:
    
    # set pauses function?
    global spectrometers_running, inttime
    spectrometers_running = False
    inttime = 1
    def init_spectrometers():
        num_connected = len(sn.find_devices())
        if num_connected == 0:
            return None, None
        devices = [sn.array_get_spec(i) for i in range(num_connected)]
        devices = sorted(devices, key=lambda x: x[1][0])
        spectrometers = [x[0] for x in devices]
        waves = [wavelengthCalibration(x['device'].get_config()["coeffs"]) for x in spectrometers]
        
        return spectrometers, waves
                    
    def wavelengthCalibration(coeffs):
        pixels = np.arange(2048)
        wave = coeffs[2]+coeffs[0]*pixels/2+coeffs[1]*(pixels/2)**2+coeffs[3]*(pixels/2)**3
        return wave

    def spawnSpectrometerThreads(specs, wavs, plot):
        names = [i for i in range(len(specs))]
        threads = []
        for spec, wav, name in zip(specs, wavs, names):
            threads.append(threading.Thread(target=StellerNetTriggerThread, args=(spec, wav, name, plot)))
        return threads
    
    def startSpectrometerThreads(threads):
        for i in threads:
            i.start()

    class StellerNetTriggerThread(threading.Thread):
        def __init__(self, spec, wav, name, spectraplotter):
            global spectrometers_running
            super(StellerNetTriggerThread,self).__init__()
            # self.inttime = inttime
            self.spec = spec
            self.wav = wav
            self.name = name
            self.plotter = spectraplotter
            self.st = time.time()
            self.last = time.time()
            self.now = time.time()
            self.do_stuff()

        def do_stuff(self):
            while spectrometers_running:
                self.external_trigger(self.spec, True)
                # print(inttime)
                data_stellar0 = self.getSpectrum(self.spec, self.wav, 1, 1)
                self.plotter.updateSpectra(self.name, data_stellar0)
                # self.now = time.time() - self.st
                # print(str(self.now)[:6] + ' ' + str(self.name) + " fired at " + str(1 / (self.now - self.last))[:4] + ' Hz')
                # self.last = self.now
            sn.reset(self.spec)
            print('spectrometer has been yeeted')

        def getSpectrum(self, spectrometer, wav, scansavg, smooth):
            spectrometer['device'].set_config(int_time=inttime, scans_to_avg=scansavg, x_smooth=smooth, tempcomp=1)
            spectrometer['device']._set_device_timing()
            # sn.setTempComp(spectrometer, True) 
            # spectrum = sn.array_spectrum(spectrometer, wav)
            spectrum = spectrometer['device'].read_spectrum()
            return spectrum 
        
        def external_trigger(self, spectrometer,trigger):
            sn.ext_trig(spectrometer,trigger)   


    class SpectraPlotter:
        def __init__(self, wavs, ax, plotfunc):
            print("plotter init")
            global spectrometers_running
            self.specs = [None, None, None, None, None, None]
            self.wavs = wavs
            self.ax = ax
            self.t = threading.Thread(target=self.plotSpectra)
            self.plotfunc = plotfunc
            self.data_plotted = False
            
        def updateSpectra(self, target, spectra):
            "0: 200-300; 1: 300-400, etc"
            target = int(target)
            self.specs[target] = spectra
        
        def resetSpectra(self):
            self.specs = [None, None, None, None, None, None]
            # self.t = threading.Thread(target=self.plotSpectra)
            # self.awaitSpectra()
            self.plotSpectra()
            
        def plotSpectra(self):
            while None in self.specs:
                time.sleep(0.1)
            while not self.data_plotted:
                time.sleep(0.1)
            self.data_plotted = False
            # self.plotfunc(self.specs, self.wavs)
            
            # for i, j in zip(self.wavs, self.specs):    
            #     self.ax.plot(i, j, clear=True)
            
            
            # ax.figure.canvas.draw()
            
            # print("all spectra obtained")
            # print(self.specs)
            self.resetSpectra()
            
        def awaitSpectra(self):
            # if spectrometers_running:
            self.t.start()
            
        def getSpectra(self):
            return self.wavs, self.specs

    if __name__ == '__main__':
        specs, wavs = init_spectrometers()
        names = [i for i in range(len(specs))]
        print(len(specs), len(wavs))
        for i in range(len(specs)):
            print(specs[i]['device'].get_device_id(), wavs[i][0], wavs[i][-1])
        
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # plt.show()
        spectrometers_running = True
        spectraplotter = SpectraPlotter(wavs, ax)
        threads = []
        for spec, wav, name in zip(specs, wavs, names):
            threads.append(threading.Thread(target=StellerNetTriggerThread, args=(spec, wav, 1, name, spectraplotter)))
        for i in threads:
            i.start()
        print("all spectrometers initalized")
        input()

        spectrometers_running = False
        
        
