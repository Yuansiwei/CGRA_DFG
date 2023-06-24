# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 自定义单选组件示例
# XXX Discription: 组件是构成节点的基础
# blender本身自带了NodeSocketInt、NodeSocketFloat、NodeSocketString等组件

import bpy
from bpy.types import NodeSocket

class Socket_Enum_List(NodeSocket):
    bl_idname = '_enum_list'
    bl_label = "enum_list"

    # 选项列表
    my_items = (
        # [(identifier, name, description, icon, number), ...]
        ('C://', "C://", ""),
        ('D://', "D://", ""),
        ('E://', "E://", ""),
        ('F://', "F://", ""),
    )

    # 组件基本信息
    myenum: bpy.props.EnumProperty(
        name="Direction",# 名称
        description="一个例子",# 描述
        items=my_items,# 可选择的项目
        default='C://',# 默认选择
    )
    def val(self):
        return self.myenum

    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        if self.is_linked:
            # 如果被连接，只显示的文本
            # text += bpy.props.
            layout.label(text=text)
        else:
            # 没有被连接时，显示文本和选项
            layout.prop(self, "myenum", text=text)

    # 组件颜色【那个小点点】
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)
