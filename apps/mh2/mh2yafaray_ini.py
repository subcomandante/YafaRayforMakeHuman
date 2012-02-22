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
#print '#                   #'

# The output path defines the standard output directory and the generated include file name.
# The default directory is pov_output, within the MakeHuman installation directory.
# The default include file name is makehuman.inc.
outputpath = 'yafa_output/makehuman.inc'

# The export routine can generate a simple mesh2 object that is quick to render, but
# quite inflexible, or it can generate an array based format along with various macros
# that can be used in a wide variety of ways, but which is slower to render.

format = ''  # "array" or "mesh2"

# The POV-Ray export function can just export the object or it can also call POV-Ray to
# render a scene file. By default the scene file will be the generated sample scene file.

action = 'export'  # "export" or "render"

# By default the "render" action renders the generated POV scene file, but you can
# specify a scene file to render instead.

renderscenefile = ''  # Use "" to render the default scene file.

# Configure the following variable to point to the POV-Ray executable on your system.
# A number of typical examples are provided.
# Don't use the backslash character in the path.

#povray_path = 'C:\\Users\\mflerackers\\AppData\\Local\\Programs\\POV-Ray\\3.7\\bin\\pvengine64.exe'  # MultiProcessor Version
yafaray_path = 'H:/yafy/Release/yafaray.bat' # is need?


