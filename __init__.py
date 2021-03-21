# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import Panel, Operator
import re

bl_info = {
    "name": "Dimensions Per Keyframe",
    "author": "MURATAGAWA Kei",
    "description": "Store render dimensions per keyframe",
    "blender": (2, 83, 0),
    "version": (0, 0, 2),
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

    def execute(self, context):
        markers = find_dimension_markers()
        marker_str = str(bpy.context.scene.render.resolution_x) + \
            ":" + str(bpy.context.scene.render.resolution_y)

        # TODO Overwrite if already exists
        if len(markers) > 0:
            self.report({'INFO'}, "Dimensions saved (overwrite).")
            # bpy.ops.marker.rename(name="40:20")
        else:
            self.report({'INFO'}, "Dimensions saved.")
            # bpy.ops.marker.add()

        return {'FINISHED'}


class DPK_OT_delete(Operator):
    bl_idname = "object.dpk_delete"
    bl_label = "Delete"
    bl_description = "Delete dimensions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # TODO
        self.report({'INFO'}, "Dimensions deleted.")
        return {'FINISHED'}


class DPK_PT_save_panel(Panel):
    bl_idname = "DPK_PT_save_panel"
    bl_label = "(WIP) Save/Delete Dimensions to Keyframe Marker"
    bl_parent_id = "RENDER_PT_dimensions"
    # bl_context = "context"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    def draw(self, context):
        layout = self.layout
        layout.operator(DPK_OT_save.bl_idname)
        layout.operator(DPK_OT_delete.bl_idname)


def find_dimension_markers():
    result = []

    # Get markers of current frame
    # TODO Rewrite to filter() function
    all_marker_items = bpy.context.scene.timeline_markers.items()
    current_frame = bpy.context.scene.frame_current
    items = [item
             for item in all_marker_items if item[1].frame == current_frame]

    if len(items) < 1:
        return result

    # Parse marker strings to X,Y dimensions
    for item in items:
        matched = re.match(MARKER_PATTERN, item[0])
        if matched:
            result.append(item)

    return result


def get_dimensions_from_marker():
    markers = find_dimension_markers()

    if len(markers) < 1:
        return "", ""

    marker_str = markers[0][0]
    m = re.match(MARKER_PATTERN, marker_str)
    return int(m.group(1)), int(m.group(2))


def update_dimensions(scene):
    x, y = get_dimensions_from_marker()
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
