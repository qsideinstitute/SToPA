'''
Purpose: 
to verify that the path locations defined in 
./code/settings.py (relative to the project's 
home directory) are accessible.

'''
import sys
from importlib import util
import os

##
# construct file location ../code/settings.py
settings_file = os.path.join(
os.path.dirname( os.path.dirname(__file__) ),
'code',
'settings.py'
)

##
# import a py file as a module from a file location.
spec = util.spec_from_file_location("placeholder", settings_file)
settings = util.module_from_spec(spec)
sys.modules["placeholder"] = settings

spec.loader.exec_module(settings)

##
# the locations defined in settings should exist.
settings_paths = [
'PROJECT_FOLDER',
'DATA_FOLDER',
'PDF_FOLDER',
'CODE_FOLDER',
'TEST_FOLDER'
]

##
# Keep track of each variable name and store whether 
# the file location in that variable exists. 
folder_exists = {}
for folder_name in settings_paths:
    exists = os.path.exists( getattr(settings, folder_name) )
    folder_exists[folder_name] = exists
        
success = all( folder_exists.values() )
