import time
from icomr8500 import IcomR8500

icom = IcomR8500()
# print(icom.printPort())
# print(icom.printRadioAddress())
# print(icom.returnBaudrate())
# print(icom.readOperFreq())
# print(icom.Power_Off()) # toimii
#time.sleep(5)
# print(icom.Power_On()) # toimii
print(icom.readOperFreq())
print(icom.readOperMode())
print(icom.readModelID())
icom.readSmeterLevel()
icom.setFreq(1)