��          �               �  '   �  &   �  
        '     8  �   A  -   >  4   l  ?   �     �     �     �  	          U        i     p  
   x     �  	   �  *   �  -   �     �       �        �  �     B   �  D   �     A  &   [      �  �  �  ^   X
  g   �
  c     +   �     �     �     �     �  �        �     �     �  �   �     �  Q   �  G   (  +   p     �  b  �        :abbr:`HDR (High Dynamic Range)` image. :abbr:`LDR (Low Dynamic Range)` image. Adaptation Color Correction Contrast Essentially, tone mapping addresses the problem of strong contrast reduction from the scene values (radiance) to the displayable range, while preserving the image details and color appearance. This is important to appreciate the original scene content. If 0, global; if 1, based on pixel intensity. If 0, same for all channels; if 1, each independent. If less than zero, darkens image; otherwise, makes it brighter. If not used, set to 1. Image Inputs Intensity Key Normally always 1, but can be used as an extra control to alter the brightness curve. Offset Outputs Properties R/D Photoreceptor Rh Simple Set to 0 to use estimate from input image. The value the average luminance is mapped to. Tone Map Node Tone Map Node. Tone mapping is a technique used in image processing and computer graphics to map one set of colors to another in order to approximate the appearance of high dynamic range images in a medium that has a more limited dynamic range. Type Project-Id-Version: Blender 2.8 Manual 2.8
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2020-03-30 21:20+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Hình ảnh :abbr:`HDR (Dải Động Cao -- High Dynamic Range)`. Hình ảnh :abbr:`LDR (Dải Động Thấp -- Low Dynamic Range)`. Tuỳ Ứng -- Adaptation Chỉnh Sửa Màu -- Color Correction Độ Tương Phản -- Contrast Về cơ bản mà nói, Ánh Xạ Sắc Thái giải quyết vấn đề về phương pháp thuyên giảm độ tương phản mạnh từ các giá trị của cảnh (*trong đơn vị rad*) sang một phạm vi có thể hiển thị được (*trên màn hình*), song đồng thời, bảo toàn các chi tiết và màu sắc của hình ảnh. Điều này rất quan trọng để duy trì nội dung của cảnh ban đầu. Nếu là 0 thì toàn cầu; nếu là 1 thì dựa trên cường độ của điểm ảnh. Nếu 0 thì tất cả các kênh đều giống nhau; nếu là 1 thì mỗi cái sẽ riêng biệt. Nếu nhỏ hơn 0 thì sẽ làm tối hình ảnh đi; nếu không thì làm cho nó sáng hơn. Nếu không sử dụng thì đặt là 1. Hình Ảnh -- Image Đầu Vào -- Inputs Cường Độ -- Intensity Khóa -- Key Thông thường thì nó luôn luôn là 1, song có thể được sử dụng như một điều khiển bổ sung để thay đổi đường cong về độ sáng. Dịch Chuyển -- Offset Đầu Ra -- Outputs Tính Chất -- Properties Tế bào cảm nhận ánh sáng :abbr:`R/D (Erik Reinhard, và Kate Devlin, http://erikreinhard.com/papers/tvcg2005.pdf)` -- `R/D Photoreceptor <http://erikreinhard.com/papers/tvcg2005.pdf>`__ Rh Đơn Giản -- Rh Simple Đặt thành 0 để sử dụng sự ước tính từ hình ảnh đầu vào. Độ sáng trung bình sẽ được ánh xạ thành giá trị này. Nút Ánh Xạ Sắc Thái -- Tone Map Node Nút Ánh Xạ Sắc Thái. Ánh Xạ Sắc Thái (*Tone mapping*) là một kỹ thuật được sử dụng trong quá trình xử lý hình ảnh và trong đồ họa máy tính để ánh xạ một bộ màu sắc nào đó sang một cái khác, hòng nhằm tính ước lệ diện mạo của các hình ảnh có dải động cao (*high dynamic range, viết tắt là HDR*) trên một phương tiện thông tin có dải động (*dynamic range*) hạn chế hơn (*hiển thị hình ảnh có dải động lớn trên một thiết bị hiển thị có giới hạn về sức biểu đạt ánh sáng chẳng hạn*). Thể Loại -- Type 