import bpy
from bpy.types import Panel

class CCTOOLS_PT_uv_tools(Panel):
    """UV工具主面板"""
    bl_label = "UV工具集"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CCTools'
    bl_options = {'DEFAULT_CLOSED'}  # 默认折叠

    def draw(self, context):
        layout = self.layout
        
        # 重命名工具
        box = layout.box()
        box.label(text="重命名工具")
        op = box.operator("cctools.rename_uv_maps")
        box.prop(op, "prefix")
        
        # 复制工具
        box = layout.box()
        box.label(text="复制工具")
        box.operator("cctools.copy_uv_maps")
        
        # 合并工具
        box = layout.box()
        box.label(text="合并工具")
        box.operator("cctools.merge_uv_maps")

classes = (
    CCTOOLS_PT_uv_tools,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls) 