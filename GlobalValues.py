import bpy

class My_settings(bpy.types.PropertyGroup):
    is_refine: bpy.props.BoolProperty(
        name='is_refine',
        default=True
    )
   
    index_add: bpy.props.IntProperty(
        name='index_add',
        default=1
    )
    
    node_note:bpy.props.StringProperty(
        name='node_note',
        default=""
    )
    
    key_cal:bpy.props.BoolProperty(
        name='key_cal',
        default=True
    )
    
    opcode:bpy.props.StringProperty(
        name='opcode',
        default=""
    )
    
    pref_num:bpy.props.IntProperty(
        name='pref_num',
        default=1,
        min=0,
        max=3
    )
    
    wb_num:bpy.props.IntProperty(
        name='wb_num',
        default=1,
        min=0,
        max=1
    )
    
    pref0:bpy.props.IntVectorProperty(
        name='pref0',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref1:bpy.props.IntVectorProperty(
        name='pref1',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref2:bpy.props.IntVectorProperty(
        name='pref2',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref3:bpy.props.IntVectorProperty(
        name='pref3',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref4:bpy.props.IntVectorProperty(
        name='pref4',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref5:bpy.props.IntVectorProperty(
        name='pref5',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref6:bpy.props.IntVectorProperty(
        name='pref6',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref7:bpy.props.IntVectorProperty(
        name='pref7',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref8:bpy.props.IntVectorProperty(
        name='pref8',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref9:bpy.props.IntVectorProperty(
        name='pref9',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref10:bpy.props.IntVectorProperty(
        name='pref10',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref11:bpy.props.IntVectorProperty(
        name='pref11',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref12:bpy.props.IntVectorProperty(
        name='pref12',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref13:bpy.props.IntVectorProperty(
        name='pref13',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    
    pref14:bpy.props.IntVectorProperty(
        name='pref14',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    pref15:bpy.props.IntVectorProperty(
        name='pref15',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )
    
    wb0:bpy.props.IntVectorProperty(
        name='wb0',
        default=(0,0,16384),
        min=0,
        max=2 ** 31 - 1,
        size=3
    )