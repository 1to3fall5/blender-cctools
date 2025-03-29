bl_info = {
    "name": "CCTools",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > CCTools",
    "description": "CC工具集合",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
from . import operators
from . import panels
from . import preferences

def register():
    preferences.register()
    operators.register()
    panels.register()

def unregister():
    panels.unregister()
    operators.unregister()
    preferences.unregister()

if __name__ == "__main__":
    register() 