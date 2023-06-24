'''

'''


import sys

import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class PENode(Node, MyCustomTreeNode):
    bl_idname = 'PENode'
    bl_label = "PE"
    bl_icon = 'ALIGN_LEFT'
    

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(PENode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.1, 0.2,0.25 )
        
                
                    
                    
            
                
    
    def out_update(self, context):
        self.self_update()
        for item in self.outputs[0].links:
            new_node=item.to_socket.node
            new_node.self_update() 
        
        
    # 自定义节点属性，可用于定义节点时传参        
    opcode: bpy.props.StringProperty(name='opcode')
    note: bpy.props.StringProperty(name='note')
    index: bpy.props.IntProperty(name='pe index',default=0,update=out_update)
    reg0: bpy.props.StringProperty(name='reg0',default='null')
    reg1: bpy.props.StringProperty(name='reg1',default='null')
    reg2: bpy.props.StringProperty(name='reg2',default='null')
    
    self_loop:bpy.props.BoolProperty(name='self_loop', default=False)
    is_float:bpy.props.BoolProperty(name='is_float', default=False)
    
    key_cal:bpy.props.BoolProperty(name='key_cal', default=False)
    
    
    branch:bpy.props.EnumProperty(
        name='branch',
        items=(
                ('null', 'null', 'null'),
                ('cb', 'cb', 'cb'),
                ('cinvb', 'cinvb', 'cinvb'),
                ('merge', 'merge', 'merge')),
        default='null')
    
    loop:bpy.props.EnumProperty(
        name='loop',
        items=(
                ('null', 'null', 'null'),
                ('loop', 'loop', 'loop'),
                ('transin', 'transin', 'transin'),
                ('last_match0', 'last_match0', 'last_match0'),
                ('last_match1', 'last_match1', 'last_match1'),
                ('break_gen', 'break_gen', 'break_gen'),
                ('break_pre', 'break_pre', 'break_pre'),
                ('break_post', 'break_post', 'break_post'),
                ('systolic', 'systolic', 'systolic'),
                ('continue_', 'continue_', 'continue_'),
                ('sync_loop', 'sync_loop', 'sync_loop'),
                ('transout', 'transout', 'transout')),
        
        default='null')

    has_moved_reg:bpy.props.BoolProperty(name='has_moved_reg', default=False)
    
    
    partition_times:bpy.props.IntProperty(name='partition_times',default=0)
    def init(self, context):
        self.inputs.new('_Port', "in0")
        self.inputs.new('_Port', "in1")
        self.inputs.new('_Port', "in2")
        #self.inputs['in0'].default_value = PortData()
        #self.inputs['in1'].default_value = PortData()
        #self.inputs['in2'].default_value = PortData()

        self.outputs.new('_Port_Out', "out")
        #self.outputs['out'].default_value = PortData()
        

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
        
        layout.prop(self, "branch")
        layout.prop(self, "loop")
        layout.prop(self, "self_loop")
        layout.prop(self, "is_float")
        layout.prop(self, "key_cal")
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "opcode")
        layout.prop(self, "index")
        layout.prop(self, "note")
        
        layout.prop(self, "branch")
        layout.prop(self, "loop")
        layout.prop(self, "self_loop")
        layout.prop(self, "is_float")
        layout.prop(self, "key_cal")
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")


    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        return "pe"+str(self.index)+'  '+self.opcode+'  '+note
    
    
            
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
        if not self.has_moved_reg and len(self.inputs)>=3:
            
            self.inputs[0].reg_val=self.reg0
            self.inputs[1].reg_val=self.reg1
            self.inputs[2].reg_val=self.reg2
            self.has_moved_reg=True
        
            
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
            
            
        self.loop_level=loop_level
        self.delay_level=delay_level+1
        if self.loop=="last_match0" or self.loop=="last_match1":
            self.loop_level=self.loop_level-1
        elif self.loop=="transout" and self.inputs['in2'].is_linked:
            self.loop_level=self.inputs['in2'].default_value.loop_level
        #self.outputs['out'].default_value.index= self.index
        #self.outputs['out'].default_value.type='pe'
        #self.outputs['out'].default_value.loop_level=self.loop_level
        domain=0
        for input in self.inputs:
            domain=max(input.default_value.domain,domain)
           
        for i in range(len(self.outputs['out'].links)):
            self.outputs['out'].links[i].to_socket.default_value.index=self.index
            self.outputs['out'].links[i].to_socket.default_value.type='PE'
            self.outputs['out'].links[i].to_socket.default_value.loop_level=self.loop_level
            self.outputs['out'].links[i].to_socket.default_value.delay_level=self.delay_level
            self.outputs['out'].links[i].to_socket.default_value.domain=domain
            self.outputs['out'].links[i].to_socket.default_value.note=self.note
        
        
        
    
    
    
    def print_xml(self,file,is_refine):
        self.reg0=self.inputs[0].reg_val
        self.reg1=self.inputs[1].reg_val
        self.reg2=self.inputs[2].reg_val
        
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
            in1_port=self.inputs['in1']. default_value.port
            in1=F'<input type="{type_change[in1_type]}" index="{in1_index}" port="0"/>'
            if(in1_type=="AG_IN" ):
                in1=F'<input type="{type_change[in1_type]}" index="{in1_index+in1_port}" port="0"/>'
        if self.inputs['in2'].is_linked:
            buffer2_from="in2"
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2_port=self.inputs['in2']. default_value.port
            in2=F'<input type="{type_change[in2_type]}" index="{in2_index}" port="0"/>'
           
            if(in2_type=="AG_IN"):
                #print(in2_index)
                in2=F'<input type="{type_change[in2_type]}" index="{in2_index+in2_port}" port="0"/>'
        
        is_float="false"
        if(self.is_float==True):
            is_float="true"
            
        self_loop="false"
        if(self.self_loop==True):
            self_loop="true"
            buffer1_from="in1"
        if(self.self_loop==True and is_refine==0):
            buffer1_from="aluin1"
                
            
            
        key_cal="false"
        if(self.key_cal==True):
            key_cal="true"
        
        loop_control=self.loop
        
        
        branch_control=self.branch
        
        buffer0_constant="true"
        buffer0_mode="keep"
        if (not self.inputs['in0'].is_linked) and self.inputs['in0'].reg_val=="null":
            buffer0_constant="false"
            buffer0_mode="buffer"
        elif self.inputs['in0'].is_linked and (self.loop=="last_match0" or self.loop=="last_match1")and self.loop_level+1==self.inputs['in0']. default_value.loop_level:
            buffer0_constant="false"
            buffer0_mode="buffer"
        elif self.inputs['in0'].is_linked and self.loop=="transout"  :
            if self.loop_level<self.inputs['in0']. default_value.loop_level:
                buffer0_constant="false"
                buffer0_mode="buffer"
            else:
                buffer0_constant="true"
                buffer0_mode="keep"
        elif self.inputs['in0'].is_linked and self.loop_level==self.inputs['in0']. default_value.loop_level:
            buffer0_constant="false"
            buffer0_mode="buffer"
        
            
        buffer1_constant="true"
        buffer1_mode="keep"
        if (not self.inputs['in1'].is_linked) and self.inputs['in1'].reg_val=="null":
            buffer1_constant="false"
            buffer1_mode="buffer"
        elif self.inputs['in1'].is_linked and (self.loop=="last_match0" or self.loop=="last_match1")and self.loop_level+1==self.inputs['in1']. default_value.loop_level:
            buffer1_constant="false"
            buffer1_mode="buffer"
        elif self.inputs['in1'].is_linked and self.loop=="transout" :
            if  self.loop_level<self.inputs['in1']. default_value.loop_level:
                  buffer1_constant="false"
                  buffer1_mode="buffer"
            else:
                  buffer1_constant="true"
                  buffer1_mode="keep"
        elif self.inputs['in1'].is_linked and self.loop_level==self.inputs['in1']. default_value.loop_level:
            buffer1_constant="false"
            buffer1_mode="buffer"
        
            
        if(buffer1_from=="aluin1"):
            buffer1_mode="buffer"
            
            
        buffer2_constant="true"
        buffer2_mode="keep"
        if (not self.inputs['in2'].is_linked) and self.inputs['in2'].reg_val=="null":
            buffer2_constant="false"
            buffer2_mode="buffer"
        elif self.inputs['in2'].is_linked and (self.loop=="last_match0" or self.loop=="last_match1")and self.loop_level+1==self.inputs['in2']. default_value.loop_level:
            buffer2_constant="false"
            buffer2_mode="buffer"
        elif self.inputs['in2'].is_linked and self.loop=="transout":
            if self.loop_level<self.inputs['in2']. default_value.loop_level:
                buffer2_constant="false"
                buffer2_mode="buffer"
            else:
                buffer2_constant="true"
                buffer2_mode="keep"
        elif self.inputs['in2'].is_linked and self.loop_level==self.inputs['in2']. default_value.loop_level:
            buffer2_constant="false"
            buffer2_mode="buffer"
            
        reg0_xml=self.inputs[0].reg_val
        reg1_xml=self.inputs[1].reg_val
        reg2_xml=self.inputs[2].reg_val
        if(self.inputs[0].is_linked):
            reg0_xml='null'
        if(self.inputs[1].is_linked):
            reg1_xml='null'
        if(self.inputs[2].is_linked):
            reg2_xml='null'
        if loop_control=="systolic":
            reg2_xml="0"
        if is_refine:
            outbuffer="null"
            if loop_control=="last_match0" or loop_control=="last_match1":
                
                outbuffer=self.loop_level+1
            elif loop_control=="transout" and self.inputs['in2'].is_linked:
                outbuffer=self.inputs['in2']. default_value.loop_level+1
            domain=0
            for input in self.inputs:
                domain=max(input.default_value.domain,domain)
            partition_times=str(self.partition_times)
            if self.partition_times==1:
                partition_times+='st'
            elif self.partition_times==2:
                partition_times+='nd'
            elif self.partition_times==3:
                partition_times+='rd'
            else:
                partition_times+='th'
            partition_times=F'''partition_times="{partition_times}"'''
            if(domain!=2):
                partition_times=""
            xml_str=F'''
<node type="pe" index="{self.index}" domain="{domain}" opcode="{self.opcode}" is_float="{is_float}" loop_control="{loop_control}" branch_control="{branch_control}" self_loop="{self_loop}" key_cal="{key_cal}" {partition_times} >
    <inner_connection
    buffer0_constant="{buffer0_constant}" buffer1_constant="{buffer1_constant}" buffer2_constant="{buffer2_constant}"
    buffer0_from="{buffer0_from}" buffer1_from="{buffer1_from}" buffer2_from="{buffer2_from}"
    pick_initial="false"/>
    {in0}
    {in1}
    {in2}
    <inbuffer value0="{reg0_xml}" value1="{reg1_xml}" value2="{reg2_xml}"/>
    <outbuffer value="{outbuffer}"/>
    <placement cord="[0, 0]"/>
</node>
'''
        else:
            alu_precision='int32'
            if self.is_float:
                alu_precision='FP32'
            if loop_control=="last_match0" or loop_control=="last_match1":
                buffer2_mode="buffer"
            if loop_control=="transin":
                loop_control="trans"
            xml_str=F'''
<node type="pe" index="{self.index}" opcode="{self.opcode}" alu_precision="{alu_precision}" loop_control="{loop_control}" branch_control="{branch_control}"  key_cal="{key_cal}">
    <inner_connection
    buffer0_mode="{buffer0_mode}" buffer1_mode="{buffer1_mode}" buffer2_mode="{buffer2_mode}"
    buffer0_from="{buffer0_from}" buffer1_from="{buffer1_from}" buffer2_from="{buffer2_from}"
    input_buffer_bypass="inbuffer" output_buffer_bypass="outbuffer"/>
    {in0}
    {in1}
    {in2}
    <reg value="{reg0_xml}"/>
    <reg value="{reg1_xml}"/>
    <reg value="{reg2_xml}"/>
    <placement cord="[0, 0]"/>
</node>
'''

        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        
