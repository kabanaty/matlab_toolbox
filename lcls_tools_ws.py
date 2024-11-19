import time
import os
import sys
from pydm import Display
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from qtpy.QtWidgets import (QAbstractItemView, QVBoxLayout, QComboBox, 
                            QFrame, QRadioButton, QHBoxLayout)
import atexit
import numpy as np
from tmit_loss import TMITLoss
from lcls_tools.common.devices.reader import create_wire
import meme.names as mn
import wirescan_gui_navigation as ws_nav

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(1, 1, 1)
        super(MplCanvas, self).__init__(fig) 

class Selection:
    def __set_name__(self, owner, name):
        self._name = name
        
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
        
    def __set__(self, instance, value):
        instance.__dict__[self._name] = value

class UserSelection:
    beampath = Selection()
    linac = Selection()
    area = Selection()
    wire = Selection()
    pmt = Selection()
    bpms = Selection()
    plane = Selection()
    fit = Selection()
    name = Selection()

    def __init__(self, beampath, linac, area, wire, control_name,
                       element_name, pmt, bpms, plane, fit):
        self.beampath = beampath
        self.linac = linac
        self.area = area
        self.wire = wire
        self.control_name = control_name
        self.element_name = element_name
        self.pmt = pmt
        self.bpms = bpms
        self.plane = plane
        self.fit = fit

class WireScan(Display):

    def __init__(self, parent=None, args=None, macros=None):
        super(WireScan, self).__init__(parent=parent, args=args, macros=None)

        init_wire = create_wire(area="DL1", name="WS01")
        
        self.us = UserSelection(beampath = "CU_HXR", 
                                linac = "CU", 
                                area = "DL1",
                                wire = init_wire,
                                control_name = init_wire.controls_information.control_name,
                                element_name = init_wire.name,
                                pmt = "PMT:IN20:511", 
                                bpms = [], 
                                plane = "X",
                                fit = "Gaussian")
                                
        self.my_data = ws_nav.my_data

        self.wire_callback(self.us.control_name)
        
        self.init_ui()
        # self.reserve_buffers()
        atexit.register(self.my_exit_callback)

    def ui_filename(self):
        # Point to our UI file
        return 'new_ws.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                                 self.ui_filename())

    def reserve_buffers(self):
        username = os.getlogin()
        # username = "kabanaty"
        host = os.uname()[1]
        user = username + "@" + host
    
        self.my_eDef = EventDefinition("WireScanGUI-test", user=user)
        self.my_bsa = BSABuffer("WireScanGUI-test", user=user)
        self.my_bsa.destination_mode = 2
        
        print(f"Reserved BSA {self.my_bsa.number}")
        
    def my_exit_callback(self):
        print('Releasing eDef')
        self.my_eDef.release()
        print('Releasing BSA')
        self.my_bsa.release()

    def init_ui(self):   
        self.ui.beampathCombo.addItems(ws_nav.beampaths)
        self.ui.beampathCombo.currentTextChanged.connect(self.beampath_callback)
        
        self.ui.areaCombo.addItems(ws_nav.beampath_areas[self.us.beampath])
        self.ui.areaCombo.currentTextChanged.connect(self.area_callback)
        
        self.ui.wireCombo.addItems(ws_nav.wires[self.us.area])
        self.ui.wireCombo.currentTextChanged.connect(self.wire_callback)
        self.ui.wireCombo.currentTextChanged.connect(self.set_parameters_pvs)
        
        self.ui.pmtCombo.addItems(self.us.wire.metadata.lblms)
        self.ui.pmtCombo.currentTextChanged.connect(self.pmt_callback)
        
        self.ui.bpmList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.bpmList.addItems(self.us.wire.metadata.bpms)
        self.ui.bpmList.itemSelectionChanged.connect(self.bpm_callback)
        
        self.ui.startButton.clicked.connect(self.start_scan_callback)
        self.ui.abortButton.clicked.connect(self.abort_scan_callback)
        
        self.plotLayout = QVBoxLayout()
        self.ui.plotFrame.setLayout(self.plotLayout)
        
        self.topPlot = MplCanvas(self, width=5, height=4, dpi=100)
        self.bottomPlot = MplCanvas(self, width=5, height=4, dpi=100)
        
        self.bottomPlotControls = QFrame()
        self.bottomPlotControlsLay = QHBoxLayout()
        self.bottomPlotControls.setLayout(self.bottomPlotControlsLay)
        
        self.xRadio = QRadioButton("X Plane")
        #self.xRadio.toggled.connect(self.plane_callback)
        self.yRadio = QRadioButton("Y Plane")
        #self.yRadio.toggled.connect(self.plane_callback)
        self.uRadio = QRadioButton("U Plane")
        #self.uRadio.toggled.connect(self.plane_callback)
        
        #for radio, plane in zip([self.xRadio, self.yRadio, self.uRadio], ["X", "Y", "U"]):
        #    if self.us.plane == plane:
        #        radio.setChecked(True)
        
        self.fitCombo = QComboBox()
        self.fitCombo.addItems(ws_nav.fit_choices)
        #self.fitCombo.currentTextChanged.connect(self.fit_callback) 
        
        self.bottomPlotControlsLay.addWidget(self.xRadio)
        self.bottomPlotControlsLay.addWidget(self.yRadio)
        self.bottomPlotControlsLay.addWidget(self.uRadio)
        self.bottomPlotControlsLay.addWidget(self.fitCombo)
        
        self.plotLayout.addWidget(self.topPlot)
        self.plotLayout.addWidget(self.bottomPlot)
        self.plotLayout.addWidget(self.bottomPlotControls)
        
        self.set_parameters_pvs()

    def beampath_callback(self, beampath):
        self.us.beampath = beampath
        self.update_area_combo()
        self.us.linac = self.us.beampath[0:2]

    def area_callback(self, area):
        if area != '':
            self.us.area = area
            self.update_gui_display()
            
    def wire_callback(self, wire):
        if wire != '':
            try:
                self.us.control_name = wire
                element_name = mn.list_elements(f'{self.us.control_name}%')[0]
                self.us.element_name = element_name
                self.us.wire = create_wire(area=self.us.area, name=element_name)
            except:
                print("Error setting wire")

    def pmt_callback(self, pmt):
        if pmt != '':
            self.us.pmt = pmt
            self.update_plots()
            
    def plane_callback(self, plane):
        if plane:
            if self.us.wire.use_x_wire:
                self.us.plane = "X"
            elif self.us.wire.use_y_wire:
                self.us.plane = "Y"
            elif self.us.wire.use_u_wire:
                self.us.plane = "U"
            self.update_plots()
            
    def bpm_callback(self):
        self.us.bpms = [item.text() for item in self.ui.bpmList.selectedItems()]
        self.plot_top_plot()
        
    def fit_callback(self, fit):
        self.us.fit = fit
        self.update_plots()
        
    def update_area_combo(self):
        self.ui.areaCombo.clear()
        self.ui.areaCombo.addItems(ws_nav.beampath_areas[self.us.beampath])
        
    def update_wire_combo(self):
        self.ui.wireCombo.clear()
        self.ui.wireCombo.addItems(ws_nav.wires[self.us.area])
        
    def update_pmt_combo(self):
        self.ui.pmtCombo.clear()
        self.ui.pmtCombo.addItems(self.us.wire.metadata.lblms)
        if self.us.linac == "SC":
            self.ui.pmtCombo.addItems("TMIT Loss")
        self.update_plots()
        
    def update_bpm_list(self):
        self.ui.bpmList.clear()
        self.ui.bpmList.addItems(self.us.wire.metadata.bpms)
        
    def update_gui_display(self):
        self.update_wire_combo()
        self.update_pmt_combo()
        self.update_bpm_list()
        self.update_plots()
        
    def update_plots(self):
        if self.my_data[self.us.control_name][self.us.control_name] == []:
            self.topPlot.axes.cla()
            self.bottomPlot.axes.cla()
            self.topPlot.draw()
            self.bottomPlot.draw()
        else:
            self.plot_top_plot()
            self.plot_bottom_plot()
        
    def set_parameters_pvs(self):
        planes = ["x", "y", "u"]
        checks = [self.ui.useXWire, self.ui.useYWire, self.ui.useUWire]
        inners = [self.ui.innerX, self.ui.innerY, self.ui.innerU]
        outers = [self.ui.outerX, self.ui.outerY, self.ui.outerU]

        pvs = self.us.wire.controls_information.PVs

        def set_channel_attributes(check, inner, outer, plane, pvs):
            check.channel = inner.channel = outer.channel = None
            use_name = f"use_{plane}_wire"
            inner_name = f"{plane}_wire_inner"
            outer_name = f"{plane}_wire_outer"

            check.channel = getattr(pvs, use_name).pvname
            inner.channel = getattr(pvs, inner_name).pvname
            outer.channel = getattr(pvs, outer_name).pvname

        for plane, check, inner, outer in zip(planes, checks, inners, outers):
            set_channel_attributes(check, inner, outer, plane, pvs)

        self.ui.scanPoints.channel = None
        self.ui.scanPoints.channel = pvs.scan_pulses.pvname

    def start_scan_callback(self):
        #data = self.us.wire.perform_measurement(beam_path = self.us.beampath)
        print("TEST")

    def abort_scan_callback(self):
        print("raboof")

    def plot_top_plot(self):
        self.topPlot.axes.cla()
        
        my_data = self.my_data[self.us.control_name]
        
        if my_data[self.us.control_name] != []:        
            #for bpm in self.configuration.bpms:
             #   self.topPlot.axes.plot(my_data[bpm], label = bpm)

            self.topPlot.axes.plot(my_data[self.us.pmt],
                label = self.us.pmt)
            self.topPlot.axes.plot(my_data[self.us.wire],
                label = self.us.wire)
                
            full_range = np.linspace(6000, 46000, 600, dtype = "int")
            inners = [self.ui.innerX, self.ui.innerY, self.ui.innerU]
            outers = [self.ui.outerX, self.ui.outerY, self.ui.outerU]
            
            for plane in ["X", "Y", "U"]:
                for inner, outer in zip(inners, outers):
                    inner_val = epics.caget(f"{self.configuration.wire}:{plane}WIREINNER")
                    outer_val = epics.caget(f"{self.configuration.wire}:{plane}WIREOUTER")
                    inner_index = next(x for x, val in enumerate(full_range) 
                        if val >= inner_val)
                    outer_index = next(x for x, val in enumerate(full_range) 
                        if val >= outer_val)
                    
                    # Actual code to use for real wire scans
                    # inner_index = next(x for x, 
                        # val in enumerate(my_data[self.configuration.wire]) 
                        # if val > inner_val)
                    # outer_index = next(x for x, 
                        # val in enumerate(my_data[self.configuration.wire]) 
                        # if val > outer_val)
                    
                if  plane == self.us.plane:
                    self.topPlot.axes.axvspan(inner_index, outer_index, 
                        alpha = 0.1, color = "blue")
                else:
                    self.topPlot.axes.axvspan(inner_index, outer_index, 
                        alpha = 0.1, color = "grey")
                
            self.topPlot.axes.legend()
            self.topPlot.draw() 

    def plot_bottom_plot(self):
        self.bottomPlot.axes.cla()

        my_data = self.my_data[self.us.control_name]

        inner_val = getattr(self.us.wire, f"{plane}_wire_inner")
        outer_val = getattr(self.us.wire, f"{plane}_wire_outer")
        
        full_range = np.linspace(6000, 46000, 600, dtype = "int")
        
        inner_index = next(x for x, val in enumerate(full_range) if val >= inner_val)
        outer_index = next(x for x, val in enumerate(full_range) if val >= outer_val)
        
        posn_by_plane = full_range[inner_index:outer_index]
        xdata = np.asarray(posn_by_plane)
        pmt_by_plane = my_data[self.configuration.pmt][inner_index:outer_index]
        ydata = np.asarray(pmt_by_plane)
        
        if self.us.fit == "Gaussian":
            fit_y = self.gaussian_fit(xdata, ydata)
        elif self.us.fit == "Asymmetric":
            fit_y = self.asymmetric_fit(xdata, ydata)    
            
        self.bottomPlot.axes.plot(xdata, ydata, 'bo', 
            label = self.us.pmt)
        self.bottomPlot.axes.plot(xdata, fit_y, 'm-', 
            label = f"{self.us.fit} Fit")
        
        self.bottomPlot.axes.legend()
        self.bottomPlot.draw()

    def gaussian_fit(self, xdata, ydata):       
        def Gauss(x, A, B):
            y = A*np.exp(-1*B*x**2)
            return y
            
        parameters, covariance = curve_fit(Gauss, xdata, ydata)
        
        fit_A = parameters[0]
        fit_B = parameters[1]
        
        fit_y = Gauss(xdata, fit_A, fit_B)
        return fit_y
        
    def asymmetric_fit(self, xdata, ydata):
        model = SkewedGaussianModel()
        params = model.make_params(amplitude=400, center=3, sigma=7, gamma=1)
        result = model.fit(ydata, params, x=xdata)
        
        return result.best_fit
