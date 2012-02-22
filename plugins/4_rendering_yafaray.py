#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
if 'nt' in sys.builtin_module_names:
    sys.path.append('./pythonmodules')

# We need this for rendering

import mh2yafaray

# We need this for gui controls

import gui3d

print 'YafaRay imported'

class YafaRayTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'YafaRay')

        optionsBox = self.addView(gui3d.GroupBox([10, 80, 9.0], 'Main Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        
        #Buttons
        renderBox = self.addView(gui3d.GroupBox([10, 380, 9.0], 'Render Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        
        source=[]
        self.iniButton = renderBox.addView(gui3d.RadioButton(source, 'Use render console'))
        self.guiButton = renderBox.addView(gui3d.RadioButton(source, 'Use render GUI', selected = True))
        format=[]
        self.arrayButton = renderBox.addView(gui3d.RadioButton(format, 'XML format'))
        self.mesh2Button = renderBox.addView(gui3d.RadioButton(format, 'GUI format', selected = True))
        action=[]
        self.toExportButton = renderBox.addView(gui3d.RadioButton(action , 'Export to XML', selected = True))
        self.toRenderButton = renderBox.addView(gui3d.RadioButton(action , 'Export and render'))
        
        #self.worldButton = optionsBox.addView(gui3d.Button('World'))
        #
        self.renderButton = renderBox.addView(gui3d.Button('Render GUI'))
        #self.xmlButton = renderBox.addView(gui3d.Button('Export XML'))
        #
        lightingBox = self.addView(gui3d.GroupBox([140, 380, 9.0], 'Integrators', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        lighting = []
        self.dlButton = lightingBox.addView(gui3d.RadioButton(lighting, 'DirectLighting', selected = True))
        self.pmButton = lightingBox.addView(gui3d.RadioButton(lighting, 'Photon Map'))
        self.ptButton = lightingBox.addView(gui3d.RadioButton(lighting, 'Pathtracing'))
        
        worldBox = self.addView(gui3d.GroupBox([140, 80, 9.0], 'Background', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        world=[]
        self.sunskyButton = worldBox.addView(gui3d.RadioButton(world, 'SunSky'))
        self.texButton = worldBox.addView(gui3d.RadioButton(world, 'Texture'))
        self.colButton = worldBox.addView(gui3d.RadioButton(world, 'Color', selected = True))
              

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2yafaray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2yafaray.yafarayRenderer(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'ini' if self.iniButton.selected else 'gui',
                 'format':'array' if self.arrayButton.selected else 'mesh2',
                 'action':'export' if self.toExportButton.selected else 'render',
                 'world':'sunsky' if self.sunskyButton.selected else 'color'})

    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addView(YafaRayTaskView(category))

    print 'YafaRay loaded'

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    
    print 'YafaRay unloaded'


