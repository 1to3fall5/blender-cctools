from . import uv_panels
from . import model_panels

modules = (
    uv_panels,
    model_panels,
)

def register():
    for module in modules:
        module.register()

def unregister():
    for module in modules:
        module.unregister() 