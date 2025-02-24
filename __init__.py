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

bl_info = {
    "name" : "Make Corner and Make End",
    "author" : "Jrome",
    "description" : "Connect Vertices To Turn Ngons Into Quads",
    "blender" : (2, 90, 0),
    "version" : (0, 5, 1),
    "location" : "Context Menu, Pie Menu (Alt-Comma), Toolbar",
    "doc_url": "https://blenderartists.org/t/make-corner-and-make-end/1273026",
    "warning" : "",
    "category" : "Mesh"
}

if "bpy" in locals():
    import importlib
    importlib.reload()
    importlib.reload()
else:

    from . import (
        make_corner,
        make_end,
        four_to_two,
        five_to_three,
        three_to_two,
        mce_menu,
        tools,
        preferences,
    )
import os
import bpy

from bpy.types import PropertyGroup
from bpy.props import BoolProperty
from bpy.utils.toolsystem import ToolDef

from . preferences import MCE_Preferences
from . mce_menu import MCE_MT_PieMenu
from . make_corner import MCE_OT_MakeCorner
from . make_end import MCE_OT_MakeEnd
from . four_to_two import MCE_OT_MakeFourToTwo
from . five_to_three import MCE_OT_MakeFiveToThree
from . three_to_two import MCE_OT_MakeThreeToTwo
from . tools import (Tool_MakeCorner, MCE_GGT_MakeCorner, MCE_GGT_MakeEnd, Tool_MakeEnd,
                    Tool_FourToTwo, MCE_GGT_FourToTwo, Tool_FiveToThree, MCE_GGT_FiveToThree, Tool_FiveToThreeAlt, MCE_GGT_FiveToThreeAlt,
                    Tool_ThreeToTwo, MCE_GGT_ThreeToTwo)


def get_addon_preferences():
    preferences = bpy.context.preferences
    return preferences.addons[__package__].preferences

def add_to_toolbar():
    bpy.utils.register_tool(Tool_MakeCorner, separator=True)
    bpy.utils.register_tool(Tool_MakeEnd, after={Tool_MakeCorner.bl_idname})

    if get_addon_preferences().add_optional_to_toolbar:
        bpy.utils.register_tool(Tool_FourToTwo, after={Tool_MakeEnd.bl_idname}, group=True)
        bpy.utils.register_tool(Tool_FiveToThree, after={Tool_FourToTwo.bl_idname})
        bpy.utils.register_tool(Tool_FiveToThreeAlt, after={Tool_FiveToThree.bl_idname})
        bpy.utils.register_tool(Tool_ThreeToTwo, after={Tool_FiveToThreeAlt.bl_idname})

def add_to_context_menu():
     bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_draw)

def remove_from_context_menu():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_draw)

def menu_draw(self, context):
    layout = self.layout
    layout.separator()
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator(make_corner.MCE_OT_MakeCorner.bl_idname, text='Make Corner')
    layout.operator(make_end.MCE_OT_MakeEnd.bl_idname, text='Make End')
    layout.operator(four_to_two.MCE_OT_MakeFourToTwo.bl_idname, text='Four To Two')
    layout.operator(five_to_three.MCE_OT_MakeFiveToThree.bl_idname, text='Five To Three')
    layout.operator(three_to_two.MCE_OT_MakeThreeToTwo.bl_idname, text='Three To Two')

classes = [ MCE_Preferences,
            MCE_MT_PieMenu,
            MCE_OT_MakeCorner,
            MCE_OT_MakeEnd,
            MCE_GGT_MakeCorner,
            MCE_GGT_MakeEnd,
            MCE_OT_MakeFourToTwo,
            MCE_GGT_FourToTwo,
            MCE_OT_MakeFiveToThree,
            MCE_GGT_FiveToThree,
            MCE_GGT_FiveToThreeAlt,
            MCE_OT_MakeThreeToTwo,
            MCE_GGT_ThreeToTwo
            ]

addon_keymaps = []
def register():


    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu_draw)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_draw)

    preferences = get_addon_preferences()
    if preferences.enable_context_menu:
        add_to_context_menu()

    if preferences.add_to_toolbar:
       add_to_toolbar()

    # handle the keymap
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi = km.keymap_items.new("wm.call_menu_pie", 'COMMA', 'PRESS', alt=True, repeat=False)
    kmi.properties.name = MCE_MT_PieMenu.bl_idname

    addon_keymaps.append((km, kmi))


def unregister():

    try:
        if get_addon_preferences().add_to_toolbar:
            bpy.utils.unregister_tool(Tool_MakeCorner)
            bpy.utils.unregister_tool(Tool_MakeEnd)

            if get_addon_preferences().add_optional_to_toolbar:
                bpy.utils.unregister_tool(Tool_FourToTwo)

                bpy.utils.unregister_tool(Tool_FiveToThree)

                bpy.utils.unregister_tool(Tool_FiveToThreeAlt)

                bpy.utils.unregister_tool(Tool_ThreeToTwo)
    except (ValueError, AttributeError):
        pass

    finally:
        for c in reversed(classes):
            bpy.utils.unregister_class(c)

        bpy.types.VIEW3D_MT_edit_mesh_edges.remove(menu_draw)
        bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_draw)
        remove_from_context_menu()

        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

        addon_keymaps.clear()
