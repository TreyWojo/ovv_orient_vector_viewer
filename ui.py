import bpy
from bpy.types import Panel, Menu

MATH_NODES = {"VV Axis Angle to Quat": ".vv_axis_angle_to_quat",
              "VV Inverse Quat": ".vv_inverse_quat",
              "VV Quat Dot Product": ".vv_quat_dot",
              "VV Switch Quat": ".vv_quat_field_switch",
              "VV Quat Multiply": ".vv_quat_multiply",
              "VV Normalize Quat": ".vv_normalize_quat",
              "VV Quat Negate": ".vv_quat_negate",
              "VV Rotation to Quat": ".vv_rot_to_quat",
              "VV Quat Slerp": ".vv_quat_slerp",
              "VV Quat to Axis Angle": ".vv_quat_to_axis_angle",
              "VV Quat to Rotation": ".vv_quat_to_rot",
              "VV Quat Power": ".vv_raise_quat_to_t",
              "VV Matrix Lerp":".vv_matrix_lerp",
              }

class VECTORVIEWER_PT_Sidebar(Panel):
    bl_label: str = "Vector Viewer"
    bl_idname: str = "VECTORVIEWER_PT_Sidebar"
    bl_space_type: str = "NODE_EDITOR"
    bl_region_type: str = "UI"
    bl_category:str = "Vector Viewer"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == "GeometryNodeTree"

    def draw(self, layout):
        layout = self.layout
        layout.label(text="Testing auto update")
        layout.operator('vv.create_vector_viewer', text="Add Viewer Node")


class NODE_MT_Submenu(Menu):
    bl_label: str = "Vector Viewer Add Menu"
    bl_idname: str = "VV_MT_Menu"
    bl_space_type: str = "NODE_EDITOR"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == "GeometryNodeTree"

    def draw(self, layout):
        layout = self.layout
        layout.operator('vv.create_vector_viewer', text="Vector Viewer")


class NODE_MT_mathMenu(Menu):
    bl_label: str = "Math Operations"
    bl_idname: str = "VV_MT_Math_Menu"
    bl_space_type: str = "NODE_EDITOR"

    def draw(self, layout):
        layout = self.layout
        for key, value in MATH_NODES.items():
            op = layout.operator('vv.create_quat_node', text=key)
            op.node_to_import = value
            op.node_label = key


def draw_submenu(self, context):
    if context.area.ui_type == "GeometryNodeTree":
        self.layout.menu("VV_MT_Menu", text="Vector Viewer")
        self.layout.menu("VV_MT_Math_Menu", text ="VV Math Operations")


def setup_keyconfig():
    key_config = bpy.context.window_manager.keyconfigs.addon
    if key_config:
        key_map = key_config.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
        key_entry = key_map.keymap_items.new("vv.create_vector_viewer", 
                                             type='V', value="PRESS")
        #key_entry.properties.name = "OT_create_vector_viewer_node"


def register():
    bpy.utils.register_class(VECTORVIEWER_PT_Sidebar)
    bpy.utils.register_class(NODE_MT_Submenu)
    bpy.utils.register_class(NODE_MT_mathMenu)
    setup_keyconfig()
    bpy.types.NODE_MT_add.append(draw_submenu)


def unregister():
    bpy.utils.unregister_class(VECTORVIEWER_PT_Sidebar)
    bpy.utils.unregister_class(NODE_MT_Submenu)
    bpy.utils.unregister_class(NODE_MT_mathMenu)
    bpy.types.NODE_MT_add.remove(draw_submenu)
