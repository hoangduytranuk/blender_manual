��    h      \              �  }   �       #   (    L  &   Y     �     �     �     �     �     �  /   �  !   	  (   /	     X	  $   x	     �	  
   �	  �   �	     �
     �
  1   �
  �   �
     �     �     �  c   �     3     K  #   g     �     �     �  U   �     )     8     H     V  I   c  H   �  +   �     "     *     B     Z     s     �     �     �  !   �  9   �  }   +  `   �     
          7     M     _     f  O   v     �  h   �     @  ;   E     �  !   �  +   �  5   �  $        1     Q     _     n  `   }  	   �     �     �  \        r  Z   �     �        8   %  	   ^  	   h     r  '   w  ,   �  1   �  @   �  A   ?  b   �     �     �  j   �  �   g  M  �  @  :  	   {     �  ~   �  ~     o   �  �    }   �     <  #   I    m  &   z     �     �     �     �     �     �  E   �  !   D  (   f     �  $   �     �  '   �  �         �      !  Q   ,!  �   ~!      "  3   5"  D   i"  c   �"     #  L   *#  f   w#  @   �#  O   $  @   o$  U   �$  (   %  /   /%  )   _%  $   �%  I   �%  H   �%  +   A&     m&     �&  %   �&  $   �&     �&  0   '  )   2'  )   \'  !   �'  9   �'  }   �'  �   `(     �(  I   )     \)  *   r)     �)  *   �)  O   �)  ,   .*  h   [*     �*  ;   �*     +  !   5+  +   W+  ?   �+  $   �+     �+  )   ,  *   2,  $   ],  `   �,     �,  !   �,  T   -  �   t-  K   .  Z   Y.  >   �.  M   �.  a   A/     �/     �/     �/  '   �/  ,   0  1   <0  @   n0  A   �0  b   �0     T1  -   e1  j   �1  �   �1  M  �2  @  �3     5  ,   ,5  ~   Y5  ~   �5  o   W6   *Clean Keyframes* resets the keyframe tangents on selected keyframes to their auto-clamped shape, if they have been modified. :kbd:`Alt-O` :kbd:`B` for border select/deselect :kbd:`Ctrl-LMB` inserts a keyframe to the active F-Curve at the mouse position. The newly added keyframes will be selected, making it easier to quickly tweak the newly added keyframes. All previously selected keyframes are kept selected by using :kbd:`Shift-Ctrl-LMB`. :kbd:`Ctrl-LMB`, :kbd:`Shift-Ctrl-LMB` :kbd:`G` to grab :kbd:`R` to rotate :kbd:`S` to scale :kbd:`Shift-M` :kbd:`Shift-S` :kbd:`X` :menuselection:`Key --> Bake Sound to F-Curves` :menuselection:`Key --> Channels` :menuselection:`Key --> Clean Keyframes` :menuselection:`Key --> Mirror` :menuselection:`Key --> Smooth Keys` :menuselection:`Key --> Snap` Accumulate Acts like the *Clean Keyframes* tool but will also delete the channel itself if it is only left with a single keyframe containing the default property value and it's not being used by any generative f-curve modifiers or drivers. Additive After Flatten Handles. All values lower than this threshold result in 0. And of course you can lock the transformation along the X axis (time frame) or Y axis (value) by pressing :kbd:`X` or :kbd:`Y` during transformation. Attack time Bake Curves :kbd:`Alt-C` Bake Sound to F-Curves Baking a curve replaces it with a set of sampled points, and removes the ability to edit the curve. Before Flatten Handles. By Times Over Current Frame By Times over First Selected Marker By Times over Time 0 By Values over Cursor Value By Values over Value 0 By default, when new channels are added, the *Graph Editor* sets them to *Edit Mode*. Clean Channels Clean Keyframes Current Frame Cursor Value Cutoff frequency of a high-pass filter that is applied to the audio data. Cutoff frequency of a low-pass filter that is applied to the audio data. Divide Transformation by 10.0 :kbd:`Shift`. Editing F-Curve after cleaning. F-Curve after sampling. F-Curve after smoothing. F-Curve before cleaning. F-Curve before sampling. F-Curve before smoothing. Flatten Handles Flatten Handles snapping example. Flatten the *Bézier* handles for the selected keyframes. For precise control of the keyframe position and value, you can set values in the *Active Keyframe* of the Properties Region. Gives the output as a square curve. Negative values always result in -1, and positive ones in 1. Hide :kbd:`H` Hide Unselected :kbd:`Shift-H` Hide selected curves. Highest frequency Hotkey Insert Keyframe Keyframes can be snapped to different properties by using the *Snap Keys* tool. Lowest frequency Many of the hotkeys are the same as the :doc:`3D View ones </editors/3dview/object/index>`, for example: Menu Minimum amplitude value needed to influence the hull curve. Mirror Mirror horizontally over frame 0. Mirror horizontally over the *Time Cursor*. Mirror horizontally over the first selected *Marker*. Mirror vertically over the *Cursor*. Mirror vertically over value 0. Nearest Frame Nearest Marker Nearest Second Only the positive differences of the hull curve amplitudes are summarized to produce the output. Reference Release time Sample Keyframes :kbd:`Shift-O` Sampling a set of keyframes replaces interpolated values with a new keyframe for each frame. Sampling and Baking Keyframes Selected keyframes can be mirrored over different properties using the *Mirror Keys* tool. Show Hidden :kbd:`Alt-H` Show all previous hidden curves. Show only the selected curve (and hide everything else). Show/Hide Smoothing Snap Snap Transformation to 1.0 :kbd:`Ctrl`. Snap the selected keyframes to the *Cursor*. Snap the selected keyframes to the *Time Cursor*. Snap the selected keyframes to their nearest frame individually. Snap the selected keyframes to their nearest marker individually. Snap the selected keyframes to their nearest second individually, based on the *FPS* of the scene. Square Square Threshold The *Bake Sound to F-Curves* tool takes a sound file and uses its sound wave to create the animation data. The amplitudes of the hull curve are summarized. If *Accumulate* is enabled, both positive and negative differences are accumulated. The modified curve left after the Clean tool is run is not the same as the original, so this tool is better used before doing custom editing of f-curves and after initial keyframe insertion, to get rid of any unwanted keyframes inserted while doing mass keyframe insertion (by selecting all bones and pressing :kbd:`I` for instance). There is also an option to smooth the selected curves, but beware: its algorithm seems to be to divide by two the distance between each keyframe and the average linear value of the curve, without any setting, which gives quite a strong smoothing! Note that the first and last keys seem to be never modified by this tool. Threshold Transform Snapping Value for the hull curve calculation that tells how fast the hull curve can fall. The lower the value the steeper it can fall. Value for the hull curve calculation that tells how fast the hull curve can rise. The lower the value the steeper it can rise. When transforming keyframes with :kbd:`G`, :kbd:`R`, :kbd:`S`, the transformation can be snapped to increments. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-01-17 21:30+0000
PO-Revision-Date: 2019-01-21 01:57+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 *Clean Keyframes* resets the keyframe tangents on selected keyframes to their auto-clamped shape, if they have been modified. :kbd:`Alt-O` :kbd:`B` for border select/deselect :kbd:`Ctrl-LMB` inserts a keyframe to the active F-Curve at the mouse position. The newly added keyframes will be selected, making it easier to quickly tweak the newly added keyframes. All previously selected keyframes are kept selected by using :kbd:`Shift-Ctrl-LMB`. :kbd:`Ctrl-LMB`, :kbd:`Shift-Ctrl-LMB` :kbd:`G` to grab :kbd:`R` to rotate :kbd:`S` to scale :kbd:`Shift-M` :kbd:`Shift-S` :kbd:`X` :menuselection:`Khóa --> Nướng Âm Thanh thành Đường Cong-F` :menuselection:`Key --> Channels` :menuselection:`Key --> Clean Keyframes` :menuselection:`Key --> Mirror` :menuselection:`Key --> Smooth Keys` :menuselection:`Key --> Snap` Chồng Chất/Tích Tụ -- Accumulate Acts like the *Clean Keyframes* tool but will also delete the channel itself if it is only left with a single keyframe containing the default property value and it's not being used by any generative f-curve modifiers or drivers. Bổ Sung -- Additive After Flatten Handles. Tất cả các giá trị thấp hơn ngưỡng này sẽ cho kết quả là 0. And of course you can lock the transformation along the X axis (time frame) or Y axis (value) by pressing :kbd:`X` or :kbd:`Y` during transformation. Thời gian công -- Attack time Nướng Đường Cong -- Bake Curves :kbd:`Alt-C` Nướng Âm Thanh thành Đường Cong-F -- Bake Sound to F-Curves Baking a curve replaces it with a set of sampled points, and removes the ability to edit the curve. Before Flatten Handles. Theo Thời Gian qua Khung Hình Hiện Tại -- By Times Over Current Frame Theo Thời Gian dùng Dấu Mốc Được Chọn Đầu Tiên -- By Times over First Selected Marker Theo Thời Gian qua Mốc Thời Gian 0 -- By Times over Time 0 Theo Giá Trị dùng Giá Trị của Con Trỏ -- By Values over Cursor Value Theo Giá Trị qua Mốc Giá Trị 0 -- By Values over Value 0 By default, when new channels are added, the *Graph Editor* sets them to *Edit Mode*. Dọn Dẹp các Kênh -- Clean Channels Dọn Dẹp các Khung Khóa -- Clean Keyframes Khung Hình Hiện Tại -- Current Frame Giá Trị Con Trỏ -- Cursor Value Cutoff frequency of a high-pass filter that is applied to the audio data. Cutoff frequency of a low-pass filter that is applied to the audio data. Divide Transformation by 10.0 :kbd:`Shift`. Biên Soạn -- Editing F-Curve after cleaning. Đường cong-F sau khi lấy mẫu. Đường cong-F sau khi làm mịn. F-Curve before cleaning. Đường cong-F trước khi lấy mẫu vật. Đường cong-F trước khi làm mịn. Căn Thẳng Tay Cầm -- Flatten Handles Flatten Handles snapping example. Flatten the *Bézier* handles for the selected keyframes. For precise control of the keyframe position and value, you can set values in the *Active Keyframe* of the Properties Region. Cho kết quả là một đường cong hình vuông. Các giá trị âm luôn luôn có kết quả là -1 và những giá trị dương là 1 Ẩn :kbd:`H` -- Hide :kbd:`H` Ẩn Giấu Cái Không Được Chọn -- Hide Unselected :kbd:`Shift-H` Hide selected curves. Tần số cao nhất -- Highest frequency Phím Tắt -- Hotkey Chèn Thêm Khung Khóa -- Insert Keyframe Keyframes can be snapped to different properties by using the *Snap Keys* tool. Tần số thấp nhất -- Lowest frequency Many of the hotkeys are the same as the :doc:`3D View ones </editors/3dview/object/index>`, for example: Trình Đơn -- Menu Minimum amplitude value needed to influence the hull curve. Đối Xứng/Gương -- Mirror Mirror horizontally over frame 0. Mirror horizontally over the *Time Cursor*. Đối xứng theo chiều ngang qua *Dấu Mốc* đầu tiên Mirror vertically over the *Cursor*. Mirror vertically over value 0. Khung Hình Gần Nhất -- Nearest Frame Dấu Mốc Gần Nhất -- Nearest Marker Giây Gần Nhất -- Nearest Second Only the positive differences of the hull curve amplitudes are summarized to produce the output. Tham Chiếu -- Reference Thời gian thả -- Release time Lấy Mẫu Vật các Khung Hình :kbd:`Shift-O` -- Sample Keyframes :kbd:`Shift-O` Việc lấy mẫu vật của một bộ các khung hình sẽ thay thế các giá trị nội suy với một khung khóa mới cho mỗi khung hình Lấy Mẫu Vật và Nướng Khung Hình -- Sampling and Baking Keyframes Selected keyframes can be mirrored over different properties using the *Mirror Keys* tool. Hiển Thị cái bị Ẩn Giấu -- Show Hidden :kbd:`Alt-H` Hiển thị toàn bộ các  đường cong bị ẩn giấu trước đây. Chỉ hiển thị các đường cong được chọn (ẩn giấu tất cả mọi thứ khác) Hiện/Ẩn -- Show/Hide Làm Mịn -- Smoothing Bám Dính -- Snap Snap Transformation to 1.0 :kbd:`Ctrl`. Snap the selected keyframes to the *Cursor*. Snap the selected keyframes to the *Time Cursor*. Snap the selected keyframes to their nearest frame individually. Snap the selected keyframes to their nearest marker individually. Snap the selected keyframes to their nearest second individually, based on the *FPS* of the scene. Vuông -- Square Giới Hạn Hình Vuông -- Square Threshold The *Bake Sound to F-Curves* tool takes a sound file and uses its sound wave to create the animation data. The amplitudes of the hull curve are summarized. If *Accumulate* is enabled, both positive and negative differences are accumulated. The modified curve left after the Clean tool is run is not the same as the original, so this tool is better used before doing custom editing of f-curves and after initial keyframe insertion, to get rid of any unwanted keyframes inserted while doing mass keyframe insertion (by selecting all bones and pressing :kbd:`I` for instance). There is also an option to smooth the selected curves, but beware: its algorithm seems to be to divide by two the distance between each keyframe and the average linear value of the curve, without any setting, which gives quite a strong smoothing! Note that the first and last keys seem to be never modified by this tool. Giới Hạn -- Threshold Bám Dính Biến Hóa -- Transform Snapping Value for the hull curve calculation that tells how fast the hull curve can fall. The lower the value the steeper it can fall. Value for the hull curve calculation that tells how fast the hull curve can rise. The lower the value the steeper it can rise. When transforming keyframes with :kbd:`G`, :kbd:`R`, :kbd:`S`, the transformation can be snapped to increments. 