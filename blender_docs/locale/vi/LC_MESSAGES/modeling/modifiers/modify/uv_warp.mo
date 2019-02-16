��          �               L    M     _  �   h  ]   �  �   S       o     8   �  �   �  E   _  U   �     �  	                  %     +  ?   8  �  x    0     B	  �   O	  ]   �	  �   :
     �
  o     8   �  �   �  E   U  U   �     �     �          )     =  %   R  ?   x   Assuming the *UV Axis* of the modifier is X/Y and the scale of the objects is (1, 1, 1), if the *to* object is one unit away from the *from* object on the X axis, the UVs will be transformed on the U axis (horizontally) by one full UV space (the entire width of the image). From, To How the UVs are warped is determined by the difference between the transforms (location, rotation and scale) of the *from* and *to* objects. If the *to* object has the same transforms as the *from* object, the UVs will not be changed. Its purpose is to give you direct control over the object's UVs in the 3D View, allowing you to directly translate, rotate and scale existing UV coordinates using controller objects or bones. Options The UV Warp Modifier uses two objects to define a transformation which is applied to the chosen UV coordinates. The axes to use when mapping the 3D coordinates into 2D. The center point of the UV map to use when applying scale or rotation. With (0, 0) at the bottom left and (1, 1) at the top right. Defaults to (0.5, 0.5). The two objects used to define the transformation. See *Usage* below. The vertex group can be used to scale the influence of the transformation per vertex. UV Axis UV Center UV Map UV Warp Modifier Usage Vertex Group Which UV map to modify. Defaults to the active rendering layer. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-07 02:04+0000
PO-Revision-Date: 2018-12-07 02:06+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Assuming the *UV Axis* of the modifier is X/Y and the scale of the objects is (1, 1, 1), if the *to* object is one unit away from the *from* object on the X axis, the UVs will be transformed on the U axis (horizontally) by one full UV space (the entire width of the image).  -- From, To How the UVs are warped is determined by the difference between the transforms (location, rotation and scale) of the *from* and *to* objects. If the *to* object has the same transforms as the *from* object, the UVs will not be changed. Its purpose is to give you direct control over the object's UVs in the 3D View, allowing you to directly translate, rotate and scale existing UV coordinates using controller objects or bones. Tùy Chọn -- Options The UV Warp Modifier uses two objects to define a transformation which is applied to the chosen UV coordinates. The axes to use when mapping the 3D coordinates into 2D. The center point of the UV map to use when applying scale or rotation. With (0, 0) at the bottom left and (1, 1) at the top right. Defaults to (0.5, 0.5). The two objects used to define the transformation. See *Usage* below. The vertex group can be used to scale the influence of the transformation per vertex.  -- UV Axis Tâm UV -- UV Center Ánh Xạ UV -- UV Map -- UV Warp Modifier Sử Dụng -- Usage Nhóm Điểm Đỉnh -- Vertex Group Which UV map to modify. Defaults to the active rendering layer. 