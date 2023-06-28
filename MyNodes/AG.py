'''

'''


import sys
import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class AG_INNode(Node, MyCustomTreeNode):
    bl_idname = 'AG_INNode'
    bl_label = "AG_IN"
    bl_icon = 'ALIGN_LEFT'
    count=0

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(AG_INNode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.075, 0.16, 0 )
        
        

    def out_update(self, context):
        self.self_update()
        for output in self.outputs:
            for item in output.links:
                new_node=item.to_socket.node
                new_node.self_update() 
            
        
    def times_update(self, context):
        if(self.times>len(self.outputs)):
            start=len(self.outputs)
            for i in range(self.times-len(self.outputs)):
                self.outputs.new('_Port_Out', "out"+str(start))    
                start+=1
        elif  self.times<len(self.outputs):
            start=self.times 
            for i in range(len(self.outputs)-self.times):
                self.outputs.remove(self.outputs["out"+str(start)])    
                start+=1   
    # 自定义节点属性，可用于定义节点时传参
    
    
    index: bpy.props.IntProperty(name='ag index',default=0,update=out_update,min=0,max=7)
    
    
    reg0: bpy.props.StringProperty(name='reg0',default='null')
    reg1: bpy.props.StringProperty(name='reg1',default='null')
    reg2: bpy.props.StringProperty(name='reg2',default='null')
    note: bpy.props.StringProperty(name='note')
    is_padding:bpy.props.BoolProperty(name='is_padding',default=False)
    in0LU:bpy.props.StringProperty(name='in0LU',default='null null')
    in1LU:bpy.props.StringProperty(name='in1LU',default='null null')
    in2LU:bpy.props.StringProperty(name='in2LU',default='null null')
    priority:bpy.props.IntProperty(name='priority',default=0)
    direction:bpy.props.EnumProperty(
        name='direction',
        items=(
                ('row', 'row', 'row'),
                ('col', 'col', 'col'),
                ('channel', 'channel', 'channel')),
        default='row')
    stride:bpy.props.IntProperty(name='stride',default=1)
    stride_str:bpy.props.StringProperty(name='stride_str',default='1')
    times:bpy.props.IntProperty(name='times',default=1,min=1,max=16,update=times_update)
    catalogue:bpy.props.EnumProperty(
        name='catalogue',
        items=(
                ('a', 'a', 'a'),
                ('b', 'b', 'b')),
        default='a')
    branch:bpy.props.StringProperty(name='branch',default='null null null')
    
    
    ##############spm   attributions
    show_spm:bpy.props.BoolProperty(name='show_spm',default=False)
    ddr_addr:bpy.props.StringProperty(name='ddr_addr',default='0')
    #local_addr:bpy.props.StringProperty(name='local_addr',default='0')
    size_data:bpy.props.StringProperty(name='size_data',default='64')
    stride_lsu:bpy.props.StringProperty(name='stride_lsu',default='0')
    cnt_lsu:bpy.props.StringProperty(name='cnt_lsu',default='1')
    bank_sram:bpy.props.EnumProperty(name='bank_sram',items=(
                ('16', '16', '16'),
                ('32', '32', '32')),
        default='32')
    is_spm:bpy.props.EnumProperty(name='is_spm',items=(
                ('true', 'true', 'true'),
                ('false', 'false', 'false')),
        default='true')
    
    pattern:bpy.props.EnumProperty(name='pattern',items=(
                ('0', '0', '0'),
                ('1', '1', '1'),
                ('2', '2', '2'),
                ('3', '3', '3'),
                ('4', '4', '4'),
                ('5', '5', '5')),
        default='5')
    pow2_mode:bpy.props.EnumProperty(name='pow2_mode',items=(
                ('true', 'true', 'true'),
                ('false', 'false', 'false')),
        default='false')
    row_local:bpy.props.StringProperty(name='row_local',default='0')
    col_local:bpy.props.StringProperty(name='col_local',default='0')
    bank_num:bpy.props.EnumProperty(name='bank_num',items=(
                ('4', '4', '4'),
                ('8', '8', '8'),
                ('16', '16', '16'),
                ('32', '32', '32'),),
        default='16')
    multi_in0:bpy.props.StringProperty(name='multi_in0',default='1')
    multi_in1:bpy.props.StringProperty(name='multi_in1',default='1')
    
    has_moved_reg:bpy.props.BoolProperty(name='has_moved_reg', default=False)
    ########################################################################
    
    max_loop_level:bpy.props.IntProperty(name='max_loop_level',default=0)
    
    ######################################################################
    placement: bpy.props.StringProperty(name='placement',default='null')
    fifo_placement:bpy.props.StringProperty(name='fifo_placement',default='')
    
    rdfifo_start:bpy.props.IntProperty(name='rdfifo_start',default=0)
    def init(self, context):
        self.inputs.new('_Port', "in0")
        self.inputs.new('_Port', "in1")
        self.inputs.new('_Port', "in2")
        
        self.outputs.new('_Port_Out', "out"+"0")
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text='loop_level= '+str(self.loop_level))
        layout.label(text='delay_level= '+str(self.delay_level))
        layout.prop(self, "note")
        layout.prop(self, "index")
        
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")
        
        layout.prop(self,"priority")
        layout.prop(self,"times")
        layout.prop(self,"stride_str")
        layout.prop(self,"catalogue")
        layout.prop(self,"direction")
        layout.prop(self, "is_padding")
        
        if(self.is_padding== True):
            layout.prop(self, "in0LU")
            layout.prop(self, "in1LU")
            layout.prop(self, "in2LU")
        layout.prop(self, "branch")
        
        
        layout.prop(self, "show_spm")
        if(self.show_spm== True):
            layout.prop(self, "ddr_addr")
            layout.prop(self, "size_data")
            layout.prop(self, "stride_lsu")
            layout.prop(self, "cnt_lsu")
            #layout.prop(self, "bank_sram")
            layout.prop(self, "is_spm")
            
            layout.prop(self, "pattern")
            layout.prop(self, "pow2_mode")
            layout.prop(self, "row_local")
            layout.prop(self, "col_local")
            layout.prop(self, "bank_num")
            layout.prop(self, "multi_in0")
            layout.prop(self, "multi_in1")
        layout.prop(self, "placement")
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "note")
        layout.prop(self, "index")
        
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")
        layout.prop(self,"priority")
        layout.prop(self,"times")
        layout.prop(self,"stride_str")
        layout.prop(self,"catalogue")
        layout.prop(self,"direction")
        layout.prop(self, "is_padding")
        if(self.is_padding== True):
            layout.prop(self, "in0LU")
            layout.prop(self, "in1LU")
            layout.prop(self, "in2LU")
        layout.prop(self, "branch")
        
        layout.prop(self, "show_spm")
        if(self.show_spm== True):
            layout.prop(self, "ddr_addr")
            layout.prop(self, "size_data")
            layout.prop(self, "stride_lsu")
            layout.prop(self, "cnt_lsu")
            #layout.prop(self, "bank_sram")
            layout.prop(self, "is_spm")
            
            layout.prop(self, "pattern")
            layout.prop(self, "pow2_mode")
            layout.prop(self, "row_local")
            layout.prop(self, "col_local")
            layout.prop(self, "bank_num")
            layout.prop(self, "multi_in0")
            layout.prop(self, "multi_in1")
        layout.prop(self, "placement")

    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        if self.placement!="null":
            return "ag"+str(self.index)+'  '+note+' '+F'[{self.placement}]'
        return "ag"+str(self.index)+'  '+note
    
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
                        if hash[new_node]==len(new_node.inputs):
                            node_queue.put(new_node)
    def self_update(self):
        if not self.has_moved_reg:
            
            self.inputs[0].reg_val=self.reg0
            self.inputs[1].reg_val=self.reg1
            self.inputs[2].reg_val=self.reg2
            self.has_moved_reg=True
        
        #循环层处理
        loop_level=0
        delay_level=0
        for input in self.inputs:
            if input.is_linked:
                loop_level=max(loop_level,input.default_value.loop_level)
                delay_level=max(delay_level,input.default_value.delay_level)
        
        self.loop_level=loop_level
        self.delay_level=delay_level+1
        #输出
        output_index=0
        out_count=0;
        for output in self.outputs:
            for i in range(len(output.links)):
                output.links[i].to_socket.default_value.index=self.index
                output.links[i].to_socket.default_value.type='AG_IN'
                output.links[i].to_socket.default_value.loop_level=self.loop_level
                output.links[i].to_socket.default_value.delay_level=self.delay_level
                output.links[i].to_socket.default_value.port=output_index
                output.links[i].to_socket.default_value.domain=2
                output.links[i].to_socket.default_value.note=self.note
            output_index+=1
        #self.outputs['out'].default_value.index= self.index
        #self.outputs['out'].default_value.type='ls'
        #self.outputs['out'].default_value.loop_level=self.loop_level
        
        
    
    
    
    def print_xml(self,file):
        self.reg0=self.inputs[0].reg_val
        self.reg1=self.inputs[1].reg_val
        self.reg2=self.inputs[2].reg_val
        
        
        in0='<input type="null"/>'
        in1='<input type="null"/>'
        in2='<input type="null"/>'
        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        if self.inputs['in0'].is_linked:
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0_port=self.inputs['in0'].default_value.port
            if(in0_type=="AG_IN" ):
                rdfifo_start=self.inputs['in0'].links[0].from_socket.node.rdfifo_start
                in0=F'''<input type="{type_change[in0_type]}" index="{rdfifo_start+in0_port}" port="{self.inputs['in0'].rdfifo_port}"/>'''
            else:
                in0=F''' <input type="{type_change[in0_type]}" index="{in0_index}" port="0"/>'''
            
        if self.inputs['in1'].is_linked:
            in1_type=self.inputs['in1']. default_value.type
            in1_index=self.inputs['in1']. default_value.index
            in1_port=self.inputs['in1'].default_value.port
            if(in1_type=="AG_IN" ):
                rdfifo_start=self.inputs['in1'].links[0].from_socket.node.rdfifo_start
                in1=F'''<input type="{type_change[in1_type]}" index="{rdfifo_start+in1_port}" port="{self.inputs['in1'].rdfifo_port}"/>'''
            else:
                in1=F'''<input type="{type_change[in1_type]}" index="{in1_index}" port="0"/>'''
        if self.inputs['in2'].is_linked:
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2_port=self.inputs['in2'].default_value.port
            if(in2_type=="AG_IN" ):
                rdfifo_start=self.inputs['in2'].links[0].from_socket.node.rdfifo_start
                in2=F'''<input type="{type_change[in2_type]}" index="{rdfifo_start+in2_port}" port="{self.inputs['in2'].rdfifo_port}"/>'''
            else:
                in2=F'''<input type="{type_change[in2_type]}" index="{in2_index}" port="0"/>'''
        
        buffer0_constant="false"
        if self.loop_level>self.inputs['in0']. default_value.loop_level or (self.inputs['in0'].is_linked==False ):
            buffer0_constant="true"
        buffer1_constant="false"
        if self.loop_level>self.inputs['in1']. default_value.loop_level or(self.inputs['in1'].is_linked==False ):
            buffer1_constant="true"
        buffer2_constant="false"
        if self.loop_level>self.inputs['in2']. default_value.loop_level or (self.inputs['in2'].is_linked==False ):
            buffer2_constant="true"
            
            
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
        times_index=str(self.rdfifo_start)
        for i in range(len(self.outputs)-1):
              times_index+='_'
              times_index+=str(self.rdfifo_start+i+1) 
        branch_in0,branch_in1,branch_in2=self.branch.split()
        
        reg0_xml=self.inputs[0].reg_val
        reg1_xml=self.inputs[1].reg_val
        reg2_xml=self.inputs[2].reg_val
        if(self.inputs[0].is_linked):
            reg0_xml='null'
        elif reg0_xml=='null':
            reg0_xml='0'
        if(self.inputs[1].is_linked):
            reg1_xml='null'
        elif reg1_xml=='null':
            reg1_xml='0'
        if(self.inputs[2].is_linked):
            reg2_xml='null'
        elif reg2_xml=='null':
            reg2_xml='0'
        xml_str=F'''
<node type="ag" index="{self.index}" domain="1" ag_mode="s2p" opcode="joint" buffer0_constant="{buffer0_constant}" buffer1_constant="{buffer1_constant}" buffer2_constant="{buffer2_constant}">
    {in0}
    {in1}
    {in2}
    <inbuffer value0="{reg0_xml}" value1="{reg1_xml}" value2="{reg2_xml}"/>
    <priority value="{self.priority}"/>
    <direction value="{self.direction}"/>
    <stride value="{self.stride_str}"/>
    <times value="{self.times}" index="{times_index}"/>{padding_str}
    <branch in0="{branch_in0}" in1="{branch_in1}" in2="{branch_in2}"/>
    <placement cord="[{self.placement}]"/>
</node>
'''
        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        access_inner="false"
        if(self.max_loop_level==self.loop_level and self.catalogue!='b'):
               access_inner="true"
        #生成fifo的placement
        fifo_cords=self.fifo_placement.split('_')      
        if(len(fifo_cords)<self.times):
            fifo_cords=["null,null"]*self.times
             
        for i in range(self.times):
            rdfifo_str=F'''
<node type="rdfifo" index="{self.rdfifo_start+i}" catalogue="{self.catalogue}" access_inner="{access_inner}" domain="2" size="2">
        <placement cord="[{fifo_cords[i]}]"/>
</node>'''
            file.write(rdfifo_str)
        file.write('\n')
        
        
        
    
#################################################################################################################################



class AG_OUTNode(Node, MyCustomTreeNode):
    bl_idname = 'AG_OUTNode'
    bl_label = "AG_OUT"
    bl_icon = 'ALIGN_LEFT'
    count=0

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(AG_OUTNode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.use_custom_color = True
            self.color=( 0.15, 0.05, 0 )
        
        

    def out_update(self, context):
        self.self_update()
        for output in self.outputs:
            for item in output.links:
                new_node=item.to_socket.node
                new_node.self_update() 
            
        
    def times_update(self, context):
        if(self.times>len(self.inputs)-3):
            start=len(self.inputs)
            for i in range(self.times-len(self.inputs)+3):
                self.inputs.new('_Port', "in"+str(start)) 
                self.inputs["in"+str(start)].belong_to_LOOP=True
                start+=1
        elif  self.times<len(self.inputs)-3:
            start=self.times +3
            for i in range(len(self.inputs)-3-self.times):
                self.inputs.remove(self.inputs["in"+str(start)])    
                start+=1   
    # 自定义节点属性，可用于定义节点时传参
    
    
    index: bpy.props.IntProperty(name='ag index',default=0,update=out_update)
    
    
    reg0: bpy.props.StringProperty(name='reg0',default='null')
    reg1: bpy.props.StringProperty(name='reg1',default='null')
    reg2: bpy.props.StringProperty(name='reg2',default='null')
    note: bpy.props.StringProperty(name='note')
    
    opcode: bpy.props.StringProperty(name='opcode',default="nop")
    priority:bpy.props.IntProperty(name='priority',default=0)
    direction:bpy.props.EnumProperty(
        name='direction',
        items=(
                ('row', 'row', 'row'),
                ('col', 'col', 'col'),
                ('channel', 'channel', 'channel')),
        
        default='row')
    stride:bpy.props.IntProperty(name='stride',default=1)
    stride_str:bpy.props.StringProperty(name='stride_str',default='1')
    times:bpy.props.IntProperty(name='times',default=1,min=1,max=16,update=times_update)
    branch:bpy.props.StringProperty(name='branch',default='null null null')
    
    ##############spm   attributions
    show_spm:bpy.props.BoolProperty(name='show_spm',default=False)
    ddr_addr:bpy.props.StringProperty(name='ddr_addr',default='0')
    #local_addr:bpy.props.StringProperty(name='local_addr',default='0')
    size_data:bpy.props.StringProperty(name='size_data',default='64')
    stride_lsu:bpy.props.StringProperty(name='stride_lsu',default='0')
    cnt_lsu:bpy.props.StringProperty(name='cnt_lsu',default='1')
    bank_sram:bpy.props.EnumProperty(name='bank_sram',items=(
                ('16', '16', '16'),
                ('32', '32', '32')),
        default='32')
    
    is_spm:bpy.props.EnumProperty(name='is_spm',items=(
                ('true', 'true', 'true'),
                ('false', 'false', 'false')),
        default='true')
    
    pattern:bpy.props.EnumProperty(name='pattern',items=(
                ('0', '0', '0'),
                ('1', '1', '1'),
                ('2', '2', '2'),
                ('3', '3', '3'),
                ('4', '4', '4'),
                ('5', '5', '5')),
        default='5')
    pow2_mode:bpy.props.EnumProperty(name='pow2_mode',items=(
                ('true', 'true', 'true'),
                ('false', 'false', 'false')),
        default='false')
    row_local:bpy.props.StringProperty(name='row_local',default='0')
    col_local:bpy.props.StringProperty(name='col_local',default='0')
    bank_num:bpy.props.EnumProperty(name='bank_num',items=(
                ('4', '4', '4'),
                ('8', '8', '8'),
                ('16', '16', '16'),
                ('32', '32', '32'),),
        default='16')
    multi_in0:bpy.props.StringProperty(name='multi_in0',default='1')
    multi_in1:bpy.props.StringProperty(name='multi_in1',default='1')
    
    has_moved_reg:bpy.props.BoolProperty(name='has_moved_reg', default=False)
    ########################################################################
    max_loop_level:bpy.props.IntProperty(name='max_loop_level',default=0)
    
    ######################################################################3
    placement: bpy.props.StringProperty(name='placement',default='null')
    
    fifo_placement:bpy.props.StringProperty(name='fifo_placement',default='')
    
    wrfifo_start:bpy.props.IntProperty(name='wrfifo_start',default=0)
    def init(self, context):
        self.inputs.new('_Port', "in0")
        self.inputs.new('_Port', "in1")
        self.inputs.new('_Port', "in2")
        
        self.inputs.new('_Port', "in"+"3")
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text='loop_level= '+str(self.loop_level))
        layout.label(text='delay_level= '+str(self.delay_level))
        layout.prop(self, "note")
        layout.prop(self, "index")
        
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")
        
        layout.prop(self,"priority")
        layout.prop(self,"times")
        layout.prop(self,"stride_str")
        layout.prop(self,"direction")
        layout.prop(self,"branch")
        layout.prop(self,"opcode")
        layout.prop(self, "show_spm")
        if(self.show_spm== True):
            layout.prop(self, "ddr_addr")
            layout.prop(self, "size_data")
            layout.prop(self, "stride_lsu")
            layout.prop(self, "cnt_lsu")
            #layout.prop(self, "bank_sram")
            layout.prop(self, "is_spm")
            
            layout.prop(self, "pattern")
            layout.prop(self, "pow2_mode")
            layout.prop(self, "row_local")
            layout.prop(self, "col_local")
            layout.prop(self, "bank_num")
            layout.prop(self, "multi_in0")
            layout.prop(self, "multi_in1")
        layout.prop(self, "placement")
       

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "note")
        layout.prop(self, "index")
        
        #layout.prop(self, "reg0")
        #layout.prop(self, "reg1")
        #layout.prop(self, "reg2")
        layout.prop(self,"priority")
        layout.prop(self,"times")
        layout.prop(self,"stride_str")
        layout.prop(self,"direction")
        layout.prop(self,"branch")
        layout.prop(self,"opcode")
        layout.prop(self, "show_spm")
        if(self.show_spm== True):
            layout.prop(self, "ddr_addr")
            layout.prop(self, "size_data")
            layout.prop(self, "stride_lsu")
            layout.prop(self, "cnt_lsu")
            #layout.prop(self, "bank_sram")
            layout.prop(self, "is_spm")
            
            layout.prop(self, "pattern")
            layout.prop(self, "pow2_mode")
            layout.prop(self, "row_local")
            layout.prop(self, "col_local")
            layout.prop(self, "bank_num")
            layout.prop(self, "multi_in0")
            layout.prop(self, "multi_in1")
        layout.prop(self, "placement")

    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        if self.placement!="null":
            return "ag"+str(self.index)+'  '+note+' '+F'[{self.placement}]'
        return "ag"+str(self.index)+'  '+note
    
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
        for input_index in range(len(self.inputs)):
            if(input_index>=3):
                self.inputs[input_index].belong_to_LOOP=True
            
        if not self.has_moved_reg:
            
            self.inputs[0].reg_val=self.reg0
            self.inputs[1].reg_val=self.reg1
            self.inputs[2].reg_val=self.reg2
            self.has_moved_reg=True
        
        #循环层处理
        loop_level=0
        delay_level=0
        for input in self.inputs:
            if input.is_linked:
                loop_level=max(loop_level,input.default_value.loop_level)
                delay_level=max(delay_level,input.default_value.delay_level)
        
            
        
        self.loop_level=loop_level
        self.delay_level=delay_level+1
       
        
        
    
    
    
    def print_xml(self,file):
        self.reg0=self.inputs[0].reg_val
        self.reg1=self.inputs[1].reg_val
        self.reg2=self.inputs[2].reg_val
        
        
        in0='<input type="null"/>'
        in1='<input type="null"/>'
        in2='<input type="null"/>'
        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        if self.inputs['in0'].is_linked:
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0_port=self.inputs['in0'].default_value.port
            if(in0_type=="AG_IN" ):
                    rdfifo_start=self.inputs['in0'].links[0].from_socket.node.rdfifo_start
                    in0=F'''<input type="{type_change[in0_type]}" index="{rdfifo_start+in0_port}" port="{self.inputs['in0'].rdfifo_port}"/>'''
            else:
                    in0=F'''<input type="{type_change[in0_type]}" index="{in0_index}" port="0"/>'''
            
        if self.inputs['in1'].is_linked:
            in1_type=self.inputs['in1']. default_value.type
            in1_index=self.inputs['in1']. default_value.index
            in1_port=self.inputs['in1'].default_value.port
            if(in1_type=="AG_IN" ):
                    rdfifo_start=self.inputs['in1'].links[0].from_socket.node.rdfifo_start
                    in1=F'''<input type="{type_change[in1_type]}" index="{rdfifo_start+in1_port}" port="{self.inputs['in1'].rdfifo_port}"/>'''
            else:
                    in1=F'''<input type="{type_change[in1_type]}" index="{in1_index}" port="0"/>'''
        if self.inputs['in2'].is_linked:
            in2_type=self.inputs['in2']. default_value.type
            in2_index=self.inputs['in2']. default_value.index
            in2_port=self.inputs['in2'].default_value.port
            if(in2_type=="AG_IN" ):
                    rdfifo_start=self.inputs['in2'].links[0].from_socket.node.rdfifo_start
                    in2=F'''<input type="{type_change[in2_type]}" index="{rdfifo_start+in2_port}" port="{self.inputs['in2'].rdfifo_port}"/>'''
            else:
                    in2=F'''<input type="{type_change[in2_type]}" index="{in2_index}" port="0"/>'''
        
        buffer0_constant="false"
        if self.loop_level>self.inputs['in0']. default_value.loop_level or (self.inputs['in0'].is_linked==False ):
            buffer0_constant="true"
        buffer1_constant="false"
        if self.loop_level>self.inputs['in1']. default_value.loop_level or(self.inputs['in1'].is_linked==False ):
            buffer1_constant="true"
        buffer2_constant="false"
        if self.loop_level>self.inputs['in2']. default_value.loop_level or (self.inputs['in2'].is_linked==False ):
            buffer2_constant="true"
            
            
       
        
       
       
        times_index=str(self.wrfifo_start)
        for i in range(len(self.inputs)-3-1):
              times_index+='_'
              times_index+=str(self.wrfifo_start+i+1) 
        branch_in0,branch_in1,branch_in2=self.branch.split()
        
        
        reg0_xml=self.inputs[0].reg_val
        reg1_xml=self.inputs[1].reg_val
        reg2_xml=self.inputs[2].reg_val
        if(self.inputs[0].is_linked):
            reg0_xml='null'
        elif reg0_xml=='null':
            reg0_xml='0'
        if(self.inputs[1].is_linked):
            reg1_xml='null'
        elif reg1_xml=='null':
            reg1_xml='0'
        if(self.inputs[2].is_linked):
            reg2_xml='null'
        elif reg2_xml=='null':
            reg2_xml='0'
        xml_str=F'''
<node type="ag" index="{self.index}" domain="1" ag_mode="p2s" opcode="joint" buffer0_constant="{buffer0_constant}" buffer1_constant="{buffer1_constant}" buffer2_constant="{buffer2_constant}">
    {in0}
    {in1}
    {in2}
    <inbuffer value0="{reg0_xml}" value1="{reg1_xml}" value2="{reg2_xml}"/>
    <priority value="{self.priority}"/>
    <direction value="{self.direction}"/>
    <stride value="{self.stride_str}"/>
    <times value="{self.times}" index="{times_index}"/>
    <branch in0="{branch_in0}" in1="{branch_in1}" in2="{branch_in2}"/>
    <placement cord="[{self.placement}]"/>
</node>
'''
        note_str=F'''
<!-- {self.note} -->'''
        access_inner="false"
        if(self.max_loop_level==self.loop_level):
               access_inner="true"
        fifo_cords=self.fifo_placement.split('_') 
        print(fifo_cords)     
        if(len(fifo_cords)<self.times):
            fifo_cords=["null,null"]*self.times
        for i in range(self.times):
            wrfifo_in=''
            if not self.inputs[i+3].is_linked:
                wrfifo_in='''<input type="null"/>'''
                print(F"AG_OUT.{self.index} lack input!")
            else:
                type=self.inputs[i+3].default_value.type
                if type=="AG_IN" :
                    wrfifo_in=F'''
                    <input type="{type_change[type]}" index="{self.inputs[i+3].default_value.index+self.inputs[i+3].default_value.port}" port="{self.inputs[i+3].rdfifo_port}"/>'''
                elif type=="WRFIFO":
                    wrfifo_in=self.inputs[i+3].links[0].from_socket.node.wrfifo_input
                else:
                    wrfifo_in=F'''
                    <input type="{type_change[self.inputs[i+3].default_value.type]}" index="{self.inputs[i+3].default_value.index}" port="0"/>'''
            wrfifo_str=F'''
<node type="wrfifo" index="{self.wrfifo_start+i}"  opcode="{self.opcode}" access_inner="{access_inner}" domain="2" size="2">{wrfifo_in}
        <placement cord="[{fifo_cords[i]}]"/>
</node>'''
            file.write(wrfifo_str)
            
        
        if self.note!='':
            file.write(note_str)
        
        file.write(xml_str)
        
        
    
#################################################################################################################################