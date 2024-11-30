import time
from icomr8500 import IcomR8500

icom = IcomR8500("/dev/ttyUSB0")
#print(icom.readFreqEdges())
# print(icom.printPort())
# print(icom.printRadioAddress())
# print(icom.returnBaudrate())
#print("Operation Frequency")
#print(icom.readOperFreq())
#print(icom.Power_Off()) # toimii
#time.sleep(5)
#print(icom.Power_On()) # toimii
#print("Operation Mode")
#print(icom.readOperMode())

# icom.BankSelection("01")
#icom.readSmeterLevel()
#print(icom.readOperFreq())

#for i in np.arange(0,10):
#    icom.setOpMode(i)
#    time.sleep(1)
#icom.setOpMode("AM")


#for i in np.arange(0,14):
#    icom.SetTuningStep(i)
#    time.sleep(1)

#print("Operation Frequency")
#print(icom.setFreq(94.0e6))
#print(icom.readOperFreq())

print("read bank name")
channel = icom.readMchContentsPackage(19,23)
print("jee")
print(channel.frequency)
#print(channel.frequency)
#print(channel.mode)
#print(channel.tuningstep)
#print(channel.attenuation)
#print(channel.SCN)
#print(channel.channelname)
#print(icom.MemClear_AGC_Off())
#print(icom.MemClear_AGC_On())
#print(icom.readSmeterLevel())
#icom.SetBankName(1,"Radeo")
#icom.readModelID()
#icom.setFreq(94e6)
print(icom.SetMCHContentAndWritePackage(0,10,channel))
#icom.AFGain(40)
#icom.SquelchLevel(120)
#icom.IFShift(128)
#icom.APFControl(128)
#print(icom.readSmeterLevel())
#print(icom.SetTuningStep(11))

#icom.APF_On()
#time.sleep(5)
#icom.APF_Off()