��    :      �              �     �     �     �  /   �  $     +   8  !   d     �  	   �  9  �     �  	   �     �     �  "   �     "     )     1     :     C     I     [     k     s          �     �  )   �  *   �     �            �         �  b   �     %     *     7     >     L     _     l     s  I   x     �  	   �     �     �  	   �     �  
   �  �   	  �   �	  (   �
  �     ?   �     �  �  �     �     �     �  Q   �  G     K   e  *   �     �     �  9    *   H     s  ,   �     �  /   �       !        9     Q     l  7   �  -   �     �            !  7   6  '   n  :   �  ;   �          $     ?  �   \       b   '     �      �     �     �  +   �          7     O  I   d     �     �     �     �               8  �   J  �   9  (   5  �   ^  t   �     d   :kbd:`Ctrl-E` :kbd:`Shift-E` :kbd:`T` :menuselection:`Channel --> Extrapolation Mode` :menuselection:`Key --> Easing Type` :menuselection:`Key --> Interpolation Mode` After moving the second keyframe. Aligned Amplitude As mentioned, Blender's fundamental unit of time is the "frame", which usually lasts just a fraction of a second, depending on the *frame rate* of the scene. As animation is composed of incremental changes spanning multiple frames, usually these properties are **not** manually modified *frame-by-frame*, because: Auto Clamped Automatic Automatic Easing Back Before moving the second keyframe. Bounce Bézier Circular Constant Cubic Direction of Time Dynamic Effects Ease In Ease In Out Ease Out Easing (by strength) Easing Type Effect fades out from the first keyframe. Effect occurs on both ends of the segment. Elastic Exponential Extrapolation F-Curves have three additional properties, which control the interpolation between points, extension behavior, and the type of handles. For example, if you have: For more info and a few live demos, see http://easings.net and http://www.robertpenner.com/easing/ Free Handle Types Hotkey Interpolation Interpolation Mode Introduction Linear Menu Mode for the :term:`Interpolation` between the current and next keyframe. Period Quadratic Quartic Quintic Reference Settings Sinusoidal The idea is simple: you define a few Keyframes, which are multiple frames apart. Between these keyframes, the properties' values are computed (interpolated) by Blender and filled in. Thus, the animators' workload is significantly reduced. The same goes for all intermediate frames: with just two points, you get a smooth increase from (0 to 10) along the 25 frames. Obviously, if you would like the frame 15 to have a value of 9, you would have to add another control point (or keyframe)... There are two basic extrapolation modes: There is another curve option quite useful for Bézier-interpolated curves. You can set the type of handle to use for the curve points :kbd:`V`. Two control points switching: the curve cannot go back in time! Vector Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-10-26 00:56+1100
PO-Revision-Date: 2019-04-22 13:17+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 :kbd:`Ctrl-E` :kbd:`Shift-E` :kbd:`T` :menuselection:`Kênh (Channel) --> Chế Độ Ngoại Suy (Extrapolation Mode)` :menuselection:`Khóa (Key) --> Thể Loại Chậm Rãi (Easing Type)` :menuselection:`Khóa (Key) --> Chế Độ Nội Suy (Interpolation Mode)` Sau khi di chuyển khung khóa thứ hai. Thẳng Hàng -- Aligned Biên Độ -- Amplitude As mentioned, Blender's fundamental unit of time is the "frame", which usually lasts just a fraction of a second, depending on the *frame rate* of the scene. As animation is composed of incremental changes spanning multiple frames, usually these properties are **not** manually modified *frame-by-frame*, because: Tự Động Hạn Định -- Auto Clamped Tự Động -- Automatic Tự Động Chậm Rãi -- Automatic Easing Sau/Lưng/Quay Lại -- Back Trước khi di chuyển khung khóa thứ hai. Nẩy -- Bounce Đường Cong Bézier -- Bézier Vòng Tròn -- Circular Đồng Đều -- Constant Lập Phương -- Cubic Chiều Hướng của Thời Gian -- Direction of Time Hiệu Ứng Năng Động -- Dynamic Effects Nới Vào -- Ease In Nới Vào và Ra -- Ease In Out Nới Ra -- Ease Out Nới Lỏng (theo mức độ) -- Easing (by strength) Thể Loại Chậm Rãi -- Easing Type Hiệu ứng mờ dần ra khỏi khung khóa đầu tiên Ảnh hưởng xảy ra ở hai đầu của phân đoạn. Đàn Hồi -- Elastic Lũy Thừa -- Exponential Ngoại Suy -- Extrapolation Đường cong có 3 tính chất bổ sung điều khiển quá trình nội suy giữa các điểm, hành xử của sự nới rộng và thể loại của các tay cầm. For example, if you have: For more info and a few live demos, see http://easings.net and http://www.robertpenner.com/easing/ Tự Do -- Free Loại Tay Cầm -- Handle Types Phím Tắt -- Hotkey Nội Suy -- Interpolation Chế Độ Nội Suy -- Interpolation Mode Giới Thiệu -- Introduction Tuyến Tính -- Linear Trình Đơn -- Menu Mode for the :term:`Interpolation` between the current and next keyframe. Chu Kỳ -- Period Bậc Hai -- Quadratic Bậc Bốn -- Quartic Bậc Năm -- Quintic Tham Chiếu -- Reference Sắp Đặt -- Settings Sin -- Sinusoidal The idea is simple: you define a few Keyframes, which are multiple frames apart. Between these keyframes, the properties' values are computed (interpolated) by Blender and filled in. Thus, the animators' workload is significantly reduced. The same goes for all intermediate frames: with just two points, you get a smooth increase from (0 to 10) along the 25 frames. Obviously, if you would like the frame 15 to have a value of 9, you would have to add another control point (or keyframe)... There are two basic extrapolation modes: There is another curve option quite useful for Bézier-interpolated curves. You can set the type of handle to use for the curve points :kbd:`V`. Chuyển đổi giữa 2 điểm điều khiển: đường cong không thể quay trở ngược dòng thời gian! Vectơ -- Vector 