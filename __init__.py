# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoPicker
                                 A QGIS plugin
 A geologic picking tool for conceptual model building
                             -------------------
        begin                : 2017-01-31
        copyright            : (C) 2017 by mmarchildon
        email                : mmarchildon@owrc.ca
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeoPicker class from file GeoPicker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geo_picker import GeoPicker
    return GeoPicker(iface)
