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
        self.addProperty("beamline_setup", "string", "/Qt4_beamline-setup")
        self.addProperty("mnemonic", "string", "/lnls/lnls-beam-center")

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
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionHorChanged'), self.positionHorChanged)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('positionVerChanged'), self.positionVerChanged)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('intensityChanged'), self.intensityChanged)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('centeringConcluded'), self.centeringConcluded)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointHorizontal'), self.plotNewPointHorizontal)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearHorizontal'), self.plotClearHorizontal)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotNewPointVertical'), self.plotNewPointVertical)
            self.connect(self.beam_center_hwobj, QtCore.SIGNAL('plotClearVertical'), self.plotClearVertical)

    def positionHorChanged(self, new_hor_position):
        self.beam_center_widget.positionHorChanged(new_hor_position)

    def positionVerChanged(self, new_ver_position):
        self.beam_center_widget.positionVerChanged(new_ver_position)

    def intensityChanged(self, new_intensity):
        self.beam_center_widget.intensityChanged(new_intensity)

    def centeringConcluded(self):
        self.beam_center_widget.centeringConcluded()

    def plotNewPointHorizontal(self, x, y):
        self.beam_center_widget.plotNewPointHorizontal(x, y)

    def plotClearHorizontal(self):
        self.beam_center_widget.plotClearHorizontal()

    def plotNewPointVertical(self, x, y):
        self.beam_center_widget.plotNewPointVertical(x, y)

    def plotClearVertical(self):
        self.beam_center_widget.plotClearVertical()