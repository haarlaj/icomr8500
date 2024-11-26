import time
import numpy as np
from icomr8500 import IcomR8500

icom = IcomR8500()
# icom.readFreqEdges()
# print(icom.printPort())
# print(icom.printRadioAddress())
# print(icom.returnBaudrate())
print("Operation Frequency")
print(icom.readOperFreq())
#print(icom.Power_Off()) # toimii
#time.sleep(5)
#print(icom.Power_On()) # toimii
print("Operation Mode")
print(icom.readOperMode())
print("Model ID")
print(icom.readModelID())

icom.readFreqEdges()
icom.BankSelection("01")
#icom.readSmeterLevel()
#print(icom.readOperFreq())

#for i in np.arange(0,10):
#    icom.setOpMode(i)
#    time.sleep(1)
#icom.setOpMode("AM")


#for i in np.arange(0,14):
#    icom.SetTuningStep(i)
#    time.sleep(1)