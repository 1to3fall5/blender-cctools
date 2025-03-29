import bpy
from bpy.types import Operator
from bpy.props import StringProperty

class CCTOOLS_OT_rename_uv_maps(Operator):
    """重命名选中物体的所有UV通道"""
    bl_idname = "cctools.rename_uv_maps"
    bl_label = "重命名UV通道"
    bl_options = {'REGISTER', 'UNDO'}
    
    prefix: StringProperty(
        name="前缀",
        description="UV通道名称前缀",
        default="UVmap"
    )
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        processed_count = 0
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                processed_count += 1
                uv_layers = obj.data.uv_layers
                
                if len(uv_layers) == 0:
                    continue
                
                # 创建临时名称列表
                temp_names = [f"temp_{i}" for i in range(len(uv_layers))]
                
                # 第一步：给所有UV通道临时名称以避免冲突
                for i, uv_layer in enumerate(uv_layers):
                    uv_layer.name = temp_names[i]
                
                # 第二步：按照正确的顺序重命名
                for i, uv_layer in enumerate(uv_layers):
                    new_name = f"{self.prefix}_{i + 1}"
                    uv_layer.name = new_name
                    
        self.report({'INFO'}, f"已处理 {processed_count} 个物体的UV通道")
        return {'FINISHED'}

classes = (
    CCTOOLS_OT_rename_uv_maps,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls) 