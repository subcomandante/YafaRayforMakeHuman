#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
YafaRay Export parameters.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Chris Bartlett

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module allows YafaRay renderer parameters to be configured. 
These parameters can be changed while the MakeHuman application is running without having
to reload the application.

"""

print 'YafaRay Render Parameter File'

import sys
import os
import ctypes

# set path and load needed dlls.
#
# Only changed the HOME_PATH line.
# Lack define 'darwin' (OSX systems) path format ( same of unix?) 

if sys.platform == 'win32':
    HOME_PATH = "H:/makehuman"   # change for your own installation path
    # Loading order of the dlls is sensible please do not alter it
    dllArray = ['zlib1','iconv','zlib','libpng15','libxml2','QtCore4','QtGui4',\
                'yafaraycore','yafarayplugin','yafarayqt']

elif sys.platform == 'darwin':
    HOME_PATH= '/home/user/programs/makehuman'  # need revision
    dllArray = ['libyafaraycore.dylib', 'libyafarayplugin.dylib']

else:
    HOME_PATH="/home/pedro/programas/makehuman"  #change for your own installation path
    dllArray = ['libyafaraycore.so', 'libyafarayplugin.so', 'libyafarayqt.so']
# 
BIN_PATH = HOME_PATH +"/shared/yafy/bin"
PLUGIN_PATH = BIN_PATH +"/plugins"

sys.path.append(BIN_PATH)

for dll in dllArray:
    try:
        ctypes.cdll.LoadLibrary(os.path.join(BIN_PATH, dll))
    except Exception as e:
        print("ERROR: Failed to load library " + dll + ", " + repr(e))

print 'YafaRay Libs loaded sucesfull'

# The output path defines the standard output directory and the generated image files.
# The default directory is yafaray_output, within the MakeHuman installation directory.
# The default exported XML file name is yafaray.xml.

outputpath = 'yafaray_output/'

# Define the format of render; gui, console or export to xml file

#format = 'gui'  

# The YafaRay export function can just export the object or it can also call POV-Ray to
# render a scene file. By default the scene file will be the generated sample scene file.

action = 'render'  # "export" or "render"

# 'gui' for use QT4 YafaRay interface, 'console' for YafaRay render console or 'xml' for export to .xml file
source = 'gui'

# Lighting mode: 'dl' for use directlighting or 'pm' for PhotonMap 
lighting = 'dl'

# define background for YafaRay
world = 'texture'

# By default the "render" action renders the generated image.

renderscenefile = ''  # Use "" to render the default scene file.

# Configure folder to the YafaRay resource files.

yafaray_path = HOME_PATH +'/shared/yafy/resources'




