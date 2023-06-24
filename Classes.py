import sys
import os
current_file_path=os.path.dirname(__file__)
sys.path.append(f"{current_file_path}/") 
sys.path.append(f"{current_file_path}/MyNodes/") 
sys.path.append(f"{current_file_path}/MySockets/") 

# 面板
from Button import *


''' 自定义节点面板 '''
# 节点树--节点组件--节点--节点目录
# from .myNodes import *
from MyCustomTree import *
from MyCustomSocket import Socket_classes
from MyCustomNodes import Node_classes
from GlobalValues import My_settings



    

classes = (
    My_settings,
    Test_OT_Hello, 
    OT_TestOpenFilebrowser,
    Test_PT_HelloPanel, 
    Test_OT_xml,
    xml_Panel,
    Test_OT_Location,
    Location_Panel,
    Test_OT_index_add,
    Test_PT_indexPanel,
    Test_OT_note,
    Test_OT_opcode,
    Test_OT_key_cal,
    Test_PT_batch_Panel,
    Test_PT_lsuPanel,
    myCustomTree,
)


### NOTE:创建节点目录 ###
node_categories = [
    # identifier, label, items list
    # -->标识符、标签(展示的名称)、项目列表

    MyNodeCategory('INPUT', "输入节点", items=[
        #NodeItem("TextNode"),
        #NodeItem("FileNode"),
        NodeItem("LOADNode"),
        NodeItem("AG_INNode"),
    ]),
    MyNodeCategory('OUTPUT', "输出节点", items=[
        #NodeItem("PrintNode"),
        NodeItem("SAVENode"),
        NodeItem("AG_OUTNode"),
    ]),
    MyNodeCategory('OTHERNODES', "运算节点", items=[
        NodeItem("PENode"),
        NodeItem("LOOPNode"),
        NodeItem("FIFONode"),
        
    ]),
    
]