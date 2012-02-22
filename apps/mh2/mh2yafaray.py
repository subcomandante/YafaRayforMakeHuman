#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
YafaRay Export functions.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Chris Bartlett

**Copyright(c):**      MakeHuman Team 2001-2011

**Licensing:**         GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
--------

This module implements functions to export a human model in POV-Ray format. POV-Ray is a 
Raytracing application (a renderer) that is free to download and use. The generated text 
file contains POV-Ray Scene Description Language (SDL), which consists of human-readable 
instructions for building 3D scenes. 

This module supports the export of a simple mesh2 object or the export of arrays of data
with accompanying macros to assemble POV-Ray objects. Both formats include some handy 
variable and texture definitions that are written into a POV-Ray include file. A POV-Ray 
scene file is also written to the output directory containing a range of examples 
illustrating the use of the include file.

The content of the generated files follows naming conventions intended to make it simple
to adjust to be compliant with the standards for the POV-Ray Object Collection. All 
identifiers start with 'MakeHuman\_'. You can easily perform a global change on this
prefix so that you end up with your own unique prefix.

"""

import os
import string
import shutil
import subprocess
import mh2yafaray_ini
import random
import mh
#
from math import pi, sin, cos
import yafrayinterface
#yi = yafrayinterface.yafrayInterface_t()


def yafarayRenderer(obj, app, settings):
    """
  This function exports data in a format that can be used to reconstruct the humanoid 
  object in POV-Ray. It supports a range of options that can be specified in the Python 
  script file mh2povray_ini.py, which is reloaded each time this function is run. This 
  enables these options to be changed while the MakeHuman application is still running.
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.

  camera:
      *Camera object*. The camera to render from 
  
  """

    print 'YafaRay Export of object: ', obj.name

    # Read settings from an ini file. This reload enables the settings to be
    # changed dynamically without forcing the user to restart the MH
    # application for the changes to take effect.
  
    camera = app.modelCamera
    resolution = (app.settings.get('rendering_width', 800), app.settings.get('rendering_height', 600))

    reload(mh2yafaray_ini)
    
    path = os.path.join(mh.getPath('render'), mh2yafaray_ini.outputpath)
    
    format = mh2yafaray_ini.format if settings['source'] == 'ini' else settings['format']
    action = mh2yafaray_ini.action if settings['source'] == 'ini' else settings['action']
    #
    #yi = yafrayinterface.yafrayInterface_t()

    # The ini format option defines whether a simple mesh2 object is to be generated
    # or the more flexible but slower array and macro combo is to be generated.
    #
    ID = 0

    if format == 'array':
        print 'Format array (xml) tryed'
        #povrayExportArray(obj, camera, resolution, path)
    if format == 'mesh2':
        print 'Format mesh2 (gui) tryed'
        #povrayExportMesh2(obj, camera, resolution, path)
        #ID = yafarayGeometry(yi, obj)

    outputDirectory = os.path.dirname(path)

    # Export the hair model as a set of spline definitions.
    # Load the test hair dataand write it out in POV-Ray format.
  
    #still unsupported
    #povrayLoadHairsFile('data/hairs/test.hair')
    #povrayWriteHairs(outputDirectory, obj)

    # The ini action option defines whether or not to attempt to render the file once
    # it's been written.

    if action == 'render':
        
        if not os.path.isfile(mh2yafaray_ini.yafaray_path):
            app.prompt('YafaRay not found', 'You don\'t seem to have YafaRay installed or the path in mh2yafaray_ini.py is incorrect.', 'Download', 'Cancel', downloadPovRay)
            return
        
        if mh2yafaray_ini.renderscenefile == '':
            outputSceneFile = path.replace('.inc', '.pov')
            baseName = os.path.basename(outputSceneFile)
        else:
            baseName = mh2yafaray_ini.renderscenefile
        cmdLineOpt = ' +I%s' % baseName
        if os.name == 'nt':
            cmdLineOpt = ' /RENDER %s' % baseName
        cmdLineOpt += ' +W%d +H%d' % resolution
        #
        if format == 'mesh2':
            yi = yafrayinterface.yafrayInterface_t()
            #plugins = mh2yafaray_ini.PLUGIN_PATH
            yi.loadPlugins(mh2yafaray_ini.PLUGIN_PATH)
        else:
            yi = yafrayinterface.xmlInterface_t()
        #
        #yafarayCameraData(yi, camera, resolution)

        # pathHandle = subprocess.Popen(cwd = outputDirectory, args = mh2povray_ini.povray_path + " /RENDER " + baseName)
        
        #print mh2yafaray_ini.yafaray_path + cmdLineOpt

        #pathHandle = subprocess.Popen(cwd=outputDirectory, args=mh2yafaray_ini.yafaray_path + cmdLineOpt)
        ##--------------------
        ## load interface and plugins
        #yi = yafrayinterface.yafrayInterface_t()
        #yi.loadPlugins(PLUGIN_PATH)

        ##------------
        yi.startScene()
        
        ##--- texture --------------------
        yi.paramsClearAll()
        texName ="rgb_cube1"
        yi.paramsSetString("type", "rgb_cube")
        yi.createTexture(texName)
        
        ##--- material -----------------------------
        yi.paramsClearAll()
        yi.paramsSetColor("color", 0.9, 0.15, 0.19 )
        yi.paramsSetString("type", "shinydiffusemat")
        
        yi.paramsPushList()
        yi.paramsSetString("element", "shader_node") 
        yi.paramsSetString("type", "texture_mapper")
        yi.paramsSetString("name", "rgbcube_mapper")
        yi.paramsSetString("texco", "global")
        yi.paramsSetString("texture", texName )
        yi.paramsSetString("mapping", "sphere" )
        yi.paramsEndList();
        
        yi.paramsSetString("diffuse_shader", "rgbcube_mapper")

        mat = yi.createMaterial("myMat")
        
        ##----- lights ------------------------------
        yi.paramsClearAll()
        yi.paramsSetString("type", "directional")
        yi.paramsSetPoint("direction", -0.3, -0.3, 0.8 )
        yi.paramsSetColor("color", 1.0, 1.0, 0.9 )
        yi.paramsSetFloat("power", 1.0 )
        yi.createLight("myDirectional")

        #
        yi.paramsClearAll()
        yi.paramsSetColor("color", 1, 1, 1, 1)
        yi.paramsSetPoint("from", 11, 3, 8)
        yi.paramsSetFloat("power", 160)
        yi.paramsSetString("type", "pointlight")
        yi.createLight("LAMP1")
        
        def makeSphere( nu, nv, x, y, z, rad, mat):
            # get next free id from interface

            ID = yi.getNextFreeID()

            yi.startGeometry()

            if not yi.startTriMesh(ID, 2 + (nu - 1) * nv, 2 * (nu - 1) * nv, False, False):
                yi.printError("Couldn't start trimesh!")

            yi.addVertex(x, y, z + rad)
            yi.addVertex(x, y, z - rad)
            for v in range(0, nv):
                t = v / float(nv)
                sin_v = sin(2.0 * pi * t)
                cos_v = cos(2.0 * pi * t)
                for u in range(1, nu):
                    s = u / float(nu)
                    sin_u = sin(pi * s)
                    cos_u = cos(pi * s)
                    yi.addVertex(x + cos_v * sin_u * rad, y + sin_v * sin_u * rad, z + cos_u * rad)

            for v in range(0, nv):
                yi.addTriangle(0, 2 + v * (nu - 1), 2 + ((v + 1) % nv) * (nu - 1), mat)
                yi.addTriangle(1, ((v + 1) % nv) * (nu - 1) + nu, v * (nu - 1) + nu, mat)
                for u in range(0, nu - 2):
                    yi.addTriangle(2 + v * (nu - 1) + u, 2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, mat)
                    yi.addTriangle(2 + v * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u + 1, 2 + ((v + 1) % nv) * (nu - 1) + u, mat)

            yi.endTriMesh()
            yi.endGeometry()

            return ID
        #------------
        nu = 24
        nv = 48
        x=0
        y=0
        z=0
        rad= .5   
        #ID = makeSphere(nu, nv, x, y, z, rad, mat)
        ID = yafarayGeometry(yi, obj)

        
        ##--- create cam ---------------------------
        yafarayCameraData(yi, camera, resolution)
        
        '''
        yi.paramsClearAll()
        yi.paramsSetString("type", "perspective")
        yi.paramsSetPoint("from", -1.5, -2.0, 1.7 )
        yi.paramsSetPoint("to", 0, 0, 0.2 )
        yi.paramsSetPoint("up", -1.5, -2.0, 2.7 )
        yi.paramsSetInt("resx", 640)
        yi.paramsSetInt("resy", 480)
        yi.paramsSetFloat("focal", 1.04)
        yi.createCamera("camera")
        '''
        ##---- background --------------------------
        yi.paramsClearAll()
        yi.paramsSetString("type", "constant")
        yi.paramsSetColor("color", 0.4, 0.5, 0.9 )
        yi.createBackground("world_background")

        ##--- integrator ---------------------------
        yi.paramsClearAll()
        yi.paramsSetBool("do_AO", True)
        yi.paramsSetInt("AO_samples", 16 )
        yi.paramsSetFloat("AO_distance", 1 )
        yi.paramsSetColor("AO_color", 0.9, 0.9, 0.9)
        yi.paramsSetString("type", "directlighting")
        yi.createIntegrator("myDL")

        ##--- volume integrator --------------------
        yi.paramsClearAll()
        yi.paramsSetString("type", "none")
        yi.createIntegrator("volintegr")

        ##-- output ---------------------------------
        yi.paramsClearAll()
        file_type = 'png'
        yi.paramsSetString("type", file_type)
        yi.paramsSetBool("alpha_channel", False)
        yi.paramsSetBool("z_channel", False)
        yi.paramsSetInt("width", resolution[0])#640)
        yi.paramsSetInt("height", resolution[1])#480)
        ih = yi.createImageHandler("outFile")
        output = yafrayinterface.imageOutput_t(ih, 'H:/makehuman/apps/yafy/test.png', 0, 0)

        ##--render ---------------------------------------
        yi.paramsClearAll()
        yi.paramsSetString("camera_name", "camera")
        yi.paramsSetString("integrator_name", "myDL")
        yi.paramsSetString("volintegrator_name", "volintegr")
        yi.paramsSetFloat("gamma", 2.2)
    
        yi.paramsSetInt("AA_minsamples", 4)
        yi.paramsSetFloat("AA_pixelwidth", 1.5)
        yi.paramsSetString("tiles_order", "random")
        yi.paramsSetString("filter_type", "mitchell")
        yi.paramsSetInt("width", resolution[0])#640)
        yi.paramsSetInt("height", resolution[1])#480)
        yi.paramsSetString("background_name", "world_background")

        ##-- QT interface ------------------------------------
        use_gui=True
        mega = mh2yafaray_ini.mega
        if mega:
            use_gui = False
        #---------
        if use_gui:
            import yafqt
            yafqt.initGui()
            guiSettings = yafqt.Settings()
            guiSettings.autoSave = False
            guiSettings.closeAfterFinish = False
            guiSettings.mem = None
            guiSettings.fileName = 'test.png'
            guiSettings.autoSaveAlpha = False
            #-- create render window
            yafqt.createRenderWidget(yi, 640, 480, 0, 0, guiSettings)
        else:
            yi.render(output)
 
        yi.clearAll()
        #del yi
        
def povrayExportArray(obj, camera, resolution, path):
    """
  This function exports data in the form of arrays of data the can be used to 
  reconstruct a humanoid object using some very simple POV-Ray macros. These macros 
  can build this data into a variety of different POV-Ray objects, including a
  mesh2 object that represents the human figure much as it was displayed in MakeHuman. 

  These macros can also generate a union of spheres at the vertices and a union of 
  cylinders that follow the edges of the mesh. A parameter on the mesh2 macro can be 
  used to generate a slightly inflated or deflated mesh. 

  The generated output file always starts with a standard header, is followed by a set 
  of array definitions containing the object data and is ended by a standard set of 
  POV-Ray object definitions. 
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  camera:
      *Camera object*. The camera to render from. 
  
  path:
      *string*. The file system path to the output files that need to be generated. 
  """

  # Certain files and blocks of SDL are mostly static and can be copied directly
  # from reference files into the generated output directories or files.

    headerFile = 'data/povray/headercontent.inc'
    staticFile = 'data/povray/staticcontent.inc'
    sceneFile = 'data/povray/makehuman.pov'
    groupingsFile = 'data/povray/makehuman_groupings.inc'
    pigmentMap = 'data/textures/texture.tif'

  # Define some additional file related strings

    outputSceneFile = path.replace('.inc', '.pov')
    baseName = os.path.basename(path)
    nameOnly = string.replace(baseName, '.inc', '')
    underScores = ''.ljust(len(baseName), '-')
    outputDirectory = os.path.dirname(path)

  # Make sure the directory exists

    if not os.path.isdir(outputDirectory):
        try:
            os.makedirs(outputDirectory)
        except:
            print 'Error creating export directory.'
            return 0

  # Open the output file in Write mode

    try:
        outputFileDescriptor = open(path, 'w')
    except:
        print 'Error opening file to write data.'
        return 0

  # Write the file name into the top of the comment block that starts the file.

    outputFileDescriptor.write('// %s\n' % baseName)
    outputFileDescriptor.write('// %s\n' % underScores)

  # Copy the header file SDL straight across to the output file

    try:
        headerFileDescriptor = open(headerFile, 'r')
    except:
        print 'Error opening file to read standard headers.'
        return 0
    headerLines = headerFileDescriptor.read()
    outputFileDescriptor.write(headerLines)
    outputFileDescriptor.write('''

''')
    headerFileDescriptor.close()

  # Declare POV_Ray variables containing the current makehuman camera.

    povrayCameraData(camera, resolution, outputFileDescriptor)
    
    outputFileDescriptor.write('#declare MakeHuman_TranslateX      = %s;\n' % -obj.x)
    outputFileDescriptor.write('#declare MakeHuman_TranslateY      = %s;\n' % obj.y)
    outputFileDescriptor.write('#declare MakeHuman_TranslateZ      = %s;\n\n' % obj.z)
    
    outputFileDescriptor.write('#declare MakeHuman_RotateX         = %s;\n' % obj.rx)
    outputFileDescriptor.write('#declare MakeHuman_RotateY         = %s;\n' % -obj.ry)
    outputFileDescriptor.write('#declare MakeHuman_RotateZ         = %s;\n\n' % obj.rz)

  # Calculate some useful values and add them to the output as POV-Ray variable
  # declarations so they can be readily accessed from a POV-Ray scene file.

    povraySizeData(obj, outputFileDescriptor)

  # Vertices - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_VertexArray = array[%s] {\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.co[0], v.co[1], v.co[2]))
    outputFileDescriptor.write('''
}

''')

  # Normals - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_NormalArray = array[%s] {\n  ' % len(obj.verts))
    for v in obj.verts:
        outputFileDescriptor.write('<%s,%s,%s>' % (v.no[0], v.no[1], v.no[2]))
    outputFileDescriptor.write('''
}

''')

    faces = [f for f in obj.faces if not 'joint-' in f.group.name]

  # UV Vectors - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_UVArray = array[%s] {\n  ' % len(obj.uvValues))
    for uv in obj.uvValues:
        
        outputFileDescriptor.write('<%s,%s>' % (uv[0], uv[1]))

    # outputFileDescriptor.write("\n")

    outputFileDescriptor.write('''
}

''')

  # Faces - Write a POV-Ray array of arrays to the output stream

    outputFileDescriptor.write('#declare MakeHuman_FaceArray = array[%s][3] {\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('{%s,%s,%s}' % (f.verts[0].idx, f.verts[1].idx, f.verts[2].idx))
        outputFileDescriptor.write('{%s,%s,%s}' % (f.verts[2].idx, f.verts[3].idx, f.verts[0].idx))
    outputFileDescriptor.write('''
}

''')

  # FaceGroups - Write a POV-Ray array to the output stream and build a list of indices
  # that can be used to cross-reference faces to the Face Groups that they're part of.

    outputFileDescriptor.write('#declare MakeHuman_FaceGroupArray = array[%s] {\n  ' % obj.faceGroupCount)
    fgIndex = 0
    faceGroupIndex = {}
    for fg in obj.faceGroups:
        faceGroupIndex[fg.name] = fgIndex
        outputFileDescriptor.write('  "%s",\n' % fg.name)
        fgIndex += 1
    outputFileDescriptor.write('''}

''')

  # FaceGroupIndex - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_FaceGroupIndexArray = array[%s] {\n  ' % len(faces))
    for f in faces:
        outputFileDescriptor.write('%s,' % faceGroupIndex[f.group.name])
    outputFileDescriptor.write('''
}

''')

  # UV Indices for each face - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('#declare MakeHuman_UVIndexArray = array[%s][3] {\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('{%s,%s,%s}' % (f.uv[0], f.uv[1], f.uv[2]))
        outputFileDescriptor.write('{%s,%s,%s}' % (f.uv[2], f.uv[3], f.uv[0]))
    outputFileDescriptor.write('''
}

''')

  # Joint Positions - Write a set of POV-Ray variables to the output stream

    faceGroupExtents = {}
    for f in obj.faces:
        if 'joint-' in f.group.name:

      # Compare the components of each vertex to find the min and max values for this faceGroup

            if f.group.name in faceGroupExtents:
                maxX = max([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0], faceGroupExtents[f.group.name][3]])
                maxY = max([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1], faceGroupExtents[f.group.name][4]])
                maxZ = max([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2], faceGroupExtents[f.group.name][5]])
                minX = min([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0], faceGroupExtents[f.group.name][0]])
                minY = min([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1], faceGroupExtents[f.group.name][1]])
                minZ = min([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2], faceGroupExtents[f.group.name][2]])
            else:
                maxX = max([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0]])
                maxY = max([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1]])
                maxZ = max([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2]])
                minX = min([f.verts[0].co[0], f.verts[1].co[0], f.verts[2].co[0], f.verts[3].co[0]])
                minY = min([f.verts[0].co[1], f.verts[1].co[1], f.verts[2].co[1], f.verts[3].co[1]])
                minZ = min([f.verts[0].co[2], f.verts[1].co[2], f.verts[2].co[2], f.verts[3].co[2]])
            faceGroupExtents[f.group.name] = [minX, minY, minZ, maxX, maxY, maxZ]

  # Write out the centre position of each joint

    for fg in obj.faceGroups:
        if 'joint-' in fg.name:
            jointVarName = string.replace(fg.name, '-', '_')
            jointCentreX = (faceGroupExtents[fg.name][0] + faceGroupExtents[fg.name][3]) / 2
            jointCentreY = (faceGroupExtents[fg.name][1] + faceGroupExtents[fg.name][4]) / 2
            jointCentreZ = (faceGroupExtents[fg.name][2] + faceGroupExtents[fg.name][5]) / 2

      # jointCentre  = "<"+jointCentreX+","+jointCentreY+","+jointCentreZ+">"

            outputFileDescriptor.write('#declare MakeHuman_%s=<%s,%s,%s>;\n' % (jointVarName, jointCentreX, jointCentreY, jointCentreZ))
    outputFileDescriptor.write('''

''')

  # Copy macro and texture definitions straight across to the output file.

    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        print 'Error opening file to read static content.'
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

  # The POV-Ray include file is complete

    outputFileDescriptor.close()
    print "POV-Ray '#include' file generated."

  # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        print 'Error opening file to read standard scene file.'
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        print 'Error opening file to write standard scene file.'
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

  # Copy the textures.tif file into the output directory

    try:
        shutil.copy(pigmentMap, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Copy the makehuman_groupings.inc file into the output directory

    try:
        shutil.copy(groupingsFile, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    print 'Sample POV-Ray scene file generated.'

def yafarayGeometry(yi, obj):
    """
  This function exports data in the form of a mesh2 humanoid object. The POV-Ray 
  file generated is fairly inflexible, but is highly efficient. 
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  camera:
      *Camera object*. The camera to render from. 
  
  path:
      *string*. The file system path to the output files that need to be generated. 
    """

  # Certain blocks of SDL are mostly static and can be copied directly from reference
  # files into the output files.

  # Mesh2 Object - Write the initial part of the mesh2 object declaration
  # povman
    have_uv = False
    vertcount= len(obj.verts)
    facescount = len(obj.faces)
    if len(obj.uvValues) > 0:
        have_uv = True

    print str(facescount)
    # default mat
    yi.paramsClearAll()
    yi.paramsSetColor("color", 0.9, 0.15, 0.19 )
    yi.paramsSetString("type", "shinydiffusemat")
    mat = yi.createMaterial("myMat")
    #
    ID = yi.getNextFreeID()
    yi.startGeometry()
    yi.startTriMesh(ID, vertcount, facescount, False, have_uv, 0)
    #
    for v in obj.verts:
        yi.addVertex(v.co[0], v.co[1], v.co[2])
    
    faces = [f for f in obj.faces if not 'joint-' in f.group.name]

    # UV Vectors - Write a POV-Ray array to the output stream

    #outputFileDescriptor.write('  uv_vectors {\n  ')
    #outputFileDescriptor.write('    %s\n  ' % len(obj.uvValues))
    
    for uv in obj.uvValues:
        yi.addUV(uv[0], uv[1])
        
    #outputFileDescriptor.write('<%s,%s>' % (uv[0], uv[1]))
        
    
    # Faces - Write a POV-Ray array of arrays to the output stream

    #.write('  face_indices {\n  ')
    #outputFileDescriptor.write('    %s\n  ' % (len(faces) * 2))
    for f in faces:
        yi.addTriangle(f.verts[0].idx, f.verts[1].idx, f.verts[2].idx, f.uv[0], f.uv[1], f.uv[2], mat)
        yi.addTriangle(f.verts[2].idx, f.verts[3].idx, f.verts[0].idx, f.uv[2], f.uv[3], f.uv[0], mat)
        
    yi.endTriMesh()
    yi.endGeometry()
    #
    return ID
        
    """
        
        outputFileDescriptor.write('<%s,%s,%s>' % (f.verts[0].idx, f.verts[1].idx, f.verts[2].idx))
        outputFileDescriptor.write('<%s,%s,%s>' % (f.verts[2].idx, f.verts[3].idx, f.verts[0].idx))
    outputFileDescriptor.write('''
  }

''')

  # UV Indices for each face - Write a POV-Ray array to the output stream

    outputFileDescriptor.write('  uv_indices {\n  ')
    outputFileDescriptor.write('    %s\n  ' % (len(faces) * 2))
    for f in faces:
        outputFileDescriptor.write('<%s,%s,%s>' % (f.uv[0], f.uv[1], f.uv[2]))
        outputFileDescriptor.write('<%s,%s,%s>' % (f.uv[2], f.uv[3], f.uv[0]))
    outputFileDescriptor.write('''
  }
''')

  # Mesh2 Object - Write the end squiggly bracket for the mesh2 object declaration

    outputFileDescriptor.write('''
  uv_mapping
''')
    outputFileDescriptor.write('''}

''')

  # Copy texture definitions straight across to the output file.

    try:
        staticContentFileDescriptor = open(staticFile, 'r')
    except:
        print 'Error opening file to read static content.'
        return 0
    staticContentLines = staticContentFileDescriptor.read()
    outputFileDescriptor.write(staticContentLines)
    outputFileDescriptor.write('\n')
    staticContentFileDescriptor.close()

  # The POV-Ray include file is complete

    outputFileDescriptor.close()
    print "POV-Ray '#include' file generated."

  # Copy a sample scene file across to the output directory

    try:
        sceneFileDescriptor = open(sceneFile, 'r')
    except:
        print 'Error opening file to read standard scene file.'
        return 0
    try:
        outputSceneFileDescriptor = open(outputSceneFile, 'w')
    except:
        print 'Error opening file to write standard scene file.'
        return 0
    sceneLines = sceneFileDescriptor.read()
    sceneLines = string.replace(sceneLines, 'xxFileNamexx', nameOnly)
    sceneLines = string.replace(sceneLines, 'xxUnderScoresxx', underScores)
    sceneLines = string.replace(sceneLines, 'xxLowercaseFileNamexx', nameOnly.lower())
    outputSceneFileDescriptor.write(sceneLines)

  # Copy the textures.tif file into the output directory

    try:
        shutil.copy(pigmentMap, outputDirectory)
    except (IOError, os.error), why:
        print "Can't copy %s" % str(why)

  # Job done

    outputSceneFileDescriptor.close()
    sceneFileDescriptor.close()
    print 'Sample POV-Ray scene file generated'


"""
#
def yafarayCameraData(yi, camera, resolution):
    """
    This function outputs standard camera data common to all YafaRay format exports. 

    Parameters
    ----------
  
    cameraSettings:
      *list of floats*. A list of float values conveying camera and image related 
      information. This includes the position, orientation and field of view of the
      camera along with the screen dimensions from MakeHuman. These values are passed 
      along to YafaRay as variables so that the default rendered image can mimic the
      image last displayed in MakeHuman. 
     """     
    
    # povman
    ##--- create cam
    yi.paramsClearAll()
    yi.paramsSetString("type", "perspective")
    yi.paramsSetPoint("from", camera.eyeX, camera.eyeY, camera.eyeZ )
    yi.paramsSetPoint("to", camera.focusX, camera.focusY, camera.focusZ )
    yi.paramsSetPoint("up", camera.upX, camera.upY, camera.upZ )
    yi.paramsSetInt("resx", resolution[0]) #640)
    yi.paramsSetInt("resy", resolution[1]) #480)
    yi.paramsSetFloat("focal", 1.04) # fovAngle ??
    yi.createCamera("camera")
    #
    print "    Yafy: Create camera from Makehuman"
    

def povraySizeData(obj, outputFileDescriptor):
    """
  This function outputs standard object dimension data common to all POV-Ray 
  format exports. 

  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
  outputFileDescriptor:
      *file descriptor*. The file to which the camera settings need to be written. 
  """

    maxX = 0
    maxY = 0
    maxZ = 0
    minX = 0
    minY = 0
    minZ = 0
    for v in obj.verts:
        maxX = max(maxX, v.co[0])
        maxY = max(maxY, v.co[1])
        maxZ = max(maxZ, v.co[2])
        minX = min(minX, v.co[0])
        minY = min(minY, v.co[1])
        minZ = min(minZ, v.co[2])
    outputFileDescriptor.write('// Figure Dimensions. \n')
    outputFileDescriptor.write('#declare MakeHuman_MaxExtent = < %s, %s, %s>;\n' % (maxX, maxY, maxZ))
    outputFileDescriptor.write('#declare MakeHuman_MinExtent = < %s, %s, %s>;\n' % (minX, minY, minZ))
    outputFileDescriptor.write('#declare MakeHuman_Center    = < %s, %s, %s>;\n' % ((maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2))
    outputFileDescriptor.write('#declare MakeHuman_Width     = %s;\n' % (maxX - minX))
    outputFileDescriptor.write('#declare MakeHuman_Height    = %s;\n' % (maxY - minY))
    outputFileDescriptor.write('#declare MakeHuman_Depth     = %s;\n' % (maxZ - minZ))
    outputFileDescriptor.write('''

''')


# Temporary Function: The loading of hairs should be done by the main application.


def povrayLoadHairsFile(path):

    pass
    #hairsClass.loadHairs(path)


def povrayWriteHairs(outputDirectory, mesh):
    """
  This function generates hair for the POV-Ray format export. Each hair is 
  written out as a sphere_sweep. 

  Parameters
  ----------
  
  outputDirectory:
      *directory path*. A string containing the name of the directory into which the
      output file is to be written. 
  
  mesh:
      *mesh object*. The humanoid mesh object to which hair is added. 
  """
    return # This code needs to be updated
    print 'Writing hair'

    hairsClass.humanVerts = mesh.verts
    hairsClass.adjustGuides()
    hairsClass.generateHairStyle1()
    hairsClass.generateHairStyle2()

  # The output file name should really be picked up from screen field settings.

    hairFileName = '%s/makehuman_hair.inc' % outputDirectory
    hairFile = open(hairFileName, 'w')

  # Need to work out the total number of hairs upfront to know what size
  # array will be needed in POV-Ray. Writing to an array rather than adding
  # the hairs directly to the scene helps reduce the rendering times for
  # test renders, because you can easily render every 10th hair or every
  # 100th hair.

    totalNumberOfHairs = 0
    for hSet in hairsClass.hairStyle:
        totalNumberOfHairs += len(hSet.hairs)
    hairFile.write('#declare MakeHuman_HairArray = array[%i] {\n' % totalNumberOfHairs)

  # MakeHuman hair styles consist of lots of sets of hairs.

    hairCounter = 0
    for hSet in hairsClass.hairStyle:
        if 'clump' in hSet.name:
            hDiameter = hairsClass.hairDiameterClump * random.uniform(0.5, 1)
        else:
            hDiameter = hairsClass.hairDiameterMultiStrand * random.uniform(0.5, 1)

    # Each hair is represented as a separate sphere_sweep in POV-Ray.

        for hair in hSet.hairs:
            hairCounter += 1
            hairFile.write('sphere_sweep{')
            hairFile.write('b_spline ')
            hairFile.write('%i,' % len(hair.controlPoints))
            controlPointCounter = 0

      # Each control point is written out, along with the radius of the
      # hair at that point.

            for cP in hair.controlPoints:
                controlPointCounter += 1
                hairFile.write('<%s,%s,%s>,%s' % (round(cP[0], 4), round(cP[1], 4), round(cP[2], 4), round(hDiameter / 2, 4)))

      # All coordinates except the last need a following comma.

                if controlPointCounter != len(hair.controlPoints):
                    hairFile.write(',')

      # End the sphere_sweep declaration for this hair

            hairFile.write('}')

      # All but the final sphere_sweep (each array element) needs a terminating comma.

            if hairCounter != totalNumberOfHairs:
                hairFile.write(',\n')
            else:
                hairFile.write('\n')

  # End the array declaration.

    hairFile.write('}\n')
    hairFile.write('\n')

  # Pick up the hair color and create a default POV-Ray hair texture.

    hairFile.write('#ifndef (MakeHuman_HairTexture)\n')
    hairFile.write('  #declare MakeHuman_HairTexture = texture {\n')
    hairFile.write('    pigment {rgb <%s,%s,%s>}\n' % (hairsClass.tipColor[0], hairsClass.tipColor[1], hairsClass.tipColor[2]))
    hairFile.write('  }\n')
    hairFile.write('#end\n')
    hairFile.write('\n')

  # Dynamically create a union of the hairs (or a subset of the hairs).
  # By default use every 25th hair, which is usually ok for test renders.

    hairFile.write('#ifndef(MakeHuman_HairStep) #declare MakeHuman_HairStep = 25; #end\n')
    hairFile.write('union{\n')
    hairFile.write('  #local MakeHuman_I = 0;\n')
    hairFile.write('  #while (MakeHuman_I < %i)\n' % totalNumberOfHairs)
    hairFile.write('    object {MakeHuman_HairArray[MakeHuman_I] texture{MakeHuman_HairTexture}}\n')
    hairFile.write('    #local MakeHuman_I = MakeHuman_I + MakeHuman_HairStep;\n')
    hairFile.write('  #end\n')

  # hairFile.write('  translate -z*0.0\n')

    hairFile.write('}')
    hairFile.close()
    print 'Totals hairs written: ', totalNumberOfHairs
    print 'Number of tufts', len(hairsClass.hairStyle)


