import bpy
from pathlib import Path
from bpy.types import Operator
from mathutils import Vector

VIS_FILE = Path(__file__).parent / "ovv_orient_vector_vis.blend"
NODE_VER = [1,0,1]
OVV_GROUP_NAME = ".ovv_orient_vector_vis"


class OT_create_vector_viewer_node(Operator):
    bl_idname = "ovv.create_vector_viewer"
    bl_label = "Create Vector Viewer Node"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context) -> bool:
        return is_space_geo_node_tree(context)

    def execute(self, context):
        node_ops = bpy.ops.node
        geo_out = None
        node_tree = context.space_data.edit_tree

        if valid_group := get_custom_node(OVV_GROUP_NAME):
            if active_node := context.active_node:
                if geo_out_pins := check_output_pins_for_geo(active_node):
                    geo_out = geo_out_pins[0]

            node_ops.select(deselect_all=True)
            ovv_node = make_custom_node(node_tree, "GeometryNodeGroup", 
                             location=Vector((self.x, self.y)), 
                             width=225, group=valid_group)

            set_ovv_group_defaults(context, ovv_node)
            if geo_out: node_tree.links.new(geo_out, ovv_node.inputs[0])

            viewer = make_custom_node(node_tree, "GeometryNodeViewer", 
                             Vector((self.x + (ovv_node.width * 1.1), self.y)))

            #setup viewer connections
            viewer.viewer_items.new('GEOMETRY', "Geometry")
            viewer.viewer_items.new('RGBA', "Attribute")
            node_tree.links.new(ovv_node.outputs[0], viewer.inputs[0])
            node_tree.links.new(ovv_node.outputs[1], viewer.inputs[1])
            viewer.domain = 'INSTANCE'
            node_tree.nodes.active = viewer
            node_ops.activate_viewer()
            bpy.ops.transform.translate('INVOKE_DEFAULT', True)

        else:
            self.report({'ERROR'}, "Node group not found")
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        region = context.region.view2d
        ui_scale = context.preferences.system.ui_scale
        region_loc = region.region_to_view(event.mouse_region_x, event.mouse_region_y)
        if region_loc:
            self.x,self.y = region_loc[0]/ui_scale, region_loc[1]/ui_scale
            return self.execute(context)
        self.x, self.y = 0, 0
        return self.execute(context)


class OT_create_quat_node(Operator):
    bl_idname = "ovv.create_quat_node"
    bl_label = "Create Quat Node"
    bl_options = {'REGISTER', 'UNDO'}
    node_to_import: bpy.props.StringProperty()
    node_label: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context) -> bool:
        return is_space_geo_node_tree(context)

    def execute(self, context):
        node_ops = bpy.ops.node
        node_tree = context.space_data.edit_tree

        if valid_group := get_custom_node(self.node_to_import):
            node_ops.select(deselect_all=True)
            make_custom_node(node_tree, "GeometryNodeGroup",
                             Vector((self.x, self.y)), 150, group=valid_group)
            bpy.ops.transform.translate('INVOKE_DEFAULT', True)

        else:
            self.report({'ERROR'}, "Node group not found")
            return {'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):
        region = context.region.view2d
        ui_scale = context.preferences.system.ui_scale
        region_loc = region.region_to_view(event.mouse_region_x, event.mouse_region_y)
        if region_loc:
            self.x,self.y = region_loc[0]/ui_scale, region_loc[1]/ui_scale
            return self.execute(context)
        self.x, self.y = 0, 0
        return self.execute(context)

def is_space_geo_node_tree(context: bpy.types.Context) -> bool:
        space = context.space_data
        return (space.type == "NODE_EDITOR" and 
                space.edit_tree is not None and
                space.edit_tree.type == "GEOMETRY")

def get_linked_nodes_by_idname(node: bpy.types.Node, *, idname:str) -> list[str] | None:
    output_nodes = []

    for out in node.outputs:
        if len(links := out.links) > 0:
            for link in links:
                linked_node = link.to_node
                if linked_node.bl_idname == idname:
                    output_nodes.append(linked_node.name)
    if output_nodes:
        return output_nodes
    return None


def get_active_node_tree(context):
    if type(context.space_data) is bpy.types.SpaceNodeEditor:
        return context.space_data.edit_tree
    return None


def make_custom_node(node_tree: bpy.types.NodeTree, node_type:str, location:Vector, width:int=None, group=None):
    ovv_node = node_tree.nodes.new(node_type)
    if group: ovv_node.node_tree = group 
    ovv_node.location = location
    if width: ovv_node.width = width
    return ovv_node


def check_output_pins_for_geo(node: bpy.types.Node) -> list[bpy.types.NodeSocket] | None:
    valid_geo_outs = []
    for output in node.outputs:
        if output.type == 'GEOMETRY':
            valid_geo_outs.append(output)
    if valid_geo_outs:
        return valid_geo_outs
    return None


def set_ovv_group_defaults(context, node):
    prefs = context.preferences.addons[__package__].preferences
    names = prefs.rna_type.properties.keys()
    inputs = node.inputs
    for name in names:
        adj_name = name.replace("_", " ").title()
        if adj_name in inputs.keys():
            node.inputs[adj_name].default_value = getattr(prefs, name)

def check_file_node_groups(name:str) -> bpy.types.Node | None:
    if my_node := bpy.data.node_groups.get(name, None):
        if output_node_ver := my_node.nodes.get("Group Output").get("version", None):
            if output_node_ver.to_list() != NODE_VER:
                bpy.data.node_groups.remove(my_node)
                my_node = None
    return my_node


def import_node_group(name, blend_file) -> bpy.types.Node | None:
    with bpy.data.libraries.load(str(blend_file)) as (data_from, data_to):
       data_to.node_groups = [name]

    imported_group = data_to.node_groups[0]
    return imported_group


def get_custom_node(node_group_name:str) -> bpy.types.Node | None:
    if valid_group := (check_file_node_groups(node_group_name) or 
                       import_node_group(node_group_name, blend_file=VIS_FILE)):
        return valid_group
    return None


def register():
    bpy.utils.register_class(OT_create_vector_viewer_node)
    bpy.utils.register_class(OT_create_quat_node)


def unregister():
    bpy.utils.unregister_class(OT_create_vector_viewer_node)
    bpy.utils.unregister_class(OT_create_quat_node)
