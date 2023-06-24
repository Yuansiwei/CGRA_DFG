# 与节点部分无关

import bpy

class Test_PT_HelloPanel(bpy.types.Panel):
    bl_idname = "my_panel.hello_panel"
    bl_label = "Test Hello"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "test Addon"

    def draw(self, context):
        layout = self.layout
        
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("my_operator.hello")