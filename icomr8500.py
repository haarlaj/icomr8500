import serial
import numpy as np

class IcomR8500:
    header = "FEFE" # fixed header
    radioAddress = "4A"
    computerAddress = "E0"
    radTofreq = [8,9,6,7,4,5,2,3,0,1]
    freqToRad = [8,9,6,7,4,5,2,3,0,1]

    #ser = serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=1)
    def __init__(self, serialport="/dev/ttyUSB0", baudrate=19200, timeout=1):

        # header = "FEFE"
        # radioAddress = "A4"
        # computerAddress = "E0"

        self.serialPort = serialport
        self.baudrate = baudrate
        self.timeout = timeout
        
        try:
            self.ser = serial.Serial(self.serialPort,baudrate=self.baudrate,timeout=self.timeout)
        except:
            return "Init failed to open radio"

    def setPort(self,serialPort = "/dev/ttyUSB0"):
        self.serialPort = serialPort

    def printPort(self):
        return self.serialPort

    def setRadioAddress(self,radioAddress = "4A"):
        self.radioAddress = radioAddress

    def printRadioAddress(self):
        return self.radioAddress

    def setBaudrate(self, baudrate = "19600"):
        self.baudrate = baudrate

    def returnBaudrate(self):
        return self.baudrate

    def setComputerAddress(self, computerAddress = "E0"):
        self.computerAddress = computerAddress

    def readFreqEdges(self): # return min and max frequencies for the radio, toimii
        Cn = "02"
        value = self.writeToRadio(Cn)
        freq1 = self.FreqToRad(value[:10]) # min freq
        freq2 = self.FreqToRad(value[12:]) # max freq
        return freq1, freq2
    
    def readOperFreq(self): # toimii
        Cn = "03"
        freq = self.writeToRadio(Cn)
        return int(self.FreqToRad(freq))
        
    def readOperMode(self): # toimii
        Cn = "04"
        mode = self.writeToRadio(Cn)
        print(mode)
        if mode == "0001":
            return "LSB 2.2kHz"
        elif mode == "0101":
            return "USB 2.2kHz"
        elif mode == "0202":
            return "AM 5.5kHz"
        elif mode == "0201":
            return "AM narrow 2.2kHz"
        elif mode == "0203":
            return "AM wide 12kHz"
        elif mode == "0301":
            return "CW 2.2kHz"
        elif mode == "0302":
            return "CW narrow 500Hz"
        elif mode == "0501":
            return "FM 12kHz"
        elif mode == "0502":
            return "FM narrow 5.5kHz"
        elif mode == "0601":
            return "FM wide 150kHz"
        return mode
        
    def readMchContentsPackage(self,data):
        Cn = "1A"
        Sc = "01"
        return self.writeToRadio(Cn,Sc,data)
        
    def readBankName(self,data):
        Cn = "1A"
        Sc = "03"
        return self.writeToRadio(Cn,Sc,data)

        # returns squelch on (0101) / off (0100)
    def readSquelchCondition(self): 
        Cn = "15"
        Sc = "01"
        value = self.writeToRadio(Cn,Sc)
        if value == "0101":
            print("Squelch Off")
        else:
            print("Squelch On")
        return value
    
        # returns S-meter level
    def readSmeterLevel(self):
        Cn = "15"
        Sc = "02"
        return self.writeToRadio(Cn,Sc)
    
        # returns Radio address
    def readModelID(self):
        Cn = "19"
        Sc = "00"
        return self.writeToRadio(Cn,Sc)

    def setFreq(self, freq):
        Cn = "05"
        Sc = ""
        data = self.FreqToRad(freq)
        return self.writeToRadio(Cn,Sc,data)
        
    def setOpMode(self, mode): # toimii
        Cn = "06"
        if mode == "LSB" or mode == 0:
            Sc = "0001"
        elif mode == "USB" or mode == 1:
            Sc = "0101"
        elif mode == "AM" or mode == 2:
            Sc = "0202"
        elif mode == "AMn" or mode == 3:
            Sc = "0201"
        elif mode == "AMw" or mode == 4:
            Sc = "0203"
        elif mode == "CW" or mode == 5:
            Sc = "0301"
        elif mode == "CWn" or mode == 6:
            Sc = "0302"
        elif mode == "FM" or mode == 7:
            Sc = "0501"
        elif mode == "FMn" or mode == 8:
            Sc = "0502"
        elif mode == "FMw" or mode == 9:
            Sc = "0601"
        else:
            return "Mode not supperted"
        return self.writeToRadio(Cn,Sc)

        # set Memory channel (from 00 to 99)
    def MemoryChannelSelection(self, data):
        Cn = "08"
        Sc = ""
        return self.writeToRadio(Cn, Sc, data)

        # set Bank selection (from 00 to 19)
    def BankSelection(self, data):
        Cn = "08"
        Sc = "A0"
        return self.writeToRadio(Cn, Sc, data)

    def MemoryWrite(self):
        Cn = "09"
        Sc = None
        return self.writeToRadio(Cn)

    def SetMCHContentAndWritePackage(self):
        Cn = "1A"
        Sc = "00"
        return self.writeToRadio(Cn)

        # set bank name 8 char long. ascii values
    def SetBankName(self, name):
        Cn = "1A"
        Sc = "02"
        return self.writeToRadio(Cn, Sc, name)

    def MemoryClear(self):
        Cn = "0B"
        Sc = None
        return self.writeToRadio(Cn)

    def StopScan(self):
        Cn = "0E"
        Sc = "00"
        return self.writeToRadio(Cn)

    def ProgrammedScanStart(self):
        Cn = "0E"
        Sc = "02"
        return self.writeToRadio(Cn)

    def AutoMemoryWriteScanStart(self):
        Cn = "0E"
        Sc = "04"
        return self.writeToRadio(Cn)

    def MemoryScanStart(self):
        Cn = "0E"
        Sc = "22"
        return self.writeToRadio(Cn)

    def SelectMemoryScanStart(self):
        Cn = "0E"
        Sc = "23"
        return self.writeToRadio(Cn)

    def ModeSelectScanStart(self):
        Cn = "0E"
        Sc = "24"
        return self.writeToRadio(Cn)

    def PriorityScan(self):
        Cn = "0E"
        Sc = "42"
        return self.writeToRadio(Cn)

    def SEL_CH_Release(self):
        Cn = "0E"
        Sc = "B0"
        return self.writeToRadio(Cn)

    def SEL_CH_Tag(self):
        Cn = "0E"
        Sc = "B1"
        return self.writeToRadio(Cn)

    def VSC_Deactivation(self):
        Cn = "0E"
        Sc = "C0"
        return self.writeToRadio(Cn)

    def VSC_Activation(self):
        Cn = "0E"
        Sc = "C1"
        return self.writeToRadio(Cn)

    def Scan_Resume_Selection_inf(self):
        Cn = "0E"
        Sc = "D0"
        return self.writeToRadio(Cn)

    def Scan_Resume_Selection_off(self):
        Cn = "0E"
        Sc = "D1"
        return self.writeToRadio(Cn)

    def Scan_Resume_Selection_DLY(self):
        Cn = "0E"
        Sc = "D3"
        return self.writeToRadio(Cn)

        # toimii, custom step todo
        # programmable step 0.5 - 199.5 kHz in 0.5 kHz steps
    def SetTuningStep(self, stepfreq, custom = ""):
        Cn = "10"
        if stepfreq == "10Hz" or stepfreq == 0:
            Sc = "00"
        elif stepfreq == "50Hz" or stepfreq == 1:
            Sc = "01"
        elif stepfreq == "100Hz" or stepfreq == 2:
            Sc = "02"
        elif stepfreq == "1kHz" or stepfreq == 3:
            Sc = "03"
        elif stepfreq == "2.5kHz" or stepfreq == 4:
            Sc = "04"
        elif stepfreq == "5kHz" or stepfreq == 5:
            Sc = "05"
        elif stepfreq == "9kHz" or stepfreq == 6:
            Sc = "06"
        elif stepfreq == "10kHz" or stepfreq == 7:
            Sc = "07"
        elif stepfreq == "12.5kHz" or stepfreq == 8:
            Sc = "08"
        elif stepfreq == "20kHz" or stepfreq == 9:
            Sc = "09"
        elif stepfreq == "25kHz" or stepfreq == 10:
            Sc = "10"
        elif stepfreq == "100kHz" or stepfreq == 11:
            Sc = "11"
        elif stepfreq == "1MHz" or stepfreq == 12:
            Sc = "12"
        elif stepfreq == "Prog" or stepfreq == 13:
            Sc = "13"
            custom = "9519"
        else:
            return "Mode not supperted"
        return self.writeToRadio(Cn, Sc, custom)
        
    def setAttenuator(self, attenuation): #toimii
        Cn = "11"
        if attenuation == "OFF" or attenuation == 0:
            Sc = "00"
        elif attenuation == "10dB" or attenuation == 1:
            Sc = "10"
        elif attenuation == "20dB" or attenuation == 2:
            Sc = "20"
        elif attenuation == "30dB" or attenuation == 3:
            Sc = "30"
        else:
            return "Value not supported"
        return self.writeToRadio(Cn,Sc)

        # ei hajua mitä tekee / toimiiko
    def VoiceSynt(self, value):
        Cn = "13"
        Sc = "00"
        return self.writeToRadio(Cn,Sc,value)

        # range 0000 to 0255
    def AFGain(self, value): # toimii
        Cn = "14"
        Sc = "01"
        value = str(int(value)).zfill(4)
        return self.writeToRadio(Cn, Sc, value)
    
        # range 0000 to 0255
    def SquelchLevel(self, value): # toimii
        Cn = "14"
        Sc = "03"
        value = str(int(value)).zfill(4)
        return self.writeToRadio(Cn, Sc, value)
    
        # range 0000 to 0255, center 128
    def IFShift(self, value): # toimii
        Cn = "14"
        Sc = "04"
        value = str(int(value)).zfill(4)
        return self.writeToRadio(Cn, Sc, value)

        # range 0000 to 0255, center 128
    def APFControl(self, value): # toimii
        Cn = "14"
        Sc = "05"
        value = str(int(value)).zfill(4)
        return self.writeToRadio(Cn, Sc, value)

        # Automatic Gain Control
    def MemClear_AGC_Off(self):
        Cn = "16"
        Sc = "10"
        return self.writeToRadio(Cn)

        # Automatic Gain Control
    def MemClear_AGC_On(self):
        Cn = "16"
        Sc = "11"
        return self.writeToRadio(Cn)
        
        # Noice Blocker
    def MemClear_NB_Off(self):
        Cn = "16"
        Sc = "20"
        return self.writeToRadio(Cn)
        
        # Noice Blocker
    def MemClear_NB_On(self):
        Cn = "16"
        Sc = "21"
        return self.writeToRadio(Cn)

        # Audio peak filter
    def MemClear_APF_Off(self):
        Cn = "16"
        Sc = "30"
        return self.writeToRadio(Cn, Sc)

        # Audio peak filter
    def MemClear_APF_On(self):
        Cn = "16"
        Sc = "31"
        return self.writeToRadio(Cn, Sc)

    def Power_Off(self): # toimii
        Cn = "18"
        Sc = "00"
        self.writeToRadio(Cn,Sc)
        
    def Power_On(self): # toimii
        Cn = "18"
        Sc = "01"
        self.writeToRadio(Cn,Sc)
        
    def FreqToRad(self, value=0): # toimii
        value = str(int(value)).zfill(10)
        #print(''.join([value[i] for i in [8,9,6,7,4,5,2,3,0,1]]))
        return ''.join([value[i] for i in [8,9,6,7,4,5,2,3,0,1]])
    

    def writeToRadio(self, Cn = "", Sc="", data=""):
        dataToRadio = self.header + self.radioAddress + self.computerAddress + Cn + Sc + data + "FD"
        print("dataToRadio: " + dataToRadio)
        testcode = bytes.fromhex(dataToRadio)
        # print("sending over serial:" + str(testcode))
        self.ser.write(testcode)
        
        testcode_echo = self.ser.read_until(b'\xfd').hex()
        reply = self.ser.read_until(b'\xfd').hex()[10:-2]
        
        print("reading reply: " + reply)
        if (reply.lower() == (self.header + self.radioAddress +  self.computerAddress + "FB" + "FD").lower()):
            return "OK"
        elif (reply.lower() == (self.header + self.radioAddress + self.computerAddress + "FA" + "FD").lower()):
            return "NG"
        else:
            return reply