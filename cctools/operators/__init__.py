import importlib

# 动态导入模块
module_names = [
    "uv_rename",
    "uv_copy",
    "uv_merge",
    "fbx_export"
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
            try:
                module.register()
            except Exception as e:
                print(f"注册模块出错 {module.__name__}: {str(e)}")

def unregister():
    # 反向遍历模块列表进行注销
    for module in reversed(modules):
        if hasattr(module, 'unregister'):
            try:
                module.unregister()
            except Exception as e:
                print(f"注销模块出错 {module.__name__}: {str(e)}") 