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


# povman
import sys
import os
import ctypes
#
BIN_PATH="H:/makehuman/apps/yafy/bin"
PLUGIN_PATH = BIN_PATH +"/plugins"

sys.path.append(BIN_PATH)

# Preload needed libraries
# povman = minimal Msvc version and Qt libs
# mega = Mingw version ( by Megasoft, from Gaphicall )
povman = True
mega = False
#--
if sys.platform == 'win32':
    if povman:
        dllArray = ['zlib1', 'yafaraycore', 'yafarayplugin', 'yafarayqt']
    else:
        # Loading order of the dlls is sensible please do not alter it
        dllArray = ['zlib1', 'libxml2-2', 'libgcc_s_sjlj-1', 'Half', 'Iex', 'IlmThread', 'IlmImf', \
    'libjpeg-8', 'libpng14', 'libtiff-3', 'libfreetype-6', 'libyafaraycore', 'libyafarayplugin']
elif sys.platform == 'darwin':
    dllArray = ['libyafaraycore.dylib', 'libyafarayplugin.dylib']
else:
    dllArray = ['libyafaraycore.so', 'libyafarayplugin.so']

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

format = 'gui'  

# The YafaRay export function can just export the object or it can also call POV-Ray to
# render a scene file. By default the scene file will be the generated sample scene file.

action = 'render'  # "export" or "render"

# 'gui' for use QT4 YafaRay interface, 'console' for YafaRay render console or 'xml' for export to .xml file
source = 'gui'

# Lighting mode: 'dl' for use directlighting or 'pm' for PhotonMap 
lighting = 'dl'

# define background fron YafaRay
world = 'texture'

# By default the "render" action renders the generated POV scene file, but you can
# specify a scene file to render instead.

renderscenefile = ''  # Use "" to render the default scene file.

# Configure the following variable to point to the POV-Ray executable on your system.
# A number of typical examples are provided.
# Don't use the backslash character in the path.

#
yafaray_path = 'H:/makehuman/apps/yafy/resources'




