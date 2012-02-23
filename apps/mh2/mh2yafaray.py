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

This module implements functions to export a human model in YafaRay  API format. YafaRay is a 
Raytracing application (a renderer) that is free to download and use.

"""

import os
import shutil
import subprocess
import mh2yafaray_ini
import random
import mh
#
from math import pi, sin, cos
import yafrayinterface
#
materialMap={}
        
def yafarayRenderer(obj, app, settings):
    """
  This function exports data in a format that can be used to reconstruct the humanoid 
  object in YafaRay. It supports a range of options that can be specified in the Python 
  script file mh2yafaray_ini.py, which is reloaded each time this function is run. This 
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
    source = mh2yafaray_ini.source if settings['source'] == 'gui' else settings['source']
    action = mh2yafaray_ini.action 
    lighting = mh2yafaray_ini.lighting if settings['lighting'] == 'dl' else settings['lighting']
    world = mh2yafaray_ini.world if settings['world'] == 'texture' else settings['world']
    image_path = mh2yafaray_ini.yafaray_path 
        
    if action == 'render':
        
        if source == 'xml':
            yi = yafrayinterface.xmlInterface_t()
        else:
            yi = yafrayinterface.yafrayInterface_t()
            yi.loadPlugins(mh2yafaray_ini.PLUGIN_PATH)
        
        #--
        yi.startScene()
        
        #-- texture ----
        yafarayTexture(yi, image_path)
                
        #-- create material ----
        yafarayMaterial(yi)
             
        #-- lights ----
        yafarayLights(yi)
                
        #-- geometry ----
        yafarayGeometry(yi, obj)

        #-- create cam ----
        yafarayCameraData(yi, camera, resolution)
        
        #-- background ----
        yafarayBackground(yi, world)
        
        #-- integrator ----
        yafarayIntegrators(yi, lighting)
        
        #-- output ----
        if source == 'console':
            
            yi.paramsClearAll()
            path_net = str(path).replace("\"","/") # use / for campatibility by Unix systems ?
            file_type = 'tga' # To do; create option in GUI ?
            yi.paramsSetString("type", file_type)
            yi.paramsSetBool("alpha_channel", False)
            yi.paramsSetBool("z_channel", False)
            yi.paramsSetInt("width", resolution[0])
            yi.paramsSetInt("height", resolution[1])
            ih = yi.createImageHandler("outFile")
            output = yafrayinterface.imageOutput_t(ih, path_net + 'test.exr', 0, 0) # Todo; revised for Unix systems
        
        #
        if source == 'xml':
            output = yafrayinterface.imageOutput_t()
        
        #-- render options ----
        yafarayRender(yi, resolution)
        
        #-- QT interface ----
        if source == 'gui':
            import yafqt
            yafqt.initGui()
            guiSettings = yafqt.Settings()
            guiSettings.autoSave = False
            guiSettings.closeAfterFinish = False
            guiSettings.mem = None
            #guiSettings.fileName = 'test.png'
            guiSettings.autoSaveAlpha = False
            #-- create render window
            yafqt.createRenderWidget(yi, resolution[0], resolution[1], 0, 0, guiSettings)
        else:
            yi.render(output)
 
        yi.clearAll()
        #del yi
        
def yafarayTexture(yi, image_path):
    #
    yi.paramsClearAll()
    yi.paramsSetString("filename", image_path +"/body.png") #lighting_blur.jpg")
    yi.paramsSetFloat("gamma", 2.2 )
    yi.paramsSetBool("use_alpha", True )
    yi.paramsSetBool("calc_alpha", True )
    yi.paramsSetFloat("normalmap", False )
    yi.paramsSetString("type", "image")
    yi.createTexture("body")
    #--
    yi.paramsClearAll()
    yi.paramsSetInt("depth", 6)
    yi.paramsSetBool("hard", False)
    yi.paramsSetString("noise_type", "newperlin")
    yi.paramsSetFloat("size", 90.9091)
    yi.paramsSetString("type", "clouds")
    #-
    yi.createTexture("bump_skin")

def yafarayMaterial(yi):
    # material definitions
    yi.paramsClearAll()
    yi.paramsSetFloat("IOR",  1)
    yi.paramsSetString("bump_shader", "bump_layer")
    yi.paramsSetColor("color", 0.675, 0.38, 0.294, 0)
    yi.paramsSetString("diffuse_brdf", "oren_nayar")
    yi.paramsSetFloat("diffuse_reflect",  1)
    yi.paramsSetString("diffuse_shader", "diff_layer")
    yi.paramsSetFloat("emit", 0)
    yi.paramsSetBool("fresnel_effect", False)
    yi.paramsSetColor("mirror_color",  0.682, 0.384, 0.294, 0)
    yi.paramsSetFloat("sigma", 0.579386)
    yi.paramsSetFloat("specular_reflect", 0.018)
    yi.paramsSetFloat("translucency", 0.524)
    yi.paramsSetFloat("transmit_filter", 1)
    yi.paramsSetFloat("transparency", 0)
    yi.paramsSetString("type", "shinydiffusemat")
       
    yi.paramsPushList()
    yi.paramsSetFloat("colfac", 1)
    yi.paramsSetBool("color_input", True)
    yi.paramsSetColor("def_col", 1, 0, 1, 1)
    yi.paramsSetFloat("def_val", 1)
    yi.paramsSetBool("do_color", True)
    yi.paramsSetBool("do_scalar", False)
    yi.paramsSetString("element", "shader_node")
    yi.paramsSetString("input", "diffuse_map")
    yi.paramsSetInt("mode", 0)
    yi.paramsSetString("name", "diff_layer")
    yi.paramsSetBool("negative", False)
    yi.paramsSetBool("noRGB", False)
    yi.paramsSetBool("stencil", False)
    yi.paramsSetString("type", "layer")
    yi.paramsSetColor("upper_color", 0.675, 0.38, 0.294, 1)
    yi.paramsSetFloat("upper_value", 0)
    yi.paramsSetBool("use_alpha", False)
    yi.paramsEndList()
        
    yi.paramsPushList()
    yi.paramsSetString("element", "shader_node")
    yi.paramsSetString("mapping", "plain")
    yi.paramsSetString("name", "diffuse_map")
    yi.paramsSetPoint("offset", 0, 0, 0)
    yi.paramsSetInt("proj_x", 1)
    yi.paramsSetInt("proj_y", 2)
    yi.paramsSetInt("proj_z", 3)
    yi.paramsSetPoint("scale", 1, 1, 1)
    yi.paramsSetString("texco", "uv")
    yi.paramsSetString("texture", "body")
    yi.paramsSetString("type", "texture_mapper")
    yi.paramsEndList()
        
    yi.paramsPushList()
    yi.paramsSetBool("color_input", False)
    yi.paramsSetColor("def_col", 1, 0, 1, 1)
    yi.paramsSetFloat("def_val", 1)
    yi.paramsSetBool("do_color", False)
    yi.paramsSetBool("do_scalar", True)
    yi.paramsSetString("element", "shader_node")
    yi.paramsSetString("input", "bump_map")
    yi.paramsSetInt("mode", 0)
    yi.paramsSetString("name", "bump_layer")
    yi.paramsSetBool("negative", False) 
    yi.paramsSetBool("noRGB", False)
    yi.paramsSetBool("stencil",  False)
    yi.paramsSetString("type", "layer")
    yi.paramsSetColor("upper_color", 0, 0, 0, 1)
    yi.paramsSetFloat("upper_value", 0)
    yi.paramsSetBool("use_alpha", False)
    yi.paramsSetFloat("valfac", 0.1)
    yi.paramsEndList()
    #--
    yi.paramsPushList()
    yi.paramsSetFloat("bump_strength", 0.1)
    yi.paramsSetString("element", "shader_node")
    yi.paramsSetString("mapping", "sphere")
    yi.paramsSetString("name", "bump_map")
    yi.paramsSetPoint("offset", 0, 0, 0)
    yi.paramsSetInt("proj_x", 1)
    yi.paramsSetInt("proj_y", 2)
    yi.paramsSetInt("proj_z", 3)
    yi.paramsSetPoint("scale", 1, 1, 1)
    yi.paramsSetString("texco", "global")
    yi.paramsSetString("texture", "bump_skin")
    yi.paramsSetString("type", "texture_mapper")
    yi.paramsEndList()
    
    mat = yi.createMaterial("Skin_test")
    materialMap['Skin_test']= mat
    
    #-
    yi.paramsClearAll()
    yi.paramsSetFloat("IOR", 0.548 ) # human skyn
    yi.paramsSetColor("color", 1.0, 0.5, 0.71, 1 )
    yi.paramsSetFloat("diffuse_reflect", 0.8296860309 )
    yi.paramsSetFloat("emit", 0 )
    yi.paramsSetBool("fresnel_effect", False )
    yi.paramsSetColor("mirror_color", 1, 0, 0, 1 )
    yi.paramsSetFloat("specular_reflect", 0.005 )
    yi.paramsSetFloat("translucency", 0 )
    yi.paramsSetFloat("transmit_filter", 1 )
    yi.paramsSetFloat("transparency", 0 )
    yi.paramsSetString("type", "shinydiffusemat")
    
    yi.paramsPushList()
    yi.paramsSetString("element", "shader_node") 
    yi.paramsSetString("type", "texture_mapper")
    yi.paramsSetString("name", "rgbcube_mapper")
    yi.paramsSetString("texco", "uv")
    yi.paramsSetString("texture", "body")
    yi.paramsSetString("mapping", "plain" )
    yi.paramsEndList()
       
    yi.paramsSetString("diffuse_shader", "rgbcube_mapper")
    yi.createMaterial("myMat")
        
    materialMap['myMat'] = mat
                               
def yafarayLights(yi):
    #
    yi.paramsClearAll()
    yi.paramsSetString("type", "directional")
    yi.paramsSetPoint("direction", -0.3, -0.3, 0.8 )
    yi.paramsSetColor("color", 0.9, 0.9, 0.9 )
    yi.paramsSetFloat("power", 1.0 )
    yi.createLight("myDirectional")
    #
    yi.paramsClearAll()
    yi.paramsSetColor("color", 1, 1, 1, 1)
    yi.paramsSetPoint("from", 11, 3, 8)
    yi.paramsSetFloat("power", 160)
    yi.paramsSetString("type", "pointlight")
    yi.createLight("LAMP1")

def yafarayGeometry(yi, obj):
    """
  This function exports mesh data direct in the form of YafaRay Api.
  
  Parameters
  ----------
  
  obj:
      *3D object*. The object to export. This should be the humanoid object with
      uv-mapping data and Face Groups defined.
  
    """
    
    # create geometry
    ''' filter 'joints' objects '''
    faces = [f for f in obj.faces if not 'joint-' in f.group.name]
    #
    have_uv = False
    v_count= len(obj.verts)
    f_count = len(faces)*2
    if len(obj.uvValues) > 0:  have_uv = True
    #
    mat = materialMap['myMat'] # Skin_test

    #
    ID = yi.getNextFreeID()
    yi.startGeometry()
    yi.startTriMesh(ID, v_count, f_count, False, have_uv, 0)
    #
    for v in obj.verts:
        yi.addVertex(v.co[0], v.co[1], v.co[2])
    
    # UV Vectors 
    ''' have_uv always is True? '''
    if have_uv:
        for uv in obj.uvValues:
            yi.addUV(uv[0], uv[1])
    
    # face index. 
    ''' only quads in the human mesh ? '''
    for f in faces:
        if have_uv:
            yi.addTriangle(f.verts[0].idx, f.verts[1].idx, f.verts[2].idx, f.uv[0], f.uv[1], f.uv[2], mat)
            yi.addTriangle(f.verts[2].idx, f.verts[3].idx, f.verts[0].idx, f.uv[2], f.uv[3], f.uv[0], mat)
        else:
            yi.addTriangle(f.verts[0].idx, f.verts[1].idx, f.verts[2].idx, mat)
            yi.addTriangle(f.verts[2].idx, f.verts[3].idx, f.verts[0].idx, mat)
        
    yi.endTriMesh()
    yi.smoothMesh(ID, 181)
    yi.endGeometry()
    
    #
    return ID

def yafarayCameraData(yi, camera, resolution):
    """
    This function outputs standard camera data common to all YafaRay format Api. 

    Parameters
    ----------
  
    cameraSettings:
      *list of floats*. A list of float values conveying camera and image related 
      information. This includes the position, orientation and field of view of the
      camera along with the screen dimensions from MakeHuman. These values are passed 
      along to YafaRay as variables so that the default rendered image can mimic the
      image last displayed in MakeHuman. 
     """     
    
    #-- create cam ----
    ''' change eyeY for eyeZ. In YafaRay, Z is up '''
    yi.paramsClearAll()
    yi.paramsSetString("type", "perspective")
    yi.paramsSetPoint("from", camera.eyeX, camera.eyeY, camera.eyeZ )
    yi.paramsSetPoint("to", camera.focusX, camera.focusY, camera.focusZ )
    yi.paramsSetPoint("up", camera.upX, camera.eyeZ, camera.eyeY )
    yi.paramsSetInt("resx", resolution[0])
    yi.paramsSetInt("resy", resolution[1])
    yi.paramsSetFloat("focal", 1.5) #TO do; revised formule for calulate corrected focal value.(fovAngle ?)
    yi.createCamera("camera")
    #
    yi.printInfo("Yafy: Create camera from Makehuman")
                    
def yafarayBackground(yi, world):
    #
    yi.paramsClearAll()
    #
    if world == 'color':
        yi.paramsSetString("type", "constant")
        yi.paramsSetColor("color", 0.4, 0.5, 0.9 )
        
    elif world == 'texture':
        
        #
        image_path = mh2yafaray_ini.yafaray_path
        image_file = image_path + "/uv.png"
        #image_file = normpath(image_file)
        yi.paramsSetString("filename", image_file) #"h:/trabajo/hdri/paris_saint_louis_island.hdr")
        #  studio016.hdr
        yi.paramsSetFloat("exposure_adjust", 0.1)                    
        yi.paramsSetString("interpolate", "none") # bilinear
        yi.paramsSetString("type", "image")        
        yi.createTexture("world_texture")

        ''' need clear params here '''
        yi.paramsClearAll()
        
        yi.paramsSetString("mapping", "sphere") # sphere, probe
        
        yi.paramsSetString("texture", "world_texture")
        yi.paramsSetBool("ibl", False)
        yi.paramsSetBool("with_caustic", False)
        yi.paramsSetBool("with_diffuse", False)
        yi.paramsSetInt("ibl_samples", 1)
        yi.paramsSetFloat("power", 1.0)
        yi.paramsSetFloat("rotation", 0.0)
        yi.paramsSetString("type", "textureback")
                
    else:
        #
        yi.paramsSetPoint("from", 0, 10, 40)
        yi.paramsSetFloat("turbidity", 2)
        yi.paramsSetFloat("a_var", 1.0)
        yi.paramsSetFloat("b_var", 1.0)
        yi.paramsSetFloat("c_var", 1.0)
        yi.paramsSetFloat("d_var", 1.0)
        yi.paramsSetFloat("e_var", 1.0)
        yi.paramsSetBool("add_sun", False)
        yi.paramsSetFloat("sun_power", 1)
        yi.paramsSetBool("background_light", False)
        yi.paramsSetInt("light_samples", 8)
        yi.paramsSetFloat("power", 1.0)
        yi.paramsSetString("type", "sunsky")
        
    yi.createBackground("world_background")
    
def yafarayIntegrators(yi, lighting):
    #
    yi.paramsClearAll()
    #
    if lighting == 'dl':
        yi.paramsSetBool("do_AO", True)
        yi.paramsSetInt("AO_samples", 16 )
        yi.paramsSetFloat("AO_distance", 1 )
        yi.paramsSetColor("AO_color", 0.9, 0.9, 0.9)
        yi.paramsSetString("type", "directlighting")
        yi.paramsSetInt("raydepth", 3)
    else:
        yi.paramsSetString("type", "photonmapping")
        yi.paramsSetInt("fg_samples", 16)
        yi.paramsSetInt("photons", 1000000)
        yi.paramsSetInt("cPhotons", 1)
        yi.paramsSetFloat("diffuseRadius", 1.0)
        yi.paramsSetFloat("causticRadius", 1.0)
        yi.paramsSetInt("search", 100)
        yi.paramsSetBool("show_map", False)
        yi.paramsSetInt("fg_bounces", 3)
        yi.paramsSetInt("caustic_mix", 100)
        yi.paramsSetBool("finalGather", True)
        yi.paramsSetInt("bounces", 3)
    yi.createIntegrator("default")
        
    #--- volume integrator ----
    ''' need clear params for create a new integrator '''
    yi.paramsClearAll() 
    yi.paramsSetString("type", "none")
    yi.createIntegrator("volintegr")


def makeSphere(yi, nu, nv, x, y, z, rad, mat):
    # 
    nu = 24
    nv = 48
    x=0
    y=0
    z=0
    rad= .5   

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
                     
def yafarayRender(yi, resolution):
    #
    yi.paramsClearAll()
    yi.paramsSetString("camera_name", "camera")
    yi.paramsSetString("integrator_name", "default")
    yi.paramsSetString("volintegrator_name", "volintegr")
    yi.paramsSetFloat("gamma", 2.2)    
    yi.paramsSetInt("AA_passes", 2)
    yi.paramsSetInt("AA_minsamples", 1)
    yi.paramsSetInt("AA_inc_samples", 2)
    yi.paramsSetFloat("AA_pixelwidth", 1.5)
    yi.paramsSetFloat("AA_threshold", 0.002)
    yi.paramsSetString("filter_type", "gauss")
    #
    yi.paramsSetBool("clamp_rgb", False)
    yi.paramsSetBool("show_sam_pix", True)
    yi.paramsSetBool("premult", False);
    
    yi.paramsSetString("tiles_order", "random")
    yi.paramsSetInt("width", resolution[0])
    yi.paramsSetInt("height", resolution[1])
    yi.paramsSetString("background_name", "world_background")



