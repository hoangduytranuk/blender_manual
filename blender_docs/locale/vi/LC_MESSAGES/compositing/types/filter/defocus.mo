��    >                    �     �  g  
     r     �  E   �  2  �  
             *     7  �   E  4   �  |        �     �     �  �   �     X	     i	  �   o	     #
  �   )
  ?  &     f  �   m  =  "     `     i     u     �  %  �  �   �  Q   �     �        
     G        [  \   a  �   �  �   d  +  
  S   6     �     �  E   �  b   �  <   `  �   �  �   J  m  �  �   U  	   �  �   �     �  Y  �  �      2   �      �      �   ^   �   �  ,!     �"  g  �"  ^   Y$     �$  [   �$  2  (%     [&  4   v&     �&     �&  *  �&  4   (  |   :(  '   �(     �(     �(  �   )  '   �)     �)    �)     +  �   +  �  ,     �-    .  =  /     [2  '   w2  >   �2  '   �2  %  3  �  ,4  j   �5     T6     i6     �6  G   �6     �6  \   �6  )  S7  �   }8  +  l9  S   �=  &   �=  *   >  |   >>  b   �>  f   ?  �   �?  �   2@  m  �@  
  mB     xC  �   �C      0D  Y  QD  �   �E  2   /F     bF     dF  �   {F   "Focus Pull" A final word of warning, since there is no way to detect if an actual Z-buffer is connected to the node, be **very** careful with the *No Z-buffer* switch. If the *Z scale* value happens to be large, and you forget to set it back to some low value, the values may suddenly be interpreted as huge blur radius values that will cause processing times to explode. Aliasing at Low f-Stop Values Angle Applies a gamma correction on the image before and after blurring it. At very low values, less than 5, the node will start to remove any oversampling and bring the objects at DoF Distance very sharply into focus. If the object is against a contrasting background, this may lead to visible stair-stepping (aliasing) which OSA is designed to avoid. If you run into this problem: Bokeh Type Camera Settings Defocus Node Defocus Node. Disk (to emulate a perfect circle) or Triangle (3 blades), Square (4 blades), Pentagon (5 blades), Hexagon (6 blades), Heptagon (7 blades) or Octagon (8 blades). Distance setting in the Camera Depth of Field panel. Do your own OSA by rendering at twice the intended size and then scaling down, so that adjacent pixels are blurred together. Edge Artifacts Examples F-Stop For minimum artifacts, try to setup your scene such that differences in distances between two objects that may visibly overlap at some point are not too large. Gamma Correction Hints If enabled a limited amount of (quasi-)random samples are used to render the preview. This way of sampling introduces additional noise, which will not show up in the final render. Image In general, use preview mode, change parameters to your liking, only then disable preview mode for the final render. This node is computationally intensive, so watch your console window, and it will give you status as it computes each render scan line. In this `blend-file example <https://wiki.blender.org/uploads/7/79/Doftest.blend>`__, the ball array image is blurred as if it was taken by a camera with an f-stop of 2.8 resulting in a fairly narrow depth of field centered on 7.5 Blender units from the camera. As the balls recede into the distance, they get blurrier. Inputs It is typically used to emulate depth of field (:term:`DOF`) using a post-processing method with a Z-buffer input. But also allows to blur images that are not based on Z depth too. Keep in mind that this is not real DoF, only a post-processing simulation. Some things cannot be done which would be no problem for real DoF at all. A typical example is a scene with some object very close to the camera, and the camera focusing on some point far behind it. In the real world, using shallow depth of field, it is not impossible for nearby objects to become completely invisible, in effect allowing the camera to see behind them. Hollywood cinematographers use this visual characteristic to achieve the popular "focus pull" effect, where the focus shifts from a nearby to a distant object, such that the "other" object all but disappears. Well, this is simply not possible to do with the current post-processing method in a single pass. If you really want to achieve this effect, quite satisfactorily, here is how: Max Blur No Z-Buffer No Z-Buffer Examples No Z-buffer Now, combine the two results, each with their own "defocus" nodes driven by the same Time node, but with one of them inverted. (e.g. using a "Map Value" node with a Size of -1). As the defocus of one increases, the defocus on the other decreases at the same rate, creating a smooth transition. Only active when *No Z-buffer* is enabled. When *No Z-buffer* is used, the input is used directly to control the blur radius (similar to *f-Stop* when using the Z-buffer). This parameter can be used to scale the range of the Z input. Only change this value, if there is an occurring problem with an in-focus object. Outputs Preview Properties Rearrange the objects in your scene to use a lower-contrast background. Scene Set DoF Distance off by a little, so that the object in focus is blurred by the tiniest bit. Should be activated for a non Z-buffer in the Z input. No Z-buffer will be enabled automatically whenever a node that is not image based is connected to the Z input. Some artifacts, like edge bleed, may occur, if the blur difference between pixels is large. This value controls how large that blur difference considered to be safe. Sometimes might want to have more control to blur the image. For instance, you may want to only blur one object while leaving everything else alone (or the other way around), or you want to blur the whole image uniformly all at once. The node, therefore, allows you to use something other than an actual Z-buffer as the Z input. For instance, you could connect an image node and use a grayscale image where the color designates how much to blur the image at that point, where white is the maximum blur and black is no blur. Or, you could use a Time node to uniformly blur the image, where the time value controls the maximum blur for that frame. It may also be used to obtain a possibly slightly better DoF blur, by using a fake depth-shaded image instead of a Z-buffer. (A typical method to create the fake depth-shaded image is by using a linear blend texture for all objects in the scene or by using the "fog/mist" fake depth shading method). This also has the advantage that the fake depth image can have anti-aliasing, which is not possible with a real Z-buffer. Split up your scene into "nearby" and "far" objects, and render them in two passes. Standard image input. Standard image output. The *Defocus Node* blurs areas of an image based on a map/mask input. The *Defocus* node uses the actual camera data in your scene if supplied by a *Render Layer* node. The number of iris blades of the virtual camera's diaphragm. The parameter *No Z-buffer*, becomes then the main blur control. The input has to be scaled, because usually the value of a texture is only in the numeric range 0.0 to 1.0. This button is deactivated, if the Bokeh Type is set to Disk. It can be used to add a rotation offset to the Bokeh shape. The value is the angle in degrees. This option controls the amount of focal blur in the same way as a real camera. It simulates the aperture *f* of a real lens' iris, without modifying the luminosity of the picture. The default value 128 is assumed to be infinity: everything is in perfect focus. Half the value will double the amount of blur. This button is deactivated, if *No Z-buffer* is enabled. This value limits the amount of blur by setting a maximum blur radius. Could be used to optimize the performance. The default value of 0 means no limit. Threshold To make the focal point visible, enable the camera *Limits* option, the focal point is then visible as a yellow cross along the view direction of the camera. To select the linked scene. To set the point of focus, the camera now has a *Distance* parameter, which is shorthand for Depth of Field Distance. Use this camera parameter to set the focal plane of the camera (objects Depth of Field Distance away from the camera are in focus). Set *Distance* in the main *Camera* edit panel; the button is right below the *Depth of Field*. Use a higher f-Stop, which will start the blur, and then use the Z socket to a Map Value to a Blur node to enhance the blur effect. Use the blur node with a setting of 2 for X and Y. Z Z Scale Z-buffer input, but could also be a (grayscale) image used as a mask, or a single value input. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-07 02:04+0000
PO-Revision-Date: 2018-12-07 21:29+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 "Focus Pull" A final word of warning, since there is no way to detect if an actual Z-buffer is connected to the node, be **very** careful with the *No Z-buffer* switch. If the *Z scale* value happens to be large, and you forget to set it back to some low value, the values may suddenly be interpreted as huge blur radius values that will cause processing times to explode. Chống Răng Chưa tại các Giá Trị Khẩu Độ Thấp -- Aliasing at Low f-Stop Values Góc Độ -- Angle Áp dụng hiệu chỉnh gamma trên hình ảnh trước và sau khi làm nhòe mờ nó. At very low values, less than 5, the node will start to remove any oversampling and bring the objects at DoF Distance very sharply into focus. If the object is against a contrasting background, this may lead to visible stair-stepping (aliasing) which OSA is designed to avoid. If you run into this problem: Loại Bokeh -- Bokeh Type Sắp Đặt của Máy Quay Phim -- Camera Settings Nút Làm Mờ -- Defocus Node Nút Làm Mờ. Đĩa (Disk) (để mô phỏng một vòng tròn (circle) hoàn hảo) hoặc Hình Tam Giác (Triangle) (3 lá), Hình Vuông (Square) (4 lá), Hình Ngũ Giác (Pentagon) (5 lá), Hình Lục Giác (Hexagon) (6 lá), Hình Bảy Góc (Heptagon) (7 lá) hoặc hình Bát Giác (Octagon) (8 lá). Distance setting in the Camera Depth of Field panel. Do your own OSA by rendering at twice the intended size and then scaling down, so that adjacent pixels are blurred together. Giả Tượng Cạnh -- Edge Artifacts Các Ví Dụ -- Examples Khẩu Độ -- F-Stop For minimum artifacts, try to setup your scene such that differences in distances between two objects that may visibly overlap at some point are not too large. Chỉnh Sửa Gamma -- Gamma Correction Gợi ý -- Hints Nếu được kích hoạt thì một lượng giới hạn (quasi-) mẫu vật ngẫu nhiên sẽ được sử dụng để kết xuất bản xem trước. Đây là cách lấy mẫu vật có  nhiễu, cái mà mình sẽ không thấy trong bản kết xuất cuối cùng. Hình Ảnh -- Image In general, use preview mode, change parameters to your liking, only then disable preview mode for the final render. This node is computationally intensive, so watch your console window, and it will give you status as it computes each render scan line. Trong `ví dụ  tập tin blend (blend-file example) <https://wiki.blender.org/uploads/7/79/Doftest.blend>`__ này, mảng các dãy quả bóng nhòe đi như thể nó được chụp bởi một máy ảnh với khẩu độ F2,8 (f-stop 2.8), dẫn đến độ sâu trường ảnh khá hẹp, với trung điểm nằm ở vị trí 7,5 đơn vị Blender, từ máy ảnh ra. Các quả bóng càng cách xa bao nhiêu thì chúng càng bị mờ hơn bấy nhiêu. Đầu Vào -- Inputs Nó thường được sử dụng để mô phỏng độ sâu trường ảnh (:term:`DOF`) sử dụng phương thức hậu xử lý với đầu vào bộ đệm Z (Z-buffer), song cũng cho phép làm nhòe các hình ảnh không dựa trên độ sâu Z (Z depth) nữa. Keep in mind that this is not real DoF, only a post-processing simulation. Some things cannot be done which would be no problem for real DoF at all. A typical example is a scene with some object very close to the camera, and the camera focusing on some point far behind it. In the real world, using shallow depth of field, it is not impossible for nearby objects to become completely invisible, in effect allowing the camera to see behind them. Hollywood cinematographers use this visual characteristic to achieve the popular "focus pull" effect, where the focus shifts from a nearby to a distant object, such that the "other" object all but disappears. Well, this is simply not possible to do with the current post-processing method in a single pass. If you really want to achieve this effect, quite satisfactorily, here is how: Nhòe Tối Đa -- Max Blur Không Có Bộ Đệm Z -- No Z-Buffer Các Ví dụ Không Có Bộ Đệm Z -- No Z-Buffer Examples Không Có Bộ Đệm Z -- No Z-buffer Now, combine the two results, each with their own "defocus" nodes driven by the same Time node, but with one of them inverted. (e.g. using a "Map Value" node with a Size of -1). As the defocus of one increases, the defocus on the other decreases at the same rate, creating a smooth transition. Chỉ hoạt động khi tùy chọn *Không có bộ đệm Z* (No Z-buffer) được kích hoạt. Khi tùy chọn *Không Có Bộ Đệm Z* được sử dụng, đầu vào được sử dụng trực tiếp để điều khiển bán kính nhòe mờ (tương tự *Khẩu Độ* (f-Stop) khi sử dụng bộ đệm Z (Z-buffer). Tham số này có thể được sử dụng để tỷ lệ hóa phạm vi của đầu vào Z (Z input). Chỉ thay đổi giá trị này, nếu có vấn đề xảy ra đối với đối tượng lấy nét. Đầu Ra -- Outputs Duyệt Thảo -- Preview Tính Chất -- Properties Rearrange the objects in your scene to use a lower-contrast background. Cảnh -- Scene Set DoF Distance off by a little, so that the object in focus is blurred by the tiniest bit. Nên được kích hoạt cho một đầu vào Z không có bộ đệm Z (Z-buffer). Tùy chọn Không Có Bộ Đệm Z (No Z-buffer) sẽ được kích hoạt tự động bất cứ khi nào một nút không có nền tảng hình ảnh được kết nối với đầu vào Z (Z input). Một số giả tượng, như rò rỉ cạnh, có thể xảy ra, nếu sự chênh lệch nhòe mờ giữa các điểm đỉnh lớn. Giá trị này kiểm soát mức độ chênh lệch nhòe mờ lớn được coi là an toàn. Sometimes might want to have more control to blur the image. For instance, you may want to only blur one object while leaving everything else alone (or the other way around), or you want to blur the whole image uniformly all at once. The node, therefore, allows you to use something other than an actual Z-buffer as the Z input. For instance, you could connect an image node and use a grayscale image where the color designates how much to blur the image at that point, where white is the maximum blur and black is no blur. Or, you could use a Time node to uniformly blur the image, where the time value controls the maximum blur for that frame. It may also be used to obtain a possibly slightly better DoF blur, by using a fake depth-shaded image instead of a Z-buffer. (A typical method to create the fake depth-shaded image is by using a linear blend texture for all objects in the scene or by using the "fog/mist" fake depth shading method). This also has the advantage that the fake depth image can have anti-aliasing, which is not possible with a real Z-buffer. Split up your scene into "nearby" and "far" objects, and render them in two passes. Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. *Nút Làm Mờ* làm nhòe một số vùng của hình ảnh dựa trên ánh xạ/màn chắn cung cấp ở đầu vào. The *Defocus* node uses the actual camera data in your scene if supplied by a *Render Layer* node. Số lượng lá khẩu của màng chắn (bộ lá khẩu trong ống kính) của máy ảnh ảo. The parameter *No Z-buffer*, becomes then the main blur control. The input has to be scaled, because usually the value of a texture is only in the numeric range 0.0 to 1.0. Nút này sẽ bị tắt nếu thể loại nhòe Bokeh (Bokeh Type) là Đĩa (Disk). Nó có thể được sử dụng để thêm hiệu ứng xoay chiều cho hình Bokeh. Giá trị là độ góc. This option controls the amount of focal blur in the same way as a real camera. It simulates the aperture *f* of a real lens' iris, without modifying the luminosity of the picture. The default value 128 is assumed to be infinity: everything is in perfect focus. Half the value will double the amount of blur. This button is deactivated, if *No Z-buffer* is enabled. Giá trị này giới hạn lượng nhòe mờ bằng cách đặt bán kính làm mờ tối đa. Cái này có thể được sử dụng để tối ưu hóa hiệu suất hoạt động. Giá trị mặc định bằng 0 có nghĩa là không có giới hạn. Giới Hạn -- Threshold To make the focal point visible, enable the camera *Limits* option, the focal point is then visible as a yellow cross along the view direction of the camera. Để chọn cảnh liên kết. To set the point of focus, the camera now has a *Distance* parameter, which is shorthand for Depth of Field Distance. Use this camera parameter to set the focal plane of the camera (objects Depth of Field Distance away from the camera are in focus). Set *Distance* in the main *Camera* edit panel; the button is right below the *Depth of Field*. Use a higher f-Stop, which will start the blur, and then use the Z socket to a Map Value to a Blur node to enhance the blur effect. Use the blur node with a setting of 2 for X and Y. Z Tỷ Lệ Z -- Z Scale Đầu vào bộ đệm Z (Z-buffer), song cũng có thể là một hình ảnh (thang độ xám) được sử dụng làm màn chắn hoặc một đơn giá trị được cung cấp. 