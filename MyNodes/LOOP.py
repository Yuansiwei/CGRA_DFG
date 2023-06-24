'''

'''


import sys

import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class LOOPNode(Node, MyCustomTreeNode):
    bl_idname = 'LOOPNode'
    bl_label = "LOOP"
    bl_icon = 'ALIGN_LEFT'
    count=0

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(LOOPNode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.2, 0.2,0 )
        
            
                
    def out_update(self, context):
        self.self_update()
        for item in self.outputs[0].links:
            new_node=item.to_socket.node
            new_node.self_update() 
    # 自定义节点属性，可用于定义节点时传参
    
    opcode: bpy.props.EnumProperty(
        name='opcode',
        items=(
                ('lt', 'lt', 'lt'),
                ('gt', 'gt', 'gt'),
                ('lte', 'lte', 'lte'),
                ('gte', 'gte', 'gte')),
        default='lt')
    index: bpy.props.IntProperty(name='pe index',default=0,update=out_update)
    step: bpy.props.StringProperty(name='step',default='1')
    start: bpy.props.StringProperty(name='start',default='0')
    end: bpy.props.StringProperty(name='end',default='10')
    note: bpy.props.StringProperty(name='note')
    need_step:bpy.props.BoolProperty(name='need_step',default=False)
        

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
        is_refine=context.scene.my_prop.is_refine
        layout.label(text='loop_level= '+str(self.loop_level))
        layout.label(text='delay_level= '+str(self.delay_level))
        layout.prop(self, "note")
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        if not is_refine:
            layout.prop(self, "need_step")
        if (is_refine) or self.need_step==True :
            layout.prop(self, "step")
        if (is_refine) or self.need_step==False :    
            layout.prop(self, "start")
        layout.prop(self, "end")

    def draw_buttons_ext(self, context, layout):
        is_refine=context.scene.my_prop.is_refine
        layout.prop(self, "note")
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        if not is_refine:
            layout.prop(self, "need_step")
        if (is_refine) or self.need_step==True :
            layout.prop(self, "step")
        if (is_refine) or self.need_step==False :    
            layout.prop(self, "start")
        layout.prop(self, "end")


    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        return "pe"+str(self.index)+'  '+note
    
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
            if len(node_get.inputs)>0:
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
        if (not self.inputs['in0'].is_linked)and(not self.inputs['in1'].is_linked)and(not self.inputs['in2'].is_linked):  
            self.loop_level=0
            self.delay_level=0
        else:
            self.loop_level=loop_level+1
            self.delay_level=delay_level+1
        #输出 
        #self.outputs['out'].default_value.index= self.index
        #self.outputs['out'].default_value.type='pe'
        #self.outputs['out'].default_value.loop_level=self.loop_level
        for i in range(len(self.outputs['out'].links)):
            self.outputs['out'].links[i].to_socket.default_value.index=self.index
            self.outputs['out'].links[i].to_socket.default_value.type='LOOP'
            self.outputs['out'].links[i].to_socket.default_value.loop_level=self.loop_level
            self.outputs['out'].links[i].to_socket.default_value.delay_level=self.delay_level
            self.outputs['out'].links[i].to_socket.default_value.note=self.note
        
        
    
    
    
    def print_xml(self,file,is_refine):
        
        input_count=0;
        for input in self.inputs:
            input_count+=input.is_linked
        buffer0_from="null" 
        buffer1_from="null" 
        buffer2_from="null"
        in0='<input type="null"/>'
        in1='<input type="null"/>'
        in2='<input type="null"/>'
        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        if self.inputs['in0'].is_linked:
            buffer0_from="in0"
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0=F'<input type="{type_change[in0_type]}" index="{in0_index}" port="0"/>'
            if(in0_type=="AG_IN" ):
                in0_port=self.inputs['in0']. default_value.port
                in0=F'<input type="{type_change[in0_type]}" index="{in0_index+in0_port}" port="0"/>'
        if self.inputs['in1'].is_linked:
            buffer1_from="in1"
            in1_type=self.inputs['in1']. default_value.type
            in1_index=self.inputs['in1']. default_value.index
            in1=F'<input type="{type_change[in1_type]}" index="{in1_index}" port="0"/>'
            if(in1_type=="AG_IN" ):
                in1_port=self.inputs['in1']. default_value.port
                in1=F'<input type="{type_change[in1_type]}" index="{in1_index+in1_port}" port="0"/>'
        if self.inputs['in2'].is_linked:
            buffer2_from="in2"
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2=F'<input type="{type_change[in2_type]}" index="{in2_index}" port="0"/>'
            if(in2_type=="AG_IN" ):
                in2_port=self.inputs['in2']. default_value.port
                in2=F'<input type="{type_change[in2_type]}" index="{in2_index+in2_port}" port="0"/>'
            
        loop_control="loop"    
        if input_count==0 and is_refine==0:
            loop_control="outermost_loop"
        elif self.need_step==False:
            loop_control='inner_loop'
        elif self.need_step==True:
            loop_control='inner_loop_ini'
                
        if is_refine:
            xml_str=F'''
<node type="pe" index="{self.index}" domain="0" opcode="{self.opcode}" is_float="false" loop_control="loop" branch_control="null" self_loop="true" key_cal="false">
    <inner_connection
    buffer0_constant="true" buffer1_constant="true" buffer2_constant="true"
    buffer0_from="{buffer0_from}" buffer1_from="{buffer1_from}" buffer2_from="{buffer2_from}"
    pick_initial="false" />
    {in0}
    {in1}
    {in2}
    <inbuffer value0="{self.step}" value1="{self.start}" value2="{self.end}"/>
    <outbuffer value="{self.loop_level}"/>
    <placement cord="[1, 3]"/>
</node>
'''
        else:
            reg0='null'
            if self.need_step==True:
                reg0=self.step
            else:
                reg0=self.start
                
            xml_str=F'''
<node type="pe" index="{self.index}" opcode="{self.opcode}" loop_control="{loop_control}" branch_control="null"  >
    <inner_connection
    buffer0_mode="keep" buffer1_mode="buffer" buffer2_mode="keep"
    buffer0_from="{buffer0_from}" buffer1_from="aluin1" buffer2_from="{buffer2_from}"
    input_buffer_bypass="inbuffer" output_buffer_bypass="outbuffer"/>
    {in0}
    {in1}
    {in2}
    <reg value="{reg0}"/>
    <reg value="null"/>
    <reg value="{self.end}"/>
    <placement cord="[1, 3]"/>
</node>
'''
        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        
        
    
