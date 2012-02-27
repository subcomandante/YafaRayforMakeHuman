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

        # Buttons
        posy = 80
        worldBox = self.addView(gui3d.GroupBox([10, posy, 9.0], 'Background', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        world=[]
        self.sunskyButton = worldBox.addView(gui3d.RadioButton(world, 'SunSky'))
        self.texButton = worldBox.addView(gui3d.RadioButton(world, 'Texture'))
        self.colButton = worldBox.addView(gui3d.RadioButton(world, 'Color', selected = True))
        #
        lightingBox = self.addView(gui3d.GroupBox([10, 190, 9.0], 'Integrators', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        lighting = []
        self.dlButton = lightingBox.addView(gui3d.RadioButton(lighting, 'DirectLighting', selected = True))
        self.pmButton = lightingBox.addView(gui3d.RadioButton(lighting, 'Photon Map'))
        #
        renderBox = self.addView(gui3d.GroupBox([10, 275, 9.0], 'Render Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        source=[]
        self.consoleButton = renderBox.addView(gui3d.RadioButton(source, 'Render console'))
        self.guiButton = renderBox.addView(gui3d.RadioButton(source, 'Render GUI', selected = True))
        self.xmlButton = renderBox.addView(gui3d.RadioButton(source, 'Write XML'))
        self.renderButton = renderBox.addView(gui3d.Button('Render'))
        #
        
        '''
        optionsBox = self.addView(gui3d.GroupBox([10, 420, 9.0], 'Main Options', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        options = []
        self.raydButton = optionsBox.addView(gui3d.RadioButton(options, 'RayDepth'))
        self.zbufButton = optionsBox.addView(gui3d.RadioButton(options, 'Z Buffer'))
        #
        #aaBox = self.addView(gui3d.GroupBox([10, 190, 9.0], 'Antialias', gui3d.GroupBoxStyle._replace(height=25+24*7+6)))
        '''        
                      

        @self.renderButton.event
        def onClicked(event):            
            
            reload(mh2yafaray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            mh2yafaray.yafarayRenderer(gui3d.app.selectedHuman.mesh, gui3d.app,
                {'source':'console' if self.consoleButton.selected else 'gui' if self.guiButton.selected else 'xml',
                 'lighting':'dl' if self.dlButton.selected else 'pm',
                 'world':'sunsky' if self.sunskyButton.selected else 'texture' if self.texButton.selected else 'color'})

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


