'''

'''


import sys
 
import bpy
from bpy.types import Node
from MyCustomTree import *
from MyCustomSocket import *
from CGRA_INTERFACE import *
from queue import Queue 
class FIFONode(Node, MyCustomTreeNode):
    bl_idname = 'FIFONode'
    bl_label = "FIFO"
    bl_icon = 'ALIGN_LEFT'
    

    def __init__(self):
        if 'in0' not in self.inputs.keys() :
            super(FIFONode,self).__init__()
            MyCustomTreeNode.__init__(self)
            self.index_value =0
            self.use_custom_color = True
            self.color=( 0.25, 0,0.25 )
        
        


    def out_update(self,context):
        self.self_update()
        for item in self.outputs[0].links:
            new_node=item.to_socket.node
            new_node.self_update() 
        
    
    index: bpy.props.IntProperty(name='fifo index',default=0,update=out_update)
    note: bpy.props.StringProperty(name='note')
    

    def init(self, context):
        self.inputs.new('_Port', "in0")
        

        self.outputs.new('_Port_Out', "out")
        #self.outputs['out'].default_value = PortData()
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text='loop_level= '+str(self.loop_level))
        layout.label(text='delay_level= '+str(self.delay_level))
        layout.prop(self, "index")
        
        

    def draw_buttons_ext(self, context, layout):
        
        layout.prop(self, "index")
        


    def draw_label(self):
        note='('+self.note+')'
        if self.note=='':
            note=''
        return "fifo"+str(self.index)+'  '+note

    loop_level: bpy.props.IntProperty(name='loop_level',default=0)
    delay_level: bpy.props.IntProperty(name='delay_level',default=0)
    
    partition_times:bpy.props.IntProperty(name='partition_times',default=0)
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
        loop_level=0
        delay_level=0
        if self.inputs['in0'].is_linked:
            loop_level=max(loop_level,self.inputs['in0'].default_value.loop_level)
            delay_level=max(delay_level,self.inputs['in0'].default_value.delay_level)
            self.note=self.inputs['in0'].default_value.note
        else:
            self.note=''    
            
        self.loop_level=loop_level
        self.delay_level=delay_level+1
        domain=0
        for input in self.inputs:
            domain=max(input.default_value.domain,domain)
        
        for i in range(len(self.outputs['out'].links)):
            self.outputs['out'].links[i].to_socket.default_value.index=self.index
            self.outputs['out'].links[i].to_socket.default_value.type='FIFO'
            self.outputs['out'].links[i].to_socket.default_value.loop_level=self.loop_level
            self.outputs['out'].links[i].to_socket.default_value.delay_level=self.delay_level
            self.outputs['out'].links[i].to_socket.default_value.domain=domain
            self.outputs['out'].links[i].to_socket.default_value.note=self.note
        
    
    
    
    def print_xml(self,file): 

        in0='<input type="null"/>'

        type_change={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'rdfifo','AG_OUT':'wrfifo','TRANS':'pe','FIFO':'fifo'}
        if self.inputs['in0'].is_linked:
            in0_type=self.inputs['in0']. default_value.type
            in0_index=self.inputs['in0']. default_value.index
            in0=F'<input type="{type_change[in0_type]}" index="{in0_index}" port="0"/>'
            in0_port=self.inputs['in0']. default_value.port
            if(in0_type=="AG_IN" ):
                in0=F'<input type="{type_change[in0_type]}" index="{in0_index+in0_port}" port="0"/>'
        
        domain=0
        for input in self.inputs:
            domain=max(input.default_value.domain,domain)
        if self.index>=20:
            domain=2
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
<node type="fifo" index="{self.index}" domain="{domain}" size="5" {partition_times}>
    {in0}
    <placement cord="[10, 11]"/>
</node>
'''
        
        note_str=F'''<!-- {self.note} -->'''
        if self.note!='':
            file.write(note_str)
        file.write(xml_str)
        
        
