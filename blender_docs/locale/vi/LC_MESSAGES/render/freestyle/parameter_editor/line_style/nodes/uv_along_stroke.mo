��          �               <  �   =     �  v   �     >  D  E     �  
   �  �   �    4  �   8     "     ;     >     S     i     �  ]   �  �  �  �   �
     )  v   =     �  D  �          $  �   ?    �  �   �  !   �     �  4   �          4     S  ]   m   Allows to use lower quarters of a texture image for the head and tail tips of a stroke, while the upper half for the stroke body. Example In Blender Render equivalent options can be found in :menuselection:`Properties editor --> Texture --> Mapping` panel. Inputs It is noted that the texture image ``FS_floral_brush.png`` shown in the screen capture is an example of Freestyle brush images with tips. Specifically, the upper half of the image is used as a seamless horizontal tile of the stroke body, whereas the parts in the lower half are tips (stroke caps) at both ends of the stroke. Outputs Properties The *UV Along Stroke* input node is maps textures along the stroke length, making it possible to mimic pencil, paintbrush, and other art medium marks. The following screen capture shows a typical shader node tree that maps a floral texture image along strokes. The UV Along Stroke input node retrieves UV maps defined by Freestyle along generated strokes, and feeds them to the Vector input channel of the Image Texture node. A texture image is selected in the Image Texture node, and its color is fed to the Alpha channel of the Line Style Output node. Since the Alpha Factor is set to one, the texture image replaces the base alpha transparency of the active line style (shown in the Freestyle Line Style panel). On the other hand, the Mix blend mode is selected in the Line Style Output node with the Color Factor set to zero, so that the gradient line color specified in the active line style is applied along strokes. These UV maps become available only during the Freestyle rendering process. Hence, the UV Along Stroke node cannot be replaced by the conventional UV Map input node which takes an existing UV map already defined as part of mesh data. This node has no inputs. UV UV Along Stroke Node UV Along Stroke Node. UV maps defined along strokes. Use Tips `.blend <https://wiki.blender.org/wiki/File:Blender_272_textured_strokes_in_cycles.blend>`__. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-14 21:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Allows to use lower quarters of a texture image for the head and tail tips of a stroke, while the upper half for the stroke body. Ví Dụ -- Example In Blender Render equivalent options can be found in :menuselection:`Properties editor --> Texture --> Mapping` panel. Đầu Vào -- Inputs It is noted that the texture image ``FS_floral_brush.png`` shown in the screen capture is an example of Freestyle brush images with tips. Specifically, the upper half of the image is used as a seamless horizontal tile of the stroke body, whereas the parts in the lower half are tips (stroke caps) at both ends of the stroke. Đầu Ra -- Outputs Tính Chất -- Properties The *UV Along Stroke* input node is maps textures along the stroke length, making it possible to mimic pencil, paintbrush, and other art medium marks. The following screen capture shows a typical shader node tree that maps a floral texture image along strokes. The UV Along Stroke input node retrieves UV maps defined by Freestyle along generated strokes, and feeds them to the Vector input channel of the Image Texture node. A texture image is selected in the Image Texture node, and its color is fed to the Alpha channel of the Line Style Output node. Since the Alpha Factor is set to one, the texture image replaces the base alpha transparency of the active line style (shown in the Freestyle Line Style panel). On the other hand, the Mix blend mode is selected in the Line Style Output node with the Color Factor set to zero, so that the gradient line color specified in the active line style is applied along strokes. These UV maps become available only during the Freestyle rendering process. Hence, the UV Along Stroke node cannot be replaced by the conventional UV Map input node which takes an existing UV map already defined as part of mesh data. Nút này không có đầu vào. UV Nút UV Dọc Theo Nét Vẽ -- UV Along Stroke Node UV Along Stroke Node. UV maps defined along strokes. Dùng Đỉnh -- Use Tips `.blend <https://wiki.blender.org/wiki/File:Blender_272_textured_strokes_in_cycles.blend>`__. 