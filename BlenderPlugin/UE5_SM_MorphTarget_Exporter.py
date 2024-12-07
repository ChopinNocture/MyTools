bl_info = {
    "name": "Export UE5 Static Mesh Morph Target",
    "blender": (3, 50, 0),
    "category": "Gearllusion",
}


from functools import wraps
import bpy
import bmesh
import math
import mathutils


def nearest_power_of_2(n):
    return 2 ** math.ceil(math.log2(n))

def check_mesh_selected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = bpy.context.view_layer.objects.active # bpy.context.object
        err_text = ""
        if obj is None:
            err_text = "没有活动对象，无法执行操作。"
            print(err_text)
            raise ValueError(err_text)
        
        if obj.type != 'MESH':
            err_text = "活动对象必须是一个网格对象。"
            print(err_text)
            raise ValueError(err_text)
        return func(*args, **kwargs)    
    return wrapper


# 确保对象处于Edit Mode
def ensure_edit_mode(func):
    @wraps(func)
    def wrapper(*args, **kwargs):        
        if bpy.context.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        return func(*args, **kwargs)    
    return wrapper

#----------------
# 确保4个UV
@check_mesh_selected
def ensure_uv_layers(obj, required_layers=4):
    # 获取当前的 UV 层数量
    current_uv_layers = len(obj.data.uv_layers)
    print(f"当前 UV 层数量: {current_uv_layers}")

    # 如果 UV 层少于所需数量，则创建新的 UV 层
    for i in range(current_uv_layers, required_layers):
        uv_layer = obj.data.uv_layers.new(name=f"uv_morph{i}")
        obj.data.uv_layers.active = uv_layer
        for j, v in enumerate(obj.data.vertices):
            uv_layer.data[j].uv = (0.0, 0.0)
        print(f"已创建 UV 层 {i + 1}")


@check_mesh_selected
def ensure_uv_for_all_vertices(obj, uv_idx):
    if uv_idx >= 0 and uv_idx<len(obj.data.uv_layers):
        obj.data.uv_layers.active = obj.data.uv_layers[uv_idx]
        uv_layer = obj.data.uv_layers.active
        
        uv_data = uv_layer.data

        # 如果 UV 层的顶点数量少于网格的顶点数量，则为缺失的顶点添加默认 UV 坐标
        num_vertices = len(obj.data.vertices)
        
        if len(uv_data) < num_vertices:
            print(f"UV 层 '{uv_layer.name}' 有缺失的顶点 UV，正在填充... {len(uv_data)}")
            # 遍历网格的每个顶点，为每个缺失的 UV 坐标分配默认值
            for i in range(num_vertices):
                if i >= len(uv_data):
                    # 为缺失的顶点设置默认的 UV 坐标 (例如：(0.0, 0.0))
                    uv_data.add(count=1)
                uv_data[i].uv = (0.0, 0.0)  # 默认的 UV 坐标
                
        else:
            print(f"UV 层 '{uv_layer.name}' 已包含所有顶点的 UV 坐标")


@check_mesh_selected
@ensure_edit_mode
def pack_normals_into_vertex_color(mesh):
     # 获取BMesh数据
    bm = bmesh.from_edit_mesh(mesh)

    normals = []
    for v in bm.verts:
        normals.append(v.normal.copy())

    # 如果对象没有顶点颜色层，则创建一个
    if not mesh.vertex_colors:
        mesh.vertex_colors.new(name="MorphNormal")

    color_layer = mesh.vertex_colors.active.data

    # 确保顶点数量与法线数量匹配
    for i, color in enumerate(color_layer):
        if i < len(normals):
            normal = normals[i]
            normal *= (1.0, -1.0, 1.0)
            normal = (normal + 1.0) * 0.5
            normal *= 255.0
            # 将法线转换为0到1的范围，Blender的法线范围是[-1, 1]，需要将其转换
            color.color = normal # [(normal.x + 1) * 0.5, (normal.y + 1) * 0.5, (normal.z + 1) * 0.5]

    mesh.update()

    bmesh.update_edit_mesh(mesh)


#@ensure_edit_mode
def pack_shape_vertex_offset_to_uv(base_shape, morph_shape, obj, is_target1=True):
    base_verts = base_shape.data
    morph_verts = morph_shape.data
    offset_list = []

    length = len(base_verts)
    # 遍历所有顶点，计算 Basis 和目标形状键的差值
    for vert_index in range(0, length):
        # 获取顶点坐标
        basis_pos = base_verts[vert_index].co
        
        #---------------------------
        # 计算偏移量
        target_pos = morph_verts[vert_index].co
        offset = (target_pos - basis_pos)  # 差值
        # 压缩到 [0,1] 范围        
        offset_normalized = (offset + mathutils.Vector((1.0, 1.0, 1.0))) * 0.5  # [-1,1] -> [0,1]
        offset_list.append(offset_normalized)

    if is_target1:
        # shape1存储到 UV 通道2v,3
        for loop in obj.data.loops :
            offset_normalized = offset_list[loop.vertex_index]
            
            obj.data.uv_layers.active = obj.data.uv_layers[2]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv.y = (1-offset_normalized.x) * 255.0

            obj.data.uv_layers.active = obj.data.uv_layers[3]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv = (-255.0 * offset_normalized.y, 255 * (1-offset_normalized.z))
    else:
        # shape2存储到 UV 通道1,2u
        for loop in obj.data.loops :
            offset_normalized = offset_list[loop.vertex_index]
            
            obj.data.uv_layers.active = obj.data.uv_layers[1]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv = (255.0 * offset_normalized.x, 255.0 * (1 + offset_normalized.y))

            obj.data.uv_layers.active = obj.data.uv_layers[2]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv.x = 255 * offset_normalized.z


    # 更新视图
    bpy.context.view_layer.update()


#=======================================================
# 创建面板界面
class MorphTargetPanel(bpy.types.Panel):
    bl_label = "Static Mesh Morph Targets"  # 面板标题
    bl_idname = "OBJECT_PT_morph_targets"   # 面板 ID
    bl_space_type = 'VIEW_3D'               # 面板显示在3D视图中
    bl_region_type = 'UI'                   #'WINDOW'  # 面板显示在UI区域
    bl_category = 'Gearllusion'             # 面板所属的选项卡

    def draw(self, context):
        layout = self.layout

        layout.operator("object.pick_morph_target_1", text="Pick Morph Target 1")
        layout.operator("object.pick_morph_target_2", text="Pick Morph Target 2")


# 操作：选择形态目标1
class OperatorPickMorphTarget1(bpy.types.Operator):
    bl_idname = "object.pick_morph_target_1"
    bl_label = "Pack Morph Target 1"
    
    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        if not obj:
            return {'CANCELLED'}
        
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            print("对象没有形态键！")
            return {'CANCELLED'}
        
        idx = bpy.context.object.active_shape_key_index
        if idx == 0:
            print("不能处理Basis形态！")
            return {'CANCELLED'}
        
        # 这里进行顶点处理和存储到UV通道的操作
        # 例如，计算偏移量和法线，并存储到顶点颜色或UV通道
        
        pack_normals_into_vertex_color(obj.data)

        bpy.ops.object.mode_set(mode='OBJECT')
        base_shape = shape_keys.reference_key
        morph_target = shape_keys.key_blocks[idx]

        ensure_uv_layers(obj)
        # ensure_uv_for_all_vertices(obj, 1)
        
        pack_shape_vertex_offset_to_uv(base_shape, morph_target, obj)

        #print(obj.data.shape_keys)
        return {'FINISHED'}


# 操作：选择形态目标2
class OperatorPickMorphTarget2(bpy.types.Operator):
    bl_idname = "object.pick_morph_target_2"
    bl_label = "Pack Morph Target 2"
    
    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        if not obj:
            return {'CANCELLED'}
        
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            print("对象没有形态键！")
            return {'CANCELLED'}
        
        idx = bpy.context.object.active_shape_key_index
        if idx == 0:
            print("不能处理Basis形态！")
            return {'CANCELLED'}
        
        # 这里进行顶点处理和存储到UV通道的操作
        # 例如，计算偏移量和法线，并存储到顶点颜色或UV通道

        bpy.ops.object.mode_set(mode='OBJECT')
        base_shape = shape_keys.reference_key
        morph_target = shape_keys.key_blocks[idx]

        ensure_uv_layers(obj)
        
        pack_shape_vertex_offset_to_uv(base_shape, morph_target, obj, False)        
                
        return {'FINISHED'}


###------------------------------------------------------
classes = (
    MorphTargetPanel,
    OperatorPickMorphTarget1,
    OperatorPickMorphTarget2,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
