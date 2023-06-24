# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 打印组件
# XXX Discription: 即时刷新，专为打印节点编写

import bpy
from bpy.types import NodeSocket

# 打印信息组件
class Socket_Print_Info(NodeSocket):
    bl_idname = '_print_info'
    bl_label = "info"
    description = "打印得到的内容，只能作为输入节点"
    display_shape = 'DIAMOND'

    def set_fun(self, value):
        self['value'] = value
        self.node.update()

    def get_fun(self):
        if 'value' in self.keys():
            return self['value']
        else:
            return ''

    default_value: bpy.props.StringProperty(
        set = set_fun,
        get = get_fun,
        maxlen=1000,
    )

    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text = text)
        else:
            layout.prop(self, 'default_value', text = text)

    # 组件颜色
    def draw_color(self, context, node):
        return (1.0, 0.8, 0.216, 0.5)
