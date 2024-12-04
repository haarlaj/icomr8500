import serial

class ChannelData:
    def __init__(self, freqRead, modeRead, tuningStepRead, ATTRead, SCNRead, ChannelNameRead):
        self.frequency = freqRead
        self.mode = modeRead
        self.tuningstep = tuningStepRead
        self.attenuation = ATTRead
        # 00 none, 01 SEL-CH, 02 SKIP-CH, 03 In manual 01 and 02 are reversed?
        self.SCN = SCNRead
        self.channelname = ChannelNameRead

    def raw(self):
        frequency = str(int(self.frequency)).zfill(10)
        frequency = ''.join([frequency[i] for i in [8,9,6,7,4,5,2,3,0,1]])
        mode = self.mode
        tuningstep = self.tuningstep
        attenuation = self.attenuation
        SCN = self.SCN
        channelname = "{:>8}".format(self.channelname[:8]).encode("ASCII").hex()
        # print(frequency)
        # print(mode)
        # print(tuningstep)
        # print(attenuation)
        # print(SCN)
        # print(channelname)
        return frequency+mode+tuningstep+attenuation+SCN+channelname

#todo
# def VoiceSynt(self, value)
# def SetTuningStep <- custom step

class IcomR8500:
    header = "FEFE" # fixed header
    radioAddress = "4A"
    computerAddress = "E0"

    def __init__(self, serialport="/dev/ttyUSB0", baudrate=19200, timeout=1): # toimii

        self.serialPort = serialport
        self.baudrate = baudrate
        self.timeout = timeout
        
        try:
            self.ser = serial.Serial(self.serialPort,baudrate=self.baudrate,timeout=self.timeout)
        except:
            return "Init failed to open radio"

    def readFreqEdges(self): # return min and max frequencies for the radio, toimii
        Cn = "02"
        value = self.writeToRadio(Cn)
        self.freqlo = self.FreqToRad(value[:10]) # min freq
        self.freqhi = self.FreqToRad(value[12:]) # max freq
        return self.freqlo, self.freqhi
    
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
        
    def readMchContentsPackage(self,bank,channel): # toimii
        Cn = "1A"
        Sc = "01"
        bank = str(bank).zfill(2)
        channel = str(channel).zfill(4)
        data=bank+channel

        value = self.writeToRadio(Cn,Sc,data)
        bankRead = int(value[0:2])
        channelRead = int(value[2:6])
        data = value[6:]
        if data != "ff":
            freqRead = str(int(self.FreqToRad(data[:10])))
            modeRead = data[10:14]
            tuningStepRead = data[14:20]
            ATTRead = data[20:22]
            SCNRead = data[22:24]
            ChannelNameRead = bytes.fromhex(data[24:]).decode()[1:]
            print("Bank: " + str(bankRead) + " Channel: " + str(channelRead) + " Frequency: " + freqRead + " mode: " + modeRead + " tuning step: " + tuningStepRead + " ATT: " + ATTRead + " SCN: " + SCNRead + " Channel Name: " + ChannelNameRead)
            return ChannelData(freqRead, modeRead, tuningStepRead, ATTRead, SCNRead, ChannelNameRead)
        else:
            print("Channel empty")
            return "Bank: " + str(bankRead) + " Channel: " + str(channelRead) + " Empty"
        
    def readBankName(self,bank): # toimii
        Cn = "1A"
        Sc = "03"
        if bank == "free":
            bank = 20
        elif bank == "auto":
            bank = 21
        elif bank == "skip":
            bank = 22
        elif bank == "prog":
            bank = 23
        elif bank == "prio":
            bank = 24
        bank = str(bank).zfill(2)
        value = self.writeToRadio(Cn,Sc,bank)
        return bytes.fromhex(value).decode()[1:]

        # returns squelch on (01) / off (00) # toimii
    def readSquelchCondition(self): 
        Cn = "15"
        Sc = "01"
        value = self.writeToRadio(Cn,Sc)
        if value == "01":
            print("Squelch Off")
        else:
            print("Squelch On")
        return value
    
        # returns S-meter level # toimii
    def readSmeterLevel(self):
        Cn = "15"
        Sc = "02"
        return int(self.writeToRadio(Cn,Sc))
    
        # returns Radio address # toimii
    def readModelID(self):
        Cn = "19"
        Sc = "00"
        return self.writeToRadio(Cn,Sc)

    def setFreq(self, freq): # toimii
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

        # set Memory channel (from 00 to 99) # toimii
    def MemoryChannelSelection(self, channelnumber):
        Cn = "08"
        Sc = ""
        channelnumber = str(channelnumber).zfill(4)
        return self.writeToRadio(Cn, Sc, channelnumber)

        # set Bank selection (from 00 to 19) # toimii
    def BankSelection(self, banknumber):
        Cn = "08"
        Sc = "A0"
        banknumber = str(banknumber).zfill(2)
        return self.writeToRadio(Cn, Sc, banknumber)

        # select bank and channel, apply frequency etc and last MemoryWrite()
    def MemoryWrite(self): # toimii
        Cn = "09"
        Sc = ""
        return self.writeToRadio(Cn)

        # set channel parameters and write
    def SetMCHContentAndWritePackage(self, banknumber, channelnumber, ChannelData): # toimii
        Cn = "1A"
        Sc = "00"
        banknumber = str(banknumber).zfill(2)
        channelnumber = str(channelnumber).zfill(4)
        data = banknumber+channelnumber+ChannelData.raw()
        return self.writeToRadio(Cn, Sc, data)

        # set bank name 5 char long. ascii values
    def SetBankName(self, bank, name): # toimii
        Cn = "1A"
        Sc = "02"
        name = "{:>5}".format(name[:5])
        name = name.encode("ASCII").hex()
        bank = str(bank).zfill(2)
        data = bank+name
        return self.writeToRadio(Cn, Sc, data)

        # applies to currently selected channel, use BankSelection() and MemoryChannelSelection()
    def MemoryClear(self): # toimii
        Cn = "0B"
        Sc = ""
        return self.writeToRadio(Cn, Sc)

    def StopScan(self): # toimii
        Cn = "0E"
        Sc = "00"
        return self.writeToRadio(Cn,Sc)

        # scan specified frequency range
    def ProgrammedScanStart(self): # toimii
        Cn = "0E"
        Sc = "02"
        return self.writeToRadio(Cn,Sc)

        # scan specified frequency range. save active frequencies.
    def AutoMemoryWriteScanStart(self): # toimii
        Cn = "0E"
        Sc = "04"
        return self.writeToRadio(Cn,Sc)

        # scan whole bank, except skip # toimii
    def MemoryScanStart(self):
        Cn = "0E"
        Sc = "22"
        return self.writeToRadio(Cn,Sc)

        # scan only marked channels # toimii
    def SelectMemoryScanStart(self):
        Cn = "0E"
        Sc = "23"
        return self.writeToRadio(Cn,Sc)

    def ModeSelectScanStart(self): # toimii
        Cn = "0E"
        Sc = "24"
        return self.writeToRadio(Cn,Sc)

    def PriorityScan(self): # toimii
        Cn = "0E"
        Sc = "42"
        return self.writeToRadio(Cn,Sc)

    def SEL_CH_Release(self): # toimii
        Cn = "0E"
        Sc = "B0"
        return self.writeToRadio(Cn,Sc)

    def SEL_CH_Tag(self): # toimi
        Cn = "0E"
        Sc = "B1"
        return self.writeToRadio(Cn,Sc)

        # Voice scan control
    def VSC_Deactivation(self): # toimii
        Cn = "0E"
        Sc = "C0"
        return self.writeToRadio(Cn,Sc)

        # Voice scan control
    def VSC_Activation(self): # toimii
        Cn = "0E"
        Sc = "C1"
        return self.writeToRadio(Cn,Sc)

    def Scan_Resume_Selection_inf(self): # toimii
        Cn = "0E"
        Sc = "D0"
        return self.writeToRadio(Cn,Sc)

    def Scan_Resume_Selection_off(self): # toimii
        Cn = "0E"
        Sc = "D1"
        return self.writeToRadio(Cn,Sc)

    def Scan_Resume_Selection_DLY(self): # toimii
        Cn = "0E"
        Sc = "D3"
        return self.writeToRadio(Cn,Sc)

        # toimii, custom step TODO
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
            custom = ''.join([str(custom*10)[i] for i in [2,3,0,1]])
            #custom = "9519"
            return self.writeToRadio(Cn, Sc, custom)
        else:
            return "Mode not supported"
        return self.writeToRadio(Cn, Sc)
        
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

        # Automatic Gain Control # toimii
    def AGC_Off(self):
        Cn = "16"
        Sc = "10"
        return self.writeToRadio(Cn,Sc)

        # Automatic Gain Control # toimii
    def AGC_On(self):
        Cn = "16"
        Sc = "11"
        return self.writeToRadio(Cn,Sc)
        
        # Noice Blocker # toimii
    def NB_Off(self):
        Cn = "16"
        Sc = "20"
        return self.writeToRadio(Cn,Sc)
        
        # Noice Blocker # toimii
    def NB_On(self):
        Cn = "16"
        Sc = "21"
        return self.writeToRadio(Cn,Sc)

        # Audio peak filter # toimii
    def APF_Off(self):
        Cn = "16"
        Sc = "30"
        return self.writeToRadio(Cn, Sc)

        # Audio peak filter # toimii
    def APF_On(self):
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
        return ''.join([value[i] for i in [8,9,6,7,4,5,2,3,0,1]])
    

    def writeToRadio(self, Cn="", Sc="", data=""): # toimii
        dataToRadio = self.header + self.radioAddress + self.computerAddress + Cn + Sc + data + "FD"
        print("dataToRadio: " + dataToRadio)
        testcode = bytes.fromhex(dataToRadio)
        self.ser.write(testcode)
        
        testcode_echo = self.ser.read_until(b'\xfd').hex()
        headerlen = len(self.header + self.radioAddress + self.computerAddress + Cn + Sc)
        reply = self.ser.read_until(b'\xfd').hex()[headerlen:-2]
        
        print("reading reply: " + reply)
        if (reply.lower() == (self.header + self.radioAddress + self.computerAddress + "FB" + "FD").lower()):
            return "OK"
        elif (reply.lower() == (self.header + self.radioAddress + self.computerAddress + "FA" + "FD").lower()):
            return "NG"
        else:
            return reply