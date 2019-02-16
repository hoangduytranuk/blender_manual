��    �      t              �
  �   �
  <   N     �     �  *   �      �  '   �  '   !  2   I  �  |          (  '   B  B   j  D   �  	   �     �  �     	   �     �  �   �     �     �  M   �  =   �     -     4     J     \     k  3   �     �  �   �     �     �     �  R  �  �        �  	            /     8  3   K  <     �   �     i  T  x  '   �     �  k   �  
   j  �   u  �       �     �  �   �     �     �     �  L   �     2  �   :     �     �  �        �     �               -     C     P  �   W  F         Z      j   	   o   !   y      �   ;   �      �   �   �      �!  "   �!     �!     �!     �!  �   �!     �"  �   �"  �   �#     6$  `   B$     �$     �$     �$  	   �$     �$     �$     �$  �   �$  .   �%  	   �%     &     &  �   %&  $   �&  ^   �&  �   Z'  :   �'  D   0(  [   u(  T   �(  q   &)     �)  
   �)  �   �)  )   3*  �   ]*     "+  
   )+     4+  �   @+     �+  ?   �+     /,  �   4,     -     -  �   )-  �   .  �   �.  l   �/  8  0  �   O1  X   2  P   u2  �   �2  �   u3  �   4  Q   �4  �   �4  k   �5  �   6  �   �6     m7  B   t7  �   �7  C   �8  _  �8  �   B:  
   ;  3   &;  .   Z;  �   �;  �   �<     t=  �   y=  z   >     �>     �>  �   �>  �   0?  �   �?  %  S@  �   yA  �   B  Q   �B  '   &C  �  NC  �   E  <   �E     �E     �E  *   �E      F  '   2F  '   ZF  2   �F  �  �F     UH     eH  '   H  B   �H  D   �H     /I     II  �   OI     �I     �I  �    J     �J     �J  M   K  =   _K     �K     �K     �K  4   �K     L  3   ,L     `L  �   zL     \M  +   qM     �M  R  �M  �   �N     �O  	  �O     	Q      Q  &   1Q  3   XQ  <   �Q  �   �Q  ,   vR  T  �R  '   �S      T  k   ;T      �T  �   �T  �   aU    V     "W  �   @W  %   *X  
   PX      [X  L   |X     �X  �   �X     ~Y     �Y  �   �Y     �Z  &   �Z  &   �Z  .    [  .   /[  #   ^[     �[  �   �[  F   T\     �\     �\  $   �\  !   �\     ]  ;   ]     Y]  �   l]     >^  &   S^  #   z^     �^     �^  �   �^     s_  �   �_  �   |`  &   a  `   -a     �a  ;   �a     �a     �a  "   b  %   8b     ^b  �   qb  .   Gc     vc  *   �c     �c  �   �c  $   �d  ^   �d  �   e  :   �e  D   �e  [   !f  T   }f  q   �f     Dg     ]g  �   zg  )   h  �   +h     �h  +   i     8i  �   Hi     �i  ?   �i     :j  �   Qj      k     0k  �   Jk  �   =l  �   �l  l   �m  8  7n  �   po  X   =p  P   �p  �   �p  �   �q  �   1r  Q   �r  �   s  k   �s  �   0t  �   �t      �u  B   �u  �   �u  C   �v  _  w  �   }x     Vy  3   ey  .   �y  �   �y  �   �z     �{  �   �{  z   _|     �|  .   �|  �   #}  �   �}  �   9~  %  �~  �   �  �   ��  Q   R�  '   ��   *Composition Guides* are available from the menu, which can help when framing a shot. There are eight types of guides available: :doc:`3D View clipping </editors/3dview/properties/panels>`. :kbd:`Ctrl-B` :kbd:`Ctrl-Numpad0` :menuselection:`Camera --> Depth of Field` :menuselection:`Camera --> Lens` :menuselection:`Properties -->  Camera` :menuselection:`View --> Render Border` :ref:`Presets <ui-presets>` to match real cameras. A *Camera* is an object that provides a means of rendering images from Blender. It defines which portion of a scene is visible in the rendered image. By default a scene contains one camera. However, a scene can contain more than one camera, but only one of them will be used at a time. So you will only need to add a new camera if you are making cuts between them. See :ref:`Animating Cameras <marker-bind-camera>`. Action Safe Active camera (left one). Adds lines connecting opposite corners. Adds lines dividing the frame in half vertically and horizontally. Adds lines dividing the frame in thirds vertically and horizontally. All modes Alpha Also known as *Graphics Safe*. Place all important information (graphics or text) inside this area to ensure it can be seen by the majority of viewers. Aperature Aperture Aperture radius *size*, or F-Stop *number* used for the render, and render preview. Using the F-Stop with a low number, or Radius with a large size will result in a strong blur, also allowing the use of the *bokeh effect*. Aperture type Blades Blender defaults show a ``4:3`` (square) ratio inside ``16:9`` (wide-screen). By :ref:`binding the camera to markers <marker-bind-camera>`. Camera Camera Display panel. Camera Operations Camera Presets Camera Presets panel. Camera view displaying safe areas, sensor and name. Cameras Cameras are invisible in renders, so they do not have any material or texture settings. However, they do have *Object* and *Editing* setting panels available which are displayed when a camera is the selected (active!) object. Center Center Diagonal Center-Cuts Center-cuts are a second set of safe areas to ensure content is seen correctly on screens with a different aspect ratio. Old TV sets receiving ``16:9`` or ``21:9`` video will cut off the sides. Position content inside the center-cut areas to make sure the most important elements of your composition can still be visible in these screens. Change the amount of distortion to simulate the anamorphic bokeh effect. A setting of 1.0 shows no distortion, where a number below 1.0 will cause a horizontal distortion, and a higher number will cause a vertical distortion. Changing the Active Camera Choose an object which will determine the focal point. Linking an object will deactivate the distance parameter. Typically this is used to give precise control over the position of the focal point, and also allows it to be animated or constrained to another object. Clip Start and End Clipping Composition Guides Controls the transparency of the passepartout mask. Cyan line: action center safe. Blue line: title center safe. Cycles supports Equirectangular and Fisheye panoramic cameras. Note that these cannot be displayed with OpenGL rendering in the viewport; they will only work for rendering. Depth of Field Different screens have varying amounts of :term:`overscan` (especially older TV sets). That means that not all content will be visible to all viewers, since parts of the image surrounding the edges are not shown. To work around this problem TV producers defined two areas where content is guaranteed to be shown: action safe and title safe. Displays a dotted frame in camera view. Distance Divides the width and height into Golden proportions (about 0.618 of the size from all sides of the frame). Dolly Zoom Draws a diagonal line from the lower left to upper right corners, then adds perpendicular lines that pass through the top left and bottom right corners. Draws a diagonal line from the lower left to upper right corners, then lines from the top left and bottom right corners to 0.618 the lengths of the opposite side. Each country sets a legal standard for broadcasting. These include, among other things, specific values for safe areas. Blender defaults for safe areas follow the EBU (European Union) standard. Make sure you are using the correct values when working for broadcast to avoid any trouble. Editor Enables the High Quality *viewport* depth of field, giving a more accurate representation of *depth of field*. This allows the viewport depth of field to be closely represented to that of the render and render preview depth of field. Equirectangular F-Stop Field of View Field of view angle, going to 360 and more to capture the whole environment. Fisheye Fisheye lenses are typically wide angle lenses with strong distortion, useful for creating panoramic images for e.g. dome projection, or as an artistic effect. Focal Length/Field of View Focus Object For OpenGL display, setting clipping distances to limited values is important to ensure sufficient rasterization precision. Ray tracing renders do not suffer from this issue so much, and as such more extreme values can safely be set. Golden Golden Triangle A Golden Triangle B Harmonious Triangle A Harmonious Triangle B High Quality Hotkey Hover the mouse over the *Distance* property and press :kbd:`E` to use a special *Depth Picker*. Then click on a point in the 3D View to sample the distance from that point to the camera. In Blender, safe areas can be set from the Camera and Sequencer views. Legal Standards Lens Lens Unit Lens focal length in millimeters. Limits Limits of the vertical and horizontal field of view angles. Main Safe Areas Make sure any significant action or characters in the shot are inside this area. This zone also doubles as a sort of "margin" for the screen which can be used to keep elements from piling up against the edges. Menu Minimum/Maximum Latitude/Longitude Mirror Ball Mist Mode Modern LCD/plasma screens with purely digital signals have no :term:`overscan`, yet safe areas are still considered best practice and may be legally required for broadcast. Name Note that this is effectively the only setting which applies to orthographic perspective. Since parallel lines do not converge in orthographic mode (no vanishing points), the lens shift settings are equivalent to translating the camera in the 3D View. Notice how the horizontal lines remain perfectly horizontal when using the lens shift, but do get skewed when rotating the camera object. Object Mode Option to control which dimension (vertical or horizontal) along which field of view angle fits. Orthographic Orthographic Scale Panel Panoramic Passepartout Perspective Ratio Real-world cameras transmit light through a lens that bends and focuses it onto the sensor. Because of this, objects that are a certain distance away are in focus, but objects in front and behind that are blurred. Red line: Action safe. Green line: Title safe. Reference Render Border Render Border toggle. Render a panoramic view of the scenes from the camera location and use an equirectangular projection, always rendering the full 360° over the X axis and 180° over the Y axis. Render border and associated render. Render from the same camera angle as the previous examples, but with orthographic perspective. Render is if taking a photo of a reflective mirror ball. This can be useful in rare cases to compare with a similar photo taken to capture an environment. Render of a train track scene with a *Perspective* camera. Render of a train track scene with a horizontal lens shift of 0.330. Render of a train track scene with a rotation of the camera object instead of a lens shift. Render of the same scene as above, but with a focal length of 210mm instead of 35mm. Rotate the polygonal blades along the facing axis, and will rotate in a clockwise, and counter-clockwise fashion. Rotation Safe Areas Safe areas are guides used to position elements to ensure that the most important parts of the content can be seen across all screens. Same as A, but with the opposite corners. Select the camera you would like to make active and press :kbd:`Ctrl-Numpad0` (by doing so, you also switch the view to camera view). In order to render, each scene **must** have an active camera. Sensor Sensor Fit Sensor size Sets the distance to the focal point when no *Focus Object* is specified. If *Limits* are enabled, a yellow cross is shown on the camera line of sight at this distance. Shift Shows a line which indicates *Start* and *End Clipping* values. Size Size of the camera visualization in the 3D View. This setting has **no** effect on the render output of a camera. The camera visualization can also be scaled using the standard Scale :kbd:`S` transform key. Size/Number Switching between Cameras The *Fisheye Equidistant* lens does not correspond to any real lens model; it will give a circular fisheye that does not take any sensor information into account but rather uses the whole sensor. This is a good lens for full-dome projections. The *Fisheye Equisolid* lens will best match real cameras. It provides a lens focal length and field of view angle, and will also take the sensor dimensions into account. The *Shift* setting allows for the adjustment of *vanishing points*. *Vanishing points* refer to the positions to which parallel lines converge. In this example, the most obvious vanishing point is at the end of the railroad. The *active* camera is the camera that is currently being used for rendering and camera view :kbd:`Numpad0`. The :term:`focal length` controls the amount of zoom, i.e. the amount of the scene which is visible all at once. Longer focal lengths result in a smaller :abbr:`FOV (Field of View)` (more zoom), while short focal lengths allow you to see more of the scene at once (larger :abbr:`FOV (Field of View)`, less zoom). The Safe Areas can be customized by their outer margin, which is a percentage scale of the area between the center and the render size. Values are shared between the Video Sequence editor and camera view. The Safe areas panel found in the camera properties, and the view mode of the Sequencer. The active camera can also be set in the *Scene* tab of the *Properties Editor*. The active camera, as well as the layers, can be specific to a given view, or global (locked) to the whole scene. See :doc:`Local Camera </editors/3dview/properties/panels>`. The area in focus is called the *focal point* and can be set using either an exact value, or by using the distance between the camera and a chosen object: The border can be disabled by disabling the *Border* option in the *Dimensions* panel in the *Render* tab or by activating the option again. The camera lens options control the way 3D objects are represented in a 2D image. The camera with the solid triangle on top is the active camera. Limit and mist indicators of cameras are drawn darker if the camera is not the active camera for the current scene. The focal length can be set either in terms of millimeters or the actual :term:`Field of View` as an angle. The interval in which objects are directly visible, Any objects outside this range still influence the image indirectly, as further light bounces are not clipped. The number of polygonal sides to give blurred objects in the viewport. The minimum number of blades needed to enable the bokeh effect is 3 (triangle). (Only available with High Quality). Thirds This controls the apparent size of objects projected on the image. This matches how you view things in the real world. Objects in the distance will appear smaller than objects in the foreground, and parallel lines (such as the rails on a railroad) will appear to converge as they get farther away. This option darkens the area outside of the camera's field of view. This projection is compatible with the environment texture as used for world shaders, so it can be used to render an environment map. To match the default mapping, set the camera object rotation to (90, 0, -90) or pointing along the positive X axis. This corresponds to looking at the center of the image using the default environment texture mapping. This setting is an alternative way to control the focal length, it is useful to match the camera in Blender to a physical camera & lens combination, e.g. for :doc:`motion tracking </editors/movie_clip_editor/index>`. Title Safe To see how this works, take the following examples: Toggle name display on and off in camera view. Toggles viewing of the mist limits on and off. The limits are shown as two connected white dots on the camera line of sight. The mist limits and other options are set in the *World* panel, in the :doc:`Mist section </render/blender_render/world/mist>`. Total number of polygonal blades used to alter the shape of the blurred objects in the render, and render preview. As with the viewport, the minimum amount of blades to enable the bokeh effect is 3, resulting in a triangular-shaped blur. Type Use F-Stop or Radius to set the aperture for the render, and render preview. F-Stop is the focal ratio, where Radius is the radius of the focal point. Using lens shift is equivalent to rendering an image with a larger :abbr:`FOV (Field of View)` and cropping it off-center. Viewport Viewport Display Viewport depth of field aperture measured in F-Stops. Smaller numbers will cause more blur in the viewport, OpenGL renders, and Sequencer. When *Limits* in the *Display* panel is enabled, the clip bounds will be visible as two yellow connected dots on the camera line of sight. When Render Border is activated, :doc:`Sampled Motion Blur </render/blender_render/settings/motion_blur>` will become available to view in the 3D View. While in camera view, you can define a subregion to render by drawing out a rectangle within the camera's frame. Your renders will now be limited to the part of scene visible within the render border. This can be very useful for reducing render times for quick previews on an area of interest. While the camera is moving towards an object the *Focal Length* property can be decreased to produce a *Dolly Zoom* camera effect, or vice versa. With *Orthographic* perspective objects always appear at their actual size, regardless of distance. This means that parallel lines appear parallel, and do not converge like they do with *Perspective*. `This video <https://vimeo.com/15837189>`__ demos the *Dolly Zoom* camera effect. todo 2.8: move this to somewhere better Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-24 23:43+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 *Composition Guides* are available from the menu, which can help when framing a shot. There are eight types of guides available: :doc:`3D View clipping </editors/3dview/properties/panels>`. :kbd:`Ctrl-B` :kbd:`Ctrl-Numpad0` :menuselection:`Camera --> Depth of Field` :menuselection:`Camera --> Lens` :menuselection:`Properties -->  Camera` :menuselection:`View --> Render Border` :ref:`Presets <ui-presets>` to match real cameras. A *Camera* is an object that provides a means of rendering images from Blender. It defines which portion of a scene is visible in the rendered image. By default a scene contains one camera. However, a scene can contain more than one camera, but only one of them will be used at a time. So you will only need to add a new camera if you are making cuts between them. See :ref:`Animating Cameras <marker-bind-camera>`.  -- Action Safe Active camera (left one). Adds lines connecting opposite corners. Adds lines dividing the frame in half vertically and horizontally. Adds lines dividing the frame in thirds vertically and horizontally. Tổng thể -- All modes Alpha Also known as *Graphics Safe*. Place all important information (graphics or text) inside this area to ensure it can be seen by the majority of viewers. -- Aperature -- Aperture Aperture radius *size*, or F-Stop *number* used for the render, and render preview. Using the F-Stop with a low number, or Radius with a large size will result in a strong blur, also allowing the use of the *bokeh effect*.  -- Aperture type Số Lá của Khẩu -- Blades Blender defaults show a ``4:3`` (square) ratio inside ``16:9`` (wide-screen). By :ref:`binding the camera to markers <marker-bind-camera>`. Máy Quay Phim -- Camera Camera Display panel. -- Camera Operations Sắp Đặt Sẵn của Máy Quay -- Camera Presets Camera Presets panel. Camera view displaying safe areas, sensor and name. Máy Quay Phim -- Cameras Cameras are invisible in renders, so they do not have any material or texture settings. However, they do have *Object* and *Editing* setting panels available which are displayed when a camera is the selected (active!) object. Trung Tâm -- Center Đường Chéo Qua Tâm -- Center Diagonal -- Center-Cuts Center-cuts are a second set of safe areas to ensure content is seen correctly on screens with a different aspect ratio. Old TV sets receiving ``16:9`` or ``21:9`` video will cut off the sides. Position content inside the center-cut areas to make sure the most important elements of your composition can still be visible in these screens. Change the amount of distortion to simulate the anamorphic bokeh effect. A setting of 1.0 shows no distortion, where a number below 1.0 will cause a horizontal distortion, and a higher number will cause a vertical distortion. -- Changing the Active Camera Choose an object which will determine the focal point. Linking an object will deactivate the distance parameter. Typically this is used to give precise control over the position of the focal point, and also allows it to be animated or constrained to another object.  -- Clip Start and End Xén -- Clipping Khung Bố Cục -- Composition Guides Controls the transparency of the passepartout mask. Cyan line: action center safe. Blue line: title center safe. Cycles supports Equirectangular and Fisheye panoramic cameras. Note that these cannot be displayed with OpenGL rendering in the viewport; they will only work for rendering. Độ Sâu Trường Ảnh -- Depth of Field Different screens have varying amounts of :term:`overscan` (especially older TV sets). That means that not all content will be visible to all viewers, since parts of the image surrounding the edges are not shown. To work around this problem TV producers defined two areas where content is guaranteed to be shown: action safe and title safe. Displays a dotted frame in camera view. Khoảng Cách -- Distance Divides the width and height into Golden proportions (about 0.618 of the size from all sides of the frame). Lướt Thu/Phóng -- Dolly Zoom Draws a diagonal line from the lower left to upper right corners, then adds perpendicular lines that pass through the top left and bottom right corners. Draws a diagonal line from the lower left to upper right corners, then lines from the top left and bottom right corners to 0.618 the lengths of the opposite side. Each country sets a legal standard for broadcasting. These include, among other things, specific values for safe areas. Blender defaults for safe areas follow the EBU (European Union) standard. Make sure you are using the correct values when working for broadcast to avoid any trouble. Trình Biên Soạn -- Editor Enables the High Quality *viewport* depth of field, giving a more accurate representation of *depth of field*. This allows the viewport depth of field to be closely represented to that of the render and render preview depth of field. Vuông Góc Đều -- Equirectangular  -- F-Stop Trường Ảnh -- Field of View Field of view angle, going to 360 and more to capture the whole environment. Mắt Cá -- Fisheye Fisheye lenses are typically wide angle lenses with strong distortion, useful for creating panoramic images for e.g. dome projection, or as an artistic effect.  -- Focal Length/Field of View  -- Focus Object For OpenGL display, setting clipping distances to limited values is important to ensure sufficient rasterization precision. Ray tracing renders do not suffer from this issue so much, and as such more extreme values can safely be set. Tỷ Lệ Vàng -- Golden Tam Giác Vàng A -- Golden Triangle A Tam Giác Vàng B -- Golden Triangle B Tam Giác Hài Hòa A -- Harmonious Triangle A Tam Giác Hài Hòa B -- Harmonious Triangle B Chất Lượng Cao -- High Quality Phím Nóng -- Hotkey Hover the mouse over the *Distance* property and press :kbd:`E` to use a special *Depth Picker*. Then click on a point in the 3D View to sample the distance from that point to the camera. In Blender, safe areas can be set from the Camera and Sequencer views. Legal Standards Lăng Kính -- Lens Đơn Vị Thấu Kính -- Lens Unit Lens focal length in millimeters. Giới Hạn -- Limits Limits of the vertical and horizontal field of view angles. -- Main Safe Areas Make sure any significant action or characters in the shot are inside this area. This zone also doubles as a sort of "margin" for the screen which can be used to keep elements from piling up against the edges. Trình Đơn -- Menu  -- Minimum/Maximum Latitude/Longitude Địa Cầu Gương -- Mirror Ball Sương Mù -- Mist Chế Độ -- Mode Modern LCD/plasma screens with purely digital signals have no :term:`overscan`, yet safe areas are still considered best practice and may be legally required for broadcast. Tên -- Name Note that this is effectively the only setting which applies to orthographic perspective. Since parallel lines do not converge in orthographic mode (no vanishing points), the lens shift settings are equivalent to translating the camera in the 3D View. Notice how the horizontal lines remain perfectly horizontal when using the lens shift, but do get skewed when rotating the camera object. Chế Độ Vật Thể -- Object Mode Option to control which dimension (vertical or horizontal) along which field of view angle fits. Chính Giao -- Orthographic Tỷ Lệ Chính Giao -- Orthographic -- Orthographic Scale Bảng -- Panel Màn Ảnh Rộng -- Panoramic Khung Cắt Cảnh -- Passepartout Phối Cảnh Xa Gần -- Perspective Tỷ Số -- Ratio Real-world cameras transmit light through a lens that bends and focuses it onto the sensor. Because of this, objects that are a certain distance away are in focus, but objects in front and behind that are blurred. Red line: Action safe. Green line: Title safe. Tham Chiếu -- Reference Khoanh Vùng Kết Xuất -- Render Border Render Border toggle. Render a panoramic view of the scenes from the camera location and use an equirectangular projection, always rendering the full 360° over the X axis and 180° over the Y axis. Render border and associated render. Render from the same camera angle as the previous examples, but with orthographic perspective. Render is if taking a photo of a reflective mirror ball. This can be useful in rare cases to compare with a similar photo taken to capture an environment. Render of a train track scene with a *Perspective* camera. Render of a train track scene with a horizontal lens shift of 0.330. Render of a train track scene with a rotation of the camera object instead of a lens shift. Render of the same scene as above, but with a focal length of 210mm instead of 35mm. Rotate the polygonal blades along the facing axis, and will rotate in a clockwise, and counter-clockwise fashion. Xoay Chiều -- Rotation Vùng An Toàn -- Safe Areas Safe areas are guides used to position elements to ensure that the most important parts of the content can be seen across all screens. Same as A, but with the opposite corners. Select the camera you would like to make active and press :kbd:`Ctrl-Numpad0` (by doing so, you also switch the view to camera view). In order to render, each scene **must** have an active camera. Bộ Cảm Biến -- Sensor Khít với Bộ Cảm Biến -- Sensor Fit  -- Sensor size Sets the distance to the focal point when no *Focus Object* is specified. If *Limits* are enabled, a yellow cross is shown on the camera line of sight at this distance. -- Shift Shows a line which indicates *Start* and *End Clipping* values. Kích Thước -- Size Size of the camera visualization in the 3D View. This setting has **no** effect on the render output of a camera. The camera visualization can also be scaled using the standard Scale :kbd:`S` transform key.  -- Size/Number Switching between Cameras The *Fisheye Equidistant* lens does not correspond to any real lens model; it will give a circular fisheye that does not take any sensor information into account but rather uses the whole sensor. This is a good lens for full-dome projections. The *Fisheye Equisolid* lens will best match real cameras. It provides a lens focal length and field of view angle, and will also take the sensor dimensions into account. The *Shift* setting allows for the adjustment of *vanishing points*. *Vanishing points* refer to the positions to which parallel lines converge. In this example, the most obvious vanishing point is at the end of the railroad. The *active* camera is the camera that is currently being used for rendering and camera view :kbd:`Numpad0`. The :term:`focal length` controls the amount of zoom, i.e. the amount of the scene which is visible all at once. Longer focal lengths result in a smaller :abbr:`FOV (Field of View)` (more zoom), while short focal lengths allow you to see more of the scene at once (larger :abbr:`FOV (Field of View)`, less zoom). The Safe Areas can be customized by their outer margin, which is a percentage scale of the area between the center and the render size. Values are shared between the Video Sequence editor and camera view. The Safe areas panel found in the camera properties, and the view mode of the Sequencer. The active camera can also be set in the *Scene* tab of the *Properties Editor*. The active camera, as well as the layers, can be specific to a given view, or global (locked) to the whole scene. See :doc:`Local Camera </editors/3dview/properties/panels>`. The area in focus is called the *focal point* and can be set using either an exact value, or by using the distance between the camera and a chosen object: The border can be disabled by disabling the *Border* option in the *Dimensions* panel in the *Render* tab or by activating the option again. The camera lens options control the way 3D objects are represented in a 2D image. The camera with the solid triangle on top is the active camera. Limit and mist indicators of cameras are drawn darker if the camera is not the active camera for the current scene. The focal length can be set either in terms of millimeters or the actual :term:`Field of View` as an angle. The interval in which objects are directly visible, Any objects outside this range still influence the image indirectly, as further light bounces are not clipped. The number of polygonal sides to give blurred objects in the viewport. The minimum number of blades needed to enable the bokeh effect is 3 (triangle). (Only available with High Quality). Luật Một Phần Ba -- Thirds This controls the apparent size of objects projected on the image. This matches how you view things in the real world. Objects in the distance will appear smaller than objects in the foreground, and parallel lines (such as the rails on a railroad) will appear to converge as they get farther away. This option darkens the area outside of the camera's field of view. This projection is compatible with the environment texture as used for world shaders, so it can be used to render an environment map. To match the default mapping, set the camera object rotation to (90, 0, -90) or pointing along the positive X axis. This corresponds to looking at the center of the image using the default environment texture mapping. This setting is an alternative way to control the focal length, it is useful to match the camera in Blender to a physical camera & lens combination, e.g. for :doc:`motion tracking </editors/movie_clip_editor/index>`.  -- Title Safe To see how this works, take the following examples: Toggle name display on and off in camera view. Toggles viewing of the mist limits on and off. The limits are shown as two connected white dots on the camera line of sight. The mist limits and other options are set in the *World* panel, in the :doc:`Mist section </render/blender_render/world/mist>`. Total number of polygonal blades used to alter the shape of the blurred objects in the render, and render preview. As with the viewport, the minimum amount of blades to enable the bokeh effect is 3, resulting in a triangular-shaped blur. Thể Loại -- Type Use F-Stop or Radius to set the aperture for the render, and render preview. F-Stop is the focal ratio, where Radius is the radius of the focal point. Using lens shift is equivalent to rendering an image with a larger :abbr:`FOV (Field of View)` and cropping it off-center. Khung Chiếu -- Viewport Hiển Thị Khung Chiếu -- Viewport Display Viewport depth of field aperture measured in F-Stops. Smaller numbers will cause more blur in the viewport, OpenGL renders, and Sequencer. When *Limits* in the *Display* panel is enabled, the clip bounds will be visible as two yellow connected dots on the camera line of sight. When Render Border is activated, :doc:`Sampled Motion Blur </render/blender_render/settings/motion_blur>` will become available to view in the 3D View. While in camera view, you can define a subregion to render by drawing out a rectangle within the camera's frame. Your renders will now be limited to the part of scene visible within the render border. This can be very useful for reducing render times for quick previews on an area of interest. While the camera is moving towards an object the *Focal Length* property can be decreased to produce a *Dolly Zoom* camera effect, or vice versa. With *Orthographic* perspective objects always appear at their actual size, regardless of distance. This means that parallel lines appear parallel, and do not converge like they do with *Perspective*. `This video <https://vimeo.com/15837189>`__ demos the *Dolly Zoom* camera effect. todo 2.8: move this to somewhere better 