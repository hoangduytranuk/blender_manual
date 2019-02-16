��    2      �              <     =  1   K     }     �     �     �     �     �  1   �       9   !  	   [     e  �   v  �   "  R   �  �     +  �     �  |   �  a   ]     �     �     �     �  c   �  	   P	     Z	  !   j	     �	  1   �	     �	  ,   �	  (   
     /
     B
  
   R
    ]
     i  n   �  �   X  �   �  w   �  �   
  0  �     �  �   X  �   �  �   �  �  ^       1   $     V  /   l  )   �  0   �  +   �  >   #  5   b     �  9   �     �        �     �   �  R   d  �   �  +  K     w  |   �  a   
     l     �     �     �  c   �     &  2   @  $   s  (   �  1   �  '   �  ,     (   H  +   q  $   �      �    �     �  n   o  �   �  �   }   w   !  �   �!  0  -"     ^$  �   �$  �   v%  �   2&   :kbd:`Ctrl-D` :menuselection:`Tool Shelf --> Tools --> Dyntopo` Adaptive Sculpting Brush Detail Collapse Edges Constant Detail Detail Flood Fill Detail Refine Method Detail Size/Percentage, Resolution :kbd:`Shift-D` Detail Type Determines which direction the model will be symmetrized. Direction Dynamic Topology Dynamic topology (aka dyntopo) is a dynamic tessellation sculpting method, adds and removes details on-the-fly, whereas regular sculpting only affects the shape of a mesh. Dyntopo can be toggled with the checkbox in the header or with :kbd:`Ctrl-D`. With dynamic topology active, most brushes will subdivide the mesh during the stroke. Dyntopo uses three different detail methods to create dynamic detail to an object. Each Detail Type's detail is set here. Depending on the Detail Type being used this property will rather show as a pixel count (px), or percentage. Giving more control over the topology, with this method you can create topology based on the brush size. You can increase and lower topology by simply resizing the brush itself. The detail size is based the size of the brush itself, where 100% will create topology the size of the brush ring itself. Hotkey If sculpting begins to slow down while dynamic topology is enabled, use the *Optimize* button to recalculate the sculpt BVH. Just like the Subdivide tool, this method will only subdivide topology to match the detail given. Mode Multiresolution Modifier Optimize Panel Read more about the :doc:`Multiresolution Modifier </modeling/modifiers/generate/multiresolution>`. Reference Relative Detail Sample Detail Size (pipette icon) Sculpt Mode Set multires level :kbd:`Ctrl-0` to :kbd:`Ctrl-5` Smooth Shading Step down one multires level :kbd:`PageDown` Step up one multires level :kbd:`PageUp` Subdivide Collapse Subdivide Edges Symmetrize The Multiresolution Modifier is needed to sculpt. The modifier will subdivide the mesh. The more subdivision the more computing will be needed. With the Blender stack non-destructive data, multi-resolution sculpting will help when you have a clean topology base mesh. This makes it possible to sculpt complex shapes out of a simple mesh, rather than just adding details onto a modeled base mesh. This method combines the two methods, subdividing edges smaller than the detail size, and collapsing topology. This method uses a detail size based on the number of pixels, and in turn will create topology in that size. Zoom out big details, zoom in small fine details. To keep detail uniform across the entire object, Constant Detail can be used. The Detail is based on the percentage of a single :abbr:`BU (Blender Unit)`. Toggles whether mesh faces are smooth or flat-shaded. In dynamic-topology mode all faces have the same type of shading. Uses direction orientation to symmetrize. Since Dyntopo adds details dynamically it may happen that the model goes asymmetric, so this a good tool for that. When sculpting with multiple resolutions you have the ability to sculpt in different levels of subdivision, this mean you can sculpt some details in subdivision level 1 and add more details in subdivision 2 and go back to subdivision 1 correct some mistakes. While this workflow is often used, the Multiresolution Modifier has some limitations. You may end up with some mesh distortions. As an advice, add as most details as possible before adding more subdivisions. Clay brush, SculptDraw work better with multi-resolution sculpting to sculpt secondary forms. When topology is too dense, and is smaller than the detail given, edges will be collapsed to fit the detail size appropriately. When using Constant Detail mode, this option is made available, allowing you to fill the entire object with a uniform detail, based on the detail size. When using Dynamic Topology, a certain method will be used to tell how topology is handled. Setting the option will determine which of the methods will be used when altering the topology. With Constant Detail Size it is possible to sample the detail value of a certain mesh area by clicking the pipette icon next to the detail setting and then clicking on the area. Project-Id-Version: Blender 2.79 Manual 2.79
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
 :kbd:`Ctrl-D` :menuselection:`Tool Shelf --> Tools --> Dyntopo` -- Adaptive Sculpting Mức Chi Tiết theo Bút Vẽ -- Brush Detail Hòa Nhập các Cạnh -- Collapse Edges Mức Chi Tiết Cố Định -- Constant Detail Phủ Tràn Chi Tiết -- Detail Flood Fill Phương Pháp Tinh Chỉnh Chi Tiết -- Detail Refine Method  -- Detail Size/Percentage, Resolution :kbd:`Shift-D`  -- Detail Type Determines which direction the model will be symmetrized. Chiều Hướng -- Direction -- Dynamic Topology Dynamic topology (aka dyntopo) is a dynamic tessellation sculpting method, adds and removes details on-the-fly, whereas regular sculpting only affects the shape of a mesh. Dyntopo can be toggled with the checkbox in the header or with :kbd:`Ctrl-D`. With dynamic topology active, most brushes will subdivide the mesh during the stroke. Dyntopo uses three different detail methods to create dynamic detail to an object. Each Detail Type's detail is set here. Depending on the Detail Type being used this property will rather show as a pixel count (px), or percentage. Giving more control over the topology, with this method you can create topology based on the brush size. You can increase and lower topology by simply resizing the brush itself. The detail size is based the size of the brush itself, where 100% will create topology the size of the brush ring itself. Phím Tắt -- Hotkey If sculpting begins to slow down while dynamic topology is enabled, use the *Optimize* button to recalculate the sculpt BVH. Just like the Subdivide tool, this method will only subdivide topology to match the detail given. Chế Độ -- Mode -- Multiresolution Modifier Tối Ưu -- Optimize Bảng -- Panel Read more about the :doc:`Multiresolution Modifier </modeling/modifiers/generate/multiresolution>`. Tham Chiếu -- Reference Mức Chi Tiết Tương Đối -- Relative Detail -- Sample Detail Size (pipette icon) Chế Độ Điêu Khắc -- Sculpt Mode Set multires level :kbd:`Ctrl-0` to :kbd:`Ctrl-5` Tô Bóng Mịn Màng -- Smooth Shading Step down one multires level :kbd:`PageDown` Step up one multires level :kbd:`PageUp` Rút Độ Phân Hóa -- Subdivide Collapse Phân Chia Cạnh -- Subdivide Edges Đối Xứng Hóa -- Symmetrize The Multiresolution Modifier is needed to sculpt. The modifier will subdivide the mesh. The more subdivision the more computing will be needed. With the Blender stack non-destructive data, multi-resolution sculpting will help when you have a clean topology base mesh. This makes it possible to sculpt complex shapes out of a simple mesh, rather than just adding details onto a modeled base mesh. This method combines the two methods, subdividing edges smaller than the detail size, and collapsing topology. This method uses a detail size based on the number of pixels, and in turn will create topology in that size. Zoom out big details, zoom in small fine details. To keep detail uniform across the entire object, Constant Detail can be used. The Detail is based on the percentage of a single :abbr:`BU (Blender Unit)`. Toggles whether mesh faces are smooth or flat-shaded. In dynamic-topology mode all faces have the same type of shading. Uses direction orientation to symmetrize. Since Dyntopo adds details dynamically it may happen that the model goes asymmetric, so this a good tool for that. When sculpting with multiple resolutions you have the ability to sculpt in different levels of subdivision, this mean you can sculpt some details in subdivision level 1 and add more details in subdivision 2 and go back to subdivision 1 correct some mistakes. While this workflow is often used, the Multiresolution Modifier has some limitations. You may end up with some mesh distortions. As an advice, add as most details as possible before adding more subdivisions. Clay brush, SculptDraw work better with multi-resolution sculpting to sculpt secondary forms. When topology is too dense, and is smaller than the detail given, edges will be collapsed to fit the detail size appropriately. When using Constant Detail mode, this option is made available, allowing you to fill the entire object with a uniform detail, based on the detail size. When using Dynamic Topology, a certain method will be used to tell how topology is handled. Setting the option will determine which of the methods will be used when altering the topology. With Constant Detail Size it is possible to sample the detail value of a certain mesh area by clicking the pipette icon next to the detail setting and then clicking on the area. 