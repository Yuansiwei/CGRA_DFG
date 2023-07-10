import bpy
import os
from queue import Queue 
from operator import attrgetter
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
import xml.etree.ElementTree as xmlTree
############################ hello操作类
class Test_OT_Hello(bpy.types.Operator):
    bl_idname = "ysw_operator.hello"
    bl_label = "Hello!"
    bl_description = "插件开发测试"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #print(bpy.context.space_data.node_tree.name)
        print("Hello, is me.")
        cwd=os.getcwd()
        print(cwd)
        return {"FINISHED"}
#############    
class OT_std_version_transfer(bpy.types.Operator, ImportHelper): 
    bl_idname = "ysw_operator.std_version_transfer" 
    bl_label = "std version transfer" 
    bl_description = "转换为标准xml格式"
    filter_glob: bpy.props.StringProperty( default='*.xml', options={'HIDDEN'} ) 
    
    def execute(self, context): 
        """Do something with the selected file(s).""" 
        filename, extension = os.path.splitext(self.filepath)
        #print (extension)
        if extension!= ".xml":
            return {'FINISHED'}
        tree = xmlTree.parse(self.filepath)
        root = tree.getroot()
       
        has_domain2_partition=0;
        
        for xml_node in root:
            if xml_node.attrib["type"]=="scratchpad":
                spm_node=xml_node
        
        for xml_node in root:
            if xml_node.tag=='domain2_partition':
                has_domain2_partition=1
            
            if xml_node.tag!='node':
                continue
            #print(xml_node.attrib)
            if  xml_node.attrib["type"]=="pe" :
                if "is_float" in xml_node.attrib.keys() and not("alu_precision" in xml_node.attrib.keys() ):
                    if xml_node.attrib["is_float"]=="true" :
                        xml_node.attrib["alu_precision"]="FP32"
                    else:
                        xml_node.attrib["alu_precision"]="int32"
                    xml_node.attrib.pop("is_float")   
                if "domain" in xml_node.attrib.keys() and  xml_node.attrib["domain"]=="2" and not("partition_times" in xml_node.attrib.keys()):
                    xml_node.attrib["partition_times"]="1st"
                
            elif xml_node.attrib["type"]=="fifo" :
                 xml_node.attrib["size"]="5"

            elif xml_node.attrib["type"]=="bus" :
                 xml_node.attrib["type"]="jump"
            elif xml_node.attrib["type"]=="scratchpad":
                for item in xml_node:
                    if "stream_index" in item.attrib.keys():
                        item.attrib["index"]=item.attrib["stream_index"]
                        item.attrib.pop("stream_index")
                    if "multi" in item.attrib.keys():
                        item.attrib["multipiler"]=item.attrib["multi"]
                        item.attrib.pop("multi")
                    if "stride" in item.attrib.keys():
                        item.attrib["tile_width"]=item.attrib["stride"]
                        item.attrib.pop("stride")
                    if "local_row" in item.attrib.keys():
                        item.attrib["row_start_index"]=item.attrib["local_row"]
                        item.attrib.pop("local_row")
                    if "local_col" in item.attrib.keys():
                        item.attrib["col_start_index"]=item.attrib["local_col"]
                        item.attrib.pop("local_col")
            elif xml_node.attrib["type"]=="lsu":
                for item in xml_node:
                    if "is_spm" not in item.attrib.keys():
                        item.attrib["is_spm"]="false"
                    if item.attrib["is_spm"]=="true" and "local_base_addr" in  item.attrib.keys():
                        if item.attrib["local_base_addr"].find('{')==-1:
                            item.attrib["row_start_index"]=str(int(item.attrib["local_base_addr"])/16);
                            item.attrib["col_start_index"]=str(int(item.attrib["local_base_addr"])%16);
                        else:
                            item.attrib["row_start_index"]='('+item.attrib["local_base_addr"]+')'+"/16"
                            item.attrib["col_start_index"]='('+item.attrib["local_base_addr"]+')'+"%16"
                        item.attrib.pop("local_base_addr")
                    if "stream_index" in item.attrib.keys():
                        item.attrib["index"]=item.attrib["stream_index"]
                        item.attrib.pop("stream_index")
                    if item.attrib["is_spm"]=="true" and "tile_width" not in  item.attrib.keys():
                        stream_index=item.attrib['index']
                        for spm_item in spm_node:
                            if "stream_index" in spm_item.attrib.keys() and spm_item.attrib["stream_index"]==stream_index:
                                if "tile_width"  in spm_item.attrib.keys():
                                    item.attrib["tile_width"]=spm_item.attrib["tile_width"]
                                if "stride"  in spm_item.attrib.keys():
                                    item.attrib["tile_width"]=spm_item.attrib["stride"]
                            if "index" in spm_item.attrib.keys() and spm_item.attrib["index"]==stream_index:
                                if "tile_width"  in spm_item.attrib.keys():
                                    item.attrib["tile_width"]=spm_item.attrib["tile_width"]
                                if "stride"  in spm_item.attrib.keys():
                                    item.attrib["tile_width"]=spm_item.attrib["stride"]
                    if item.attrib["is_spm"]=="true" and "N" not in  item.attrib.keys():
                        stream_index=item.attrib['index']
                        for spm_item.attrib in spm_node:
                            if "stream_index" in spm_item.attrib.keys() and spm_item.attrib["stream_index"]==stream_index:
                                item.attrib["N"]=spm_item.attrib["N"]
                            if "index" in spm_item.attrib.keys() and spm_item.attrib["index"]==stream_index:
                                item.attrib["N"]=spm_item.attrib["N"]
            if not has_domain2_partition:
                domain2_partiton=xmlTree.Element('domain2_partiton')
                domain2_partiton.attrib['times']="1"
                domain2_partiton.attrib['physical_space']="16"
                root.insert(1,domain2_partiton);
        return {'FINISHED'}    

####xml 读取，placement载入
class OT_LoadPlacement(bpy.types.Operator, ImportHelper): 
    bl_idname = "ysw_operator.placement" 
    bl_label = "read placement" 
    bl_description = "读取节点布局"
    filter_glob: bpy.props.StringProperty( default='*.xml', options={'HIDDEN'} ) 
    
    def execute(self, context): 
        filename, extension = os.path.splitext(self.filepath)
        #建立已有节点字典
        valid_type={"pe","ls","fifo","ag","rdfifo","wrfifo"}
        type_change={"PE":"pe","AG_IN":"ag","AG_OUT":"ag","FIFO":"fifo","LOOP":"pe","LOAD":"ls","SAVE":"ls"}
        Tree_key=bpy.context.space_data.node_tree.name
        node_table={}
        for node in bpy.data.node_groups[Tree_key].nodes:
                node_table[type_change[node.bl_label]+str(node.index)]=node
              
        
        xml_node_table={}
        #填充placement
        if extension!= ".xml":
            return {'FINISHED'}
        tree = xmlTree.parse(self.filepath)
        root = tree.getroot() 
      
        for xml_node in root:
            if xml_node.tag!='node'or xml_node.attrib["type"]not in valid_type:
                continue
            xml_node_table[xml_node.attrib["type"]+xml_node.attrib["index"]]=xml_node
                
        for key in node_table.keys():
            
            if key in xml_node_table.keys():
                node=node_table[key]
                xml_node=xml_node_table[key]
                
                child=xml_node.find("placement")
                if child!=None:
                    node.placement=child.attrib["cord"].strip(" []")
                if node.bl_label=="AG_IN"or node.bl_label=="AG_OUT" :
                    node.fifo_placement=''
                    child=xml_node.find("times")
                    vector_fifo=child.attrib["index"].split('_')
                    fifo_type=None
                    if node.bl_label=="AG_IN":
                        fifo_type="rdfifo"
                    else:
                        fifo_type="wrfifo"
                    for index in vector_fifo:
                        fifo_xml_node=xml_node_table[fifo_type+index]
                        if node.bl_label=="AG_IN" and "catalogue" in fifo_xml_node.attrib.keys():
                            node.catalogue=fifo_xml_node.attrib["catalogue"]
                        fifo_placement=fifo_xml_node.find("placement").attrib["cord"].strip(" []")
                        if(node.fifo_placement!=''):
                            node.fifo_placement+='_'
                        node.fifo_placement+=fifo_placement
        return {'FINISHED'}
####xml 读取，DFG生成
class OT_TestOpenFilebrowser(bpy.types.Operator, ImportHelper): 
    bl_idname = "ysw_operator.open_filebrowser" 
    bl_label = "Open a xml file" 
    bl_description = "xml读取"
    filter_glob: bpy.props.StringProperty( default='*.xml', options={'HIDDEN'} ) 
    
    def execute(self, context): 
        filename, extension = os.path.splitext(self.filepath)
        #print (extension)
        if extension!= ".xml":
            return {'FINISHED'}
        tree = xmlTree.parse(self.filepath)
        root = tree.getroot()

        bpy.ops.node.new_node_tree()
        nodes=bpy.context.space_data.node_tree.nodes
        bpy.context.space_data.node_tree.active=nodes
        node_table={}
        ag_rdfifo_table={}
        ag_wrfifo_table={}
        lsu_node=None
        spm_node=None
        for xml_node in root:
            if xml_node.tag!='node'or xml_node.attrib["type"]=="paraset" or xml_node.attrib["type"]=="bus":
                continue
            elif xml_node.attrib["type"]=="lsu" :
                lsu_node=xml_node
                continue
            elif xml_node.attrib["type"]=="scratchpad" :
                spm_node=xml_node
                continue
            if  xml_node.attrib["type"]=="pe" :
                if xml_node.attrib["loop_control"]=="sync_loop" or xml_node.attrib["loop_control"]=="loop" or xml_node.attrib["loop_control"]=="inner_loop_sync"or xml_node.attrib["loop_control"]=="inner_loop_ini_sync" or xml_node.attrib["loop_control"]=="inner_loop"or xml_node.attrib["loop_control"]=="inner_loop_ini" or xml_node.attrib["loop_control"]=="outermost_loop":
                    new_node=nodes.new("LOOPNode")
                    new_node.index=int(xml_node.attrib["index"])
                    new_node.opcode=xml_node.attrib["opcode"]
                    reg_count=0
                    for child in xml_node:
                        if(child.tag=='reg' and reg_count==0 and (xml_node.attrib["loop_control"]=="inner_loop_ini_sync" or xml_node.attrib["loop_control"]=="inner_loop_ini")):
                            new_node.step=child.attrib["value"]
                            new_node.need_step=True
                            reg_count+=1
                        elif(child.tag=='reg' and reg_count==0 and (xml_node.attrib["loop_control"]=="inner_loop_sync" or xml_node.attrib["loop_control"]=="inner_loop" or xml_node.attrib["loop_control"]=="outermost_loop")):
                            new_node.start=child.attrib["value"]
                            reg_count+=1
                        elif(child.tag=='reg' and reg_count==1):
                            reg_count+=1
                        elif(child.tag=='reg' and reg_count==2):
                            new_node.end=child.attrib["value"]
                            reg_count+=1
                        elif(child.tag=='inbuffer'):
                            new_node.step=child.attrib["value0"]
                            new_node.start=child.attrib["value1"]
                            new_node.end=child.attrib["value2"]
                    if xml_node.attrib["loop_control"]=="inner_loop_ini":
                        new_node.start="null"
                else:
                    new_node=nodes.new("PENode")
                    
                    new_node.index=int(xml_node.attrib["index"])
                    new_node.opcode=xml_node.attrib["opcode"]
                    if "is_float" in xml_node.attrib.keys():
                        if xml_node.attrib["is_float"]=="true":
                            new_node.is_float=True
                    if "alu_precision" in xml_node.attrib.keys():
                        if xml_node.attrib["alu_precision"]=="FP32":
                            new_node.is_float=True
                    if "branch_control" in xml_node.attrib.keys():
                        new_node.branch=xml_node.attrib["branch_control"]
                    if "key_cal" in xml_node.attrib.keys() and xml_node.attrib["key_cal"]=="true":
                        new_node.key_cal=True
                    if "loop_control" in xml_node.attrib.keys():
                        loop_control=xml_node.attrib["loop_control"]
                        if loop_control=="trans" :
                            loop_control="transin"
                        new_node.loop=loop_control
                    if "self_loop" in xml_node.attrib.keys() and xml_node.attrib["self_loop"]=="true":
                        new_node.self_loop=True
                    reg_count=0
                    for child in xml_node:
                        
                        if(child.tag=='reg' and reg_count==0 ):
                            new_node.reg0=child.attrib["value"]
                            new_node.inputs[0].reg_val=child.attrib["value"]
                            reg_count+=1
                        elif(child.tag=='reg' and reg_count==1):
                            new_node.reg1=child.attrib["value"]
                            new_node.inputs[1].reg_val=child.attrib["value"]
                            reg_count+=1
                        elif(child.tag=='reg' and reg_count==2):
                            new_node.reg2=child.attrib["value"]
                            new_node.inputs[2].reg_val=child.attrib["value"]
                            reg_count+=1
                        elif(child.tag=='inbuffer'):
                            new_node.reg0=child.attrib["value0"]
                            new_node.reg1=child.attrib["value1"]
                            new_node.reg2=child.attrib["value2"]
                            new_node.inputs[0].reg_val=child.attrib["value0"]
                            new_node.inputs[1].reg_val=child.attrib["value1"]
                            new_node.inputs[2].reg_val=child.attrib["value2"]
                        elif(child.tag=="inner_connection" and child.attrib["buffer1_from"]=="aluin1"):
                            new_node.self_loop=True
                node_table["pe"+str(new_node.index)]=new_node
            elif xml_node.attrib["type"]=="fifo" :
                new_node=nodes.new("FIFONode")
                new_node.index=int(xml_node.attrib["index"])
                node_table["fifo"+str(new_node.index)]=new_node
                input_size=0
                for child in xml_node:
                    input_size+=child.tag=="input"
                new_node.input_size=input_size
            elif xml_node.attrib["type"]=="ls" and xml_node.attrib["ls_mode"]=="g2p":
                new_node=nodes.new("LOADNode")
                
                new_node.index=int(xml_node.attrib["index"])
                new_node.opcode=xml_node.attrib["opcode"]
                for child in xml_node:
                    if(child.tag=='inbuffer'):
                        new_node.inbuffer=child.attrib["value"]
                    elif(child.tag=='localreg'): 
                        new_node.reg0=child.attrib["value0"]
                        new_node.reg1=child.attrib["value1"]
                node_table["ls"+str(new_node.index)]=new_node
            elif xml_node.attrib["type"]=="ls" and xml_node.attrib["ls_mode"]=="p2g":
                new_node=nodes.new("SAVENode")
                
                new_node.index=int(xml_node.attrib["index"])
                new_node.opcode=xml_node.attrib["opcode"]
                for child in xml_node:
                    if(child.tag=='inbuffer'):
                        new_node.inbuffer=child.attrib["value"]
                    elif(child.tag=='localreg'): 
                        new_node.reg0=child.attrib["value0"]
                        new_node.reg1=child.attrib["value1"]
                node_table["ls"+str(new_node.index)]=new_node
            elif xml_node.attrib["type"]=="ag" and (xml_node.attrib["ag_mode"]=="s2p" or xml_node.attrib["ag_mode"]=="g2p"):
                new_node=nodes.new("AG_INNode")
                new_node.index=int(xml_node.attrib["index"])
                for child in xml_node:
                    if(child.tag=='inbuffer'):
                        new_node.reg0=child.attrib["value0"]
                        new_node.reg1=child.attrib["value1"]
                        new_node.reg2=child.attrib["value2"]
                        new_node.inputs[0].reg_val=child.attrib["value0"]
                        new_node.inputs[1].reg_val=child.attrib["value1"]
                        new_node.inputs[2].reg_val=child.attrib["value2"]
                    elif child.tag=='priority':
                        new_node.priority=int(child.attrib["value"])
                    elif child.tag=='direction':
                        new_node.direction=child.attrib["value"]
                    elif child.tag=='stride':
                        new_node.stride_str=child.attrib["value"]
                    elif child.tag=='times':
                        new_node.times=int(child.attrib["value"])
                        rdfifo_indexs=child.attrib["index"].split('_')
                        port_count=0
                        assert len(rdfifo_indexs)==new_node.times
                        for index in rdfifo_indexs:
                            ag_rdfifo_table['rdfifo'+index]=new_node.outputs[port_count]
                            port_count+=1
                    elif child.tag=='branch':  
                        new_node.branch=child.attrib["in0"]+' '+child.attrib["in1"]+' '+child.attrib["in2"]
                    elif child.tag=='padding':     
                        new_node.in0LU=child.attrib['in0L']+' '+child.attrib['in0U']
                        new_node.in1LU=child.attrib['in1L']+' '+child.attrib['in1U']
                        new_node.in2LU=child.attrib['in2L']+' '+child.attrib['in2U']
                        if child.attrib['in0L']!='null' or  child.attrib['in0U']!='null' or child.attrib['in1L']!='null' or  child.attrib['in1U']!='null'  or child.attrib['in2L']!='null' or  child.attrib['in2U']!='null':
                            new_node.is_padding=1
                    elif child.tag=="placement":
                        new_node.placement=child.attrib['cord'].strip('[]')
                node_table["ag"+str(new_node.index)]=new_node
            elif xml_node.attrib["type"]=="ag" and (xml_node.attrib["ag_mode"]=="p2s" or xml_node.attrib["ag_mode"]=="p2g"):
                new_node=nodes.new("AG_OUTNode")
                new_node.index=int(xml_node.attrib["index"])
                for child in xml_node:
                    if(child.tag=='inbuffer'):
                        new_node.reg0=child.attrib["value0"]
                        new_node.reg1=child.attrib["value1"]
                        new_node.reg2=child.attrib["value2"]
                        new_node.inputs[0].reg_val=child.attrib["value0"]
                        new_node.inputs[1].reg_val=child.attrib["value1"]
                        new_node.inputs[2].reg_val=child.attrib["value2"]
                    elif child.tag=='priority':
                        new_node.priority=int(child.attrib["value"])
                    elif child.tag=='direction':
                        new_node.direction=child.attrib["value"]
                    elif child.tag=='stride':
                        new_node.stride_str=child.attrib["value"]
                    elif child.tag=='times':
                        new_node.times=int(child.attrib["value"])
                        wrfifo_indexs=child.attrib["index"].split('_')
                        assert len(wrfifo_indexs)==new_node.times
                        port_count=0
                        for index in wrfifo_indexs:
                            ag_wrfifo_table['wrfifo'+index]=new_node.inputs[port_count+3]
                            port_count+=1
                    elif child.tag=='branch':  
                        new_node.branch=child.attrib["in0"]+' '+child.attrib["in1"]+' '+child.attrib["in2"]
                    elif child.tag=="placement":
                        new_node.placement=child.attrib['cord'].strip('[]')      
                node_table["ag"+str(new_node.index)]=new_node      
        links=bpy.context.space_data.node_tree.links
        for xml_node in root:
            if xml_node.tag!='node':
                continue
            input_count=0
            if xml_node.attrib["type"]=='wrfifo':
                for child in xml_node:
                    if(child.tag=='input'):
                        if (child.attrib['type']=='rdfifo'):
                            links.new(ag_wrfifo_table['wrfifo'+xml_node.attrib["index"]],ag_rdfifo_table['rdfifo'+child.attrib['index']])
                            ag_wrfifo_table['wrfifo'+xml_node.attrib["index"]].rdfifo_port=int(child.attrib['port'])
                        elif(child.attrib['type']!='null'):
                            links.new(ag_wrfifo_table['wrfifo'+xml_node.attrib["index"]],node_table[child.attrib['type']+child.attrib['index']].outputs[0])
            else:    
                for child in xml_node:
                    if(child.tag=='input'):
                        if (child.attrib['type']=='rdfifo'):
                            links.new(node_table[xml_node.attrib["type"]+xml_node.attrib["index"]].inputs[input_count],ag_rdfifo_table['rdfifo'+child.attrib['index']])
                            node_table[xml_node.attrib["type"]+xml_node.attrib["index"]].inputs[input_count].rdfifo_port=int(child.attrib['port'])
                        elif(child.attrib['type']!='null'):
                            links.new(node_table[xml_node.attrib["type"]+xml_node.attrib["index"]].inputs[input_count],node_table[child.attrib['type']+child.attrib['index']].outputs[0])
                        input_count+=1
        if (lsu_node!=None) :               
            for child in lsu_node:
                if child.tag=="prefetch":
                    ag_node=node_table["ag"+child.attrib["stream_index"]]
                    ag_node.ddr_addr=child.attrib["ddr_base_addr"]
                    ag_node.size_data=child.attrib["prefetch_times"]
                    ag_node.stride_lsu=child.attrib["prefetch_stride"]
                    ag_node.cnt_lsu=child.attrib["prefetch_cnt"]
                    ag_node.is_spm=child.attrib["is_spm"]
                elif child.tag=="writeback":
                    ag_node=node_table["ag"+child.attrib["stream_index"]]
                    ag_node.ddr_addr=child.attrib["ddr_base_addr"]
                    ag_node.size_data=child.attrib["write_times"]
                    ag_node.stride_lsu=child.attrib["write_stride"]
                    ag_node.cnt_lsu=child.attrib["write_cnt"]
                    ag_node.is_spm=child.attrib["is_spm"]
        if (spm_node!=None) : 
            for child in spm_node:
                if child.tag!="stream":
                    continue;
                ag_node=node_table["ag"+child.attrib["stream_index"]]
                if "pattern" in child.attrib.keys():
                    ag_node.pattern=child.attrib["pattern"]
                if "pow2_mode" in child.attrib.keys():
                    ag_node.pow2_mode=child.attrib["pow2_mode"]
                ag_node.row_local=child.attrib["local_row"]
                ag_node.col_local=child.attrib["local_col"]
                ag_node.bank_num=child.attrib["N"]
                ag_node.multi_in0=child.attrib["multi"]
                ag_node.multi_in1=child.attrib["stride"]
            
        bpy.ops.ysw_operator.location()
        
        for node in nodes:
            node.hide=True

        return {'FINISHED'}
############################ hello操作面板
class Test_PT_HelloPanel(bpy.types.Panel):
    bl_idname = "ysw_panel.hello_panel"
    bl_label = "Test Hello"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "test Addon"

    def draw(self, context):
        layout = self.layout
        
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.hello")
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.open_filebrowser")
        
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.placement")
        
############################ xmL操作类
class Test_OT_xml(bpy.types.Operator, ImportHelper):
    bl_idname = "ysw_operator.xml"
    bl_label = "xml generate"
    bl_description = "xml插件开发测试"
    bl_options = {"REGISTER"}
    filter_glob: bpy.props.StringProperty( default='*.xml', options={'HIDDEN'} ) 
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        fileName=self.filepath
        file=open(fileName,'w')

        Tree_key=bpy.context.space_data.node_tree.name
        
        
#######index check
        
        color_table={'FIFO':(0.25,0,0.25),'LOAD':(0.075,0.16,0),'AG_IN':(0.075,0.16,0),'SAVE':(0.15,0.05,0),'AG_OUT':(0.15,0.05,0),'PE':(0.1,0.2,0.25),'LOOP':(0.2,0.2,0)}     
        ls_table={}
        ag_table={}
        fifo_table={}
        pe_table={}
        max_loop_level=0;
        for node in bpy.data.node_groups[Tree_key].nodes:
            max_loop_level=max(max_loop_level,node.loop_level)
            if node.bl_label=='FIFO':
                if node.index in fifo_table.keys():
                    fifo_table[node.index].color=(0.6,0,0)
                    node.color=(0.6,0,0)
                else:
                    node.color=color_table[node.bl_label]
                    fifo_table[node.index]=node
            if node.bl_label=='PE' or node.bl_label=='LOOP':
                if node.index in pe_table.keys():
                    pe_table[node.index].color=(0.6,0,0)
                    node.color=(0.6,0,0)
                else:
                    node.color=color_table[node.bl_label]
                    pe_table[node.index]=node
            if node.bl_label=='SAVE' or node.bl_label=='LOAD':
                if node.index in ls_table.keys():
                    ls_table[node.index].color=(0.6,0,0)
                    node.color=(0.6,0,0)
                else:
                    node.color=color_table[node.bl_label]
                    ls_table[node.index]=node
            if node.bl_label=='AG_IN' or node.bl_label=='AG_OUT':
                if node.index in ag_table.keys():
                    ag_table[node.index].color=(0.6,0,0)
                    node.color=(0.6,0,0)
                else:
                    node.color=color_table[node.bl_label]
                    ag_table[node.index]=node
                
        
        
# #######   partition times computation for pe and fifo in domain2;  (except wrfifo and rdfifo)

#             pe_fifo_table={}
#             partition_times=0;
#             physical_space=0
#             for node in bpy.data.node_groups[Tree_key].nodes:
#                 #if node.bl_label=='PE':
#                 if (node.bl_label =="FIFO" and (node.mode!="WRFIFO" or not node.link_to_AG_OUT)) or node.bl_label=='PE':
#                     domain=0;
#                     for input in node.inputs:
#                         domain=max(input.default_value.domain,domain)
#                         if(node.bl_label =="FIFO" and node.index>=20):
#                           domain=2;
#                     if domain==2 and node not in pe_fifo_table.keys():
#                         partition_times+=1;
#                         pe_fifo_queue=Queue();
#                         pe_fifo_queue.put(node)
#                         delay_table={}
#                         pe_fifo_table[node]=1
#                         while not pe_fifo_queue.empty():
#                             node_get=pe_fifo_queue.get()
#                             if(node_get.bl_label =="PE" and node_get.delay_level not in delay_table.keys()):
#                                 delay_table[node_get.delay_level]=1
#                             elif node_get.bl_label =="PE":
#                                 delay_table[node_get.delay_level]+=1
                            
#                             node_get.partition_times=partition_times
#                             for next_input in node_get.inputs:
#                                 for link in next_input.links:
#                                     node_temp=link.from_socket.node
#                                     domain_temp=0;
#                                     for input in node_temp.inputs:
#                                         domain_temp=max(input.default_value.domain,domain_temp)
#                                     if((node.bl_label =="FIFO" and (node.mode!="WRFIFO" or not node.link_to_AG_OUT)) and node_temp.index>=20):
#                                         domain_temp=2;
#                                     if domain_temp==2 and ((node.bl_label =="FIFO" and (node.mode!="WRFIFO" or not node.link_to_AG_OUT)) or node_temp.bl_label=='PE') and node_temp not in pe_fifo_table.keys():
#                                         pe_fifo_queue.put(node_temp)
#                                         pe_fifo_table[node_temp]=1
                        
#                             for next_output in node_get.outputs:
#                                 for link in next_output.links:
#                                     node_temp=link.to_socket.node
#                                     domain_temp=0;
#                                     for input in node_temp.inputs:
#                                         domain_temp=max(input.default_value.domain,domain_temp)
#                                     if((node.bl_label =="FIFO" and (node.mode!="WRFIFO" or not node.link_to_AG_OUT)) and node_temp.index>=20):
#                                         domain_temp=2;
#                                     if domain_temp==2 and ((node.bl_label =="FIFO" and (node.mode!="WRFIFO" or not node.link_to_AG_OUT)) or node_temp.bl_label=='PE') and node_temp not in pe_fifo_table.keys():
#                                         pe_fifo_table[node_temp]=1
#                                         pe_fifo_queue.put(node_temp)
#                         #print(delay_table)
#                         for value in delay_table.values():
#                             physical_space=max(physical_space,value)
















#######rdfifo generate     
        
        rdfifo_count=0;
        wrfifo_count=0;
        agin_vector=[]
        agout_vector=[]
        for node in bpy.data.node_groups[Tree_key].nodes:
            if node.bl_label=='AG_IN':
                agin_vector.append(node)
            elif node.bl_label== "AG_OUT":
                agout_vector.append(node)
        agin_vector.sort(key=attrgetter("index"), reverse=False)
        agout_vector.sort(key=attrgetter("index"), reverse=False)
        for node in agin_vector:                
            node.rdfifo_start=rdfifo_count
            rdfifo_count+=node.times
        
        for node in agout_vector:                
            node.wrfifo_start=wrfifo_count
            wrfifo_count+=node.times
            
        
        



#######
        str=F'''<?xml version="1.0" encoding="utf-8"?>
<Config manual_placement="true">
    <config_option function="true" parameter="true"/>
    <domain2_partition times="1" physical_space="[8, 8]"/>
'''
        file.write(str)
        node_queue=Queue()
        type_table={'LOOP':'pe','PE':'pe','LOAD':'ls','SAVE':'ls','AG_IN':'ag','AG_OUT':'ag','TRANS':'pe','FIFO':'fifo'}
        bus=''
        for node in bpy.data.node_groups[Tree_key].nodes:
            root=1
            for input in node.inputs:
                if input.is_linked:
                    root=0
            if root:
                  node_queue.put(node)
            
            is_end_node=1
            for output in  node.outputs:
                if output.is_linked:
                    is_end_node=0;     
            if is_end_node or  node.bl_label=='AG_IN':
                if node.bl_label=='AG_IN':
                    for i in range(node.times):
                        if not node.outputs[i].is_linked:
                            bus+=F'rdfifo.{node.index+i}.0_'
                     
                elif node.bl_label!='AG_OUT':
                    bus+=F'{type_table[node.bl_label]}.{node.index}.0_'
        
        
        is_refine=context.scene.my_prop.is_refine
        
        
        ag_list=[]
        lsu_xml=""
        spm_xml=""
        xml_hash={}
        
        while not node_queue.empty():
            node_get=node_queue.get()
            
            if node_get.bl_label=="PE" or node_get.bl_label=="LOOP":
                node_get.print_xml(file,is_refine)
            elif node_get.bl_label=="AG_IN":
                node_get.max_loop_level=max_loop_level
                #local_addr=int(node_get.row_local)*int(node_get.bank_sram)+int(node_get.col_local)
                ag_list.append(node_get)
                
                
                node_get.print_xml(file)
            elif node_get.bl_label=="AG_OUT":
                node_get.max_loop_level=max_loop_level
                #local_addr=int(node_get.row_local)*int(node_get.bank_sram)+int(node_get.col_local)
                ag_list.append(node_get)
                
                node_get.print_xml(file)
                for i in range(node_get.times):
                    bus+=F'wrfifo.{node_get.wrfifo_start+i}.0_'
                
                    
            else:
                node_get.print_xml(file)
            for output in node_get.outputs:
                    for item in output.links:
                        new_node=item.to_socket.node
                        if not(new_node in xml_hash.keys()):
                            xml_hash[new_node]=1
                        else:
                            xml_hash[new_node]+=1
                        link_count=0
                        for input in new_node.inputs:
                            if input.is_linked:
                                link_count+=1
                        if xml_hash[new_node]==link_count:
                            node_queue.put(new_node)

#对ag 节点作 ag_index的排序
        ag_list=sorted(ag_list, key=lambda item: item.index)        

#根据stream_index顺序结果生成LSU 和 SPM       
        for i in range(len(ag_list)):
            if ag_list[i].bl_label=="AG_IN":
                lsu_xml+=F'''     <prefetch  ddr_base_addr="{ag_list[i].ddr_addr}"  local_base_addr="0" prefetch_times="{ag_list[i].size_data}"  prefetch_stride="{ag_list[i].stride_lsu}" prefetch_cnt="{ag_list[i].cnt_lsu}" is_spm="{ag_list[i].is_spm}" stream_index="{ag_list[i].index}"/>
'''
                spm_xml+=F'''     <stream stream_index="{ag_list[i].index}" mode="rd" pattern="{ag_list[i].pattern}" pow2_mode="{ag_list[i].pow2_mode}" local_row="{ag_list[i].row_local}" local_col="{ag_list[i].col_local}" multi="{ag_list[i].multi_in0}"   stride="{ag_list[i].multi_in1}"  N="{ag_list[i].bank_num}" />
'''         
            else:
                lsu_xml+=F'''     <writeback  ddr_base_addr="{ag_list[i].ddr_addr}"  local_base_addr="0" write_times="{ag_list[i].size_data}"  write_stride="{ag_list[i].stride_lsu}" write_cnt="{ag_list[i].cnt_lsu}" is_spm="{ag_list[i].is_spm}" stream_index="{ag_list[i].index}"/>
'''
                spm_xml+=F'''     <stream stream_index="{ag_list[i].index}" mode="wr" pattern="{ag_list[i].pattern}" pow2_mode="{ag_list[i].pow2_mode}" local_row="{ag_list[i].row_local}" local_col="{ag_list[i].col_local}" multi="{ag_list[i].multi_in0}"   stride="{ag_list[i].multi_in1}"  N="{ag_list[i].bank_num}"  />
'''

        pref_num=context.scene.my_prop.pref_num
        wb_num=context.scene.my_prop.wb_num
        pref0=("null","null","null")
        pref1=("null","null","null")
        pref2=("null","null","null")
        wb0=("null","null","null")
        if pref_num>=1:
            pref0=context.scene.my_prop.pref0
        if pref_num>=2:
            pref1=context.scene.my_prop.pref1 
        if pref_num>=3:    
            pref2=context.scene.my_prop.pref2
        if wb_num>=1:
            wb0=context.scene.my_prop.wb0
            
        
        
        if not lsu_xml=='':
            lsu_xml='''
<node type="lsu" index="0">'''+'\n'+lsu_xml+'''     <placement cord="[0, 0]"/>
</node>
'''
        if not spm_xml=='':
            spm_xml='''
<node type="scratchpad" index="0">'''+'\n'+spm_xml+'''     <placement cord="[0, 0]"/>
</node>
'''
        if not is_refine:
            lsu_xml=F'''
<node type="lsu" index="0">
        <prefetch0 ddr_base_addr="{pref0[0]}" local_base_addr="{pref0[1]}" prefetch_times="{pref0[2]}"/>
        <prefetch1 ddr_base_addr="{pref1[0]}" local_base_addr="{pref1[1]}" prefetch_times="{pref1[2]}"/>
        <prefetch2 ddr_base_addr="{pref2[0]}" local_base_addr="{pref2[1]}" prefetch_times="{pref2[2]}"/>
        <writeback0 ddr_base_addr="{wb0[0]}" local_base_addr="{wb0[1]}" write_times="{wb0[2]}"/>
        <placement cord="[0, 0]"/>
</node>
'''
            spm_xml=""
            
        file.write(lsu_xml)

        file.write(spm_xml)        
        bus=bus.strip( '_' )
        str=F'''
<node type="bus" index="0" level="0" end_table="{bus}">
        <placement cord="[0, 0]"/>
</node>
</Config>'''
        file.write(str)
        file.close()

                
        return {"FINISHED"}

############################ xmL操作面板
class xml_Panel(bpy.types.Panel):
    bl_idname = "ysw_panel.xml_panel"
    bl_label = "Test xml"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "test Addon"
    
    

    def draw(self, context):
        layout = self.layout
        my_prop=context.scene.my_prop
        layout.row().prop(my_prop, 'is_refine')
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.xml")
        
  
############################# 位置操作类
class Test_OT_Location(bpy.types.Operator):
    bl_idname = "ysw_operator.location"
    bl_label = "set_Location"
    bl_description = "插件开发测试"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #print(bpy.context.space_data.node_tree.name)
        #print("Hello, is me.")
        node_map=dict()
        
        Tree_key=bpy.context.space_data.node_tree.name
        for node in bpy.data.node_groups[Tree_key].nodes:
            if not (node.delay_level in node_map.keys()):
                node_map[node.delay_level]=1
                
                
            else:
                node_map[node.delay_level]+=1
                
        
        level_index=0
        node_queue=Queue()
        
        for node in bpy.data.node_groups[Tree_key].nodes:
            this_node_is_linked=0;
            for output in node.outputs:
                if output.is_linked:
                    this_node_is_linked=1
            if (not this_node_is_linked):
                  node_queue.put(node)    
        
        node_changed=dict()
        level_count={}
        while not node_queue.empty():
            
            node_get=node_queue.get()
            if(node_get in node_changed.keys()):
                continue
            
            node_changed[node_get]=1
            if not node_get.delay_level in level_count.keys():
                level_count[node_get.delay_level]=0
            else:
                level_count[node_get.delay_level]+=1
            node_get.location=(-500+200*node_get.delay_level,-50*node_map[node_get.delay_level]+100* level_count[node_get.delay_level])
            
            for input in node_get.inputs:  
                for item in input.links:
                    node_queue.put(item.from_socket.node)
        return {"FINISHED"}
############################# 位置面板
class Location_Panel(bpy.types.Panel):
    bl_idname = "ysw_panel.location_panel"
    bl_label = "Test Location"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "test Addon"

    def draw(self, context):
        layout = self.layout
        
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.location")      

############################ index 批处理操作类
class Test_OT_index_add(bpy.types.Operator):
    bl_idname = "ysw_operator.index_add"
    bl_label = "index_add"
    bl_description = "index 批加法"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = context.selected_nodes
        my_prop=context.scene.my_prop
        for node in selection:
            node.index=node.index+my_prop.index_add
        return {"FINISHED"}
            

# ############################ index 批处理操作面板
# class Test_PT_indexPanel(bpy.types.Panel):
#     bl_idname = "ysw_panel.index_panel"
#     bl_label = "Test index"
#     bl_space_type = "NODE_EDITOR"
#     bl_region_type = "UI"
#     bl_category = "test Addon"

#     def draw(self, context):
#         layout = self.layout
#         my_prop=context.scene.my_prop
#         layout.row().prop(my_prop, 'index_add')
#         # 创建一个行按钮
#         row = layout.row()
#         # 设置按钮执行的操作【填写操作的bl_idname】
#         row.operator("ysw_operator.index_add")
        
############################ note 批处理操作类
class Test_OT_note(bpy.types.Operator):
    bl_idname = "ysw_operator.node_note"
    bl_label = "node_note"
    bl_description = "node_note 批设定"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = context.selected_nodes
        my_prop=context.scene.my_prop
        for node in selection:
            node.note=my_prop.node_note
        return {"FINISHED"}
            

        
        ############################ key_cal 批处理操作类
class Test_OT_key_cal(bpy.types.Operator):
    bl_idname = "ysw_operator.key_cal"
    bl_label = "key_cal"
    bl_description = "key_cal 批设定"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = context.selected_nodes
        my_prop=context.scene.my_prop
        for node in selection:
            if(node.bl_label=="PE"):
                node.key_cal=my_prop.key_cal
        return {"FINISHED"}
    
        ############################ opcode 批处理操作类
class Test_OT_opcode(bpy.types.Operator):
    bl_idname = "ysw_operator.opcode"
    bl_label = "opcode"
    bl_description = "opcode 批设定"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = context.selected_nodes
        my_prop=context.scene.my_prop
        for node in selection:
            if(node.bl_label=="PE"):
                node.opcode=my_prop.opcode
        return {"FINISHED"}
            

############################  批处理操作面板
class Test_PT_batch_Panel(bpy.types.Panel):
    bl_idname = "ysw_panel.batch"
    bl_label = "Test batch"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "test Addon"

    def draw(self, context):
        layout = self.layout
        my_prop=context.scene.my_prop
        layout.row().prop(my_prop, 'key_cal')
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.key_cal")
        
        layout.row().prop(my_prop, 'node_note')
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.node_note")
        
        layout.row().prop(my_prop, 'opcode')
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.opcode")
        
        layout.row().prop(my_prop, 'index_add')
        # 创建一个行按钮
        row = layout.row()
        # 设置按钮执行的操作【填写操作的bl_idname】
        row.operator("ysw_operator.index_add")
        
        


############################ lsu面板
class Test_PT_lsuPanel(bpy.types.Panel):
    bl_idname = "ysw_panel.lsu"
    bl_label = "Test lsu"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "test Addon"

    def draw(self, context):
        layout = self.layout
        my_prop=context.scene.my_prop
        layout.row().prop(my_prop, 'pref_num')
        layout.row().prop(my_prop, 'wb_num')
        pref_num=my_prop.pref_num
        wb_num=my_prop.wb_num
        if pref_num>=1:
            layout.row().prop(my_prop, 'pref0')
        if pref_num>=2:
            layout.row().prop(my_prop, 'pref1')
        if pref_num>=3:    
            layout.row().prop(my_prop, 'pref2')
        if wb_num>=1:
            layout.row().prop(my_prop, 'wb0')
        