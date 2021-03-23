import bpy
from bpy.types import Panel, Operator
import re

bl_info = {
    "name": "Dimensions Per Keyframe",
    "author": "MURATAGAWA Kei",
    "description": "Store render dimensions per keyframe",
    "blender": (2, 83, 0),
    "version": (0, 1, 0),
    "location": "Timeline > Marker",
    "warning": "",
    "category": "Render",
    "wiki_url": "https://github.com/muratagawa/dimensions-per-keyframe/",
    "tracker_url": "https://github.com/muratagawa/dimensions-per-keyframe/issues",
}

MARKER_PATTERN = r"(\d+):(\d+)"


class DPK_OT_save(Operator):
    bl_idname = "object.dpk_save"
    bl_label = "Save"
    bl_description = "Save dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    def __save_marker(self, marker_str):
        bpy.context.scene.timeline_markers.new(
            name=marker_str, frame=bpy.context.scene.frame_current)

    def execute(self, context):
        markers = find_dimension_markers_in_current_frame()
        marker_str = str(bpy.context.scene.render.resolution_x) + \
            ":" + str(bpy.context.scene.render.resolution_y)

        # Overwrite if any markers exist in current frame
        if len(markers) > 0:
            for m in markers:
                bpy.context.scene.timeline_markers.remove(m[1])
            self.__save_marker(marker_str)
            self.report({'INFO'}, "Dimensions overwrited.")
        else:
            self.__save_marker(marker_str)
            self.report({'INFO'}, "Dimensions saved.")

        return {'FINISHED'}


class DPK_OT_delete(Operator):
    bl_idname = "object.dpk_delete"
    bl_label = "Delete"
    bl_description = "Delete dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        markers = find_dimension_markers_in_current_frame()
        for m in markers:
            bpy.context.scene.timeline_markers.remove(m[1])
        self.report({'INFO'}, "Dimensions deleted.")
        return {'FINISHED'}


class DPK_PT_save_panel(Panel):
    bl_idname = "DPK_PT_save_panel"
    bl_label = "Save/Delete Dimensions to Keyframe Marker"
    bl_parent_id = "RENDER_PT_dimensions"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        layout = self.layout
        layout.operator(DPK_OT_save.bl_idname)
        layout.operator(DPK_OT_delete.bl_idname)


def find_dimension_markers_in_current_frame():
    result = []

    # Get markers of current frame
    # TODO Rewrite to filter() function
    all_marker_items = bpy.context.scene.timeline_markers.items()
    current_frame = bpy.context.scene.frame_current
    items = [item
             for item in all_marker_items if item[1].frame == current_frame]

    if len(items) < 1:
        return result

    for item in items:
        matched = re.match(MARKER_PATTERN, item[0])
        if matched:
            result.append(item)

    return result


def parse_dimensions_from_marker():
    markers = find_dimension_markers_in_current_frame()

    if len(markers) < 1:
        return "", ""

    marker_str = markers[0][0]
    m = re.match(MARKER_PATTERN, marker_str)
    return int(m.group(1)), int(m.group(2))


def update_dimensions(scene):
    x, y = parse_dimensions_from_marker()
    if x != "":
        scene.render.resolution_x = x
        scene.render.resolution_y = y


classes = (
    DPK_OT_save,
    DPK_PT_save_panel,
    DPK_OT_delete,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.app.handlers.frame_change_pre.append(update_dimensions)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.app.handlers.frame_change_pre.remove(update_dimensions)


if __name__ == "__main__":
    register()
