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

import os

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas)
import matplotlib.pyplot as Plot

class BeamCenteringWidget(QtGui.QWidget):
    """
    Descript. :
    """
  
    def __init__(self, parent = None, name = None, fl = 0):
        """
        Descript. :
        """
        QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowFlags(fl))
        
        if name is not None:
            self.setObjectName(name)

        # Hardware objects ----------------------------------------------------
        self._beamline_setup_hwobj = None
        self._beam_center_hwobj = None

        # Internal variables --------------------------------------------------
        self._distanceHor = None
        self._distanceVer = None

        self._arrayHorX = []
        self._arrayHorY = []

        self._arrayVerX = []
        self._arrayVerY = []       

        self.figureHor = Figure()
        self.axHorfigureHor = self.figureHor.add_subplot(111)
        self.canvasHorizontal = FigureCanvas(self.figureHor)

        self.figureVer = Figure()
        self.axVerfigureVer = self.figureVer.add_subplot(111)
        self.canvasVertical = FigureCanvas(self.figureVer)

        # Properties ---------------------------------------------------------- 

        # Signals -------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Graphic elements ----------------------------------------------------
        self.beam_center_widget_layout = uic.loadUi(os.path.join(\
             os.path.dirname(__file__),
             "ui_files/Qt4_beam_centering_widget_layout.ui"))

        self.beam_center_widget_layout.mplHorVl.addWidget(self.canvasHorizontal)
        self.beam_center_widget_layout.mplVerVl.addWidget(self.canvasVertical)

        # Layout --------------------------------------------------------------
        __main_vlayout = QtGui.QVBoxLayout(self)
        __main_vlayout.addWidget(self.beam_center_widget_layout)
        __main_vlayout.setSpacing(0)
        __main_vlayout.setContentsMargins(0, 0, 0, 0)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.beam_center_widget_layout.distanceHorEdit.textChanged.connect(\
             self.distanceHorEdit_change)
        self.beam_center_widget_layout.distanceVerEdit.textChanged.connect(\
             self.distanceVerEdit_change)
        self.beam_center_widget_layout.startCenterButton.clicked.connect(\
             self.startCenter)
        self.beam_center_widget_layout.cancelCenterButton.clicked.connect(\
             self.cancelCenter)

        # Other --------------------------------------------------------------- 
        self.distanceHorEdit_validator = QtGui.QDoubleValidator(0, 30, 4, self)
        self.distanceVerEdit_validator = QtGui.QDoubleValidator(0, 20, 4, self)

    def distanceHorEdit_change(self, new_value):
        """
        Descript. :
        """
        #print('Value changed: %s' % (new_value))
        self._distanceHor = new_value

        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceHorizontal(new_value)

    def distanceVerEdit_change(self, new_value):
        """
        Descript. :
        """
        #print('Value changed: %s' % (new_value))
        self._distanceVer = new_value

        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceVertical(new_value)

    def set_beamline_setup(self, beamline_setup):
        """
        Descript. :
        """
        self._beamline_setup_hwobj = beamline_setup

    def set_beam_center(self, beam_center):
        """
        Descript. :
        """
        self._beam_center_hwobj = beam_center

    def startCenter(self):
        confDialog = QtGui.QMessageBox.warning(None, "Start centering beam", "Do you want to START the procedure to center beam?",
                  QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        if ((confDialog == QtGui.QMessageBox.Ok) and (self._beam_center_hwobj != None)):
            self._beam_center_hwobj.start()

    def cancelCenter(self):
        confDialog = QtGui.QMessageBox.warning(None, "Cancel centering beam", "Do you want to STOP the procedure to center beam?",
                  QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        if ((confDialog == QtGui.QMessageBox.Ok) and (self._beam_center_hwobj != None)):
            self._beam_center_hwobj.cancel()

    def positionHorChanged(self, new_hor_position):
        self.beam_center_widget_layout.positionHorText.setText(str(round(new_hor_position, 3)))

    def positionVerChanged(self, new_ver_position):
        self.beam_center_widget_layout.positionVerText.setText(str(round(new_ver_position, 3)))

    def intensityChanged(self, new_intensity):
        self.beam_center_widget_layout.intensityText.setText(str(new_intensity))

    def centeringConcluded(self):
        showDialog = QtGui.QMessageBox.warning(None, "Centered!", "Procedure to center beam concluded!",
                  QtGui.QMessageBox.Ok)

    def plotNewPointHorizontal(self, x, y):
        self._arrayHorX.append(x)
        self._arrayHorY.append(y)

        self.axHorfigureHor.plot(self._arrayHorX, self._arrayHorY, color='b')
        self.canvasHorizontal.draw()


    def plotClearHorizontal(self):
        print(self._arrayHorX)
        print(self._arrayHorY)
        self._arrayHorX = []
        self._arrayHorY = []

        self.axHorfigureHor.clear()

    def plotNewPointVertical(self, x, y):
        self._arrayVerX.append(x)
        self._arrayVerY.append(y)

        self.axVerfigureVer.plot(self._arrayVerX, self._arrayVerY, color='g')
        self.canvasVertical.draw()


    def plotClearVertical(self):
        print(self._arrayVerX)
        print(self._arrayVerY)
        self._arrayVerX = []
        self._arrayVerY = []


        self.axVerfigureVer.clear()