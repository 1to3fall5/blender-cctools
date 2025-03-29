import importlib

# 动态导入模块
module_names = [
    "uv_rename",
    "uv_copy",
    "uv_merge"
]

modules = []
for module_name in module_names:
    try:
        module = importlib.import_module(f".{module_name}", package=__package__)
        modules.append(module)
    except ImportError as e:
        print(f"Warning: Could not import {module_name}: {e}")

def register():
    for module in modules:
        if hasattr(module, 'register'):
            module.register()

def unregister():
    for module in modules:
        if hasattr(module, 'unregister'):
            module.unregister() 