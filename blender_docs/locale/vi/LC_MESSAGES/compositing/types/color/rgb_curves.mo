��    '      T              �  �   �  u   +  D   �     �  =   �  -   0     ^  <   f  )   �     �  )   �       E   3     y  9     9   �     �     �       	     U        k  �  q  x   _     �  �   �     �	  
   �	     �	     �	     �	     �	     �	  x   
  y   �
  n        p     u  �  �  #  :  �   ^  �   0     �  x   �  E   W     �  Z   �  p   	  C   z  D   �  #     i   '     �  �   �  �   @     �     �       
     �   "     �  @  �  �   6     �  L       T     i  *   �     �     �  &   �  *   �  �   (  �   �  �   �     �  "   �   A Bézier curve that varies the input levels (X axis) to produce an output level (Y axis). For the curve controls see: :ref:`Curve widget <ui-curve-widget>`. Also, read on for examples of the Darken and Contrast Enhancement curves, :doc:`here </compositing/types/color/mix>`. Below are some common curves you can use to achieve desired effects. Black Level C (Combined RGB), R (Red), G (Green), B (Blue), L (Luminance) Changing colors by inverting the red channel. Channel Clicking on one of the channels displays the curve for each. Color Correction using Black/White Levels Color Correction using Curves Color correction with Black/White Levels. Color correction with curves. Controls the amount of influence the node exerts on the output image. Curve Defines the input color that is (linear) mapped to black. Defines the input color that is (linear) mapped to white. Effects Examples Factor Film like From left to right: 1. Lighten shadows 2. Negative 3. Decrease contrast 4. Posterize. Image In this example, the White Level is set to the color of a bright spot of the sand in the background, and the Black Level to the color in the center of the fish's eye. To do this efficiently it is best to bring up the Image Editor showing the original input image. You can then use the levels' color picker to easily choose the appropriate colors from the input image, zooming into pixel level if necessary. The result can be fine-tuned with the R, G, and B curves like in the previous example. In this example, the image has too much red in it, so we run it through an *RGB Curves* node and reduce the Red channel. Inputs Manually adjusting the RGB curves for color correction can be difficult. Another option for color correction is to use the Black and White Levels instead, which really might be their main purpose. Outputs Properties RGB Curves Node RGB Curves Node. Standard Standard image input. Standard image output. The *RGB Curves Node* allows color corrections for each color channel and levels adjustments in the compositing context. The curve for C is used to compensate for the increased contrast that is a side effect of setting Black and White Levels. To define the levels, use the :ref:`eyedropper <ui-eyedropper>` to select a color sample of a displayed image. Tone White Level Project-Id-Version: Blender 2.8 Manual 2.8
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2019-07-17 21:45+0100
PO-Revision-Date: 2020-03-30 21:20+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Đường cong Bézier thay đổi mức độ của đầu vào ở (trục X) để tạo ra mức đầu ra ở (trục Y). Xin hãy xem mục :ref:`Thành Tố Đường Cong -- Curve widget <ui-curve-widget>` để biết thêm thông tin về các điều khiển của đường cong. Đồng thời, xin hãy đọc các ví dụ về các đường cong Làm Tối (*Darken*) và  Nâng Cao Độ Tương Phản (*Contrast Enhancement*) lên :doc:`tại đây </compositing/types/color/mix>`. Dưới đây là một số đường cong phổ biến mà bạn có thể sử dụng để đạt được các hiệu ứng mong muốn. Mức Độ Đen -- Black Level C (RGB Kết Hợp -- Combined RGB), R (Đỏ -- Red), G (Lục -- Green), B (Lam -- Blue), L (Độ Sáng -- Luminance) Thay đổi màu sắc bằng cách đảo ngược kênh màu đỏ. Kênh -- Channel Bấm vào một trong các kênh để hiển thị đường cong dành cho mỗi kênh. Chỉnh Màu Sắc bằng cách sử dụng các Mức Đen/Trắng -- Color Correction using Black/White Levels Chỉnh Màu bằng Đường Cong -- Color Correction using Curves Chỉnh màu sắc bằng cách sử dụng các Mức Đen/Trắng. Chỉnh màu bằng đường cong. Điều chế lượng ảnh hưởng mà nút sẽ tác động đến hình ảnh xuất ở đầu ra. Đường Cong -- Curve Xác định màu nào ở đầu vào sẽ được ánh xạ (một cách tuyến tính) thành màu đen (*màu nào được kể là màu đen*). Xác định màu nào ở đầu vào sẽ được ánh xạ (tuyến tính) thành màu trắng (*màu nào sẽ được kể là màu trắng*). Hiệu Ứng -- Effects Ví Dụ -- Examples Hệ Số -- Factor Tựa Phim Từ trái sang phải: 1. Làm Hừng Sáng Bóng Tối (*Lighten shadows*) 2. Âm Bản (*Negative*) 3. Giảm độ Tương Phản (*Decrease contrast*) 4. Áp Phích Hóa (*Posterize*). Hình Ảnh -- Image Trong ví dụ này, Mức Độ Trắng (*White Level*) được đặt là màu của một điểm sáng chói trong cát, và Mức Độ Đen (*Black Level*) bằng màu ở trung tâm của mắt con cá. Để làm được điều này một cách hiệu quả, tốt nhất là hãy mở Trình Biên Soạn UV/Hình Ảnh (*UV/Image editor*) và hiển thị hình ảnh nguồn đã được cung cấp. Sau đó, bạn có thể sử dụng công cụ chọn mức độ màu (*ống hút chấm màu -- color picker*) để dễ dàng chọn các màu phù hợp từ hình ảnh nguồn ở đầu vào, cho phóng to vào mức độ của điểm ảnh nếu cần. Mình còn có thể tinh chỉnh kết quả đạt được bằng các đường cong Đỏ,Lục,Lam (R, G, B) như trong ví dụ trước đây. Trong ví dụ này, hình ảnh có quá nhiều màu đỏ trong đó, vì vậy chúng ta đưa nó qua nút *Đường Cong RGB -- RGB Curves* và giảm kênh Đỏ (*Red*) xuống. Đầu Vào -- Inputs Điều chỉnh các đường cong RGB để hiệu chỉnh màu sắc, một cách thủ công, có thể là một việc khá khó khăn. Có một phương pháp khác để hiệu chỉnh màu sắc nữa, là cách sử dụng các Cấp Độ Đen và Trắng, tức cái lẽ ra, lại là mục đích chính của chúng. Đầu Ra -- Outputs Tính Chất -- Properties Nút Đường Cong RGB -- RGB Curves Node Nút Đường Cong RGB. Tiêu Chuẩn Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. The *Đường Cong RGB -- RGB Curves Node* cho phép hiệu chỉnh màu của mỗi kênh màu, và điều chỉnh mức của chúng trong ngữ cảnh của quá trình tổng hợp. Đường cong cho C (Combined: Kết hợp cả 3 kênh) được sử dụng để bù trừ độ tương phản bị tăng lên do tác dụng phụ của việc điều chỉnh Mức Độ Đen và Trắng gây ra. Để xác định các mức độ thì bạn hãy sử dụng :ref:`Ống Hút Chấm Màu -- eyedropper <ui-eye-dropper>` để chọn một mẫu vật màu sắc của hình ảnh được hiển thị. Sắc Thái -- Tone Mức Độ Trắng -- White Level 