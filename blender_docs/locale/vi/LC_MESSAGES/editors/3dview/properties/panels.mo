��    1      �              ,     -  �   �  �   Z     �     �     �  x     -   �  �   �  l   F  T   �  ~     e   �     �       �     �   
	  
   �	  �   �	  �   �
     N     S     Y     f  w   z     �               1  u   =     �     �     �     �  ^   �     J  �   W  [   �  6   T  L   �     �  g   �  �   Q  
   �  �   �  �   �     7     H  �  P       �   �  �   5  ?   �     �  f     x   n  -   �  �     l   �  T     ~   i  e   �  9   N  $   �  �   �  �   �     d  �   �  �   x     �  ,     .   ?  6   n  w   �  &     (   D     m     �  u   �  4   $   *   Y   )   �      �   ^   �   #    !  �   D!  [   �!  6   A"  L   x"  ,   �"  g   �"  �   Z#     �#  �   $  �   �$  &   U%     |%   A large clipping range will allow you to see both near and far objects, but reduces the depth precision resulting in artifacts. Active camera used in this view to override the (global) scene camera. The option is available only when *lock local camera and layers* toggle in the header is not enabled. Adjust the minimum and maximum distances range to be visible for the viewport camera. Objects outside the range will not be shown. All Object Origins Axis Clip Start and Clip End Control the focal length of the 3D View camera in millimeters, unlike a :doc:`rendering camera </render/cycles/camera>`. Controls the distance between the grid lines. Controls the number of sub-lines that appear in each cell of the grid. In aligned orthographic views the level of subdivision depend on the zoom. Controls the total number of lines that make the grid, in both directions (odd values will be rounded down). Controls whether the dashed parenting, constraining, hooking, etc., lines are drawn. Controls which global axes are shown as colored lines (Grid floor only). Their length depend on the defined size of that grid. Creates an estimation of what the world background will look like and uses it to draw the background. Display & View Panels Display Panel Displays only items that will be rendered. This option hides visualizations, overlays, the 3D cursor, and the grid floor. The :doc:`3D manipulator widget </editors/3dview/object/editing/transform/control/manipulators>` has to be toggled separately. Forces the origin dot of objects to always be visible, even for non-selected objects (by default, unselected objects' origins might be hidden by geometry in solid/shaded/textured shadings). Grid Floor Grid Floor is a finite grid which is shown in views that are not orthographically aligned (top, front, side). It lays on the global XY plane. The checkbox lets you show or hide that grid. In aligned orthographic views an infinite grid is shown. If disabled, the orange outline around your selected objects in *Solid*, *Shaded*, *Textured* draw types will no longer be displayed. Lens Lines Local Camera Lock Camera to View Lock the center of the view to the position of the 3D cursor. It is only available when *Lock to Object* is not active. Lock to Cursor Lock to Object Lock to Object lets you define an object in the *Object* Data ID as the center of the view. In that case, the view can be rotated around or zoomed towards that central object, but not on translation, unless you translate that itself object (this option is not available in a camera view). Only Render Options such as restrict-render, modifiers render option, dupli-parents and render layers are not taken into account. Outline Selected Relationship Lines Render Border Scale See :ref:`Troubleshooting Depth Buffer Glitches <troubleshooting-depth>` for more information. Subdivisions The *View Properties* panel lets you set other settings regarding the 3D View. You can show it with the :menuselection:`View --> View Properties...` menu entry. This can be useful for a preview and for :doc:`OpenGL </render/opengl>` viewport rendering. This is also used for the size of newly added objects. This panel lets you configure some visualization parameters of the viewport. Toggle Quad View Toggles the four view 3D View. :doc:`Read more about arranging areas </interface/window_system/areas>`. Use a Render Border when not looking through a camera. Using :kbd:`Ctrl-B` to draw a border region will automatically enable this option. View Panel When in camera view, all changes in the view (pans, rotations, zooms) will affect the active camera, which will follow all those changes. The camera frame will be outlined with a red dashed line. While the option displays the regular viewport without distracting elements, the objects displayed do **not** match the final render output. World Background X, Y, Z Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-22 15:35+0000
PO-Revision-Date: 2018-12-10 17:58+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A large clipping range will allow you to see both near and far objects, but reduces the depth precision resulting in artifacts. Active camera used in this view to override the (global) scene camera. The option is available only when *lock local camera and layers* toggle in the header is not enabled. Adjust the minimum and maximum distances range to be visible for the viewport camera. Objects outside the range will not be shown. Gốc Tọa Độ của mọi Vật Thể -- All Object Origins Trục -- Axis điểm cắt bắt đầu và điểm cắt cuối cùng (trường ảnh) -- Clip Start and Clip End Control the focal length of the 3D View camera in millimeters, unlike a :doc:`rendering camera </render/cycles/camera>`. Controls the distance between the grid lines. Controls the number of sub-lines that appear in each cell of the grid. In aligned orthographic views the level of subdivision depend on the zoom. Controls the total number of lines that make the grid, in both directions (odd values will be rounded down). Controls whether the dashed parenting, constraining, hooking, etc., lines are drawn. Controls which global axes are shown as colored lines (Grid floor only). Their length depend on the defined size of that grid. Creates an estimation of what the world background will look like and uses it to draw the background. Bảng Hiển Thị & Góc Nhìn -- Display & View Panels Bảng Hiển Thị -- Display Panel Displays only items that will be rendered. This option hides visualizations, overlays, the 3D cursor, and the grid floor. The :doc:`3D manipulator widget </editors/3dview/object/editing/transform/control/manipulators>` has to be toggled separately. Forces the origin dot of objects to always be visible, even for non-selected objects (by default, unselected objects' origins might be hidden by geometry in solid/shaded/textured shadings). Sàn Đồ Thị -- Grid Floor Grid Floor is a finite grid which is shown in views that are not orthographically aligned (top, front, side). It lays on the global XY plane. The checkbox lets you show or hide that grid. In aligned orthographic views an infinite grid is shown. If disabled, the orange outline around your selected objects in *Solid*, *Shaded*, *Textured* draw types will no longer be displayed. Lăng Kính -- Lens (Số) Đường Kẻ/Thẳng/Dòng -- Lines Máy Quay Phim Địa Phương -- Local Camera Khóa Máy Quay vào Góc Nhìn -- Lock Camera to View Lock the center of the view to the position of the 3D cursor. It is only available when *Lock to Object* is not active. Khóa vào Con Trỏ -- Lock to Cursor Khóa vào Vật Thể -- Lock to Object Lock to Object lets you define an object in the *Object* Data ID as the center of the view. In that case, the view can be rotated around or zoomed towards that central object, but not on translation, unless you translate that itself object (this option is not available in a camera view). Duy Kết Xuất -- Only Render Options such as restrict-render, modifiers render option, dupli-parents and render layers are not taken into account. Viền Nét cái Được Chọn -- Outline Selected Đường Liên Hệ -- Relationship Lines Ranh Giới Kết Xuất -- Render Border Tỷ Lệ -- Scale See :ref:`Troubleshooting Depth Buffer Glitches <troubleshooting-depth>` for more information. Lượng Phân Hóa -- Subdivisions The *View Properties* panel lets you set other settings regarding the 3D View. You can show it with the :menuselection:`View --> View Properties...` menu entry. This can be useful for a preview and for :doc:`OpenGL </render/opengl>` viewport rendering. This is also used for the size of newly added objects. This panel lets you configure some visualization parameters of the viewport. Bật/Tắt 4 Góc Nhìn -- Toggle Quad View Toggles the four view 3D View. :doc:`Read more about arranging areas </interface/window_system/areas>`. Use a Render Border when not looking through a camera. Using :kbd:`Ctrl-B` to draw a border region will automatically enable this option. Bảng Góc Nhìn -- View Panel When in camera view, all changes in the view (pans, rotations, zooms) will affect the active camera, which will follow all those changes. The camera frame will be outlined with a red dashed line. While the option displays the regular viewport without distracting elements, the objects displayed do **not** match the final render output. Nền Thế Giới -- World Background X, Y, Z 