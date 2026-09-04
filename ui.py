import bpy
from bpy.types import Panel, Menu

MATH_NODES = {"OVV Axis Angle to Quat": ".ovv_axis_angle_to_quat",
              "OVV Inverse Quat": ".ovv_inverse_quat",
              "OVV Quat Dot Product": ".ovv_quat_dot",
              "OVV Switch Quat": ".ovv_quat_field_switch",
              "OVV Quat Multiply": ".ovv_quat_multiply",
              "OVV Normalize Quat": ".ovv_normalize_quat",
              "OVV Quat Negate": ".ovv_quat_negate",
              "OVV Rotation to Quat": ".ovv_rot_to_quat",
              "OVV Quat Slerp": ".ovv_quat_slerp",
              "OVV Quat to Axis Angle": ".ovv_quat_to_axis_angle",
              "OVV Quat to Rotation": ".ovv_quat_to_rot",
              "OVV Quat Power": ".ovv_raise_quat_to_t",
              "OVV Matrix Lerp":".ovv_matrix_lerp",
              }

class VECTORVIEWER_PT_Sidebar(Panel):
    bl_label: str = "OVV Orient Vector Viewer"
    bl_idname: str = "OVV_PT_Sidebar"
    bl_space_type: str = "NODE_EDITOR"
    bl_region_type: str = "UI"
    bl_category:str = "OVV"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == "GeometryNodeTree"

    def draw(self, layout):
        layout = self.layout
        layout.label(text="Testing auto update")
        layout.operator('ovv.create_vector_viewer', text="Add OVV Node")


class NODE_MT_Submenu(Menu):
    bl_label: str = "Vector Viewer Add Menu"
    bl_idname: str = "OVV_MT_Menu"
    bl_space_type: str = "NODE_EDITOR"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == "GeometryNodeTree"

    def draw(self, layout):
        layout = self.layout
        layout.operator('ovv.create_vector_viewer', text="OVV")


class NODE_MT_mathMenu(Menu):
    bl_label: str = "Math Operations"
    bl_idname: str = "OVV_MT_Math_Menu"
    bl_space_type: str = "NODE_EDITOR"

    def draw(self, layout):
        layout = self.layout
        for key, value in MATH_NODES.items():
            op = layout.operator('ovv.create_quat_node', text=key)
            op.node_to_import = value
            op.node_label = key


def draw_submenu(self, context):
    if context.area.ui_type == "GeometryNodeTree":
        self.layout.menu("OVV_MT_Menu", text="Orient Vector Viewer")
        self.layout.menu("OVV_MT_Math_Menu", text ="OVV Math Operations")


def setup_keyconfig():
    key_config = bpy.context.window_manager.keyconfigs.addon
    if key_config:
        key_map = key_config.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")
        key_entry = key_map.keymap_items.new("ovv.create_vector_viewer", 
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
