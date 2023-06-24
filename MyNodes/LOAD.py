'''

'''


import sys

import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class LOADNode(Node, MyCustomTreeNode):
    bl_idname = 'LOADNode'
    bl_label = "LOAD"
    bl_icon = 'ALIGN_LEFT'
    count=0

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(LOADNode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.075, 0.16, 0 )
        
        

    def out_update(self, context):
        self.self_update()
        for item in self.outputs[0].links:
            new_node=item.to_socket.node
            new_node.self_update() 
            
        
    
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
    
    inbuffer: bpy.props.StringProperty(name='inbuffer',default='0')
    reg0: bpy.props.StringProperty(name='reg0',default='null')
    reg1: bpy.props.StringProperty(name='reg1',default='null')
    note: bpy.props.StringProperty(name='note')
    is_padding:bpy.props.BoolProperty(name='is_padding',default=False)
    in0LU:bpy.props.StringProperty(name='in0LU',default='null null')
    in1LU:bpy.props.StringProperty(name='in1LU',default='null null')
    in2LU:bpy.props.StringProperty(name='in2LU',default='null null')

    def init(self, context):
        self.inputs.new('_Port', "in0")
        self.inputs.new('_Port', "in1")
        self.inputs.new('_Port', "in2")
        self.outputs.new('_Port_Out', "out")
        

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
        layout.prop(self, "is_padding")
        if(self.is_padding== True):
            layout.prop(self, "in0LU")
            layout.prop(self, "in1LU")
            layout.prop(self, "in2LU")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "note")
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        layout.prop(self, "inbuffer")
        layout.prop(self, "reg0")
        layout.prop(self, "reg1")
        layout.prop(self, "is_padding")
        if(self.is_padding== True):
            layout.prop(self, "in0LU")
            layout.prop(self, "in1LU")
            layout.prop(self, "in2LU")


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
            self.inbuffer="null"
        if self.inputs['in2'].is_linked:
            loop_level=max(loop_level,self.inputs['in2'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in2'].default_value.delay_level)
        
        self.loop_level=loop_level
        self.delay_level=delay_level+1
        #输出
        for i in range(len(self.outputs['out'].links)):
            self.outputs['out'].links[i].to_socket.default_value.index=self.index
            self.outputs['out'].links[i].to_socket.default_value.type='LOAD'
            self.outputs['out'].links[i].to_socket.default_value.loop_level=self.loop_level
            self.outputs['out'].links[i].to_socket.default_value.delay_level=self.delay_level
            self.outputs['out'].links[i].to_socket.default_value.note=self.note
        #self.outputs['out'].default_value.index= self.index
        #self.outputs['out'].default_value.type='ls'
        #self.outputs['out'].default_value.loop_level=self.loop_level
        
        
    
    
    
    def print_xml(self,file):
        
        
        
        in0='<input type="null"/>'
        in1='<input type="null"/>'
        in2='<input type="null"/>'
        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        if self.inputs['in0'].is_linked:
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0=F'<input type="{ type_change[in0_type]}" index="{in0_index}" port="0"/>'
        if self.inputs['in1'].is_linked:
            in1_type=self.inputs['in1']. default_value.type
            in1_index=self.inputs['in1']. default_value.index
            in1=F'<input type="{ type_change[in1_type]}" index="{in1_index}" port="0"/>'
        if self.inputs['in2'].is_linked:
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2=F'<input type="{ type_change[in2_type]}" index="{in2_index}" port="0"/>'
        
        buffer0_mode="buffer"
        if self.loop_level>self.inputs['in0']. default_value.loop_level:
            buffer0_mode="keep"
        buffer1_mode="buffer"
        if self.loop_level>self.inputs['in1']. default_value.loop_level or self.inbuffer!='null':
            buffer1_mode="keep"
            
            
        in0LU_lu=self.in0LU.split()
        in1LU_lu=self.in1LU.split()
        in2LU_lu=self.in2LU.split()
        in0LU_l='null'
        in0LU_u='null'
        in1LU_l='null'
        in1LU_u='null'
        in2LU_l='null'
        in2LU_u='null'
        
        if(len(in0LU_lu))==2:
            in0LU_l,in0LU_u=in0LU_lu
        if(len(in1LU_lu))==2:
            in1LU_l,in1LU_u=in1LU_lu
        if(len(in2LU_lu))==2:
            in2LU_l,in2LU_u=in2LU_lu
        
        padding_str=''
        if(self.is_padding):
            padding_str=F''' 
    <padding in0L="{in0LU_l}" in0U="{in0LU_u}" in1L="{in1LU_l}" in1U="{in1LU_u}" in2L="{in2LU_l}" in2U="{in2LU_u}"/>'''   
        xml_str=F'''
<node type="ls" index="{self.index}" ls_mode="g2p" opcode="{self.opcode}" buffer0_mode="{buffer0_mode}" buffer1_mode="{buffer1_mode}">
    {in0}
    {in1}
    {in2}
    <input type="null"/>
    <inbuffer value="{self.inbuffer}"/>
    <localreg value0="{self.reg0}" value1="{self.reg1}"/>{padding_str}
    <placement cord="[6, 18]"/>
</node>
'''
        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        
        
    
