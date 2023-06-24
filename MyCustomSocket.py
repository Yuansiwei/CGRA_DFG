# Created by Jiacong Zhao @CSDN-奇偕
# XXX The last modification at：2021.06.03
# 组件注册
import sys

# 功能：打印信息
from MySockets.print_info import *

# 功能：单选组件
from MySockets.enum_list import *

# 功能：字符串
from MySockets.text import *

# 功能：接口
from MySockets.CGRA_INTERFACE import *
Socket_classes = (
    Socket_Print_Info,
    Socket_Enum_List,
    Socket_Text,
    PortData,
    PortSocket,
    PortSocket_new,
    PortSocket_Out,
)
