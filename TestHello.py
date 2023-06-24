# 与节点部分无关


import bpy
import os
# 操作类
class Test_OT_Hello(bpy.types.Operator):
    bl_idname = "my_operator.hello"
    bl_label = "Hello!"
    bl_description = "插件开发测试"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print("Hello, is me.")
        
        return {"FINISHED"}
