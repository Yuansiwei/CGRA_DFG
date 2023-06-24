
### NOTE:第一步：创建节点树 ###


import bpy
from bpy.types import NodeTree

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
# 自定义节点编辑面板的信息
# 需要注册
class myCustomTree(NodeTree):
    """一个节点树类型，它将展示在编辑器类型列表中"""
    bl_idname = 'CustomTreeType'
    bl_label = "My NodeTree"
    bl_icon = 'RNA'





# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
# 定义节点时需要这个类
class MyCustomTreeNode:
    node_init_count: bpy.props.IntProperty(name='node_init_count',default=0)
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomTreeType'





import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
# 创建节点目录时需要这个类
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'CustomTreeType'
