import glob
import numpy as np
import pandas as pd
import tables
import sys
import os
import scipy as sp
import matplotlib.pyplot as plt


# !!! START OF LIBRARY !!!

#Class SCRAMTarget: converts temperatures into emission spectra
#tempLayers holds the temperatures at each point in the copper target
#k and j hold scipy.interpolator objects that take arrays of the form [E1, E2...], [T1, T1, ...]
# Example: k([8001,120]) would return the k value at 8000keV energy and 120eV temp
#en is an array holding the energy values extracted from SCRAM
class SCRAMTarget:
    def __init__(self,temps,k,j,en):
        self.temps = [temps[0]]*5
        self.k = k
        self.j = j
        self.en = en
        self.layers = []
        self.generateLayers()

    def generateLayers(self):
        # for i,t in enumerate(self.temps):
        for t in self.temps:
            k_layer = self.k(self.en,t)
            j_layer = self.j(self.en,t)
            self.layers.append([t,k_layer,j_layer])

    def getTransmission(self,layer,projection):
        return np.exp(-layer[1]*1e-5*projection)

    # def getIntensity(self,layer,trans):
    #     return layer[2]/layer[1]*(1-trans)

    def transportEmission(self,viewingAngle = 0,rear = False):
        projection = 1./np.cos(np.radians(viewingAngle))
        intensityTotal =0
        trans_layers = [self.getTransmission(layer,projection) for layer in self.layers]

        for i,layer in enumerate(self.layers):
            intensity_layer = layer[2]/layer[1]*(1-trans_layers[i])
        if rear:
            transmission = np.prod(trans_layers[i+1:],axis = 0)
        else:
            transmission = np.prod(trans_layers[:i],axis = 0)  
        intensityTotal += intensity_layer*transmission
        return intensityTotal


    def model(self):
        
        #initialize with new temps
        self.generateLayers()

        #Assume 5um Spot Size, 1ps Emission Time
        area = np.pi*(2.5e-4)**2
        tau = 1e-12
        scaling = area*tau/(np.pi/4000)
        sigma = 8/(2*np.sqrt(2*np.log(2))) #not sure where this comes from

        #Front Von Hamos Spectra
        front_emission = self.transportEmission(45,rear=False)

        # SimulatedVH = sp.ndimage.gaussian_filter1d(front_emission*scaling,sigma)                                            #COMMENT EDIT
        #what is all the funky unit conversion?
        gaussLayerFront = sp.ndimage.gaussian_filter1d(front_emission*scaling*1000,8/(2*np.sqrt(2*np.log(2))))            #UNCOMMENT OG

        #Rear High Res. Spectra
        rear_emission = self.transportEmission(0,rear=True)
        # SimulatedHR = sp.ndimage.gaussian_filter1d(rear_emission*scaling*1000,sigma/8)                   #COMMENT EDIT
        #what is all the funky unit conversion?
        gaussLayerRear = sp.ndimage.gaussian_filter1d(rear_emission*scaling*1000,1/(2*np.sqrt(2*np.log(2))))              #UNCOMMENT OG

        #Honestly still not sure what this does... Think it can be removed, but then what is the point of this function?
        # SimulatedVH = sp.interpolate.interp1d(self.en/1000,gaussLayerFront)                                        #UNCOMMENT OG
        # SimulatedHR = sp.interpolate.interp1d(self.en/1000,gaussLayerRear)                                         #UNCOMMENT OG


        #Set up axes for VH and HR evenly spaced intensity points 
        enrg_axs_VH = np.linspace(8,9.97,3000)
        enrg_axs_HR = np.linspace(8,8.45,2000)

        # return SimulatedVH(enrg_axs_VH), SimulatedHR(enrg_axs_HR)
        # return front_emission, rear_emission
        # return SimulatedVH, SimulatedHR
        return gaussLayerFront, gaussLayerRear
