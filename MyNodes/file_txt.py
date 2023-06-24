'''
in FilePath s=''
out output s
'''

# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 文本文件节点
# XXX Discription: 打开文本文件并输出
import sys
 
import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *

class FileNode(Node, MyCustomTreeNode):
    bl_idname = 'FileNode'
    bl_label = "本地文件"
    bl_icon = 'FILE_BLANK'

    def set_func(self,value):
        self['value'] = value
        self.update()

    def get_func(self):
        if 'value' in self.keys():
            return self['value']
        else:
            return ''

    encode_items = (
        ('utf-8', "utf-8", ""),
        ('utf-16', "utf-16", ""),
        ('gbk', "gbk", ""),
        ('gbk18030', "gbk18030", ""),
        ('ansi', "ansi", ""),
        ('latin-1', "latin-1", ""),
    )
    encoding: bpy.props.EnumProperty(
        name = 'encoding',
        description = '以何种编码方式打开文件',
        items = encode_items,
        default = 'utf-8',
    )

    def init(self, context):
        self.inputs.new('_print_info', "FilePath")
        self.inputs['FilePath'].default_value = ''

        self.outputs.new('NodeSocketString', "output")
        self.outputs['output'].default_value = ''
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.label(text = 'FilePath')
            layout.prop(self, "encoding")
        else:
            layout.prop(self, "encoding")

    def draw_buttons_ext(self, context, layout):
        ...

    def draw_label(self):
        return "File Str"

    def update(self):
        if self.outputs[0].is_linked:
            fp = self.inputs[0].default_value
            if self.inputs[0].is_linked:
                fp = str(self.inputs[0].links[0].from_socket.default_value)
            with open(fp, 'r', encoding=self.encoding) as f:
                self.outputs[0].default_value = str(f.read())
            # 将数据流传导下去
            for item in self.outputs[0].links:
                item.to_socket.node.update()
