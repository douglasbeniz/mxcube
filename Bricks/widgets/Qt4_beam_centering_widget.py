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
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
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
        array = []
        array.append([])
        array.append([])

        self._arraySlit1 = []
        self._arraySlit1.append(array)
        self._arraySlit1.append(array)

        self._arraySlit2 = []
        self._arraySlit2.append(array)
        self._arraySlit2.append(array)

        self.figureHorSlit1 = Figure()
        self.axHorSlit1 = self.figureHorSlit1.add_subplot(111)
        self.canvasHorSlit1 = FigureCanvas(self.figureHorSlit1)

        self.figureVerSlit1 = Figure()
        self.axVerSlit1 = self.figureVerSlit1.add_subplot(111)
        self.canvasVerSlit1 = FigureCanvas(self.figureVerSlit1)

        self.figureHorSlit2 = Figure()
        self.axHorSlit2 = self.figureHorSlit2.add_subplot(111)
        self.canvasHorSlit2 = FigureCanvas(self.figureHorSlit2)

        self.figureVerSlit2 = Figure()
        self.axVerSlit2 = self.figureVerSlit2.add_subplot(111)
        self.canvasVerSlit2 = FigureCanvas(self.figureVerSlit2)


        # Properties ---------------------------------------------------------- 

        # Signals -------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Graphic elements ----------------------------------------------------
        self.beam_center_widget_layout = uic.loadUi(os.path.join(\
             os.path.dirname(__file__),
             "ui_files/Qt4_beam_centering_widget_layout.ui"))

        self.toolbarHorSlit1 = NavigationToolbar(self.canvasHorSlit1,
                self.beam_center_widget_layout.mplHorSlit1Window, coordinates=True)
        self.toolbarVerSlit1 = NavigationToolbar(self.canvasVerSlit1,
                self.beam_center_widget_layout.mplVerSlit1Window, coordinates=True)
        self.toolbarHorSlit2 = NavigationToolbar(self.canvasHorSlit2,
                self.beam_center_widget_layout.mplHorSlit2Window, coordinates=True)
        self.toolbarVerSlit2 = NavigationToolbar(self.canvasVerSlit2,
                self.beam_center_widget_layout.mplVerSlit2Window, coordinates=True)

        self.beam_center_widget_layout.mplHorVlSlit1.addWidget(self.canvasHorSlit1)
        self.beam_center_widget_layout.mplHorVlSlit1.addWidget(self.toolbarHorSlit1)
        self.beam_center_widget_layout.mplVerVlSlit1.addWidget(self.canvasVerSlit1)
        self.beam_center_widget_layout.mplVerVlSlit1.addWidget(self.toolbarVerSlit1)

        self.beam_center_widget_layout.mplHorVlSlit2.addWidget(self.canvasHorSlit2)
        self.beam_center_widget_layout.mplHorVlSlit2.addWidget(self.toolbarHorSlit2)
        self.beam_center_widget_layout.mplVerVlSlit2.addWidget(self.canvasVerSlit2)
        self.beam_center_widget_layout.mplVerVlSlit2.addWidget(self.toolbarVerSlit2)

        #Set enable/disable buttons
        self.beam_center_widget_layout.startCenterButton.setEnabled(True)
        self.beam_center_widget_layout.cancelCenterButton.setEnabled(False)

        # Layout --------------------------------------------------------------
        __main_vlayout = QtGui.QVBoxLayout(self)
        __main_vlayout.addWidget(self.beam_center_widget_layout)
        __main_vlayout.setSpacing(0)
        __main_vlayout.setContentsMargins(0, 0, 0, 0)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.beam_center_widget_layout.distanceHorSlit1Edit.textChanged.connect(\
             self.distanceHorSlit1Edit_change)
        self.beam_center_widget_layout.distanceVerSlit1Edit.textChanged.connect(\
             self.distanceVerSlit1Edit_change)
        self.beam_center_widget_layout.stepSlit1Edit.textChanged.connect(\
             self.stepSlit1Edit_change)
        self.beam_center_widget_layout.fullPathSlit1Check.stateChanged.connect(\
             self.fullPathSlit1Check_change)
        self.beam_center_widget_layout.centerSlit1Check.stateChanged.connect(\
             self.centerSlit1Check_change)
        self.beam_center_widget_layout.distanceHorSlit2Edit.textChanged.connect(\
             self.distanceHorSlit2Edit_change)
        self.beam_center_widget_layout.distanceVerSlit2Edit.textChanged.connect(\
             self.distanceVerSlit2Edit_change)
        self.beam_center_widget_layout.stepSlit2Edit.textChanged.connect(\
             self.stepSlit2Edit_change)
        self.beam_center_widget_layout.fullPathSlit2Check.stateChanged.connect(\
             self.fullPathSlit2Check_change)
        self.beam_center_widget_layout.centerSlit2Check.stateChanged.connect(\
             self.centerSlit2Check_change)
        self.beam_center_widget_layout.startCenterButton.clicked.connect(\
             self.startCenter)
        self.beam_center_widget_layout.cancelCenterButton.clicked.connect(\
             self.cancelCenter)

        # Other --------------------------------------------------------------- 

    def distanceHorSlit1Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceHorizontal(new_value, 1)

    def distanceVerSlit1Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceVertical(new_value, 1)

    def stepSlit1Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setStep(new_value, 1)

    def fullPathSlit1Check_change(self, state):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setFullPathSlit((state == 2), 1)
            if (state == 0):
                self.beam_center_widget_layout.distanceHorSlit1Edit.setEnabled(True)
                self.beam_center_widget_layout.distanceVerSlit1Edit.setEnabled(True)
            else:
                self.beam_center_widget_layout.distanceHorSlit1Edit.setEnabled(False)
                self.beam_center_widget_layout.distanceVerSlit1Edit.setEnabled(False)

    def centerSlit1Check_change(self, state):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setCenterSlit((state == 2), 1)

    def distanceHorSlit2Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceHorizontal(new_value, 2)

    def distanceVerSlit2Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setDistanceVertical(new_value, 2)

    def stepSlit2Edit_change(self, new_value):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setStep(new_value, 2)

    def fullPathSlit2Check_change(self, state):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setFullPathSlit((state == 2), 2)
            if (state == 0):
                self.beam_center_widget_layout.distanceHorSlit2Edit.setEnabled(True)
                self.beam_center_widget_layout.distanceVerSlit2Edit.setEnabled(True)
            else:
                self.beam_center_widget_layout.distanceHorSlit2Edit.setEnabled(False)
                self.beam_center_widget_layout.distanceVerSlit2Edit.setEnabled(False)

    def centerSlit2Check_change(self, state):
        """
        Descript. :
        """
        if (self._beam_center_hwobj != None):
            self._beam_center_hwobj.setCenterSlit((state == 2), 2)

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
            # Configure buttons
            self.beam_center_widget_layout.startCenterButton.setEnabled(False)
            self.beam_center_widget_layout.cancelCenterButton.setEnabled(True)


    def cancelCenter(self):
        confDialog = QtGui.QMessageBox.warning(None, "Cancel centering beam", "Do you want to STOP the procedure to center beam?",
                  QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        if ((confDialog == QtGui.QMessageBox.Ok) and (self._beam_center_hwobj != None)):
            self._beam_center_hwobj.cancel()
            self.beam_center_widget_layout.startCenterButton.setEnabled(True)
            self.beam_center_widget_layout.cancelCenterButton.setEnabled(False)

    def positionHorSlit1Changed(self, new_hor_position):
        self.beam_center_widget_layout.positionHorSlit1Text.setText(str(round(new_hor_position, 3)))

    def positionVerSlit1Changed(self, new_ver_position):
        self.beam_center_widget_layout.positionVerSlit1Text.setText(str(round(new_ver_position, 3)))

    def intensitySlit1Changed(self, new_intensity):
        self.beam_center_widget_layout.intensitySlit1Text.setText(str(new_intensity))

    def positionHorSlit2Changed(self, new_hor_position):
        self.beam_center_widget_layout.positionHorSlit2Text.setText(str(round(new_hor_position, 3)))

    def positionVerSlit2Changed(self, new_ver_position):
        self.beam_center_widget_layout.positionVerSlit2Text.setText(str(round(new_ver_position, 3)))

    def intensitySlit2Changed(self, new_intensity):
        self.beam_center_widget_layout.intensitySlit2Text.setText(str(new_intensity))

    def centeringConcluded(self):
        showDialog = QtGui.QMessageBox.information(None, "Centered!", "Procedure to center beam concluded!",
                  QtGui.QMessageBox.Ok)
        self.beam_center_widget_layout.startCenterButton.setEnabled(True)
        self.beam_center_widget_layout.cancelCenterButton.setEnabled(False)


    def plotClearSlit1(self, orientation):
        # orientation:
        # 0: horizontal
        # 1: vertical
        for axis in range(2):
            self._arraySlit1[orientation][axis] = []

        if (orientation == 0):
            self.axHorSlit1.clear()
        else:
            self.axVerSlit1.clear()

    def plotClearSlit2(self, orientation):
        # orientation:
        # 0: horizontal
        # 1: vertical
        for axis in range(2):
            self._arraySlit2[orientation][axis] = []

        if (orientation == 0):
            self.axHorSlit2.clear()
        else:
            self.axVerSlit2.clear()

    def plotNewPointSlit1(self, x, y, orientation):
        # orientation:
        # 0: horizontal
        # 1: vertical
        self._arraySlit1[orientation][0].append(x)
        self._arraySlit1[orientation][1].append(y)

        if (orientation == 0):
            self.axHorSlit1.plot(self._arraySlit1[orientation][0], self._arraySlit1[orientation][1], color='b')
            self.canvasHorSlit1.draw()
        else:
            self.axVerSlit1.plot(self._arraySlit1[orientation][0], self._arraySlit1[orientation][1], color='g')
            self.canvasVerSlit1.draw()

    def plotNewPointSlit2(self, x, y, orientation):
        # orientation:
        # 0: horizontal
        # 1: vertical
        self._arraySlit2[orientation][0].append(x)
        self._arraySlit2[orientation][1].append(y)

        if (orientation == 0):
            self.axHorSlit2.plot(self._arraySlit2[orientation][0], self._arraySlit2[orientation][1], color='b')
            self.canvasHorSlit2.draw()
        else:
            self.axVerSlit2.plot(self._arraySlit2[orientation][0], self._arraySlit2[orientation][1], color='g')
            self.canvasVerSlit2.draw()

    def setTab(self, index):
        if (self.beam_center_widget_layout != None):
            self.beam_center_widget_layout.graphicsTabs.setCurrentIndex(index)

    def errorCentering(self):
        QtGui.QMessageBox.critical(None, "Error centering beam", "An error occurred when trying to certer. Do you informed valid parameters?",
                  QtGui.QMessageBox.Ok)

        self.beam_center_widget_layout.startCenterButton.setEnabled(True)
        self.beam_center_widget_layout.cancelCenterButton.setEnabled(False)
