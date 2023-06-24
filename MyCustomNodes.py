# 需要注册的节点
import sys

from MyNodes.print_node import *
from MyNodes.connect_text import *
from MyNodes.file_txt import *
from MyNodes.PE import*
from MyNodes.LOOP import*
from MyNodes.LOAD import*
from MyNodes.SAVE import*
from MyNodes.FIFO import*
from MyNodes.AG import*
Node_classes = (
    TextNode,
    PrintNode,
    FileNode,
    PENode,
    LOOPNode,
    LOADNode,
    SAVENode,
    FIFONode,
    AG_INNode,
    AG_OUTNode
)