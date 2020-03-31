��    !      $              ,  �   -  u   �  D   A     �  =   �  -   �     �  <     )   C     m  )   �     �  E   �       9        Y     a     j  U   q     �  x   �     F  �   M       
        %     5     F     \  x   s  y   �     f  �  r     
  �   "  �   �     u  x   �  E        T  T   e  p   �  C   +  D   o  #   �  Y   �     2  S   J     �     �     �  �   �     �  �   �     k  �   �     u     �  *   �     �  &   �  *     �   ;  �   �  "   �   A Bézier curve that varies the input levels (X axis) to produce an output level (Y axis). For the curve controls see: :ref:`Curve widget <ui-curve-widget>`. Also, read on for examples of the Darken and Contrast Enhancement curves, :doc:`here </compositing/types/color/mix>`. Below are some common curves you can use to achieve desired effects. Black Level C (Combined RGB), R (Red), G (Green), B (Blue), L (Luminance) Changing colors by inverting the red channel. Channel Clicking on one of the channels displays the curve for each. Color Correction using Black/White Levels Color Correction using Curves Color correction with Black/White Levels. Color correction with curves. Controls the amount of influence the node exerts on the output image. Curve Defines the input color that is (linear) mapped to white. Effects Examples Factor From left to right: 1. Lighten shadows 2. Negative 3. Decrease contrast 4. Posterize. Image In this example, the image has too much red in it, so we run it through an *RGB Curves* node and reduce the Red channel. Inputs Manually adjusting the RGB curves for color correction can be difficult. Another option for color correction is to use the Black and White Levels instead, which really might be their main purpose. Outputs Properties RGB Curves Node RGB Curves Node. Standard image input. Standard image output. The *RGB Curves Node* allows color corrections for each color channel and levels adjustments in the compositing context. The curve for C is used to compensate for the increased contrast that is a side effect of setting Black and White Levels. White Level Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
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
 Đường cong Bézier thay đổi mức độ của đầu vào (trục X) để tạo ra mức đầu ra (trục Y). Đối với các điều khiển của đường cong, xin hãy xem: :ref:`Thành Tố Đường Cong -- Curve widget <ui-curve-widget>`. Ngoài ra, hãy đọc các ví dụ về các đường cong Làm Tối (*Darken*) và  Nâng Cao Độ Tương Phản (*Contrast Enhancement*), :doc:`tại đây </compositing/types/color/mix>`. Dưới đây là một số đường cong phổ biến mà bạn có thể sử dụng để đạt được các hiệu ứng mong muốn. Mức Độ Đen -- Black Level C (RGB Kết Hợp -- Combined RGB), R (Đỏ -- Red), G (Lục -- Green), B (Lam -- Blue), L (Độ Sáng -- Luminance) Thay đổi màu sắc bằng cách đảo ngược kênh màu đỏ. Kênh -- Channel Bấm vào một trong các kênh để hiển thị đường cong cho mỗi kênh. Chỉnh màu sắc bằng cách sử dụng các Mức Đen/Trắng -- Color Correction using Black/White Levels Chỉnh Màu bằng Đường Cong -- Color Correction using Curves Chỉnh màu sắc bằng cách sử dụng các Mức Đen/Trắng. Chỉnh màu bằng đường cong. Điều chế lượng ảnh hưởng mà nút tác động đến hình ảnh xuất ra. Đường Cong -- Curve Xác định màu đầu vào được ánh xạ (tuyến tính) sang màu trắng. Ảnh Hưởng -- Effects Ví Dụ -- Examples Hệ Số -- Factor Từ trái sang phải: 1. Hừng Sáng Bóng Tối (*Lighten shadows*) 2. Âm Bản (*Negative*) 3. Giảm độ Tương Phản (*Decrease contrast*) 4. Áp Phích Hóa (*Posterize*). Hình Ảnh -- Image Trong ví dụ này, hình ảnh có quá nhiều màu đỏ trong đó, vì vậy chúng ta đưa nó qua nút *Đường Cong RGB* (*RGB Curves*) và giảm kênh Đỏ (*Red*) xuống. Đầu Vào -- Inputs Điều chỉnh các đường cong RGB để hiệu chỉnh màu sắc theo cách thủ công có thể là một việc khó khăn. Một phương pháp khác để hiệu chỉnh màu sắc là sử dụng các cấp độ đen và trắng. Đầu Ra -- Outputs Tính Chất -- Properties Nút Đường Cong RGB -- RGB Curves Node Nút Đường Cong RGB. Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. The *Đường Cong RGB* cho phép hiệu chỉnh màu cho mỗi kênh màu và điều chỉnh mức trong ngữ cảnh của quá trình tổng hợp. Đường cong cho  C (Combined: Tổng hợp cả 3 kênh) được sử dụng để bù trừ độ tương phản bị tăng lên, một tác dụng phụ của việc điều chỉnh Mức Độ Đen và Trắng. Mức Độ Trắng -- White Level 