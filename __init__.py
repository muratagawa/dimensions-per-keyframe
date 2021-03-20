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
import re

bl_info = {
    "name": "Dimensions Per Keyframe",
    "author": "MURATAGAWA Kei",
    "description": "Store render dimensions per keyframe",
    "blender": (2, 83, 0),
    "version": (0, 0, 2),
    "location": "Keyframe Marker",
    "warning": "",
    "category": "Render"
}


class DimensionsPerKeyframeOperator(bpy.types.Operator):
    """Add-on information"""
    bl_label = "Dimensions Per Keyframe"
    bl_idname = "object.dpk_operator"

    def execute(self, context):
        return {'FINISHED'}


def find_dimensions():
    # Get markers of current frame
    marker_items = bpy.context.scene.timeline_markers.items()
    current_frame = bpy.context.scene.frame_current
    markers = [item[0] for item in marker_items if item[1].frame == current_frame]

    if len(markers) < 1:
        return "", ""

    # Parse marker strings to X,Y dimensions
    pattern = r"(\d+):(\d+)"
    for m in markers:
        matched = re.match(pattern, m)
        if matched:
            return int(matched.group(1)), int(matched.group(2))

    return "", ""


def update_resolution(scene):
    x, y = find_dimensions()
    if x != "":
        scene.render.resolution_x = x
        scene.render.resolution_y = y


def register():
    bpy.utils.register_class(DimensionsPerKeyframeOperator)
    bpy.app.handlers.frame_change_pre.append(update_resolution)


def unregister():
    bpy.utils.unregister_class(DimensionsPerKeyframeOperator)
    bpy.app.handlers.frame_change_pre.remove(update_resolution)


if __name__ == "__main__":
    register()
