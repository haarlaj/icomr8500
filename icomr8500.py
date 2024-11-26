import serial

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

    def readFreqEdges(self):
        Cn = "02"
        return self.writeToRadio(Cn)
    
    def readOperFreq(self):
        Cn = "03"
        reply = self.writeToRadio(Cn)
        #print(reply)
        return reply
        
    def readOperMode(self):
        Cn = "04"
        Sn = "00"
        return self.writeToRadio(Cn)
        
    def readMchContentsPackage(self,data):
        Cn = "1A"
        Sc = "01"
        return self.writeToRadio(Cn,Sc,data)
        
    def readBankName(self,data):
        Cn = "1A"
        Sc = "03"
        return self.writeToRadio(Cn,Sc,data)

        # returns squelch on (01) / off (00)
    def readSquelchCondition(self): 
        Cn = "15"
        Sc = "01"
        return self.writeToRadio(Cn,Sc)
    
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
        respTofreq
        data = "9078563412"
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

    def VoiceSynt(self):
        Cn = "13"
        Sc = "00"
        return self.writeToRadio(Cn)

        # range 0000 to 0255
    def AFGain(self, value):
        Cn = "14"
        Sc = "01"
        return self.writeToRadio(Cn)
    
        # range 0000 to 0255
    def SquelchLevel(self, value):
        Cn = "14"
        Sc = "03"
        return self.writeToRadio(Cn)
    
        # range 0000 to 0255, center 128
    def IFShift(self, level):
        Cn = "14"
        Sc = "04"
        return self.writeToRadio(Cn)

        # range 0000 to 0255, center 128
    def APFControl(self, level):
        Cn = "14"
        Sc = "05"
        return self.writeToRadio(Cn)

    def MemClear_AGC_Off(self):
        Cn = "16"
        Sc = "10"
        return self.writeToRadio(Cn)

    def MemClear_AGC_On(self):
        Cn = "16"
        Sc = "11"
        return self.writeToRadio(Cn)
        
    def MemClear_NB_Off(self):
        Cn = "16"
        Sc = "20"
        return self.writeToRadio(Cn)
        
    def MemClear_NB_On(self):
        Cn = "16"
        Sc = "21"
        return self.writeToRadio(Cn)

    def MemClear_APF_Off(self):
        Cn = "16"
        Sc = "30"
        return self.writeToRadio(Cn)

    def MemClear_APF_On(self):
        Cn = "16"
        Sc = "31"
        return self.writeToRadio(Cn)

    def Power_Off(self):
        Cn = "18"
        Sc = "00"
        self.writeToRadio(Cn,Sc)
        
    def Power_On(self):
        Cn = "18"
        Sc = "01"
        self.writeToRadio(Cn,Sc)
        
    def respToFreq(self, freqBytes):
        
        respTofreq = [8,9,6,7,4,5,2,3,0,1]
        respTofreqExp = [1e1,1e0,1e3,1e2,1e5,1e4,1e7,1e6,1e9,1e8]

        freq = fromradio[1][10:-2]
        # print(freq)
        freq2 = 0
        for idy in respTofreq:
            freq2 += int(freq[idy])*respTofreqExp[idy] 
        print(freq2)


    def writeToRadio(self, Cn = "", Sc="", data=""):
        dataToRadio = self.header + self.radioAddress + self.computerAddress + Cn + Sc + data + "FD"
        print("dataToRadio: " + dataToRadio)
        testcode = bytes.fromhex(dataToRadio)
        # print("sending over serial:" + str(testcode))
        self.ser.write(testcode)
        
        reply = self.ser.read_until(b'\xfd').hex()
        reply2 = self.ser.read_until(b'\xfd').hex()
        
        print("reading reply: " + reply)
        print("reading reply2: " + reply2)
        if (reply.lower() == (self.header + self.radioAddress + self.computerAddress + "FB" + "FD").lower()):
            return "OK"
        elif (reply.lower() == (self.header + self.radioAddress + self.computerAddress + "FA" + "FD").lower()):
            return "NG"
        else:
            return reply, reply2