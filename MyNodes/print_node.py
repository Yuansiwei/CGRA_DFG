'''
in info s
'''

# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.04
# XXX Topic: 打印节点
# XXX Discription: 将得到的任何数据转为字符串并打印，实时刷新
import sys

import time
import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *

class PrintNode(Node, MyCustomTreeNode):
    bl_idname = 'PrintNode'
    bl_label = "打印"
    bl_icon = 'CONSOLE'

    def init(self, context):
        self.inputs.new('NodeSocketString', "info")
    
    def parent_socket(self):
        return self.inputs[0].links[0].from_socket

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.label(text=str(self.parent_socket().default_value))
        else:
            layout.label(text='')

    def draw_buttons_ext(self, context, layout):
        ...

    def draw_label(self):
        return "打印"

    # 拓扑图更新时调用
    def update(self):
        print(time.ctime(),end='>>> ')
        print(str(self.parent_socket().default_value))

    # 复制时调用
    def copy(self, node):
        print("Copying from node ", node)

    # 释放时调用
    def free(self):
        print("Removing node ", self, ", Goodbye!")
