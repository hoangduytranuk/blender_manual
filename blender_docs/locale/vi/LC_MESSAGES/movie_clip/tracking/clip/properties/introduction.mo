��                        �    �               "     0     =    O     R     b  �   z     4     :     G     [     `     n     }     �     �     �  �   �  U   �  �       �	     �	     
     
     5
  �  <
    �  /        B  &   T      {  6   �    �  $   �  ?   �    ;     D     Y  9   x     �  #   �     �     �  4         I  5   j  �   �  U   �  q  �      b  ;   �     �  9   �        Another use of Track Weights is when you want to reconstruct a scene from your camera solution. In that case you can first carefully track and solve your scene, and once you're done, lock all your markers with :kbd:`Ctrl-L`, set the tracker weight in the Extra Settings of the tracker settings to zero and use the feature detection to quickly add lots of markers. Now track them and solve the scene again. Since their weight is zero they will not influence your solution at all, but you will have lots of good reference points in your scene. Auto Keyframe Channels Color Presets Custom Color Enable (eye icon) Field to select an image which will be displayed inside the plane track. This image is for preview purposes in the Movie Clip editor only. To include it in your final render, see :doc:`Plane Track Deform node </compositing/types/distort/plane_track_deform>`. Further Options Grayscale Preview (B/W) If some tracks were added and tracked to the wrong object, they can be copied to another object using :menuselection:`Track --> Copy Tracks` and :menuselection:`Track --> Paste Tracks`. Image Introduction Lock (padlock icon) Name Objects Panel Objects panel. Opacity Plane Track Panel Plane Track panel. Stabilization Weight The usage for all kind of objects (used for camera and object tracking) is the same: track features, set camera data, solve motion. Camera data is sharing between all objects and refining of camera intrinsics happens when solving camera motion only. This panel contains :ref:`tracker settings <clip-tracking-settings>` for each marker. This panel contains a :ref:`list view <ui-list-view>` with all objects which can be used for tracking, camera or object solving. By default there is only one object in this list which is used for camera solving. It cannot be deleted and other objects cannot be used for camera solving; all added objects are used for object tracking and solving only. These objects can be referenced from Follow Track and Object Solver constraints. Follow Track uses the camera object by default. Track Panel Track Preview Widget Track panel. Tracking Settings Panel Weight Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-06 20:15+0100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Another use of Track Weights is when you want to reconstruct a scene from your camera solution. In that case you can first carefully track and solve your scene, and once you're done, lock all your markers with :kbd:`Ctrl-L`, set the tracker weight in the Extra Settings of the tracker settings to zero and use the feature detection to quickly add lots of markers. Now track them and solve the scene again. Since their weight is zero they will not influence your solution at all, but you will have lots of good reference points in your scene. Tạo Khung Khóa Tự Động -- Auto Keyframe Kênh -- Channels Màu Định Trước -- Color Presets Màu Tùy Chọn -- Custom Color Bật (biểu tượng con mắt) -- Enable (eye icon) Field to select an image which will be displayed inside the plane track. This image is for preview purposes in the Movie Clip editor only. To include it in your final render, see :doc:`Plane Track Deform node </compositing/types/distort/plane_track_deform>`. Tùy Chọn Khác -- Further Options Xem Trước Gam Xám (Trắng/Đen) -- Grayscale Preview (B/W) If some tracks were added and tracked to the wrong object, they can be copied to another object using :menuselection:`Giám Sát/Rãnh (Track) --> Sao Chép Giám Sát (Copy Tracks)` and :menuselection:`Giám Sát/Rãnh (Track) --> Dán Giám Sát (Paste Tracks)`. Hình Ảnh -- Image Giới Thiệu -- Introduction Khóa (biểu tượng cái khóa) -- Lock (padlock icon) Tên -- Name Bảng Vật Thể -- Objects Panel Bảng các vật thể. Độ Đục -- Opacity Bảng Giám Sát Mặt Phẳng -- Plane Track Panel Bảng giám sát mặt phẳng. Trọng Lượng Ổn Định -- Stabilization Weight The usage for all kind of objects (used for camera and object tracking) is the same: track features, set camera data, solve motion. Camera data is sharing between all objects and refining of camera intrinsics happens when solving camera motion only. This panel contains :ref:`tracker settings <clip-tracking-settings>` for each marker. Bảng này chứa một :ref:`Danh sách liệt kê <ui-list-view>` tất cả các đối tượng có thể được sử dụng để giám sát, máy quay phim hoặc giải nghiệm vật thể. Theo mặc định, chỉ có một đối tượng trong danh sách này được sử dụng để giải nghiệm máy quay phim. Nó không thể bị xóa đi được và các đối tượng khác không thể được sử dụng để giải nghiệm máy quay phim; tất cả các đối tượng được thêm vào chỉ được sử dụng để theo dõi và giải nghiệm đối tượng mà thôi. Các đối tượng này có thể được tham chiếu từ các ràng buộc của Đi Theo Giám Sát (Follow Track) và Giải Nghiệm Vật Thể (Object Solver). Theo mặc định ràng buộc Đi Theo Giám Sát sử dụng vật thể máy quay phim. Bảng Giám Sát -- Track Panel Thành Tố Xem Trước Giám Sát -- Track Preview Widget Bảng giám sát. Bảng Sắp Đặt Giám Sát -- Tracking Settings Panel Trọng Lượng -- Weight 