import bpy
from . import pref_ui
from . import ui
from . import operators

def register():
    pref_ui.register()
    ui.register()
    operators.register()

def unregister():
    pref_ui.unregister()
    ui.unregister()
    operators.unregister()
