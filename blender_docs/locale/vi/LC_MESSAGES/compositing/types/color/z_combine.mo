��          �               �     �  ^   �     )     B  �   K     �     �     �     �       
     �   '     �  �   �  J   �     <  [  R  	   �     �     �     �     �  �   �      �      �  �  �  $   �	  �   �	  '   y
     �
  �   �
     �     �  7   �  -        =     R  �  m     �  �    a   �     -    M     k  0   �  $   �     �  "   �  `    5   r  2   �   Anti-Alias Z Applies :term:`Anti-Aliasing` to avoid artifacts at sharp edges or areas with a high contrast. Choosing closest pixels. Examples If both Z values are equal, it will use the foreground image. Whichever Z value is less decides which image pixel is used. See :term:`Z-buffer`. Image Inputs Invisible Man Effect Mix and match images. Outputs Properties The Z Combine node combines two images based on their Z-depth maps. It overlays the images using the provided Z values to detect which parts of one image are in front of the other. The background image. The chosen Image pixel alpha channel is also carried over. If a pixel is partially or totally transparent, the result of the Z Combine will also be partially transparent; in which case the background image will show through the foreground (chosen) pixel. The combined Z depth, which allows to thread multiple Z-combines together. The foreground image. This node can be used to combine a foreground with a background matte painting. Walt Disney pioneered the use of multi-plane mattes, where three or four partial mattes were painted on glass and placed on the left and right at different Z positions; minimal camera moves to the right created the illusion of depth as Bambi moved through the forest. Use Alpha Valid Input Z Combine Node Z Combine Node. Z Combine in action. Z Input Sockets do not accept fixed values; they must get a vector set (see Map Value node). Image Input Sockets will not accept a color since it does not have UV coordinates. Z depth of the background image. Z depth of the foreground image. Project-Id-Version: Blender 2.8 Manual 2.8
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2020-05-15 13:23+0100
PO-Revision-Date: 2020-04-12 10:34+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Chống Răng Cưa Z -- Anti-Alias Z Áp dụng :term:`Chống Răng Cưa -- Anti-Aliasing` để tránh giả tượng xuất hiện ở các cạnh sắc nét, hoặc các khu vực có độ tương phản cao. Chọn các điểm ảnh gần nhất. Ví Dụ -- Examples Nếu cả hai giá trị Z đều bằng nhau thì nó sẽ sử dụng hình ảnh nền trước. Giá trị Z nào kém hơn sẽ quyết định điểm ảnh nào được sử dụng. Xin xem phần về :term:`Bộ Đệm-Z -- Z-buffer`. Hình Ảnh -- Image Đầu Vào -- Inputs Hiệu ứng Người Vô Hình -- Invisible Man Effect Hòa trộn và kết hợp các hình ảnh. Đầu Ra -- Outputs Tính Chất -- Properties Nút Kết Hợp Z (*Z Combine node*) sẽ kết hợp hai hình ảnh dựa trên ánh xạ (*sơ đồ*) về độ sâu Z của chúng. Nút này chồng các hình ảnh lên nhau, và bằng cách sử dụng các giá trị Z được cung cấp, phát hiện và xác định phần nào của một hình ảnh nằm ở phía trước, và những phần nằm nằm ở phía sau. Hình ảnh nền. Kênh alpha của điểm ảnh trong hình ảnh đã chọn cũng sẽ được chuyển sang. Nếu một điểm ảnh nào đó là trong suốt, hoặc chỉ là một phần, hoặc là toàn phần, thì kết quả của quá trình Kết Hợp Z (*Z Combine*) cũng sẽ chỉ trong suốt một phần mà thôi, và do đó, hình nền sẽ nhìn thấy được, xuyên qua điểm ảnh (đã chọn -- chosen) nằm ở phía trước. Độ sâu Z kết hợp cho phép mình mắc nối nhiều sự kết hợp Z lại với nhau. Hình ảnh ở nền trước. Nút này có thể được sử dụng để kết hợp một hình ảnh nền trước với một bức vẽ lồng làm nền sau. Walt Disney là công ty tiên phong trong việc sử dụng đa lớp lồng, đa tầng lớp, trong đó ba hoặc bốn lớp lồng được vẽ trên kính và đặt ở bên trái và bên phải tại các vị trí Z khác nhau; Với phương pháp nhích máy ảnh sang bên phải, họ đã tạo được ảo tưởng về chiều sâu, khi con hươu Bambi đi xuyên qua khu rừng. Dùng Alpha -- Use Alpha Giá Trị Đầu Vào Hợp Lệ -- Valid Input Nút Kết Hợp Z -- Z Combine Node Nút Kết Hợp Z. Kết Hợp Z trong hành động. Các Ổ Cắm Đầu Vào Z (*Z Input Sockets*) sẽ không chấp nhận các giá trị cố định (*fixed values*); chúng đòi hỏi một tập hợp vectơ (xem nút Ánh Xạ Giá Trị để biết thêm). Các Ổ Cắm Đầu Vào Hình Ảnh (*Image Input Sockets*) sẽ không chấp nhận màu sắc vì nó không có tọa độ UV. Độ sâu Z của hình ảnh nền ở đằng sau. Độ sâu Z của hình ảnh ở nền trước. 