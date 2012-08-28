import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_aspect(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_aspect,self).__init__(imported_files,'./modules/aspect_ui.ui')

        self.name = 'Aspect'
        self.version = '1.0'
        self.description = 'Creates an aspect.'
        self.author = 'Chris Marsh'
        self.category = 'Terrain'

    def run(self):
    
        try:
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise ValueError()
            #call our main handler
            return self.exec_module(file=self.selected_file, name=name)
        except ValueError:
            self.mbox_error('Invalid field. Perhaps a field is empty?')
        
        return None
    
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        #create a new landclass
        r = ct.terrain.landclass()
        r.set_creator(self.name)
        r._name = kwargs['name']
        #open the file
        r.open(kwargs['file'])
        
        p,q = np.gradient(r.get_raster())

        #http://webhelp.esri.com/arcgisdesktop/9.2/index.cfm?TopicName=How%20Aspect%20works
        aspect = 180/np.pi * np.arctan2(q,-p)

        #build indexes first so we don't undo some of the corrections
        idx = aspect > 90
        idx2 = aspect <= 90  
        
        aspect[idx] = 360 - aspect[idx]+90
        
        aspect[idx2] = 90 - aspect[idx2]
        
        #aspect = 90 - aspect
        r._raster = aspect
        return r
    
    


 
 