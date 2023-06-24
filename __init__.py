# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "CGRA_DFG",
    "author" : "Yuan siwei",
    "description" : "CGRA配置可视化",
    "blender" : (2, 93, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
import sys
import os
current_file_path=os.path.dirname(__file__)
sys.path.append(f"{current_file_path}/") 
sys.path.append(f"{current_file_path}/MyNodes/") 
sys.path.append(f"{current_file_path}/MySockets/") 
from Classes import *

# 类的注册【方法一】
# register, unregister = bpy.utils.register_classes_factory(classes)

# 类的注册【方法二】
def register():
    from bpy.utils import register_class

    # 注册
    for cls in classes:
        register_class(cls)
    
    # 组件注册
    for cls in Socket_classes:
        register_class(cls)

    # 节点注册
    for cls in Node_classes:
        register_class(cls)

    # 节点目录注册
    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)
    bpy.types.Scene.my_prop = bpy.props.PointerProperty(type=My_settings)


def unregister():
    del bpy.types.Scene.my_prop 
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    # 节点
    for cls in reversed(Node_classes):
        unregister_class(cls)

    # 组件
    for cls in reversed(Socket_classes):
        unregister_class(cls)

    # 
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
