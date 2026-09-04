import bpy
from pathlib import Path

DEMO_FILE = Path(__file__).parent / "ovv_demo_scene.blend"
DOC_URL = "https://github.com/TreyWojo/ovv_orient_vector_viewer/blob/master/README.md"

class OVV_PrefMenu(bpy.types.AddonPreferences):
    bl_idname = __package__

    defaults_menu: bpy.props.BoolProperty(name="Show Defaults", default=True)
    viz_geo_menu: bpy.props.BoolProperty(name="Show Vis", default=True)
    orient_menu: bpy.props.BoolProperty(name="Show Orient", default=True)
    sample_geo: bpy.props.EnumProperty(items=[
        ("Points", "Points", "Use Points"),
        ("Faces", "Faces", "Use Faces"),
        ],
        default="Points",
        name="Sample Geo")
    hide_base_geo: bpy.props.BoolProperty(name="Hide Base Geo")
    enable_lines_only: bpy.props.BoolProperty(name="Enable Lines Only")
    geo_selection: bpy.props.EnumProperty(items=[
        ("Arrow", "Arrow", "Use Arrows"),
        ("3 Arrow Basis", "3 Arrow Basis", "Use Basis Vectors"),
        ("Cube", "Cube", "Use Cube"),
        ],
        default="Arrow",
        name="Sample Geo")
    wireframe: bpy.props.BoolProperty(name="Wireframe")
    normalize: bpy.props.BoolProperty(name="Normalize")
    scale: bpy.props.FloatProperty(name="Scale", default=0.5)
    bpy.props.FloatVectorProperty
    arrow_radius: bpy.props.FloatProperty(name="Arrow Radius", default=0.5)
    arrow_depth: bpy.props.FloatProperty(name="Arrow Depth", default=0.25)
    vector_color: bpy.props.FloatVectorProperty(name="Vector Color", subtype="COLOR",
                                                size=4, default=[1,0,0,1])
    x: bpy.props.FloatVectorProperty(name="Basis X Axis Color", subtype="COLOR",
                                                size=4, default=[1,0,0,1])
    y: bpy.props.FloatVectorProperty(name="Basis Y Axis Color", subtype="COLOR",
                                                size=4, default=[0,1,0,1])
    z: bpy.props.FloatVectorProperty(name="Basis Z Axis Color", subtype="COLOR",
                                                size=4, default=[0,0,1,1])
    invert_opposite_colors: bpy.props.BoolProperty(name="Invert Opposite Colors",
                                                   default=True)
    use_color_from_attribute: bpy.props.BoolProperty(name="Use Color From Attribute")
    include_inverse_colors: bpy.props.BoolProperty(name="Include Inverse Colors",
                                                   default=True)
    orient_method: bpy.props.EnumProperty(items=[
        ("Auto Define From Input", "Auto Define From Input", "Auto Define From Input"),
        ("Single Vector", "Single Vector", "Single Vector"),
        ("Two Vector", "Two Vector", "Two Vector"),
        ("Rotation", "Rotation", "Rotation"),
        ("Quaternion", "Quaternion", "Quaternion"),
        ("Matrix", "Matrix", "Matrix"),
        ],
        default="Auto Define From Input",
        name="Orientation Method")

    def draw(self, context):
        layout = self.layout
        col = layout
        header, body = layout.panel_prop(self, "defaults_menu")
        header.label(text="Set Defaults")
        if body is not None:
            col.prop(self, 'sample_geo')

            vis_header, vis_body = layout.panel_prop(self, "viz_geo_menu")
            vis_header.label(text="Visualization Geo")
            if vis_body is not None:
                col.prop(self, 'hide_base_geo')
                col.prop(self, 'enable_lines_only')
                col.prop(self, 'geo_selection')
                col.prop(self, 'wireframe')
                col.prop(self, 'normalize')
                col.prop(self, 'scale')
                col.prop(self, 'arrow_radius')
                col.prop(self, 'arrow_depth')
                col.prop(self, 'vector_color')
                col.prop(self, 'x')
                col.prop(self, 'y')
                col.prop(self, 'z')
                col.prop(self, 'invert_opposite_colors')
                col.prop(self, 'use_color_from_attribute')
                col.prop(self, 'include_inverse_colors')
            orient_header, orient_body = layout.panel_prop(self, "orient_menu")
            orient_header.label(text="Orientation")
            if orient_body is not None:
                col.prop(self, 'orient_method')
        row = col.row()
        file_open = row.operator("wm.open_mainfile", text="Open Demo Scene")
        file_open.filepath = DEMO_FILE.as_posix()
        file_open.check_existing = True 
        file_open.display_file_selector = False 
        row.operator("wm.url_open", text="Open Documentation").url = DOC_URL


def register():
    bpy.utils.register_class(OVV_PrefMenu)

def unregister():
    bpy.utils.unregister_class(OVV_PrefMenu)
