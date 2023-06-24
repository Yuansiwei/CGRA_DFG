# 字符串组件

import bpy
from bpy.types import NodeSocket


class PortData(bpy.types.PropertyGroup):
    type: bpy.props.StringProperty(name='type',default='')
    index: bpy.props.IntProperty(name='index',default=-1)
    loop_level: bpy.props.IntProperty(name='loop_level',default=0)
    delay_level:bpy.props.IntProperty(name='delay_level',default=0)
    port:bpy.props.IntProperty(name='port',default=0)
    domain:bpy.props.IntProperty(name='domain',default=0)
    note:bpy.props.StringProperty(name='note',default='')      

class PortSocket(NodeSocket):
    # 组件ID
    bl_idname = '_Port'

    # 组件标签
    bl_label = "Port"

    # 组件描述
    description = "接口组件"

    # 组件形状：面板上的小圆点
    display_shape = 'CIRCLE'
    # [‘CIRCLE’, ‘SQUARE’, ‘DIAMOND’, ‘CIRCLE_DOT’, ‘SQUARE_DOT’, ‘DIAMOND_DOT’], default ‘CIRCLE’

    #value = PortData()
    type = 'OBJECT'
    # [‘CUSTOM’, ‘VALUE’, ‘INT’, ‘BOOLEAN’, ‘VECTOR’, ‘STRING’, ‘RGBA’, 
    # ‘SHADER’, ‘OBJECT’, ‘IMAGE’, ‘GEOMETRY’, ‘COLLECTION’], default ‘VALUE’

    # 当这个数据被写时【被连接】执行
    def set_func(this, value):
        this['value'] = value

    # 当这个数据被读取时【连接到】执行
    def get_func(this):
        try:
            return this['value']
        except:
            return ''
        
    default_value: bpy.props.PointerProperty(type=PortData)
    
    
    reg_val:bpy.props.StringProperty(name='reg_val',default='null')
    
    belong_to_LOOP:bpy.props.BoolProperty(name='belong_to_LOOP',default=False)
    
    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        if self.is_linked and self.default_value.type=="AG_IN":
            layout.label(text=f'{self.default_value.type}.{self.default_value.index}.{self.default_value.port}')
        elif self.is_linked:
            layout.label(text=f'{self.default_value.type}.{self.default_value.index}')
        elif self.belong_to_LOOP:
            layout.label(text=text)
        else:
            layout.prop(self, "reg_val", text=text)

    # 组件颜色
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 0.5)
class PortSocket_new(NodeSocket):
    # 组件ID
    bl_idname = '_Port_new'

    # 组件标签
    bl_label = "Port_new"

    # 组件描述
    description = "接口组件"

    # 组件形状：面板上的小圆点
    display_shape = 'CIRCLE'
    # [‘CIRCLE’, ‘SQUARE’, ‘DIAMOND’, ‘CIRCLE_DOT’, ‘SQUARE_DOT’, ‘DIAMOND_DOT’], default ‘CIRCLE’

    #value = PortData()
    type = 'OBJECT'
    # [‘CUSTOM’, ‘VALUE’, ‘INT’, ‘BOOLEAN’, ‘VECTOR’, ‘STRING’, ‘RGBA’, 
    # ‘SHADER’, ‘OBJECT’, ‘IMAGE’, ‘GEOMETRY’, ‘COLLECTION’], default ‘VALUE’

    # 当这个数据被写时【被连接】执行
    def set_func(this, value):
        this['value'] = value

    # 当这个数据被读取时【连接到】执行
    def get_func(this):
        try:
            return this['value']
        except:
            return ''
        
    default_value: bpy.props.PointerProperty(type=PortData)
    
    
    reg_val:bpy.props.StringProperty(name='reg_val',default='0')

    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        if self.is_linked and self.default_value.type=="AG_IN":
            layout.label(text=f'{self.default_value.type}.{self.default_value.index}.{self.default_value.port}')
        elif self.is_linked:
            layout.label(text=f'{self.default_value.type}.{self.default_value.index}')
        else:
            layout.prop(self, "reg_val", text=text)

    # 组件颜色
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 0.5)
            


class PortSocket_Out(NodeSocket):
    # 组件ID
    bl_idname = '_Port_Out'

    # 组件标签
    bl_label = "Port_Out"

    # 组件描述
    description = "接口组件"

    # 组件形状：面板上的小圆点
    display_shape = 'CIRCLE'
    # [‘CIRCLE’, ‘SQUARE’, ‘DIAMOND’, ‘CIRCLE_DOT’, ‘SQUARE_DOT’, ‘DIAMOND_DOT’], default ‘CIRCLE’

    #value = PortData()
    type = 'OBJECT'
    # [‘CUSTOM’, ‘VALUE’, ‘INT’, ‘BOOLEAN’, ‘VECTOR’, ‘STRING’, ‘RGBA’, 
    # ‘SHADER’, ‘OBJECT’, ‘IMAGE’, ‘GEOMETRY’, ‘COLLECTION’], default ‘VALUE’

    # 当这个数据被写时【被连接】执行
    def set_func(this, value):
        this['value'] = value

    # 当这个数据被读取时【连接到】执行
    def get_func(this):
        try:
            return this['value']
        except:
            return ''
        
    default_value: bpy.props.PointerProperty(type=PortData)
    

    

    # 用于绘制在节点框里显示的文本【可选】
    def draw(self, context, layout, node, text):
        layout.label(text=text)

    # 组件颜色
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 0.5)