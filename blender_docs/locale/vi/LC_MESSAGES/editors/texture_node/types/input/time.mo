��          �               ,     -     3     ;  g   B     �     �     �  
   �  �   �  
   �  ?  �  y   �     y  	   �  
   �  T   �  �  �     �     �     �  �   �     �  0   �     
         :  7   �	  �  �	  �   �  !   �     �     �  �   �   Curve Example Factor Flipping the curve around reverses the time input, but doing so is easily overlooked in the node setup. Inputs Output values Outputs Properties Start frame and End frame of the range of time specifying the values the output should last. This range becomes the X axis of the graph. The time input could be reversed by specifying a start frame greater than the end frame. Start, End The :doc:`Map Value </compositing/types/vector/map_value>` node can be used to map the output to a more appropriate value. With sometimes curves, it is possible that the Time node may output a number larger than one or less than zero. To be safe, use the Min/Max clamping function of the Map Value node to limit output. The Y value defined by the curve is the factor output. For the curve controls see: :ref:`Curve widget <ui-curve-widget>`. This node has no inputs. Time Node Time Node. Time controls from left to right: no effect, slow down, freeze, accelerate, reverse. Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-05-15 13:23+0100
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Đường Cong -- Curve Ví Dụ -- Example Hệ Số -- Factor Đảo lật đường cong ngược lại sẽ đảo ngược thời gian cung cấp ở đầu vào, song làm như vậy sẽ khó quan sát và dễ gây ra sự lãng quên trong quá trình thiết lập nút. Đầu Vào -- Inputs Giá trị xuất ở đầu ra -- Output values Đầu Ra -- Outputs Tính Chất -- Properties Khung hình mở đầu và khung hình kết thúc trong phạm vi thời gian quyết định các giá trị đầu ra rằng chúng sẽ kéo dài bao lâu. Phạm vi này trở thành trục X của biểu đồ. Đầu vào về thời gian (*time input*) có thể được đảo ngược bằng cách xác định khung hình bắt đầu lớn hơn khung hình kết thúc. Bắt Đầu, Kết Thúc (Đầu,Cuối) -- Start, End Nút :doc:`Ánh Xạ Giá Trị -- Map Value </compositing/types/vector/map_value>` có thể được sử dụng để ánh xạ đầu ra sang thành một giá trị thích hợp hơn. Đôi khi, với các đường cong, nút Thời gian có thể xuất ra một số lớn hơn 1, hoặc nhỏ hơn 0. Để bảo toàn, xin hãy sử dụng chức năng hạn định (*clamping*) của nút Ánh Xạ Giá Trị  để giới hạn đầu ra. Giá trị Y được xác định bởi đường cong là hệ số đầu ra. Đối với các điều khiển về đường cong, xin hãy xem mục: :ref:`Thành tố điều khiển đường cong -- Curve widget <ui-curve-widget>`. Nút này không có đầu vào. Nút Thời Gian -- Time Node Nút Thời Gian. Những điều khiển về thời gian, từ trái sang phải: Vô Hiệu (*no effect*), Làm Chậm Lại (*slow down*), Đứng Im (*freeze*), Tăng Tốc (*accelerate*), Đảo Ngược (*reverse*). 