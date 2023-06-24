'''
in 字符串1 s=''
in 字符串2 s=''
inter 后缀 s=''
out 输出 s = 字符串1 + 字符串2 + 后缀
'''

# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 文本组合节点
# XXX Discription: 组合/生成字符串

import sys

import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *

class TextNode(Node, MyCustomTreeNode):
    bl_idname = 'TextNode'
    bl_label = "字符串"
    bl_icon = 'ALIGN_LEFT'

    def set_func(self,value):
        self['value'] = value
        self.update()

    def get_func(self):
        if 'value' in self.keys():
            return self['value']
        else:
            return ''

    # 自定义节点属性，可用于定义节点时传参
    my_string_prop: bpy.props.StringProperty(name='后缀', set=set_func, get=get_func)

    def init(self, context):
        self.inputs.new('_print_info', "字符串1")
        self.inputs.new('_print_info', "字符串2")
        self.inputs['字符串1'].default_value = ''
        self.inputs['字符串2'].default_value = ''

        self.outputs.new('NodeSocketString', "字符串输出")
        self.outputs['字符串输出'].default_value = ''
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.prop(self, "my_string_prop")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_string_prop")

    def draw_label(self):
        return self.bl_label

    def update(self):
        from_socket1 = self.inputs['字符串1'].default_value
        from_socket2 = self.inputs['字符串2'].default_value
        if self.inputs['字符串1'].is_linked:
            from_socket1 = str(self.inputs['字符串1'].links[0].from_socket.default_value)
        if self.inputs['字符串2'].is_linked:
            from_socket2 = str(self.inputs['字符串2'].links[0].from_socket.default_value)
        self.outputs['字符串输出'].default_value = from_socket1 + from_socket2 + self.my_string_prop
        # 将数据流传导下去
        for item in self.outputs[0].links:
            item.to_socket.node.update()
