# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 组件模板
# XXX Discription: 组件是构成节点的基础，可以承担数据处理，但不建议做数据交互
# blender本身自带了NodeSocketInt、NodeSocketFloat、NodeSocketString等组件
# 本程序只作模板，并不注册使用

import bpy
from bpy.types import NodeSocket

class Socket_Temp(NodeSocket):
    # 自定义组件的调用ID，同NodeSocketInt等
    bl_idname = '_temp'

    # 组件标签，尚不知道有什么用
    bl_label = "temp"

    # 组件描述
    description = "组件制作模板"

    # 组件形状：面板上的小圆点
    display_shape = 'CIRCLE'
    # NOTE: 可选项
    # [‘CIRCLE’, ‘SQUARE’, ‘DIAMOND’, ‘CIRCLE_DOT’, ‘SQUARE_DOT’, ‘DIAMOND_DOT’], default ‘CIRCLE’

    # 组件的默认值
    default_value = ''
    value = ''

    # 组件的类型【INT类型对应NodeSocketInt，VALUE对应NodeSocketFloat】
    type = 'CUSTOM'
    # NOTE: 可选项
    # [‘CUSTOM’, ‘VALUE’, ‘INT’, ‘BOOLEAN’, ‘VECTOR’, ‘STRING’, ‘RGBA’, 
    # ‘SHADER’, ‘OBJECT’, ‘IMAGE’, ‘GEOMETRY’, ‘COLLECTION’], default ‘VALUE’

    # 当这个property被写时【被连接】执行
    def set_func(this, value):
        ...

    # 当这个property被读取时【连接到】执行
    def get_func(this):
        ...

    """自带的组件属性"""
    # node: 包含该组件实例的节点实例
    # name: 组件名称【可以修改】
    # identifier: 组件的识别身份【我猜】，默认与name等值，但不可修改
    # links: 和这个组件实例连接的节点实例列表

    # 可以给组件一个property
    custom_info: bpy.props.StringProperty(
        default_value = '',
        set = set_func,
        get = get_func,
    )

    # 绘制组件
    def draw(self, context, layout, node, text):
        # layout --> 放置UI组件
        # node --> 包含该组件实例的节点实例
        # text --> 用于绘制文本标签

        if self.is_output or self.is_linked:
            # 这个text将自动赋给self.name

            # 重写用于展示的标签
            layout.label(text=text)
        else:
            layout.prop(self, "custom_info", text=text)
            # 1 --> 数据块
            # 2 --> identifier if property | 属性的id值
            # 3 --> 重载文本标签【可以不写，默认是属性的名称】

    # 组件颜色
    def draw_color(self, context, node):
        return (1.0, 0.8, 0.216, 0.5)
