# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPicker
                                 A QGIS plugin
 A geologic picking tool for conceptual model building
                              -------------------
        begin                : 2017-01-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by mmarchildon
        email                : mmarchildon@owrc.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QGis, QgsProject, QgsMapLayer, QgsMessageLog
from qgis.gui import QgsMessageBar
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from geo_picker_dialog import GeoPickerDialog
import os.path
from fence import Fence
from fence_plotter import Fence_viewer


class GeoPicker:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoPicker_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Geo Picker')
        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar(u'GeoPicker')
        #self.toolbar.setObjectName(u'GeoPicker')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoPicker', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = GeoPickerDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        #if add_to_toolbar:
        #    self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GeoPicker/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GeoPicker'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Geo Picker'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        #del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        root = QgsProject.instance().layerTreeRoot()
        layers = self.iface.legendInterface().layers()
        groups = self.iface.legendInterface().groups()
        linelayer_list = []
        linelayer_xr = []
        rasterlayer_list = []
        rasterlayer_xr = []        
        group_list = []
        group_xr = []
        i = -1
        for layer in layers:
            i += 1
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() == QGis.Line:
                    linelayer_list.append(layer.name())
                    linelayer_xr.append(i)
            
            if layer.type() == QgsMapLayer.RasterLayer:
                    rasterlayer_list.append(layer.name())
                    rasterlayer_xr.append(i)                
                
        i = -1
        for groupname in groups:
            i += 1
            group = root.findGroup(groupname).children()
            ii = 0
            for layer in group:
                for r in rasterlayer_list:
                    if r == layer.name():
                        ii += 1
                        break
                if ii > 1:
                    group_list.append(groupname)
                    group_xr.append(i)
                    break
        
        self.dlg.comboBox.clear()
        self.dlg.comboBox_2.clear()
        self.dlg.comboBox.addItems(linelayer_list)
        self.dlg.comboBox_2.addItems(group_list)
        
        if len(linelayer_xr) == 0:
            self.iface.messageBar().pushMessage("GeoPicker Error", "No cross-section line layer found", level=QgsMessageBar.CRITICAL, duration=3)
            QgsMessageLog.logMessage("GeoPicker Error: No line layer found")
            return
            
        if len(group_xr) == 0:
            self.iface.messageBar().pushMessage("GeoPicker Error", "No grouped raster layers found", level=QgsMessageBar.CRITICAL, duration=3)
            QgsMessageLog.logMessage("GeoPicker Error: No grouped raster layers found")
            return
        
        # show the dialog
        self.dlg.show()
        
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            selectedLayer = layers[linelayer_xr[selectedLayerIndex]]
            
            # collect features
            sections = []
            for f in selectedLayer.getFeatures():
                geom = f.geometry()
                pln = geom.asPolyline()
                vert = []
                for v in pln:
                    xy = []
                    xy.append(float(v[0]))
                    xy.append(float(v[1]))
                    vert.append(xy)
                sections.append(vert)
            
            # collect rasters    
            selectedRasterNames = []
            # selectedRasterAbstract = []
            for groupname in group_list:
                if groupname == self.dlg.comboBox_2.currentText():
                    group = root.findGroup(groupname).children()
                    for i in range(0, len(rasterlayer_list)):
                        for layer in group:
                            if layer.name() == rasterlayer_list[i]:
                                selectedRasterNames.append(layers[rasterlayer_xr[i]].dataProvider().dataSourceUri())
                                # selectedRasterAbstract.append(layers[rasterlayer_xr[i]].abstract)
                                break
            
            fnc = Fence(sections,selectedRasterNames)
            self.fv = Fence_viewer(fence=fnc,title=groupname)
            self.fv.plot()
            