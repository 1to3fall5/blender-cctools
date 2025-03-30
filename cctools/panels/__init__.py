import importlib
import sys
import os

def import_module(module_name):
    try:
        return importlib.import_module(f".{module_name}", package=__package__)
    except ImportError as e:
        print(f"无法导入模块 {module_name}: {str(e)}")
        return None

# 动态导入模块
modules = []

# 尝试导入面板模块
panel_modules = ['uv_panels', 'fbx_panels']
for module_name in panel_modules:
    module = import_module(module_name)
    if module is not None:
        modules.append(module)

def register():
    for module in modules:
        try:
            if hasattr(module, 'register'):
                module.register()
        except Exception as e:
            print(f"注册模块出错 {module.__name__}: {str(e)}")

def unregister():
    for module in reversed(modules):
        try:
            if hasattr(module, 'unregister'):
                module.unregister()
        except Exception as e:
            print(f"注销模块出错 {module.__name__}: {str(e)}") 