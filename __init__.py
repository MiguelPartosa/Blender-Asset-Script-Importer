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

bl_info = {
    "name": "Asset Script Importer",
    "author": "Miguel Partosa",
    "description": "This addon allows direct import of scripts from the asset panel",
    "blender": (4, 0, 2),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Import-Export"
}


class ImportScriptsOperator(bpy.types.Operator):
    bl_idname = "wm.importallscripts"
    bl_label = "Import All Scripts"
    bl_description = "Import all the highlighted asset's scripts"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        with bpy.data.libraries.load(context.window_manager.asset_path_dummy) as (data_from, data_to):
            for text_block in data_from.texts:
                # appends scripts only
                if text_block.endswith(".py"):
                    data_to.texts.append(text_block)
                    print(f"Appended {text_block} to {data_to.texts} \n")

        self.report({'INFO'}, "Imported All Scripts Successfully!")
        return {'FINISHED'}

    # popup
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


# Idk why i did this instead of putting it in the importscripts class, maybe because i don't know where the spacetype,regiontype, etc. is for the context asset browser
def draw_helper(self, context):
    layout = self.layout
    layout.operator("wm.importallscripts", icon='APPEND_BLEND')
    layout.separator()  # this is a margin


def register():
    bpy.utils.register_class(ImportScriptsOperator)
    bpy.types.ASSETBROWSER_PT_metadata_preview.prepend(draw_helper)


def unregister():
    bpy.utils.unregister_class(ImportScriptsOperator)
    bpy.types.ASSETBROWSER_PT_metadata_preview.remove(draw_helper)
