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
#
#  Please user PEP 0008 -- "Style Guide for Python Code" to format code
#  https://www.python.org/dev/peps/pep-0008/


import os

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from time import sleep

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import logging
#import mpldatacursor
import cbf
import gevent

import numpy as np


Map_Colors = {'Gray': 'gray_r', 'Heat': 'gist_heat', 'Rainbow': 'rainbow'}


class ImageTrackingGraphicWidget(QtGui.QWidget):
    def __init__(self, parent = None, name = "image_tracking_graphic_widget"):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName(name)

        # Hardware objects ----------------------------------------------------
        self.image_tracking_hwobj = None

        # Internal values -----------------------------------------------------
        self.image_path = None
        self.data_collection = None
        self.full_image_path = None
        self.imPlot = None
        self.cbfContent = None
        self.numpyArrayWithData = None
        self.navigate = None
        self.current_image_valid = False

        # Signals ------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Graphic elements ----------------------------------------------------
        self.image_tracking_widget_layout = uic.loadUi(os.path.join(\
                 os.path.dirname(__file__),
                 "ui_files/Qt4_image_tracking_graphic_widget_layout.ui"))

        # ---------------------
        # Include combo items
        self.image_tracking_widget_layout.cmap_combobox.addItems(['Gray', 'Heat', 'Rainbow'])
        self.image_tracking_widget_layout.cmap_combobox.setCurrentIndex(0)

        # Change spinBox to don't update every input...
        self.image_tracking_widget_layout.image_num_spinbox.setKeyboardTracking(False)
        self.image_tracking_widget_layout.vmin_spinbox.setKeyboardTracking(False)
        self.image_tracking_widget_layout.vmax_spinbox.setKeyboardTracking(False)

        # ---------------------
        self.canvas = CustomMplCanvas()

        # ---------------------
        self.toolbar = NavigationToolbar(self.canvas, self.image_tracking_widget_layout.mplImageWindow, coordinates=True)

        self.image_tracking_widget_layout.mplImageVl.addWidget(self.canvas)
        self.image_tracking_widget_layout.mplImageVl.addWidget(self.toolbar)

        # Layout --------------------------------------------------------------
        _main_vlayout = QtGui.QVBoxLayout(self)
        _main_vlayout.addWidget(self.image_tracking_widget_layout)
        _main_vlayout.setSpacing(2)
        _main_vlayout.addStretch(0)
        _main_vlayout.setContentsMargins(0, 0, 0, 0)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.image_tracking_widget_layout.view_current_button.clicked.\
             connect(self.view_current_image)
        self.image_tracking_widget_layout.view_previous_button.clicked.\
             connect(self.previous_button_clicked)
        self.image_tracking_widget_layout.view_next_button.clicked.\
             connect(self.next_button_clicked)
        self.image_tracking_widget_layout.first_button.clicked.\
             connect(self.first_clicked)
        self.image_tracking_widget_layout.last_button.clicked.\
             connect(self.last_clicked)
        self.image_tracking_widget_layout.image_num_spinbox.valueChanged.\
             connect(self.image_num_changed) 
        self.image_tracking_widget_layout.vmin_spinbox.valueChanged.\
             connect(self.view_current_image) 
        self.image_tracking_widget_layout.vmax_spinbox.valueChanged.\
             connect(self.view_current_image) 
        self.image_tracking_widget_layout.refresh_button.clicked.\
             connect(self.view_current_image)

        self.setEnabled(False)


    def updateImagePath(self, value=1):
        if (value >= 0):
            if (self.image_tracking_widget_layout.image_num_spinbox.value() != value):
                self.image_tracking_widget_layout.image_num_spinbox.setValue(value)
            # -------------------------------
            self.image_tracking_widget_layout.current_path_ledit.setText(str(self.image_path % value))
            self.image_tracking_widget_layout.current_path_ledit.setToolTip(str(self.image_path % value))
        else:
            if (self.image_tracking_widget_layout.image_num_spinbox.value() != 0):
                self.image_tracking_widget_layout.image_num_spinbox.setValue(0)
            # -------------------------------
            self.image_tracking_widget_layout.current_path_ledit.setText("")
            self.image_tracking_widget_layout.current_path_ledit.setToolTip("")


    def previous_button_clicked(self, navigating=False):
        if (not navigating and self.navigate):
            self.navigate.kill()

        # Possible to go backward
        valid = True

        value = self.image_tracking_widget_layout.\
             image_num_spinbox.value() - 1 

        if (value < self.image_tracking_widget_layout.image_num_spinbox.minimum()):
            value = self.image_tracking_widget_layout.image_num_spinbox.minimum()
            valid = False

        # ----------------------------------
        self.updateImagePath(value=value)

        # ----------------------------------
        valid = valid and self.current_image_valid

        return valid


    def next_button_clicked(self, navigating=False):
        if (not navigating and self.navigate):
            self.navigate.kill()

        # Possible to go forward
        valid = True

        value = self.image_tracking_widget_layout.\
             image_num_spinbox.value() + 1

        if (value > self.image_tracking_widget_layout.image_num_spinbox.maximum()):
            value = self.image_tracking_widget_layout.image_num_spinbox.maximum()
            valid = False

        # ----------------------------------
        self.updateImagePath(value=value)

        # ----------------------------------
        valid = valid and self.current_image_valid

        return valid


    def navigateThrowImages(self, first=True):
        continueNavigating = True

        if (first):
            while (continueNavigating):
                continueNavigating = self.previous_button_clicked(navigating=True)
                sleep(0.5)
        else:
            while (continueNavigating):
                continueNavigating = self.next_button_clicked(navigating=True)
                sleep(0.5)


    def first_clicked(self):
        if (self.navigate):
            self.navigate.kill()

        self.navigate = gevent.spawn(self.navigateThrowImages)


    def last_clicked(self):
        if (self.navigate):
            self.navigate.kill()

        self.navigate = gevent.spawn(self.navigateThrowImages, False)


    def loadBlanckImage(self):
        # Reset data path
        self.full_image_path = None
        # Array of zeros with size of image from Pilatus-2M
        self.numpyArrayWithData = np.zeros((1679, 1475), np.uint32)


    def loadCBFContent(self):
        # -----
        valid = (self.full_image_path is not None)
        # -----
        newPath = self.image_path % self.image_tracking_widget_layout.image_num_spinbox.value()
        
        if ((self.full_image_path != newPath) or (self.canvas.fullImagePath != newPath)):
            self.full_image_path = newPath
    
            try:
                self.cbfContent = cbf.read(self.full_image_path, metadata=False)
                self.numpyArrayWithData = self.cbfContent.data
                # -----
                valid = True
            except:
                # Inform user that an error occurred
                logging.getLogger('user_level_log').error('Error loading CBF image: \'%s\'!' % str(self.full_image_path))
                # Clean showed image
                self.loadBlanckImage()
                # return invalid
                valid = False

        return valid


    def updatePlot(self, vmin=None, vmax=None, cmap=None):
        if (vmin is None):
            vmin = self.image_tracking_widget_layout.vmin_spinbox.value()

        if (vmax is None):
            vmax = self.image_tracking_widget_layout.vmax_spinbox.value()

        if (cmap is None):
            cmap = Map_Colors[self.image_tracking_widget_layout.cmap_combobox.currentText()]

        # ---------------------------------
        self.imPlot = self.canvas.setAxisImage(fullImagePath=self.full_image_path, arrayImageData=self.numpyArrayWithData, cmap=cmap, vmin=vmin, vmax=vmax)

        #mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'), formatter='x, y: {i}, {j}\ni: {z:.02g}'.format)

        if (self.imPlot is not None):
            self.canvas.setTightLayout()
            self.canvas.draw()
        else:
            # Inform user that an error occurred
            logging.getLogger('user_level_log').error('Error plotting CBF: \'%s\'!' % str(self.full_image_path))


    def view_current_image(self):
        # ---------------------------------
        valid = self.loadCBFContent()
        # ---------------------------------
        self.updatePlot()
        # ---------------------------------
        self.current_image_valid = valid


    def image_num_changed(self, value):
        # Update number of image
        self.updateImagePath(value=value)

        # Update image
        self.view_current_image()


    def set_image_tracking_hwobj(self, image_tracking_hwobj):
        self.image_tracking_hwobj = image_tracking_hwobj


    def set_data_collection(self, data_collection):
        if (data_collection is not None):
            self.setEnabled(True)
        else:
            self.setEnabled(False)
        self.data_collection = data_collection
        self.refresh()


    def refresh(self):
        if (self.navigate):
            self.navigate.kill()

        if self.data_collection is not None:
            acq = self.data_collection.acquisitions[0]
            paths = acq.get_preview_image_paths()
            if acq.acquisition_parameters.shutterless and \
               len(paths) > 1:
                temp = [paths[0], paths[-1]]
                paths = temp

            self.image_path = acq.path_template.get_image_path()
            self.full_image_path = None
            
            self.image_tracking_widget_layout.image_num_spinbox.setRange(\
                acq.acquisition_parameters.first_image,
                acq.acquisition_parameters.first_image + \
                    acq.acquisition_parameters.num_images - 1)

            self.updateImagePath(value=acq.acquisition_parameters.first_image)

            self.view_current_image()
        else:
            # Clean the image view
            self.updateImagePath(value=-1)
            self.loadBlanckImage()
            self.updatePlot()


class CustomMplCanvas(FigureCanvas):
    def __init__(self):
            self.figure = Figure()
            self.ax = self.figure.add_subplot(111)
            self.dataArray = None
            self.imageShow = None
            self.fullImagePath = None

            FigureCanvas.__init__(self, self.figure)

    def setAxisImage(self, fullImagePath, arrayImageData, cmap='gray_r', vmin=0, vmax=1740):
        self.fullImagePath = fullImagePath
        self.dataArray = arrayImageData

        try:
            # To keep zoom and coordinates....
            if (self.imageShow is None):
                self.imageShow = self.ax.imshow(self.dataArray, cmap=cmap, vmin=vmin, vmax=vmax)
            else:
                self.imageShow.set_data(self.dataArray)
                self.imageShow.set_clim(vmin=vmin, vmax=vmax)
                self.imageShow.set_cmap(cmap=cmap)
        except:
            self.imageShow = None

        return self.imageShow

    def setTightLayout(self):
        self.figure.tight_layout()