import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty, StringProperty

addon_keymaps = []

# 定义快捷键配置
default_keymap_items = [
    {
        'idname': 'cctools.rename_uv_maps',
        'name': 'UV重命名',
        'key': 'U',
        'ctrl': True,
        'shift': True,
        'alt': False
    },
    {
        'idname': 'cctools.copy_uv_maps',
        'name': 'UV复制',
        'key': 'C',
        'ctrl': True,
        'shift': True,
        'alt': False
    },
    {
        'idname': 'cctools.merge_uv_maps',
        'name': 'UV合并',
        'key': 'M',
        'ctrl': True,
        'shift': True,
        'alt': False
    }
]

class CCTOOLS_preferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        
        # 快捷键显示区域
        box = layout.box()
        col = box.column()
        
        # 显示所有快捷键
        wm = context.window_manager
        kc = wm.keyconfigs.addon
        if kc:
            km = kc.keymaps.get('3D View')
            if km:
                for kmi in km.keymap_items:
                    if kmi.idname.startswith('cctools.'):
                        # 获取操作名称
                        if kmi.idname == 'cctools.rename_uv_maps':
                            op_name = "UV重命名"
                        elif kmi.idname == 'cctools.copy_uv_maps':
                            op_name = "UV复制"
                        elif kmi.idname == 'cctools.merge_uv_maps':
                            op_name = "UV合并"
                        else:
                            op_name = kmi.idname

                        # 创建显示行
                        row = col.row()
                        
                        # 操作名称
                        row.label(text=op_name)
                        
                        # 显示快捷键组合
                        key_str = kmi.type
                        mods = []
                        if kmi.shift: mods.append("Shift")
                        if kmi.ctrl: mods.append("Ctrl")
                        if kmi.alt: mods.append("Alt")
                        if mods:
                            key_str = " + ".join(mods + [key_str])
                        
                        row.label(text=key_str)
                        
                        # 分割线
                        if kmi != km.keymap_items[-1]:
                            col.separator()

def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        # 注册所有默认快捷键
        for item in default_keymap_items:
            kmi = km.keymap_items.new(
                item['idname'],
                item['key'],
                'PRESS',
                ctrl=item['ctrl'],
                shift=item['shift'],
                alt=item['alt']
            )
            addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    bpy.utils.register_class(CCTOOLS_preferences)
    register_keymaps()

def unregister():
    unregister_keymaps()
    bpy.utils.unregister_class(CCTOOLS_preferences) 