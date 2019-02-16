��    H      \              �  T   �  '  �  �        �            	     
   &     1  ~   =     �     �  
   �     �     �  �   �     �	  �   �	     a
  %   }
  L   �
  u   �
  b   f     �  �   �  B   �  �   �  �   f  	   	               1  e   9     �  �   �     +     C     c     �     �  �   �     e     q  
   x     �     �  0   �  x   �     J     R  �   Y  �     �   �  �   ~  p     r  y  p  �    ]  `   m  +   �  �   �  @   �  �     �   �  �   5  	   �       �    k   �     %  �   +  �    T   �   '  !  �   F#  $   %$     J$     P$     `$  !   y$     �$  ~   �$     4%     B%     R%  /   k%  &   �%  �   �%     q&  �   �&     ;'  %   Z'  L   �'  u   �'  b   C(  B   �(  �   �(  B   �)  �   �)  �   n*     +     -+     G+     ^+  e   s+     �+  �   �+     w,  #   �,  #   �,     �,     �,  �   �,     �-     �-     
.     %.     A.  0   O.  x   �.     �.     /  �   )/  �   �/  �   �0  �   N1  p   �1  r  I2  p  �3    -5  `   =6  +   �6  �   �6  @   �7  �   �7  �   g8  �   9     �9     �9  �  �9  k   �;     <  �   <   A :ref:`color ramp <ui-color-ramp-widget>` that maps the property to a stroke color. A modifier based on radial curvatures of the underlying 3D surface. The `curvature <https://en.wikipedia.org/wiki/Curvature>`__ of a 2D curve at a point is a measure of how quickly the curve turns at the point. The quicker the turn is, the larger the curvature is at the point. The curvature is zero if the curve is a straight line. Radial curvatures are those computed for a 2D curve that appears at the cross section between the 3D surface and a plane defined by the view point (camera location) and the normal direction of the surface at the point. A modifier based on the Crease Angle (angle between two adjacent faces). If a stroke segment does not lie on a crease (i.e. the edge does not have the *Crease Angle nature*), its properties are not touched by the modifier. Along Stroke Alpha Alpha Modifier. Amplitude Asymmetric Calligraphy Calligraphy modifier demo by T.K. `File:Toycar_Calligraphy.zip <https://wiki.blender.org/wiki/File:Toycar_Calligraphy.zip>`__. Color Color Modifier. Color Ramp Common Options Crease Angle Crease Angle modifier demo by T.K. `File:Render_freestyle_modifier_crease_angle.blend <https://wiki.blender.org/uploads/b/b4/Render_freestyle_modifier_crease_angle.blend>`__. Curvature 3D Curvature 3D modifier demo by T.K. `File:Render_freestyle_modifier_curvature_3d.blend <https://wiki.blender.org/wiki/File:Render_freestyle_modifier_curvature_3d.blend>`__. Distance from Camera/Object Distance from Object: Alpha Modifier. Effect generated with a noise thickness modifier using asymmetric thickness. Either a linear progression (from *Min Thickness* to *Max Thickness*), or a custom mapping curve (on the same range). Either a linear progression (from 0.0 to 1.0), or a custom mapping :ref:`curve <ui-curve-widget>`. Fill Range by Selection For radial curvatures to be calculated (and therefore for this modifier to have any effect), the *Face Smoothness* option has to be turned on and the object needs to have *Smooth Shading*. How much the result of this modifier affects the current property. If used with the *Split by Material* option in the *Stroke* tab, the result will not be blurred between materials along the strokes. In the reverse case properties of the materials, which are multi-components (i.e. give RGB results) the mean value will be used for Alpha and Thickness modifiers. Influence Invert Inverts the *Mapping*. Mapping Mapping between the defined range and the range input of the modifier. e.g. a range of crease values. Material Material modifiers demo by T.K. `File:Lilies_Color_Material.zip <https://wiki.blender.org/wiki/File:Lilies_Color_Material.zip>`__. Min Angle and Max Angle Min Curvature and Max Curvature Min Thickness and Max Thickness Mix Noise Note the linear non-inverted option is equivalent to "do nothing", as original values from materials are already in the (0.0 to 1.0) range. That is the case for: Crease Angle, 3D Curvature, Material, Noise, Tangent. Orientation Period Properties Range Min and Range Max Seed Seed used by the pseudo-random number generator. Set the min/max range values from the distances between the current selected mesh vertices and the camera or the target. Tangent Target The *Along Stroke* modifier alters the base property with a new one from a given range mapped along each stroke's length. In other words, it applies a gradient along each stroke. The *Calligraphy* modifier (thickness only) mimics some broad and flat pens for calligraphy. It generates different thickness based on the orientation of the stroke. The *Distance from Camera* or *Distance from Object* modifier alters the base property with a new one from a given range using the distance to the active *camera* or to a given *object* as the parameter. The *Material* modifier alters the base property with a new one taken from a given range mapped on the current material under the stroke. The *Noise* modifier uses a pseudo-random number generator to variably distribute the property along the stroke. The angle (orientation) of the virtual drawing tool, from the vertical axis of the picture. For example, an angle of 0.0 mimics a pen aligned with the vertical axis. Hence, the thickest strokes will be the vertical ones i.e. stroke's direction is aligned with the angle, and the thinnest will be the horizontal ones i.e. stroke's direction is perpendicular to the angle. The limits of the mapping from "distance to camera" to "property in mapping". If the current point of the stroke is at *Range Min* or less from the active camera or the object, it will take the start value, and conversely, if it is at *Range Max* or more from the camera/object, it will take the end value. These values are in the current scene's units, not in pixels! The limits of the mapping. If the current point of the stroke is at *Min Curvature* or less from the target, it will take the start point of the mapping, and conversely, if it is at *Max Curvature* or more from the target, it will take the end-point value of the mapping. The maximum value of the noise. A higher amplitude means a less transparent (more solid) stroke. The minimum and maximum assigned thickness. The modifier output can be mixed with the base property using the usual methods (see for example the :doc:`Mix compositing node </compositing/types/color/mix>` for further discussion of this topic). The object to measure distance from (Distance from Object only). The period of the noise. This means how quickly the property value can change. A higher value means a more smoothly changing color along the stroke. The range of input values to the mapping. Out-of-range crease angle values will be clamped by the Min and Max angles and their corresponding property values. There are several modifiers for stroke vertex properties (i.e. line color, alpha transparency and thickness) available. As with other modifier stacks in Blender, they are applied from top to bottom. Thickness Thickness Modifier. Thickness only -- Allows the thickness to be distributed unevenly at every point. Internally, the stroke is represented as a backbone with a thickness to the right and left side. All other thickness shaders make sure that the left and right thickness values are equal. For the Noise shader however, a meaningful (and good-looking) result can be created by assigning different values to either side of the backbone. This modifier bases its effect on the traveling direction of the stroke evaluated at the stroke's vertices. Types You can use various properties of the materials, among which many are mono-component (i.e. give B&W results). In this case for the color modifier, an optional color ramp can be used to map these gray-scale values to colored ones. Project-Id-Version: Blender 2.79 Manual 2.79
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
 A :ref:`color ramp <ui-color-ramp-widget>` that maps the property to a stroke color. A modifier based on radial curvatures of the underlying 3D surface. The `curvature <https://en.wikipedia.org/wiki/Curvature>`__ of a 2D curve at a point is a measure of how quickly the curve turns at the point. The quicker the turn is, the larger the curvature is at the point. The curvature is zero if the curve is a straight line. Radial curvatures are those computed for a 2D curve that appears at the cross section between the 3D surface and a plane defined by the view point (camera location) and the normal direction of the surface at the point. A modifier based on the Crease Angle (angle between two adjacent faces). If a stroke segment does not lie on a crease (i.e. the edge does not have the *Crease Angle nature*), its properties are not touched by the modifier. Dọc theo Nét Vẽ -- Along Stroke Alpha Alpha Modifier. Biên Độ -- Amplitude Bất Đối Xứng -- Asymmetric Thư Pháp -- Calligraphy Calligraphy modifier demo by T.K. `File:Toycar_Calligraphy.zip <https://wiki.blender.org/wiki/File:Toycar_Calligraphy.zip>`__. Màu -- Color Color Modifier. Dốc Màu -- Color Ramp Các Tùy Chọn Phổ Thông -- Common Options Góc Độ Nếp Gấp -- Crease Angle Crease Angle modifier demo by T.K. `File:Render_freestyle_modifier_crease_angle.blend <https://wiki.blender.org/uploads/b/b4/Render_freestyle_modifier_crease_angle.blend>`__. Độ Cong 3D -- Curvature 3D Curvature 3D modifier demo by T.K. `File:Render_freestyle_modifier_curvature_3d.blend <https://wiki.blender.org/wiki/File:Render_freestyle_modifier_curvature_3d.blend>`__. -- Distance from Camera/Object Distance from Object: Alpha Modifier. Effect generated with a noise thickness modifier using asymmetric thickness. Either a linear progression (from *Min Thickness* to *Max Thickness*), or a custom mapping curve (on the same range). Either a linear progression (from 0.0 to 1.0), or a custom mapping :ref:`curve <ui-curve-widget>`. Tính Toán Phạm Vi theo Lựa Chọn -- Fill Range by Selection For radial curvatures to be calculated (and therefore for this modifier to have any effect), the *Face Smoothness* option has to be turned on and the object needs to have *Smooth Shading*. How much the result of this modifier affects the current property. If used with the *Split by Material* option in the *Stroke* tab, the result will not be blurred between materials along the strokes. In the reverse case properties of the materials, which are multi-components (i.e. give RGB results) the mean value will be used for Alpha and Thickness modifiers. Ảnh Hưởng -- Influence Đảo Nghịch -- Invert Inverts the *Mapping*. Ánh Xạ -- Mapping Mapping between the defined range and the range input of the modifier. e.g. a range of crease values. Nguyên Liệu -- Material Material modifiers demo by T.K. `File:Lilies_Color_Material.zip <https://wiki.blender.org/wiki/File:Lilies_Color_Material.zip>`__.  -- Min Angle and Max Angle  -- Min Curvature and Max Curvature  -- Min Thickness and Max Thickness Hòa Trộn -- Mix Nhiễu -- Noise Note the linear non-inverted option is equivalent to "do nothing", as original values from materials are already in the (0.0 to 1.0) range. That is the case for: Crease Angle, 3D Curvature, Material, Noise, Tangent. Định Hướng -- Orientation Chu Kỳ -- Period Tính Chất -- Properties  -- Range Min and Range Max Mầm -- Seed Seed used by the pseudo-random number generator. Set the min/max range values from the distances between the current selected mesh vertices and the camera or the target. Tiếp Tuyến -- Tangent Mục Tiêu -- Target The *Along Stroke* modifier alters the base property with a new one from a given range mapped along each stroke's length. In other words, it applies a gradient along each stroke. The *Calligraphy* modifier (thickness only) mimics some broad and flat pens for calligraphy. It generates different thickness based on the orientation of the stroke. The *Distance from Camera* or *Distance from Object* modifier alters the base property with a new one from a given range using the distance to the active *camera* or to a given *object* as the parameter. The *Material* modifier alters the base property with a new one taken from a given range mapped on the current material under the stroke. The *Noise* modifier uses a pseudo-random number generator to variably distribute the property along the stroke. The angle (orientation) of the virtual drawing tool, from the vertical axis of the picture. For example, an angle of 0.0 mimics a pen aligned with the vertical axis. Hence, the thickest strokes will be the vertical ones i.e. stroke's direction is aligned with the angle, and the thinnest will be the horizontal ones i.e. stroke's direction is perpendicular to the angle. The limits of the mapping from "distance to camera" to "property in mapping". If the current point of the stroke is at *Range Min* or less from the active camera or the object, it will take the start value, and conversely, if it is at *Range Max* or more from the camera/object, it will take the end value. These values are in the current scene's units, not in pixels! The limits of the mapping. If the current point of the stroke is at *Min Curvature* or less from the target, it will take the start point of the mapping, and conversely, if it is at *Max Curvature* or more from the target, it will take the end-point value of the mapping. The maximum value of the noise. A higher amplitude means a less transparent (more solid) stroke. The minimum and maximum assigned thickness. The modifier output can be mixed with the base property using the usual methods (see for example the :doc:`Mix compositing node </compositing/types/color/mix>` for further discussion of this topic). The object to measure distance from (Distance from Object only). The period of the noise. This means how quickly the property value can change. A higher value means a more smoothly changing color along the stroke. The range of input values to the mapping. Out-of-range crease angle values will be clamped by the Min and Max angles and their corresponding property values. There are several modifiers for stroke vertex properties (i.e. line color, alpha transparency and thickness) available. As with other modifier stacks in Blender, they are applied from top to bottom. Độ Dày -- Thickness Thickness Modifier. Thickness only -- Allows the thickness to be distributed unevenly at every point. Internally, the stroke is represented as a backbone with a thickness to the right and left side. All other thickness shaders make sure that the left and right thickness values are equal. For the Noise shader however, a meaningful (and good-looking) result can be created by assigning different values to either side of the backbone. This modifier bases its effect on the traveling direction of the stroke evaluated at the stroke's vertices. Thể Loại -- Types You can use various properties of the materials, among which many are mono-component (i.e. give B&W results). In this case for the color modifier, an optional color ramp can be used to map these gray-scale values to colored ones. 