'''

'''


import sys

import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class SAVENode(Node, MyCustomTreeNode):
    bl_idname = 'SAVENode'
    bl_label = "SAVE"
    bl_icon = 'ALIGN_LEFT'
    count=0

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(SAVENode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.15, 0.05, 0 )
        
    def out_update(self, context):
        self.self_update()
    # 自定义节点属性，可用于定义节点时传参
    
    opcode: bpy.props.EnumProperty(
        name='opcode',
        items=(
                ('mac', 'mac', 'mac'),
                ('add', 'add', 'add'),
                ('linear2D', 'linear2D', 'linear2D'),
                ('linear3D', 'linear3D', 'linear3D')),
        default='mac')
    index: bpy.props.IntProperty(name='ls index',default=0,update=out_update)
    note: bpy.props.StringProperty(name='note')
    inbuffer: bpy.props.StringProperty(name='inbuffer',default='0')
    reg0: bpy.props.StringProperty(name='reg0',default='null')
    reg1: bpy.props.StringProperty(name='reg1',default='null')
    

    def init(self, context):
        self.inputs.new('_Port', "in0")
        self.inputs.new('_Port', "in1")
        self.inputs.new('_Port', "in2")
        self.inputs.new('_Port', "in3")
        
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text='loop_level= '+str(self.loop_level))
        layout.label(text='delay_level= '+str(self.delay_level))
        layout.prop(self, "note")
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        layout.prop(self, "inbuffer")
        layout.prop(self, "reg0")
        layout.prop(self, "reg1")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "note")
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        layout.prop(self, "inbuffer")
        layout.prop(self, "reg0")
        layout.prop(self, "reg1")


    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        return "ls"+str(self.index)+'  '+note
    
    loop_level: bpy.props.IntProperty(name='loop_level',default=0)
    delay_level: bpy.props.IntProperty(name='delay_level',default=0)
    def update(self):
        for port in self.inputs:
            if(port.is_linked):
                return
        
        hash={}
        node_queue=Queue()
            
        node_queue.put(self)
        while not node_queue.empty():
            node_get=node_queue.get()
            node_get.self_update()
            if(len(node_get.outputs)>0):
                for output in node_get.outputs:
                    for item in output.links:
                        new_node=item.to_socket.node
                        if not(new_node in hash.keys()):
                            hash[new_node]=1
                        else:
                            hash[new_node]+=1
                        link_count=0;
                        for input in new_node.inputs:
                            if input.is_linked:
                                link_count+=1;
                        if hash[new_node]==link_count:
                            node_queue.put(new_node)
    def self_update(self):
        for port in self.inputs:
            port.belong_to_LOOP=True
        #循环层处理
        loop_level=0
        delay_level=0
        if self.inputs['in0'].is_linked:
            loop_level=max(loop_level,self.inputs['in0'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in0'].default_value.delay_level)
        if self.inputs['in1'].is_linked:
            loop_level=max(loop_level,self.inputs['in1'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in1'].default_value.delay_level)
        if self.inputs['in2'].is_linked:
            loop_level=max(loop_level,self.inputs['in2'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in2'].default_value.delay_level)
        if self.inputs['in3'].is_linked:
            loop_level=max(loop_level,self.inputs['in3'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in3'].default_value.delay_level)
        
        self.loop_level=loop_level
        self.delay_level=delay_level+1
        
    
    
    
    def print_xml(self,file):
        
        
        
        in0='<input type="null"/>'
        in1='<input type="null"/>'
        in2='<input type="null"/>'
        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        
        if self.inputs['in0'].is_linked:
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0=F'<input type="{type_change[in0_type]}" index="{in0_index}" port="0"/>'
        if self.inputs['in1'].is_linked:
            in1_type=self.inputs['in1']. default_value.type
            in1_index=self.inputs['in1']. default_value.index
            in1=F'<input type="{type_change[in1_type]}" index="{in1_index}" port="0"/>'
        if self.inputs['in2'].is_linked:
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2=F'<input type="{type_change[in2_type]}" index="{in2_index}" port="0"/>'
        if self.inputs['in3'].is_linked:
            in3_type=self.inputs['in3']. default_value.type
            in3_index=self.inputs['in3']. default_value.index
            in3=F'<input type="{type_change[in3_type]}" index="{in3_index}" port="0"/>'   
             
        buffer0_mode="buffer"
        if self.loop_level>self.inputs['in0']. default_value.loop_level:
            buffer0_mode="keep"
        buffer1_mode="buffer"
        if self.loop_level>self.inputs['in1']. default_value.loop_level or self.inbuffer!='null':
            buffer1_mode="keep"
        xml_str=F'''
<node type="ls" index="{self.index}" ls_mode="p2g" opcode="{self.opcode}" buffer0_mode="{buffer0_mode}" buffer1_mode="{buffer1_mode}">
    {in0}
    {in1}
    {in2}
    {in3}
    <inbuffer value="{self.inbuffer}"/>
    <localreg value0="{self.reg0}" value1="{self.reg1}"/>
    <placement cord="[6, 18]"/>
</node>
'''
        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        
        
    
