��          �               �  P   �  0   �                8     ?     N  9   ^     �     �     �     �  
   �  "   �     �     �      �   #          .     K     Q  �  ]  {     S   �     �  5   �     /	  +   E	     q	  �   �	  $   
  +   C
     o
     �
     �
  .   �
     �
  )   �
  �  )  �    <   �  |        �  %   �   Defines a range between minimum and maximum to :term:`clamp` the input value to. Enable this to activate their related operation. Example Factor added to the input value. Inputs Map Value Node Map Value Node. Map Value node is used to scale, offset and clamp values. Min, Max Multiplying Values Offset Outputs Properties Scales (multiply) the input value. Size Standard value output. The map value node can also be used to multiply values to achieve a desired output value. In the mini-map to the right, the Time node outputs a value between 0.0 and 1.0 evenly scaled over 30 frames. The *first* Map Value node multiplies the input by 2, resulting in an output value that scales from 0.0 to 2.0 over 30 frames. The *second* Map Value node subtracts 1 from the input, giving working values between (-1.00 to 1.0), and multiplies that by 150, resulting in an output value between (-150 to 150) over a 30-frame sequence. This is particularly useful in achieving a depth of field effect, where the Map Value node is used to map a Z value (which can be 20 or 30 or even 500 depending on the scene) to the range between (0 to 1), suitable for connecting to a Blur node. Use Minimum, Maximum Using Map Value to multiply. Value Z-Depth Map Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-06-30 09:48+1000
PO-Revision-Date: 2019-03-23 14:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Xác định một phạm vi giữa tối thiểu và tối đa để hạn định (:term:`clamp`) giá trị đầu vào. Bật tính năng này lên để kích hoạt phép toán liên quan của chúng. Ví Dụ -- Example Hệ số được thêm vào giá trị đầu vào. Đầu Vào -- Inputs Nút Ánh Xạ Giá Trị -- Map Value Node Nút Ánh Xạ Giá Trị. Nút Ánh Xạ Giá Trị được sử dụng để tỷ lệ hóa (scale), dịch chuyển (offset), và hạn định (clamp) các giá trị. Tối Thiểu, Tối Đa -- Min, Max Nhân các Giá Trị -- Multiplying Values Dịch Chuyển -- Offset Đầu Ra -- Outputs Tính Chất -- Properties Tỷ lệ hóa (nhân) giá trị đầu vào. Kích Thước -- Size Đầu ra tiêu chuẩn của giá trị. Nút Ánh Xạ Giá Trị (:ref:`Map Value <bpy.types.CompositorNodeMapValue>`) cũng có thể được sử dụng để nhân giá trị lên thành một giá trị đầu ra mong muốn. Trong sơ đồ nhỏ ở bên phải, nút Thời Gian (:ref:`Time <bpy.types.TextureNodeCurveTime>`) cho ra một giá trị trong phạm vi từ 0,0 đến 1,0, được phân tỷ lệ đồng đều trên 30 khung hình. Nút Ánh Xạ Giá Trị (:ref:`Map Value <bpy.types.CompositorNodeMapValue>`) *đầu tiên* nhân giá trị đầu vào lên 2, dẫn đến giá trị của đầu ra được phân tỷ lệ từ 0,0 đến 2,0 trên 30 khung hình. Nút Ánh Xạ Giá Trị (:ref:`Map Value <bpy.types.CompositorNodeMapValue>`) *thứ hai* khấu trừ 1 khỏi giá trị đầu vào, tạo ra các giá trị hoạt động trong khoảng từ (-1,00 đến 1) và nhân nó với 150 để tạo thành giá trị đầu ra trong khoảng từ (-150 đến 150) trong trình tự 30 khung hình. Điều này đặc biệt hữu ích khi mình muốn tạo hiệu ứng độ sâu trường ảnh, trong đó nút Ánh Xạ Giá Trị (:ref:`Map Value <bpy.types.CompositorNodeMapValue>`) được sử dụng để ánh xạ giá trị Z (có thể là 20, 30 hoặc thậm chí là 500 tùy theo cảnh) sang phạm vi giữa (0 đến 1), thích hợp để kết nối với nút Làm Nhòe (:ref:`Blur <bpy.types.CompositorNodeBlur>`). Sử dụng Tối Thiểu, Tối Đa -- Use Minimum, Maximum Sử dụng nút Ánh Xạ Giá Trị (:ref:`Map Value <bpy.types.CompositorNodeMapValue>`) để thực hiện tính nhân. Giá Trị -- Value Ánh Xạ Độ Sâu Z -- Z-Depth Map 