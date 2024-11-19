import meme.names
beampaths = ["CU_HXR", "CU_SXR", "SC_DIAG0", "SC_HXR", "SC_SXR", "SC_BSYD"]
areas = ["DL1", "LI21", "LI24", "L3", "LTUH", "LTUS", "HTR", "DIAG0", "HTR",
				 "DIAG0", "COL1", "EMIT2", "BYP", "SPD"]
beampath_areas = {"CU_HXR": ["DL1", "LI21", "LI24", "L3", "LTUH"],
         "CU_SXR": ["DL1", "LI21", "LI24", "L3", "LTUS"],
         "SC_DIAG0": ["HTR", "DIAG0"],
         "SC_HXR": ["HTR", "COL1", "EMIT2", "BYP", "LTUH"],
         "SC_SXR": ["HTR", "COL1", "EMIT2", "BYP", "LTUS"],
         "SC_BSYD": ["HTR", "COL1", "EMIT2", "BYP", "SPD"]}
         
dl1_wires = ["WIRE:IN20:531", "WIRE:IN20:561", "WIRE:IN20:611", "WIRE:IN20:741"]
dl1_pmt = ["PMT:IN20:511", "PMT:IN20:512", "PMT:IN20:621", "PMT:IN20:622",
            "PMT:IN20:761", "PMT:IN20:762", "PMT:LI21:350"]
dl1_bpm = ["BPMS:IN20:525", "BPMS:IN20:581", "BPMS:IN20:631",
            "BPMS:IN20:731", "BPMS:IN20:771"]
            
li21_wires = ["WIRE:LI21:285", "WIRE:LI21:293", "WIRE:LI21:301"]
li21_pmt = ["PMT:LI21:285", "PMT:LI21:293", "PMT:LI21:301", "PMT:LI21:350",
            "PMT:LI21:401", "PMT:LI21:402"]
li21_bpm = ["BPMS:LI21:278", "BPMS:LI21:301"]

li24_wires = ["WIRE:LI24:705"]
li24_pmt = ["PMT:LI24:705", "PMT:LI24:706", "BLM:LI24:707", "BLM:LI24:740"]
li24_bpm = ["BPMS:LI24:401", "BPMS:LI24:501", "BPMS:LI24:601",
            "BPMS:LI24:701"]

l3_wires = ["WIRE:LI27:644", "WIRE:LI28:144", "WIRE:LI28:444", 
             "WIRE:LI28:744"]
l3_pmt = ["PMT:LI28:750", "PMT:LI289:150", "PMT:LTUH:756", "PMT:LTUH:820"]
l3_bpm = ["BPMS:LI27:201", "BPMS:LI27:301", "BPMS:LI27:401", "BPMS:LI27:501",
            "BPMS:LI27:601", "BPMS:LI27:701", "BPMS:LI27:801", "BPMS:LI27:901",
            "BPMS:LI28:201", "BPMS:LI28:301", "BPMS:LI28:401", "BPMS:LI28:501",
            "BPMS:LI28:601", "BPMS:LI28:701", "BPMS:LI28:801", "BPMS:LI28:901"]

ltuh_wires = ["WIRE:LTUH:122", "WIRE:LTUH:246", "WIRE:LTUH:538", 
              "WIRE:LTUH:715", "WIRE:LTUH:735", "WIRE:LTUH:755",
              "WIRE:LTUH:775"]
ltuh_pmt = ["PMT:LTUH:122", "PMT:LTUH:246", "PMT:DMPH:430", "PMT:DMPH:431",
            "PMT:LTUH:550", "PMT:LTUH:755", "PMT:LTUH:756", "PMT:LTUH:820",
            "PMT:LTUH:850", "LBLM:LTUH:738:A"]
ltuh_bpm = ["BPMS:LTUH:680", "BPMS:LTUH:720", "BPMS:LTUH:730", "BPMS:LTUH:740",
            "BPMS:LTUH:750", "BPMS:LTUH:760", "BPMS:LTUH:770", "BPMS:LTUH:820",
            "BPMS:LTUH:180", "BPMS:LTUH:190", "BPMS:LTUH:250", "BPMS:LTUH:290",
            "BPMS:BSYH:735", "BPMS:BSYH:910", "BPMS:LTUH:110", "BPMS:LTUH:120",
            "BPMS:LTUH:550"]
            
ltus_wires = ["WIRE:LTUS:715", "WIRE:LTUS:735", "WIRE:LTUS:755", 
              "WIRE:LTUS:785"]
#ltus_pmt = #["PMT:LTUH:122", "PMT:LTUH:246", "PMT:DMPH:430",
           # "PMT:DMPH:431", "PMT:LTUH:550", "PMT:LTUH:755",
           # "PMT:LTUH:756", "PMT:LTUH:820", "PMT:LTUH:850",
ltus_pmt = ["LBLM:LTUS:738:A", "PMT:LTUS:999"]
ltus_bpm = ["BPMS:LTUS:680", "BPMS:LTUS:740", "BPMS:LTUS:750", "BPMS:LTUS:820"]

htr_wires = ["WIRE:HTR:340"]
htr_pmt = ["LBLM:HTR:167:A"]#, "LBLM:HTR:167:B"]
htr_bpm = ["BPMS:HTR:120", "BPMS:HTR:320", "BPMS:HTR:365", "BPMS:HTR:460",
           "BPMS:HTR:540", "BPMS:HTR:760", "BPMS:HTR:830", "BPMS:HTR:860",
           "BPMS:HTR:960"]#, "BPMS:HTR:980"]

diag0_wires = ["WIRE:DIAG0:424"]
diag0_pmt = ["SBLM:GUNB:622", "TMITLOSS"]
diag0_bpm = ["BPMS:COL0:135", "BPMS:DIAG0:160", "BPMS:DIAG0:190", 
             "BPMS:DIAG0:210", "BPMS:DIAG0:230", "BPMS:DIAG0:270",
             "BPMS:DIAG0:285", "BPMS:DIAG0:330", "BPMS:DIAG0:370",
             "BPMS:DIAG0:390", "BPMS:DIAG0:410", "BPMS:DIAG0:470",
             "BPMS:DIAG0:480", "BPMS:DIAG0:520"]
     
col1_wires = ["WIRE:COL1:360", "WIRE:COL1:520", "WIRE:COL1:680",
              "WIRE:COL1:840"]
col1_pmt = ["LBLM:L1B:H282:A", "LBLM:L2B:0400:A", "TMITLOSS"]
col1_bpm = ["BPMS:COL1:120", "BPMS:COL1:260", "BPMS:COL1:280", "BPMS:COL1:320",
            "BPMS:COL1:400", "BPMS:COL1:480", "BPMS:COL1:560", "BPMS:COL1:640",
            "BPMS:COL1:720", "BPMS:COL1:800", "BPMS:COL1:880", "BPMS:COL1:960"]

emit2_wires = ["WIRE:EMIT2:600"]
emit2_pmt = ["LBLM:L2B:0400:A", "LBLM:L3B:1600:A"]
emit2_bpm = ["BPMS:EMIT2:150", "BPMS:EMIT2:300", "BPMS:EMIT2:800", 
             "BPMS:EMIT2:900"]

byp_wires = ["WIRE:BPN12:850", "WIRE:BPN14:850", "WIRE:BPN16:850",
             "WIRE:DOG:655"]
byp_pmt = ["LBLM:BPN15:410:A", "LBLM:DOG:740:A", "LBLM:BPN13:410:A",
           "LBLM:SPS:443:A", "LBLM:BPN17:517:A"]
byp_bpm = ["BPMS:BPN13:400", "BPMS:BPN14:400", "BPMS:BPN15:400",
           "BPMS:BPN16:400", "BPMS:BPN17:400", "BPMS:BPN18:400",
           "BPMS:BPN19:400", "BPMS:BPN20:400", "BPMS:BPN21:400",
           "BPMS:BPN22:400", "BPMS:BPN23:400", "BPMS:BPN24:400",
           "BPMS:BPN25:400", "BPMS:BPN26:400", "BPMS:BPN27:400",
           "BPMS:BPN28:200", "BPMS:BPN28:400", "BPMS:DOG:120", "BPMS:DOG:135",
           "BPMS:DOG:150", "BPMS:DOG:165", "BPMS:DOG:180", "BPMS:DOG:200",
           "BPMS:DOG:215", "BPMS:DOG:230", "BPMS:DOG:250", "BPMS:DOG:280",
           "BPMS:DOG:335", "BPMS:DOG:355", "BPMS:DOG:405", "BPMS:DOG:575",
           "BPMS:DOG:740", "BPMS:DOG:910"]

spd_wires = ["WIRE:SPD:872"]
spd_pmt = ["LBLM:SPS:443:A"]
spd_bpm = ["BPMS:SPD:135", "BPMS:SPD:255", "BPMS:SPD:340", "BPMS:SPD:420",
           "BPMS:SPD:525", "BPMS:SPD:570", "BPMS:SPD:700", "BPMS:SPD:955"]

wires = {"DL1": dl1_wires,
         "LI21": li21_wires,
         "LI24": li24_wires,
         "L3": l3_wires,
         "LTUH": ltuh_wires,
         "LTUS": ltus_wires,
         "HTR": htr_wires,
         "DIAG0": diag0_wires,
         "COL1": col1_wires,
         "EMIT2": emit2_wires,
         "BYP": byp_wires,
         "SPD": spd_wires}
         
pmts = {"DL1": dl1_pmt,
        "LI21": li21_pmt,
        "LI24": li24_pmt,
        "L3": l3_pmt,
        "LTUH": ltuh_pmt,
        "LTUS": ltus_pmt,
        "HTR": htr_pmt,
        "DIAG0": diag0_pmt,
        "COL1": col1_pmt,
        "EMIT2": emit2_pmt,
        "BYP": byp_pmt,
        "SPD": spd_pmt}
        
bpms = {"DL1": dl1_bpm,
        "LI21": li21_bpm,
        "LI24": li24_bpm,
        "L3": l3_bpm,
        "LTUH": ltuh_bpm,
        "LTUS": ltus_bpm,
        "HTR": htr_bpm,
        "DIAG0": diag0_bpm,
        "COL1": col1_bpm,
        "EMIT2": emit2_bpm,
        "BYP": byp_bpm,
        "SPD": spd_bpm}

fit_choices = ["Gaussian", "Asymmetric", "Super", "RMS",
               "RMS Cut Peak", "RMS Cut Area", "RMS Floor"]

my_data = {}

for area in areas:
    area_wires = wires[area]
    area_pmts = pmts[area]
    area_bpms = bpms[area]
    for wire in wires[area]:
        my_data[wire] = {}
        for pmt in area_pmts:
            my_data[wire][pmt] = []
        for bpm in area_bpms:
            my_data[wire][bpm] = []
        my_data[wire][wire] = []
