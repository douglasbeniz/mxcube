#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import html_template

from PyQt4 import QtGui
from PyQt4 import QtCore

from widgets.Qt4_beam_centering_widget import BeamCenteringWidget
from BlissFramework.Qt4_BaseComponents import BlissWidget


__category__ = 'Qt4_General'


class Qt4_BeamCenteringBrick(BlissWidget):
    """
    Descript. :
    """
    def __init__(self, *args):
        """
        Descript. :
        """
        BlissWidget.__init__(self, *args)

        # Hardware objects ----------------------------------------------------
        self.beamline_setup_hwobj = None
        self.session_hwobj = None
        self.beam_center_hwobj = None

        # Internal variables --------------------------------------------------

        # Properties ----------------------------------------------------------
        self.addProperty("session", "string", "/session")
        self.addProperty("beamline_setup", "string", "/lnls/lnls-beamline_setup")
        self.addProperty("mnemonic", "string", "/lnls/lnls-beam_center")

        # Signals ------------------------------------------------------------

        # Slots ---------------------------------------------------------------
       
        # Graphic elements ---------------------------------------------------- 
        self.beam_center_widget = BeamCenteringWidget(self, "beam_center_widget")
        self.stacked_widget = QtGui.QStackedWidget(self)
        self.stacked_widget.addWidget(self.beam_center_widget)
       
        # Layout -------------------------------------------------------------- 
        _main_vlayout = QtGui.QVBoxLayout(self)
        _main_vlayout.addWidget(self.stacked_widget)

        # SizePolicies -------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------

        # Other --------------------------------------------------------------- 

    def propertyChanged(self, property_name, old_value, new_value):
        """
        Descript. :
        """
        if property_name == 'session':
            self.session_hwobj = self.getHardwareObject(new_value)
        elif property_name == 'beamline_setup':
            self.beamline_setup_hwobj = self.getHardwareObject(new_value)
            self.beam_center_widget.set_beamline_setup(self.beamline_setup_hwobj)
        elif property_name == "mnemonic":
            self.beam_center_hwobj = self.getHardwareObject(new_value)
            self.beam_center_widget.set_beam_center(self.beam_center_hwobj)

            # Connect signals
            self.connectSignals()
        else:
            BlissWidget.propertyChanged(self, property_name, old_value, new_value)


    def connectSignals(self):
        if (self.beam_center_hwobj != None):
            # Connect signals
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionHorSlit1Changed'), self.positionHorSlit1Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionVerSlit1Changed'), self.positionVerSlit1Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('intensitySlit1Changed'), self.intensitySlit1Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionHorSlit2Changed'), self.positionHorSlit2Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionVerSlit2Changed'), self.positionVerSlit2Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('intensitySlit2Changed'), self.intensitySlit2Changed)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearHorSlit1'), self.plotClearHorSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearVerSlit1'), self.plotClearVerSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearHorSlit2'), self.plotClearHorSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearVerSlit2'), self.plotClearVerSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointHorSlit1'), self.plotNewPointHorSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointVerSlit1'), self.plotNewPointVerSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointHorSlit2'), self.plotNewPointHorSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointVerSlit2'), self.plotNewPointVerSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('centeringConcluded'), self.centeringConcluded)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('setTabHorSlit1'), self.setTabHorSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('setTabVerSlit1'), self.setTabVerSlit1)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('setTabHorSlit2'), self.setTabHorSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('setTabVerSlit2'), self.setTabVerSlit2)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('errorCentering'), self.errorCentering)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('errorStep'), self.errorStep)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('limitReached'), self.limitReached)

    def positionHorSlit1Changed(self, new_hor_position):
        self.beam_center_widget.positionHorSlit1Changed(new_hor_position)

    def positionVerSlit1Changed(self, new_ver_position):
        self.beam_center_widget.positionVerSlit1Changed(new_ver_position)

    def intensitySlit1Changed(self, new_intensity):
        self.beam_center_widget.intensitySlit1Changed(new_intensity)

    def positionHorSlit2Changed(self, new_hor_position):
        self.beam_center_widget.positionHorSlit2Changed(new_hor_position)

    def positionVerSlit2Changed(self, new_ver_position):
        self.beam_center_widget.positionVerSlit2Changed(new_ver_position)

    def intensitySlit2Changed(self, new_intensity):
        self.beam_center_widget.intensitySlit2Changed(new_intensity)

    def plotClearHorSlit1(self):
        self.beam_center_widget.plotClearSlit1(0)

    def plotClearVerSlit1(self):
        self.beam_center_widget.plotClearSlit1(1)

    def plotClearHorSlit2(self):
        self.beam_center_widget.plotClearSlit2(0)

    def plotClearVerSlit2(self):
        self.beam_center_widget.plotClearSlit2(1)

    def plotNewPointHorSlit1(self, x, y):
        self.beam_center_widget.plotNewPointSlit1(x, y, 0)

    def plotNewPointVerSlit1(self, x, y):
        self.beam_center_widget.plotNewPointSlit1(x, y, 1)

    def plotNewPointHorSlit2(self, x, y):
        self.beam_center_widget.plotNewPointSlit2(x, y, 0)

    def plotNewPointVerSlit2(self, x, y):
        self.beam_center_widget.plotNewPointSlit2(x, y, 1)

    def centeringConcluded(self):
        self.beam_center_widget.centeringConcluded()

    def setTabHorSlit1(self):
        self.beam_center_widget.setTab(0)

    def setTabVerSlit1(self):
        self.beam_center_widget.setTab(1)

    def setTabHorSlit2(self):
        self.beam_center_widget.setTab(2)

    def setTabVerSlit2(self):
        self.beam_center_widget.setTab(3)

    def errorCentering(self):
        self.beam_center_widget.errorCentering()

    def errorStep(self):
        self.beam_center_widget.errorStep()

    def limitReached(self):
        self.beam_center_widget.limitReached()