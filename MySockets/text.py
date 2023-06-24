# 字符串组件

import bpy
from bpy.types import NodeSocket

class Socket_Text(NodeSocket):
    # 组件ID
    bl_idname = '_text'

    # 组件标签
    bl_label = "text"

    # 组件描述
    description = "文本组件"

    # 组件形状：面板上的小圆点
    display_shape = 'CIRCLE'
    # [‘CIRCLE’, ‘SQUARE’, ‘DIAMOND’, ‘CIRCLE_DOT’, ‘SQUARE_DOT’, ‘DIAMOND_DOT’], default ‘CIRCLE’

    value = ''
    type = 'STRING'
    # [‘CUSTOM’, ‘VALUE’, ‘INT’, ‘BOOLEAN’, ‘VECTOR’, ‘STRING’, ‘RGBA’, 
    # ‘SHADER’, ‘OBJECT’, ‘IMAGE’, ‘GEOMETRY’, ‘COLLECTION’], default ‘VALUE’

    # 当这个数据被写时【被连接】执行
    def set_func(this, value):
        this['value'] = str(value)

    # 当这个数据被读取时【连接到】执行
    def get_func(this):
        try:
            return this['value']
        except:
            return ''

    # 组件值
    mystr: bpy.props.StringProperty(set = set_func , get = get_func)
    def val(self):
        return self.mystr

    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # 组件颜色
    def draw_color(self, context, node):
        return (1.0, 0.2, 0.216, 0.5)
