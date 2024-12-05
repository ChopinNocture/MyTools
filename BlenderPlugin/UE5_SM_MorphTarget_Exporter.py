bl_info = {
    "name": "Export UE5 Static Mesh Morph Target",
    "blender": (3, 50, 0),
    "category": "Gearllusion",
}


import bpy
import mathutils

# 创建面板界面
class MorphTargetPanel(bpy.types.Panel):
    bl_label = "Static Mesh Morph Targets"  # 面板标题
    bl_idname = "OBJECT_PT_morph_targets"   # 面板 ID
    bl_space_type = 'VIEW_3D'               # 面板显示在3D视图中
    bl_region_type = 'UI'                   #'WINDOW'  # 面板显示在UI区域
    bl_category = 'Gearllusion'             # 面板所属的选项卡

    def draw(self, context):
        layout = self.layout

        layout.operator("object.pick_original_mesh", text="Pick Original Mesh")
        layout.operator("object.pick_morph_target_1", text="Pick Morph Target 1")
        layout.operator("object.pick_morph_target_2", text="Pick Morph Target 2")
        layout.operator("object.process_morph_targets", text="Pack Morph Targets")


# 操作：选择原始网格
class PickOriginalMeshOperator(bpy.types.Operator):
    bl_idname = "object.pick_original_mesh"
    bl_label = "Pick Original Mesh"
    
    def execute(self, context):
        # 这里可以通过用户选择网格来设置 original_mesh 变量
        context.scene.original_mesh = bpy.context.view_layer.objects.active
        return {'FINISHED'}


# 操作：选择形态目标1
class PickMorphTarget1Operator(bpy.types.Operator):
    bl_idname = "object.pick_morph_target_1"
    bl_label = "Pick Morph Target 1"
    
    def execute(self, context):
        # 这里可以通过用户选择网格来设置 target_1 变量
        context.scene.target_1 = bpy.context.view_layer.objects.active
        return {'FINISHED'}


# 操作：选择形态目标2
class PickMorphTarget2Operator(bpy.types.Operator):
    bl_idname = "object.pick_morph_target_2"
    bl_label = "Pick Morph Target 2"
    
    def execute(self, context):
        # 这里可以通过用户选择网格来设置 target_2 变量
        context.scene.target_2 = bpy.context.view_layer.objects.active
        return {'FINISHED'}


# 操作：处理形态目标
class ProcessMorphTargetsOperator(bpy.types.Operator):
    bl_idname = "object.process_morph_targets"
    bl_label = "Process Morph Targets"
    
    def execute(self, context):
        original_mesh = context.scene.original_mesh
        target_1 = context.scene.target_1
        target_2 = context.scene.target_2

        if not original_mesh or not target_1:
            self.report({'ERROR'}, "Original Mesh or Morph Target 1 is missing!")
            return {'CANCELLED'}
        
        # 这里进行顶点处理和存储到UV通道的操作
        # 例如，计算偏移量和法线，并存储到顶点颜色或UV通道

        return {'FINISHED'}


###------------------------------------------------------
classes = (
    MorphTargetPanel,
    PickOriginalMeshOperator,
    PickMorphTarget1Operator,
    PickMorphTarget2Operator,
    ProcessMorphTargetsOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
