��                        �  �   �  u     M   �     C     H     V  	   e     o     ~     �  �   �     T  C   `  m   �  �     .        7     ?     F     K  �   d    !  �   @  �   �  u   x	  �   �	     �
     �
  �  �
  �   �  u   G  M   �       2        M      \     }     �     �  �   �       C   �  m   �  �   A  .   7     f     }     �     �  �   �      �   �  �   T  u   �  �   L  %   F     l   A vertex group name, to restrict the effect to the vertices in it only. This allows for selective, real-time casting, by painting vertex weights. Alternative size for the projected shape. If zero, it is defined by the initial shape and the control object, if any. Animating (keyframing) this control object also animates the modified object. Axis Cast Modifier Cast Modifier. Cast Type Control Object Example Factor For performance reasons, this modifier only works with local coordinates. If the modified object looks wrong, you may need to apply its rotation :kbd:`Ctrl-A`, especially when casting to a cylinder. From radius If activated, calculate *Size* from *Radius*, for smoother results. If non-zero, this radius defines a sphere of influence. Vertices outside it are not affected by the modifier. It is equivalent to the *To Sphere* tool in *Edit Mode* :menuselection:`Mesh --> Transform --> To Sphere`, :kbd:`Shift-Alt-S` and what other programs call "Spherify" or "Spherize", but, as written above, it is not limited to casting to a sphere. Menu to choose target shape of the projection. Options Radius Size Sphere, Cylinder, Cuboid The :doc:`Smooth Modifier </modeling/modifiers/deform/smooth>` is a good companion to *Cast*, since the cast shape sometimes needs smoothing to look nicer or even to fix shading artifacts. The factor to control blending between original and cast vertex positions. It is a linear interpolation: 0.0 gives original coordinates (i.e. modifier has no effect), 1.0 casts to the target shape. Values below 0.0 or above 1.0 exaggerate the deformation, sometimes in interesting ways. The name of an object to control the effect. The location of this object's origin defines the center of the projection. Also, its size and rotation transform the projected vertices. This modifier shifts the shape of a mesh, curve, surface or lattice to any of a few predefined shapes (sphere, cylinder, cuboid). Toggle buttons to enable/disable the modifier in the X, Y, Z axes directions (X and Y only for *Cylinder* cast type). Top: Suzanne without modifiers. Middle: Suzanne with each type of Cast Modifier (Sphere, Cylinder and Cuboid). Bottom: Same as above, but now only X axis is enabled. `Sample blend-file <https://wiki.blender.org/wiki/File:263-Cast-Modifier.blend>`__. Vertex Group X, Y, Z Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A vertex group name, to restrict the effect to the vertices in it only. This allows for selective, real-time casting, by painting vertex weights. Alternative size for the projected shape. If zero, it is defined by the initial shape and the control object, if any. Animating (keyframing) this control object also animates the modified object. Trục -- Axis Bộ Điều Chỉnh Đúc Khuôn -- Cast Modifier Cast Modifier. Loại Khuôn Đúc -- Cast Type  -- Control Object Ví Dụ -- Example Hệ Số -- Factor For performance reasons, this modifier only works with local coordinates. If the modified object looks wrong, you may need to apply its rotation :kbd:`Ctrl-A`, especially when casting to a cylinder.  -- From radius If activated, calculate *Size* from *Radius*, for smoother results. If non-zero, this radius defines a sphere of influence. Vertices outside it are not affected by the modifier. It is equivalent to the *To Sphere* tool in *Edit Mode* :menuselection:`Mesh --> Transform --> To Sphere`, :kbd:`Shift-Alt-S` and what other programs call "Spherify" or "Spherize", but, as written above, it is not limited to casting to a sphere. Menu to choose target shape of the projection. Tùy Chọn -- Options Bán Kính -- Radius Kích Thước -- Size Sphere, Cylinder, Cuboid The :doc:`Smooth Modifier </modeling/modifiers/deform/smooth>` is a good companion to *Cast*, since the cast shape sometimes needs smoothing to look nicer or even to fix shading artifacts. The factor to control blending between original and cast vertex positions. It is a linear interpolation: 0.0 gives original coordinates (i.e. modifier has no effect), 1.0 casts to the target shape. Values below 0.0 or above 1.0 exaggerate the deformation, sometimes in interesting ways. The name of an object to control the effect. The location of this object's origin defines the center of the projection. Also, its size and rotation transform the projected vertices. This modifier shifts the shape of a mesh, curve, surface or lattice to any of a few predefined shapes (sphere, cylinder, cuboid). Toggle buttons to enable/disable the modifier in the X, Y, Z axes directions (X and Y only for *Cylinder* cast type). Top: Suzanne without modifiers. Middle: Suzanne with each type of Cast Modifier (Sphere, Cylinder and Cuboid). Bottom: Same as above, but now only X axis is enabled. `Sample blend-file <https://wiki.blender.org/wiki/File:263-Cast-Modifier.blend>`__. Nhóm Điểm Đỉnh -- Vertex Group X, Y, Z 