# tool_paint.py
# Simple painting tool.
# Copyright (c) 2013, Graham R King
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from PySide import QtGui, QtCore
from tool import Tool, EventData, MouseButtons, KeyModifiers, Face
from plugin_api import register_plugin


class PaintingTool(Tool):

    def __init__(self, api):
        super(PaintingTool, self).__init__(api)
        # Create our action / icon
        self.action = QtGui.QAction(QtGui.QPixmap(":/images/gfx/icons/paint-brush.png"), "Paint", None)
        self.action.setStatusTip("Color Voxels")
        self.action.setCheckable(True)
        self.action.setShortcut(QtGui.QKeySequence("Ctrl+2"))
        # Register the tool
        self.priority = 2
        self.api.register_tool(self)
        # Area tool helper
        self.first_voxel = None

    # Color the targeted voxel
    def on_mouse_click(self, data):
        data.voxels.clear_selection()
        # If we have a voxel at the target, color it
        voxel = data.voxels.get(data.world_x, data.world_y, data.world_z)
        if voxel:
            shift_down = not not data.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier
            if self.first_voxel is None and not data.key_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier:
                data.voxels.set(data.world_x, data.world_y, data.world_z, self.color)
            elif self.first_voxel is None:  # and shift pressed
                self.first_voxel = (data.world_x, data.world_y, data.world_z)
            else:
                dx = 1 if data.world_x < self.first_voxel[0] else -1
                for x in xrange(data.world_x, self.first_voxel[0] + dx, dx):
                    dy = 1 if data.world_y < self.first_voxel[1] else -1
                    for y in xrange(data.world_y, self.first_voxel[1] + dy, dy):
                        dz = 1 if data.world_z < self.first_voxel[2] else -1
                        for z in xrange(data.world_z, self.first_voxel[2] + dz, dz):
                            data.voxels.set(x, y, z, self.color, True, 1)
                data.voxels.completeUndoFill()
                self.first_voxel = None

    # Color when dragging also
    def on_drag(self, data):
        data.voxels.clear_selection()
        self.on_mouse_click(data)

register_plugin(PaintingTool, "Painting Tool", "1.0")
