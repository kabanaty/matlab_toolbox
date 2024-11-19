import epics
import meme
import pandas as pd

class TMITLoss:
    def __init__(self, beampath, wire, rate, edef):
        self.beampath = beampath
        self.wire = wire
        self.rate = rate
        self.edef = edef
        
        replace_wire = self.wire.replace("WIRE", "")
        replace_colon = replace_wire.replace(":", "")
        self.region = replace_colon[0:-3]
        
        if self.region == "DOG" or "BPN" in self.region:
            self.region = "BYP"
            
        # BPM selections change based on region       
        if self.region == "HTR":
            self.bpms_before_wire = [2, 4, 5, 6, 7, 8]
            self.bpms_after_wire = list(range(9, 22))
        elif self.region == "COL1":
            self.bpms_before_wire = list(range(26, 32))
            self.bpms_after_wire = list(range(101, 109))    
        elif self.region == "LTUS":
            self.bpms_before_wire = list(range(101, 116))
            self.bpms_after_wire = list(range(136, 140))
        elif self.region == "EMIT2":
            self.bpms_before_wire = list(range(48, 52))
            self.bpms_after_wire = list(range(52, 54))
        elif self.region == "BYP":
            self.bpms_before_wire = list(range(73, 85))
            self.bpms_after_wire = list(range(97, 111))
        elif self.region == "DIAG0":
        		self.bpms_before_wire = list(range(3, 8))
        		self.bpms_after_wire = list(range(10, 12))
        		
        self.waveform = self.calculate_tmit_loss()

    def get_bpm_list(self):
        bpm_tmit_pvs = meme.names.list_pvs("BPMS:%:TMIT", tag = self.beampath,
            sort_by = "z")
        self.bpms = bpm_tmit_pvs
        
    def get_bsa_counts(self):
        counts = epics.caget("BSA:SYS0:1:" + str(self.edef) + ":CNT")
        self.counts = counts

    def get_bpm_data(self):
        tmit_hst_pvs = []
        for pv in self.bpms:
            tmit_hst_pv = pv + "HST" + str(self.edef)
            tmit_hst_pvs.append(tmit_hst_pv)
            
        unclean_tmit_data = epics.caget_many(tmit_hst_pvs)
        clean_tmit_data = list(filter(
            lambda item: item is not None, unclean_tmit_data))
        
        for i in range(len(clean_tmit_data)):
            clean_tmit_data[i] = clean_tmit_data[i][0:self.counts]

        tmit_dataframe = pd.DataFrame(data = clean_tmit_data)
        # self.tmit_data = tmit_dataframe
        clean_tmit_dataframe = tmit_dataframe.dropna(how = "any")
        self.tmit_data = clean_tmit_dataframe
        
    def get_posn_data(self):
        posn_pv = self.wire + ":POSNHST" + str(self.edef)
        posn_data_mm = epics.caget(posn_pv) / 1000
        self.posn_data = posn_data_mm
        
    def iron_bpms(self):
        tmit_median = self.tmit_data.median()
        ironed_tmit = self.tmit_data.divide(tmit_median)
        
        self.tmit_iron = ironed_tmit
        
    def shift_bpm_data(self):
        shifter = self.tmit_iron.iloc[self.bpms_before_wire]
        shifter_mean = shifter.mean()
        shifted_tmit = self.tmit_iron.divide(shifter_mean)
        self.tmit_ratio_shift = shifted_tmit
        
    def subtract_means(self):
        tmit_after = self.tmit_ratio_shift.iloc[self.bpms_after_wire]
        mean_after = tmit_after.mean()
        
        tmit_before = self.tmit_ratio_shift.iloc[self.bpms_before_wire]
        mean_before = tmit_before.mean()
        
        tmit_wires = (mean_before - mean_after) * 100

        return tmit_wires

    def calculate_tmit_loss(self):
        self.get_bpm_list()
        self.get_bsa_counts()
        self.get_bpm_data()
        self.get_posn_data()
        self.iron_bpms()
        self.shift_bpm_data()
        tmit_loss_waveform = self.subtract_means()
        
        return tmit_loss_waveform
