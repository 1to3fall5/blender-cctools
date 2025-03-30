import bpy
from bpy.types import Panel
import os

class CCTOOLS_PT_fbx_export(Panel):
    bl_label = "批量导出FBX"
    bl_idname = "CCTOOLS_PT_fbx_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CCTools'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # 主要内容
        col = layout.column(align=True)
        
        # 路径选择和历史目录按钮在同一行
        row = col.row(align=True)
        row.prop(scene, "manual_directory", text="")
        
        # 历史目录下拉按钮
        if hasattr(scene, 'text_file_enum'):
            row.menu("CCTOOLS_MT_directory_history", text="", icon='DOWNARROW_HLT')
            row.operator("cctools.delete_directory", text="", icon='X')
        
        # 导出按钮
        row = col.row()
        row.scale_y = 1.5
        row.operator("cctools.batch_export_fbx", icon='EXPORT')

# 历史目录菜单
class CCTOOLS_MT_directory_history(bpy.types.Menu):
    bl_label = "历史目录"
    bl_idname = "CCTOOLS_MT_directory_history"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # 获取枚举项列表
        enum_items = []
        try:
            from ..utils.export_utils import get_directory_items
            enum_items = get_directory_items(self, context)
        except Exception as e:
            print(f"获取目录列表出错: {str(e)}")
        
        # 显示历史目录列表
        if enum_items:
            for identifier, name, description in enum_items:
                op = layout.operator("cctools.select_directory", text=name)
                op.directory = identifier
        else:
            layout.label(text="无历史记录")

# 选择目录操作符
class CCTOOLS_OT_select_directory(bpy.types.Operator):
    bl_idname = "cctools.select_directory"
    bl_label = "选择目录"
    bl_description = "选择历史目录"
    bl_options = {'INTERNAL'}
    
    directory: bpy.props.StringProperty()
    
    def execute(self, context):
        if os.path.exists(self.directory):
            context.scene.manual_directory = self.directory
        return {'FINISHED'}

# 注册的类
classes = (
    CCTOOLS_PT_fbx_export,
    CCTOOLS_MT_directory_history,
    CCTOOLS_OT_select_directory,
)

def register():
    try:
        for cls in classes:
            bpy.utils.register_class(cls)
    except Exception as e:
        print(f"注册面板类时出错: {str(e)}")

def unregister():
    try:
        for cls in reversed(classes):
            if hasattr(cls, 'bl_rna'):
                bpy.utils.unregister_class(cls)
    except Exception as e:
        print(f"注销面板类时出错: {str(e)}") 