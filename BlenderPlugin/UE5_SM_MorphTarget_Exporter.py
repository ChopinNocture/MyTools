bl_info = {
    "name": "Export UE5 Static Mesh Morph Target",
    "blender": (3, 50, 0),
    "category": "Gearllusion",
}


from functools import wraps
import bpy
from bpy_extras.io_utils import ExportHelper
import bmesh
import math
import mathutils
import numpy as np


def nearest_power_of_2(n):
    return 2 ** math.ceil(math.log2(n))


def nearest_pow2_image_res(n):
    #return math.sqrt(nearest_power_of_2(n))
    if n>0:
        return 2 ** math.ceil(math.log2(math.sqrt(n)))
    return 0


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
def ensure_OP_mode(mode='EDIT'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):        
            if bpy.context.mode != mode:
                bpy.ops.object.mode_set(mode=mode)
            return func(*args, **kwargs)    
        return wrapper
    return decorator


def check_UV_layer_exist(uv_name="UV_ShapeKeys"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure active object exists and is a mesh
            obj = bpy.context.object
            if obj is None or obj.type != 'MESH':
                raise RuntimeError("Active object must be a mesh.")
            
            # Access the UV layers
            uv_layers = obj.data.uv_layers
            
            # Check if the UV layer with the specified name exists
            if uv_name not in uv_layers:
                # Create a new UV layer with the specified name
                uv_layer = uv_layers.new(name=uv_name)
                print(f"Created UV layer: {uv_layer.name}")
            else:
                print(f"UV layer '{uv_name}' already exists.")
            
            # Set the specified UV layer as active
            obj.data.uv_layers.active = obj.data.uv_layers[uv_name]

            # Call the wrapped function
            return func(*args, **kwargs)
        return wrapper
    return decorator


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


# @check_mesh_selected
# @ensure_OP_mode(mode='OBJECT')
# def ensure_uv_for_all_vertices(obj, uv_idx):
#     if uv_idx >= 0 and uv_idx<len(obj.data.uv_layers):
#         obj.data.uv_layers.active = obj.data.uv_layers[uv_idx]
#         uv_layer = obj.data.uv_layers.active
        
#         uv_data = uv_layer.data

#         # 如果 UV 层的顶点数量少于网格的顶点数量，则为缺失的顶点添加默认 UV 坐标
#         num_vertices = len(obj.data.vertices)
        
#         if len(uv_data) < num_vertices:
#             print(f"UV 层 '{uv_layer.name}' 有缺失的顶点 UV，正在填充... {len(uv_data)}")
#             # 遍历网格的每个顶点，为每个缺失的 UV 坐标分配默认值
#             for i in range(num_vertices):
#                 if i >= len(uv_data):
#                     # 为缺失的顶点设置默认的 UV 坐标 (例如：(0.0, 0.0))
#                     uv_data.add(count=1)
#                 uv_data[i].uv = (0.0, 0.0)  # 默认的 UV 坐标                
#         else:
#             print(f"UV 层 '{uv_layer.name}' 已包含所有顶点的 UV 坐标")


@check_mesh_selected
@ensure_OP_mode(mode='EDIT')
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
            normal *= (-1.0, -1.0, 1.0)
            normal = (normal + 1.0) * 0.5
            #normal *= 255.0
            # 将法线转换为0到1的范围，Blender的法线范围是[-1, 1]，需要将其转换
            color.color = normal # [(normal.x + 1) * 0.5, (normal.y + 1) * 0.5, (normal.z + 1) * 0.5]

    mesh.update()

    bmesh.update_edit_mesh(mesh)


def get_morph_vertex_offsets(base_shape, morph_shape):
    base_verts = base_shape.data
    morph_verts = morph_shape.data
    offset_list = []

    length = len(base_verts)
    # 遍历所有顶点，计算 Basis 和目标形状键的差值
    for vert_index in range(0, length):
        #---------------------------
        # 获取顶点坐标 计算偏移量
        basis_pos = base_verts[vert_index].co
        target_pos = morph_verts[vert_index].co

        offset_normalized = (target_pos - basis_pos)  # 差值
        offset_list.append(offset_normalized)

    return offset_list


def get_morph_vertex_normals(obj, morph_shape):
    mesh = obj.data.copy()
    bm = bmesh.new()
    bm.from_mesh(mesh)

    morph_verts = morph_shape.data
    normal_list = []

    # 替换网格的顶点位置为当前形状键的顶点位置
    for vert, sk_data in zip(bm.verts, morph_verts):
        vert.co = sk_data.co
    
    # 重新计算顶点法线
    bm.normal_update()

    for v in bm.verts:
        normal = v.normal.copy()
        normal *= mathutils.Vector((1.0, -1.0, 1.0)) 
        normal = (normal + mathutils.Vector((1.0, 1.0, 1.0))) * mathutils.Vector((0.5, 0.5, 0.5))
        normal_list.append(normal)
    
    # 清理临时数据
    bm.free()
    bpy.data.meshes.remove(mesh)

    return normal_list


@ensure_OP_mode(mode='OBJECT')
def pack_shape_vertex_offset_to_uv(base_shape, morph_shape, obj, is_target1=True):
    offset_list = get_morph_vertex_offsets(base_shape, morph_shape)

    if is_target1:
        # shape1存储到 UV 通道2v,3
        for loop in obj.data.loops:
            offset_normalized = offset_list[loop.vertex_index]
            
            obj.data.uv_layers.active = obj.data.uv_layers[2]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv.y = (1-offset_normalized.x)
            # uv_layer[loop.index].uv.y = offset_normalized.x

            obj.data.uv_layers.active = obj.data.uv_layers[3]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv = (-offset_normalized.y, (1-offset_normalized.z))
            # uv_layer[loop.index].uv = offset_normalized.y, offset_normalized.z
    else:
        # shape2存储到 UV 通道1,2u
        for loop in obj.data.loops :
            offset_normalized = offset_list[loop.vertex_index]
            
            obj.data.uv_layers.active = obj.data.uv_layers[1]
            uv_layer = obj.data.uv_layers.active.data
            uv_layer[loop.index].uv = (offset_normalized.x, (1 + offset_normalized.y))
            # uv_layer[loop.index].uv = offset_normalized.x, offset_normalized.y

            obj.data.uv_layers.active = obj.data.uv_layers[2]
            uv_layer = obj.data.uv_layers.active.data
            # uv_layer[loop.index].uv.x = 255 * offset_normalized.z
            uv_layer[loop.index].uv.x = offset_normalized.z
    # 更新视图
    bpy.context.view_layer.update()


#================================================
# 图片方案

UV_LAY_NAME = "UV_ShapeKeys"

# Save the image
def save_shape_image(pixels, size, file_path, is_normal = False):
    image = bpy.data.images.get(IMAGE_NAME)
    if image:
        # 强制清除引用
        image.user_clear()
        bpy.data.images.remove(image)
    
    image = bpy.data.images.new(IMAGE_NAME, width=size, height=size, alpha=False, float_buffer=True, is_data=True)
    image.pixels = pixels
    image.filepath_raw = bpy.path.abspath(f"//{file_path}")
    image.file_format = 'BMP' if is_normal else 'OPEN_EXR' # 
    image.save()


@ensure_OP_mode(mode='OBJECT')
@check_UV_layer_exist(UV_LAY_NAME)
def write_shape_vertex_UV():
    obj = bpy.context.object
    verts = obj.data.vertices
    
    size = nearest_pow2_image_res(len(verts))
    
    uv_layer = obj.data.uv_layers.active.data

    # 将每个顶点的像素位置映射到 UV 层
    for loop in obj.data.loops :
        i = loop.vertex_index
        pixel_x = ((i % size) + 0.5) / size  # 将顶点索引映射到图像的宽度范围 [0, 1]
        pixel_y = ((i // size) + 0.5) / size  # 将顶点索引映射到图像的高度范围 [0, 1]
        uv_layer[loop.index].uv = (pixel_x, pixel_y)


IMAGE_NAME = "Image_Shape_Keys"
@check_mesh_selected
def write_shape_into_image(base_shape, morph_shape, file_path):
    offset_list = get_morph_vertex_offsets(base_shape, morph_shape)
    number_of_verts = len(offset_list)

    size = int(nearest_pow2_image_res(number_of_verts))
    print(f"size = {size}   number_of_verts = {number_of_verts}")
    pixels = [0.0] * (size * size * 4)  # 纹理图像的像素（RGBA）
    
    for i in range(0, number_of_verts):
        pixel_index = i * 4
        offset = offset_list[i]
        
        if pixel_index < len(pixels):
            pixels[pixel_index] = offset.x
            pixels[pixel_index + 1] = -offset.y
            pixels[pixel_index + 2] = offset.z
            pixels[pixel_index + 3] = 1.0
    # image = bpy.data.images.new(IMAGE_NAME, width=size, height=size)
    # Save the image using PIL
    # img = Image.fromarray(pixels, "RGB")
    # img.save(file_path)
    
    save_shape_image(pixels, size, file_path)


@check_mesh_selected
def write_all_shape_into_image(base_shape, shape_list, number_of_verts, file_path):
    num_shape = len(shape_list)
    row_num = math.ceil(math.sqrt(num_shape))
    size = int(nearest_pow2_image_res(number_of_verts))
    size_all = size * row_num
    if size_all >= 8192:
        raise RuntimeError("Max image size can not larger than 8192.")
    
    pixels = [0.0] * (size_all * size_all * 4)  # 纹理图像的像素（RGBA）

    for iter in range(len(shape_list)):
        morph_shape = shape_list[iter]
        offset_list = get_morph_vertex_offsets(base_shape, morph_shape)
        col_idx = (iter % row_num) * size
        row_idx = (row_num - 1 - (iter // row_num)) * size
        for i in range(0, number_of_verts):
            pixel_index = ((row_idx + (i//size)) * size_all + col_idx + (i%size)) * 4
            offset = offset_list[i]            
            if pixel_index < len(pixels):
                pixels[pixel_index] = offset.x
                pixels[pixel_index + 1] = -offset.y
                pixels[pixel_index + 2] = offset.z
                pixels[pixel_index + 3] = 1.0
                
    print(f"size = {size}   number_of_verts = {number_of_verts}    row = {row_num}")
    
    save_shape_image(pixels, size_all, file_path)


@check_mesh_selected
def write_all_shape_normal_into_image(obj, shape_list, number_of_verts, file_path):
    num_shape = len(shape_list)
    row_num = math.ceil(math.sqrt(num_shape))
    size = int(nearest_pow2_image_res(number_of_verts))
    size_all = size * row_num
    if size_all >= 8192:
        raise RuntimeError("Max image size can not larger than 8192.")
    
    pixels = [0.0] * (size_all * size_all * 4)  # 纹理图像的像素（RGBA）

    for iter in range(len(shape_list)):
        morph_shape = shape_list[iter]
        list = get_morph_vertex_normals(obj, morph_shape)
        col_idx = (iter % row_num) * size
        row_idx = (row_num - 1 - (iter // row_num)) * size
        for i in range(0, number_of_verts):
            pixel_index = ((row_idx + (i//size)) * size_all + col_idx + (i%size)) * 4
            v = list[i]            
            if pixel_index < len(pixels):
                pixels[pixel_index] = v.x
                pixels[pixel_index + 1] = v.y
                pixels[pixel_index + 2] = v.z
                pixels[pixel_index + 3] = 0.0
                
    print(f"size = {size}   number_of_verts = {number_of_verts}    row = {row_num}")
    
    save_shape_image(pixels, size_all, file_path, True)

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

        # 创建一个新的列，这将创建一个垂直的空间，可以用来分组按钮
        layout.label(text="<UE>: Static Mesh Morph Targets:")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator(OperatorPickMorphTarget1.bl_idname, text="Pick Morph Target 1")
        row = col.row(align=True)
        row.operator(OperatorPickMorphTarget2.bl_idname, text="Pick Morph Target 2")

        #
        layout.label(text="<Gearllusion> Shape to Image:")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator(OpCreateVertex2PixelUV.bl_idname, text="创建顶点UV")

        row = col.row(align=True)
        row.operator(OpActiveShape2Image.bl_idname, text="当前Shape写入图片")

        row = col.row(align=True)
        row.operator(OpAllShape2Image.bl_idname, text="把所有Shape写入图片")

        row = col.row(align=True)
        row.operator(OpAllShapeNormal2Image.bl_idname, text="Shape法线写入图片")

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


# Image solution
class OpCreateVertex2PixelUV(bpy.types.Operator):
    bl_idname = "object.create_vertex_to_pixel_uv"
    bl_label = "Create vertex to pixel UV"
    
    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        if not obj:
            return {'CANCELLED'}
        write_shape_vertex_UV()
        return {'FINISHED'}


class OpActiveShape2Image(bpy.types.Operator, ExportHelper):
    bl_idname = "object.active_shape_to_image"
    bl_label = "Write Selected Shape into Picture"
    
    filename_ext = ".exr"
    filter_glob: bpy.props.StringProperty(default="*.exr", options={'HIDDEN'})

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
        
        base_shape = shape_keys.reference_key
        morph_target = shape_keys.key_blocks[idx]
        write_shape_into_image(base_shape, morph_target, self.filepath)

        #write_shape_vertex_UV()
        return {'FINISHED'}
    

class OpAllShape2Image(bpy.types.Operator, ExportHelper):
    bl_idname = "object.all_shape_to_image"
    bl_label = "Write All Shapes into Picture"
    
    filename_ext = ".exr"
    filter_glob: bpy.props.StringProperty(default="*.exr", options={'HIDDEN'})

    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        if not obj:
            return {'CANCELLED'}
        
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            print("对象没有形态键！")
            return {'CANCELLED'}
        if len(shape_keys.key_blocks) <=1: 
            print("没有形态！！")
            return {'CANCELLED'}
        
        number_of_verts = len(obj.data.vertices)
        
        base_shape = shape_keys.reference_key

        # shape_list = [key.name for key in shape_keys if key.name != 'Basis']
        shape_list = [key for key in shape_keys.key_blocks if key.name != 'Basis' and key.mute == False ]
        # for i in range(1, len(shape_keys.key_blocks)):
        #     shape_list.append(shape_keys.key_blocks[i])

        write_all_shape_into_image(base_shape, shape_list, number_of_verts, self.filepath)

        return {'FINISHED'}


class OpAllShapeNormal2Image(bpy.types.Operator, ExportHelper):
    bl_idname = "object.all_shape_normal_to_image"
    bl_label = "Write Shape Normals into Picture"
    
    filename_ext = ".bmp"
    filter_glob: bpy.props.StringProperty(default="*.bmp", options={'HIDDEN'})

    def execute(self, context):
        obj = bpy.context.view_layer.objects.active
        if not obj:
            return {'CANCELLED'}
        
        shape_keys = obj.data.shape_keys

        if not shape_keys:
            print("对象没有形态键！")
            return {'CANCELLED'}
        if len(shape_keys.key_blocks) <=1: 
            print("没有形态！！")
            return {'CANCELLED'}
        
        number_of_verts = len(obj.data.vertices)
        shape_list = [key for key in shape_keys.key_blocks if key.name != 'Basis' and key.mute == False ]

        write_all_shape_normal_into_image(obj, shape_list, number_of_verts, self.filepath)

        return {'FINISHED'}
    

###------------------------------------------------------
classes = (
    OperatorPickMorphTarget1,
    OperatorPickMorphTarget2,
    OpCreateVertex2PixelUV,
    OpActiveShape2Image,
    OpAllShape2Image,
    OpAllShapeNormal2Image, 
    MorphTargetPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
