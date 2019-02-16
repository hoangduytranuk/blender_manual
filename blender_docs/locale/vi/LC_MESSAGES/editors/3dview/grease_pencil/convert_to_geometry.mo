��    6      �              |  �   }  3   r  a   �  	     �     f        o  9   }     �     �  W   �  A   6     x  	   �     �     �     �  �  �  U   6	  x   �	  N  
  _   T     �     �     �     �  	   �     �     �     �     �          	       	      �   *     �  n   �     I  �   g  (   �  �   $  q     )   x  !   �  5   �     �            �     e   �    %  N   '  �  v  �   .  3   #  a   W  (   �  �   �  f   �  '   ?  9   g  7   �     �  W   �  A   D  )   �     �     �  $   �  1      �  2  U   �  x     N  �  _   �     7  *   O     z     �  +   �  9   �     	           :     J  )   f     �     �  �   �     m  n   �     �  �      (   �   �   �   q   �!  )   $"  !   N"  5   p"     �"  &   �"     �"  �   �"  e   �#    $  N   %   *Custom Gaps* only. The average duration (in frames) of each gap between actual strokes. Please note that the value entered here will only be exact if *Realtime* is enabled, otherwise it will be scaled, exactly as the actual strokes' timing is! :menuselection:`GPencil --> Convert to Geometry...` :menuselection:`Tool Shelf --> Grease Pencil --> Grease Pencil --> Tools: Convert to Geometry...` All Modes All this means is that with a pressure tablet, you can directly control the radius and weight of the created curve, which can affect e.g. the width of an extrusion, or the size of an object through a *Follow Path* Constraint or *Curve* Modifier! All those "timing" options need *Link Stroke* to be enabled, otherwise they would not make much sense! Bézier Curve Bézier Curve with straight line segments (auto handles). Convert to Geometry Converting to Mesh Create Bézier curves, with free "aligned" handles (i.e. also behaving like polylines). Create NURBS 3D curves of order 2 (i.e. behaving like polylines). Custom Gaps End Frame Example Frame Range Gap Duration Grease pencil stores "dynamic" data, i.e. how fast strokes are drawn. When converting to curve, this data can be used to create an *Evaluate Time* F-Curve (in other words, a path animation), that can be used e.g. to control another object's position along that curve (*Follow Path* constraint, or, through a driver, *Curve* modifier). So this allows you to reproduce your drawing movements. Here is a simple "hand writing" video created with curves converted from sketch data: If you want to convert your sketch to a mesh, simply choose *NURBS* first, and then convert the created curve to a mesh. In the 3D View, sketches on the active layer can be converted to geometry, based on the current view settings, by transforming the points recorded when drawing (which make up the strokes) into 3D space. Currently, all points will be used, so it may be necessary to simplify or subdivide parts of the created geometry for standard use. Just create the curve, without any animation data (hence all following options will be hidden). Linear Link Strokes Menu Mode No Timing Normalize Weight Options Original Panel Path Polygon Curve Realtime Reference Sketches can currently be converted into curves, as proposed by the *Convert Grease Pencil* menu popped-up by the *Convert* button in the Grease pencil properties. Start Frame The "length" of the created path animation, in frames. In other words, the highest value of *Evaluation Time*. The Convert to Curve options. The blend-file from the above example can be found `here <https://wiki.blender.org/wiki/File:ManGreasePencilConvertToCurveDynamicExample.blend>`__. The path animation will be a linear one. The path animation will reflect to original timing, but the "gaps" will get custom values. This is especially useful if you have very large pauses between some of your strokes, and would rather like to have "reasonable" ones! The path animation will reflect to original timing, including for the "gaps" (i.e. time between strokes drawing). The starting frame of the path animation. The type of object to convert to. This control lets you choose how timing data is used. Timing Timing Mode Type When *Realtime* is disabled, this defines the end frame of the path animation. This means that the drawing timing will be scaled up or down to fit into the specified range. When enabled, the path animation will last exactly the same duration it took you do draw the strokes. Will create a single spline, i.e. curve element. (enabled by default) from all strokes in active Grease pencil layer. This is especially useful if you want to use the curve as a path. All the strokes are linked in the curve by "zero weights/radii" sections. Will scale weights value so that they fit tightly into the (0.0 to 1.0) range. Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-02-01 00:53+0000
PO-Revision-Date: 2019-02-01 00:54+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 *Custom Gaps* only. The average duration (in frames) of each gap between actual strokes. Please note that the value entered here will only be exact if *Realtime* is enabled, otherwise it will be scaled, exactly as the actual strokes' timing is! :menuselection:`GPencil --> Convert to Geometry...` :menuselection:`Tool Shelf --> Grease Pencil --> Grease Pencil --> Tools: Convert to Geometry...` Toàn Bộ các Chế Độ -- All Modes All this means is that with a pressure tablet, you can directly control the radius and weight of the created curve, which can affect e.g. the width of an extrusion, or the size of an object through a *Follow Path* Constraint or *Curve* Modifier! All those "timing" options need *Link Stroke* to be enabled, otherwise they would not make much sense! Đường Cong Bézier -- Bézier Curve Bézier Curve with straight line segments (auto handles). Chuyển Đổi sang Hình Học -- Convert to Geometry Converting to Mesh Create Bézier curves, with free "aligned" handles (i.e. also behaving like polylines). Create NURBS 3D curves of order 2 (i.e. behaving like polylines). Phân Khoảng Tùy Chọn -- Custom Gaps K. Cuối -- End Frame Ví Dụ -- Example Phạm Vi Khung Hình -- Frame Range Độ Dài của Khoảng Trống -- Gap Duration Grease pencil stores "dynamic" data, i.e. how fast strokes are drawn. When converting to curve, this data can be used to create an *Evaluate Time* F-Curve (in other words, a path animation), that can be used e.g. to control another object's position along that curve (*Follow Path* constraint, or, through a driver, *Curve* modifier). So this allows you to reproduce your drawing movements. Here is a simple "hand writing" video created with curves converted from sketch data: If you want to convert your sketch to a mesh, simply choose *NURBS* first, and then convert the created curve to a mesh. In the 3D View, sketches on the active layer can be converted to geometry, based on the current view settings, by transforming the points recorded when drawing (which make up the strokes) into 3D space. Currently, all points will be used, so it may be necessary to simplify or subdivide parts of the created geometry for standard use. Just create the curve, without any animation data (hence all following options will be hidden). Tuyến Tính -- Linear Kết Nối các Nét Vẽ -- Link Strokes Trình Đơn -- Menu Chế Độ -- Mode Không Sử Dụng Thời Gian -- No Timing Bình Thường Hóa Trọng Lượng -- Normalize Weight Tùy Chọn -- Options Nguyên Bản -- Original Bảng -- Panel Đường/Đi/Dẫn -- Path Đường Cong Đa Giác -- Polygon Curve Thời Gian Thực -- Realtime Tham Chiếu -- Reference Sketches can currently be converted into curves, as proposed by the *Convert Grease Pencil* menu popped-up by the *Convert* button in the Grease pencil properties. K. Đầu -- Start Frame The "length" of the created path animation, in frames. In other words, the highest value of *Evaluation Time*. The Convert to Curve options. The blend-file from the above example can be found `here <https://wiki.blender.org/wiki/File:ManGreasePencilConvertToCurveDynamicExample.blend>`__. The path animation will be a linear one. The path animation will reflect to original timing, but the "gaps" will get custom values. This is especially useful if you have very large pauses between some of your strokes, and would rather like to have "reasonable" ones! The path animation will reflect to original timing, including for the "gaps" (i.e. time between strokes drawing). The starting frame of the path animation. The type of object to convert to. This control lets you choose how timing data is used. Thời Định -- Timing Chế Độ Thời Gian -- Timing Mode Thể Loại -- Type When *Realtime* is disabled, this defines the end frame of the path animation. This means that the drawing timing will be scaled up or down to fit into the specified range. When enabled, the path animation will last exactly the same duration it took you do draw the strokes. Will create a single spline, i.e. curve element. (enabled by default) from all strokes in active Grease pencil layer. This is especially useful if you want to use the curve as a path. All the strokes are linked in the curve by "zero weights/radii" sections. Will scale weights value so that they fit tightly into the (0.0 to 1.0) range. 