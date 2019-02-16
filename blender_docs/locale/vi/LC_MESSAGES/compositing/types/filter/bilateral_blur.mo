��          �               �  '   �     �     �  �   �  �   �  �   %     �  
   �  w   �  X   5     �     �     �     �  �   �  
   �     �  
   �     �     �  �   �     g  �   ~  %    �  2  5   �	  4    
     U
  �   s
  �   $  �   �     ~     �  �   �  l   >     �     �     �     �  �    $   �     �            &   9  �   `  *   �  �     &  �   A fine-tuning variable for blur radius. Bilateral Blur Node Bilateral Blur Node. Bilateral faked blurry refraction and smoothed ray-traced soft shadow. `blend-file example <https://en.blender.org/uploads/e/e4/Bilateral_blur_example_02.blend>`__ Bilateral smoothed Ambient Occlusion. `blend-file example <https://en.blender.org/uploads/2/2a/Bilateral_blur_example_01.blend>`__ Bilateral smoothed buffered shadow. `blend-file example <https://en.blender.org/uploads/b/ba/Bilateral_blur_example_03.blend>`__ Color Sigma Composite. Defines how many times the filter should perform the operation on the image. It practically defines the radius of blur. Defines the threshold for which color differences in the image should be taken as edges. Determinator Examples Image Inputs It can be used for various purposes like: smoothing noisy render passes to avoid longer computation times in example ray-traced ambient occlusion, blurry refractions/reflections, soft shadows, or to make non-photorealistic compositing effects. Iterations Outputs Properties Render result. Space Sigma Standard image input. If only the image input is connected, the node blurs the image depending on the edges present in the source image. Standard image output. The Bilateral Blur node performs a high-quality adaptive blur on the source image, allowing to blur images while retaining their sharp edges. Which is non-obligatory and if the Determinator is connected, it serves as the source for defining edges/borders for the blur in the image. This has great advantage in case the source image is too noisy, but normals in combination with Z-buffer can still define exact borders/edges of objects. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-29 03:19+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Một biến số tinh chỉnh bán kính nhòe mờ. Nút Nhòe Mờ Song Phương -- Bilateral Blur Node Nút Nhòe Mờ Song Phương Khúc xạ nhòe mờ giả song phương và bóng tối mịn hóa dò tia. `Ví dụ tập tin blend <https://en.blender.org/uploads/e/e4/Bilateral_blur_example_02.blend>`__ Hấp Thụ Quang Xạ Môi Trường mịn hóa song phương (Bilateral smoothed Ambient Occlusion). `Ví dụ tập tin blend <https://en.blender.org/uploads/2/2a/Bilateral_blur_example_01.blend>`__ Bóng tối đệm mịn hóa song phương. `Ví dụ tập tin blend <https://en.blender.org/uploads/b/ba/Bilateral_blur_example_03.blend>`__ Sigma của Màu -- Color Sigma Tổng hợp. Xác định số lần bộ lọc cần thực hiện thao tác trên hình ảnh. Thực ra, cái này xác định bán kính làm nhòe mờ. Xác định ngưỡng mà sự khác biệt màu sắc trong hình ảnh được coi như là các cạnh. Định Vị -- Determinator Các Ví Dụ -- Examples Hình Ảnh -- Image Đầu Vào -- Inputs Nó có thể được sử dụng cho nhiều mục đích khác nhau như: làm mịn các lượt kết xuất nhiễu để tránh thời gian tính toán dài hơn, chẳng hạn trong trường hợp Tính Hấp Thụ Quang Xạ Môi Trường Dò Tia (ray-traced ambient occlusion), khúc xạ nhòe mờ/phản quang, bóng tối mềm mại, hoặc tạo các hiệu ứng tổng hợp không giống ảnh chụp (non-photorealistic). Số Lần Lặp Lại -- Iterations Đầu Ra -- Outputs Tính Chất -- Properties Kết quả kết xuất. Sigma của Không Gian -- Space Sigma Standard image input. If only the image input is connected, the node blurs the image depending on the edges present in the source image. Đầu ra tiêu chuẩn của hình ảnh. Nút Nhòe Mờ Song Phương thực hiện hiệu ứng nhòe tùy ứng chất lượng cao trên hình ảnh nguồn, cho phép làm nhòe mờ các hình ảnh trong khi giữ nguyên các cạnh sắc nét của chúng. Là cái không bắt buộc và nếu phần Định Vị (Determinator) được kết nối vào thì nó sẽ đóng vai trò là nguồn để xác định các cạnh/đường ranh giới cho quá trình làm nhòe mờ trong hình ảnh. Điều này có lợi thế lớn trong trường hợp hình ảnh nguồn quá nhiễu, song các pháp tuyến cùng với sự kết hợp của Bộ Đệm Z (Z-buffer) vẫn có thể xác định được các đường ranh giới/cạnh của các đối tượng một cách chính xác nữa. 