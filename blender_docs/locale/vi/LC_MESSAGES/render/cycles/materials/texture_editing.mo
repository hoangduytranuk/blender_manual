��          �               <     =  �   P  �   D  �   $  �   �  �   W  �   4  �   �     �  2   �          +     4     <     L  ^   _    �  �  �     x
  �   �
  �   �  �   b  �     �   �  �   r  �   8       2   2     e          �     �     �  ^   �    6   3D View Draw Types 3D View draw types, UV mapping, and texture painting work somewhat differently when Cycles is enabled. UV maps no longer get image textures assigned themselves; rather they must always be assigned by adding an image texture node to a material. A simplified version of the entire material is drawn using GLSL shaders. This uses solid lighting, and also is mostly useful for editing, painting and mapping textures, but while seeing how they integrate with the material. For UV mapping, the active UV map as specified in the mesh properties is used. Assigning images in the UV/Image editor also affects the active image texture node. For shading nodes, the available textures are Cycles textures. For others, Blender textures are still used, but this will change in the future. For texture paint mode, the image that is painted on is taken from the active image texture node. This can be selected in the Node editor or the texture properties, and it is indicated as blue in the material properties. In the texture properties, the texture can now be selected from a list that contains all texture nodes from the world, lamps and materials, but also from e.g. modifiers, brushes and physics fields. In this draw mode the renderer does the drawing, interactively refining the full rendered image by taking more samples. Unlike offline rendering, objects still use the viewport rather than render resolution and visibility. Material Material draw modes (Texture, Material, Rendered). Painting & UV Editing Rendered Texture Texture Editing Texture Properties The Texture draw types used for Blender Internal have been replaced by three others in Cycles: This draw mode is used for editing, painting and mapping individual textures. Lighting is the same as in solid mode, so this is similar to the existing textured solid for Blender Internal. The texture drawn is the active image texture node for the material. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 -- 3D View Draw Types 3D View draw types, UV mapping, and texture painting work somewhat differently when Cycles is enabled. UV maps no longer get image textures assigned themselves; rather they must always be assigned by adding an image texture node to a material. A simplified version of the entire material is drawn using GLSL shaders. This uses solid lighting, and also is mostly useful for editing, painting and mapping textures, but while seeing how they integrate with the material. For UV mapping, the active UV map as specified in the mesh properties is used. Assigning images in the UV/Image editor also affects the active image texture node. For shading nodes, the available textures are Cycles textures. For others, Blender textures are still used, but this will change in the future. For texture paint mode, the image that is painted on is taken from the active image texture node. This can be selected in the Node editor or the texture properties, and it is indicated as blue in the material properties. In the texture properties, the texture can now be selected from a list that contains all texture nodes from the world, lamps and materials, but also from e.g. modifiers, brushes and physics fields. In this draw mode the renderer does the drawing, interactively refining the full rendered image by taking more samples. Unlike offline rendering, objects still use the viewport rather than render resolution and visibility. Nguyên Liệu -- Material Material draw modes (Texture, Material, Rendered).  -- Painting & UV Editing Kết Xuất -- Rendered Hoa Văn -- Texture  -- Texture Editing  -- Texture Properties The Texture draw types used for Blender Internal have been replaced by three others in Cycles: This draw mode is used for editing, painting and mapping individual textures. Lighting is the same as in solid mode, so this is similar to the existing textured solid for Blender Internal. The texture drawn is the active image texture node for the material. 