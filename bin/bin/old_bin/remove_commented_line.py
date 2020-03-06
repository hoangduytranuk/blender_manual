#!/usr/bin/python3 -d
import os
import sys
import re


root_dir = "/home/htran/blender_documentations/english_manual/blender_docs/locale/vi"

file_list=[
'LC_MESSAGES/animation/shape_keys/workflow.po',
'LC_MESSAGES/compositing/types/filter/blur_node.po',
'LC_MESSAGES/compositing/types/filter/vector_blur.po',
'LC_MESSAGES/data_system/scenes/properties.po',
'LC_MESSAGES/editors/3dview/grease_pencil/drawing/introduction.po',
'LC_MESSAGES/editors/3dview/object/properties/relations/parents.po',
'LC_MESSAGES/editors/graph_editor/fcurves/modifiers.po',
'LC_MESSAGES/editors/movie_clip_editor/tracking/clip/editing/solve.po',
'LC_MESSAGES/editors/nla/properties_modifiers.po',
'LC_MESSAGES/editors/uv_image/uv/textures/properties/influence/bump_normal.po',
'LC_MESSAGES/interface/controls/buttons/number.po',
'LC_MESSAGES/modeling/meshes/selecting/advanced.po',
'LC_MESSAGES/modeling/meshes/structure.po',
'LC_MESSAGES/modeling/metas/editing.po',
'LC_MESSAGES/modeling/texts/selecting_editing.po',
'LC_MESSAGES/physics/dynamic_paint/canvas.po',
'LC_MESSAGES/physics/fluid/types/control.po',
'LC_MESSAGES/physics/particles/emitter/physics/boids.po',
'LC_MESSAGES/physics/particles/mode.po',
'LC_MESSAGES/physics/smoke/baking.po',
'LC_MESSAGES/render/cycles/materials/assigning_a_material.po',
'LC_MESSAGES/render/cycles/nodes/types/shaders/sss.po',
'LC_MESSAGES/render/cycles/nodes/types/shaders/volume_principled.po',
'LC_MESSAGES/render/cycles/settings/scene/render/film.po',
'LC_MESSAGES/render/cycles/settings/scene/render/motion_blur.po',
'LC_MESSAGES/render/eevee/lightprobes/irradiance_volumes.po',
'LC_MESSAGES/render/freestyle/parameter_editor/line_style/modifiers/geometry.po',
'LC_MESSAGES/render/freestyle/parameter_editor/line_style/tabs.po',
'LC_MESSAGES/rigging/armatures/bones/editing/bones.po',
'LC_MESSAGES/rigging/armatures/bones/properties/bendy_bones.po',
'LC_MESSAGES/rigging/armatures/bones/selecting.po',
'LC_MESSAGES/rigging/armatures/properties/display.po',
'LC_MESSAGES/sculpt_paint/painting/texture_paint/slots_mask.po',
'LC_MESSAGES/sculpt_paint/painting/texture_paint/tools.po',
]

class BaseFileIO():

    def writeListToFile(self, file_name, text_list):
        with open(file_name, "w+") as f:
            for (index, text_line) in enumerate(text_list):
                f.write(text_line)
                f.write(os.linesep)
            f.close()

    def writeTextToFile(self, file_name, text):
        with open(file_name, "w+") as f:
            f.write(text)
            f.close()

    def readFile(self, file_name):
        with open(file_name) as f:
            read_text = f.read();
            f.close()
            return read_text
        return None

COMMENTED_PATTERN="^#~"

class RemoveCommentedLines(BaseFileIO):

    def __init__(self):
        self.po_file = None

    def setArgs(self, po_file):
        self.po_file = po_file

    def run(self):
        new_list=[]
        remove_list=[]
        removed_count=0
        file_text = self.readFile(self.po_file)
        #print("{}".format(file_text))

        text_list = str(file_text).strip().split(os.linesep)
        for(index, text_line) in enumerate(text_list):
            is_found = (re.search(COMMENTED_PATTERN, text_line) != None)
            if (is_found):
                remove_list.append(text_line)
                removed_count += 1
            else:
                new_list.append(text_line)

        document_changed = (removed_count > 0)
        if (document_changed):
            file_text = os.linesep.join(new_list)
            file_text += os.linesep
            #print("{}\n{}".format(os.linesep.join(remove_list), self.po_file))
            self.writeTextToFile(self.po_file, file_text)

if __name__ == "__main__":
    x = RemoveCommentedLines()
    for(index, file_name) in enumerate(file_list):
        file_path = os.path.join(root_dir, file_name)
        #x.setArgs(sys.argv[1])
        x.setArgs(file_path)
        x.run()
