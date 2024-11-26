import serial

class IcomR8500:
    header = "FEFE" # fixed header
    radioAddress = "4A"
    computerAddress = "E0"
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
        Sc = None

    def readOperFreq(self):
        Cn = "03"
        return self.writeToRadio(Cn)
        
    def readOperMode(self):
        Cn = "04"
        return self.writeToRadio(Cn)
        
    def readMchContentsPackage(self):
        Cn = "1A"
        Sc = "01"
        return self.writeToRadio(Cn,Sc)
        
    def readBankName(self):
        Cn = "1A"
        Sc = "03"
        return self.writeToRadio(Cn,Sc)

    def readSquelchCondition(self):
        Cn = "15"
        Sc = "01"
        return self.writeToRadio(Cn,Sc)
    
    def readSmeterLevel(self):
        Cn = "15"
        Sc = "02"
        return self.writeToRadio(Cn,Sc)
    
    def readModelID(self):
        Cn = "19"
        Sc = "00"
        return self.writeToRadio(Cn,Sc)

    def setFreq(self, freq):
        Cn = "05"
        Sc = ""
        data = "9078563412"
        return self.writeToRadio(Cn,Sc,data)
        
    def setOpMode(self, mode):
        Cn = "06"
        if mode == "LSB":
            Sc = "0001"
        elif mode == "USB":
            Sc = "0101"
        elif mode == "AM":
            Sc = "0202"
        elif mode == "AMn":
            Sc = "0201"
        elif mode == "AMw":
            Sc = "0203"
        elif mode == "CW":
            Sc = "0301"
        elif mode == "CWn":
            Sc = "0302"
        elif mode == "FM":
            Sc = "0501"
        elif mode == "FMn":
            Sc = "0502"
        elif mode == "FMw":
            Sc = "0601"
        else:
            return "Mode not supperted"
        return self.writeToRadio(Cn)

    def MemoryChannelSelection(self):
        Cn = "08"
        Sc = None
        return self.writeToRadio(Cn)

    def BankSelection(self):
        Cn = "08"
        Sc = "A0"
        return self.writeToRadio(Cn)

    def MemoryWrite(self):
        Cn = "09"
        Sc = None
        return self.writeToRadio(Cn)

    def SetMCHContentAndWritePackage(self):
        Cn = "1A"
        Sc = "00"
        return self.writeToRadio(Cn)

    def SetBankName(self):
        Cn = "1A"
        Sc = "02"
        return self.writeToRadio(Cn)

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

    def SetTuningStep(self, step, stepfreq):
        Cn = "10"
        if freq == "10Hz":
            Sc = "00"
        elif freq == "50Hz":
            Sc = "01"
        elif freq == "100Hz":
            Sc = "02"
        elif freq == "1kHz":
            Sc = "03"
        elif freq == "2.5kHz":
            Sc = "04"
        elif freq == "5kHz":
            Sc = "05"
        elif freq == "9kHz":
            Sc = "06"
        elif freq == "10kHz":
            Sc = "07"
        elif freq == "12.5kHz":
            Sc = "08"
        elif freq == "20kHz":
            Sc = "09"
        elif freq == "25kHz":
            Sc = "10"
        elif freq == "100kHz":
            Sc = "11"
        elif freq == "1MHz":
            Sc = "12"
        elif freq == "Prog":
            Sc = "13"
        else:
            return "Mode not supperted"
        return self.writeToRadio(Cn)
        
    def setAttenuator(self, attenuation): #toimii
        Cn = "11"
        if attenuation == "OFF":
            Sc = "00"
        elif attenuation == "10dB":
            Sc = "10"
        elif attenuation == "20dB":
            Sc = "20"
        elif attenuation == "30dB":
            Sc = "30"
        else:
            return "Value not supported"
        return self.writeToRadio(Cn,Sc)

    def VoiceSynt(self, freq):
        Cn = "13"
        Sc = "00"
        return self.writeToRadio(Cn)

    def AFGain(self, value):
        Cn = "14"
        Sc = "01"
        return self.writeToRadio(Cn)

    def SquelchLevel(self, value):
        Cn = "14"
        Sc = "03"
        return self.writeToRadio(Cn)
    
    def IFShift(self, level):
        Cn = "14"
        Sc = "04"
        return self.writeToRadio(Cn)

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
        # print(dataToRadio)
        testcode = bytes.fromhex(dataToRadio)
        print(testcode)
        self.ser.write(testcode)
        
        reply = self.ser.read_until(b'\xfd').hex()
        
        print(reply)
        if (reply == self.header + " " + self.radioAddress + " " + self.computerAddress + "FB" + data + "FD"):
            return "OK"
        elif (reply == self.header + " " + self.radioAddress + " " + self.computerAddress + "FA" + data + "FD"):
            return "NG"
        else:
            return reply