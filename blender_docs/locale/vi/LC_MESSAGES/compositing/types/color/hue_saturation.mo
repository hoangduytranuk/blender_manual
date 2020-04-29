��    !      $              ,     -  �   >  �     }   �  1   H     z  E   �     �     �                    (  !   B     d     x     �     �     �  
   �  
   �  |   �  E   4  �   z            �   0  ^   �  �   #     �     �  a   �  �  	     �
  c  �
  g  L  �   �  h   �  L     Y   ]     �  X   �      $     E  !   W  I   y  \   �  J      :   k     �     �     �     �       �     `     �   �  &   m  *   �    �  �   �  �   �     ^     t  �   �   A basic example. A blue image, with a Hue setting at either end of the spectrum (0 or 1), is output as yellow (recall that white, minus blue, equals yellow). A yellow image, with a Hue setting at 0 or 1, is blue. A gray image, where the RGB values are equal, has no hue. Therefore, this node can only affect it with *Value*. This applies to all shades of gray, from black to white; wherever the values are equal. A saturation of 0 removes hues from the image, resulting in a grayscale image. A shift greater than 1.0 increases saturation. An example of using the Factor input for masking. Changing the effect over time Controls the amount of influence the node exerts on the output image. Factor Gray & White are neutral hues HSV Example Hue Hue Saturation Node. Hue Saturation Value Node Hue and Saturation work together. Hue/Saturation Tips Hues are vice versa Image Inputs Outputs Properties Saturation So, a Hue of 0.5 keeps the blues the same shade of blue, but *Saturation* can deepen or lighten the intensity of that color. Some things to keep in mind that might help you use this node better: Specifies the hue rotation of the image. 360° are mapped to (0 to 1). The hue shifts of 0 (-180°) and 1 (+180°) have the same result. Standard image input. Standard image output. The *Hue Saturation Value Node* applies a color transformation in the HSV color space. Called "Hue Saturation Value" in shader and texture context. The Hue and Saturation values can be animated with a *Time Node* or by animating the property. The transformations are relative shifts. In the shader and texture context the following properties are available as input sockets. Tinge Value Value is the overall brightness of the image. De/Increasing values shift an image darker/lighter. Project-Id-Version: Blender 2.8 Manual 2.8
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2019-12-27 20:49-0600
PO-Revision-Date: 2020-04-10 19:26+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Một ví dụ cơ bản. Một hình ảnh màu xanh lam, với một thiết lập về Sắc Màu nằm ở một trong hai đầu của quang phổ (0 hoặc 1), thì cho ra màu vàng (nhớ rằng màu trắng trừ màu xanh lam đi thì thành màu vàng (Đỏ+Lục)). Một hình ảnh màu vàng, với thiết lập Sắc Màu tại 0 hoặc 1, sẽ là màu xanh lam. Một hình ảnh màu xám, nơi các giá trị RGB (*Đỏ, Lục, Lam*) bằng nhau, sẽ không có màu sắc. Vì vậy, nút này chỉ có thể tác động đến *Giá trị -- Value* của nó mà thôi. Điều này áp dụng cho tất cả các sắc xám, từ đen đến trắng; bất cứ nơi nào mà các giá trị đều bằng nhau. Độ bão hòa 0 sẽ loại bỏ sắc màu (*màu*) khỏi hình ảnh, dẫn đến một hình ảnh với thang độ xám (trắng/đen). Sự dịch chuyển lớn hơn 1,0 sẽ làm tăng độ bão hòa (màu tươi và rực lên). Một ví dụ về cách sử dụng Hệ Số (*Factor*) ở đầu vào cho quá trình chắn lọc. Thay đổi ảnh hưởng theo thời gian -- Changing the effect over time Điều chế lượng ảnh hưởng mà nút tác động đến hình ảnh xuất ra. Hệ Số -- Factor Màu Xám và màu Trắng là những Màu Trung Tính -- Gray & White are neutral hues Ví Dụ về HSV -- HSV Example Sắc Màu -- Hue Nút Sắc Màu, Độ Bão Hòa. Nút Sắc Màu, Độ Bão Hòa, Giá Trị -- Hue Saturation Value Node Sắc Màu và Độ Bão Hòa đồng hành với nhau -- Hue and Saturation work together. Một Số Gợi Ý về Sắc Màu/Độ Bão Hòa -- Hue/Saturation Tips Sắc Màu là sự Đảo Ngược -- Hues are vice versa Hình Ảnh -- Image Đầu Vào -- Inputs Đầu Ra -- Outputs Tính Chất -- Properties Độ Bão Hòa -- Saturation Do vậy mà nếu một Sắc Màu (*Hue*) có giá trị 0.5 thì nó sẽ giữ cho các màu lam vẫn nằm ở sắc lam, song *Độ Bão Hòa -- Saturation* có thể làm cho cường độ của màu đó trở nên tối hơn hoặc sáng hơn. Một số điều cần ghi nhớ để có thể giúp bạn sử dụng nút này tốt hơn: Chỉ định sự xoay vòng về sắc màu của hình ảnh. 360° sẽ được ánh xạ thành (0 đến 1). Những dịch chuyển về sắc màu của 0 (-180°) và 1 (+180°) sẽ có cùng một kết quả (giống nhau). Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. *Nút Sắc Màu, Độ Bão Hòa, Giá Trị -- Hue Saturation Value Node* áp dụng phép biến đổi màu trong không gian màu HSV. Trong ngữ cảnh bộ tô bóng và chất liệu thì được gọi là "Sắc Màu, Độ Bão Hòa, Giá trị -- Hue Saturation Value". Các giá trị Sắc Màu và Độ Bão Hòa đều có thể được hoạt họa với một *Nút Thời Gian -- Time Node* hoặc bằng cách hoạt họa tính chất của nó. Các biến đổi sẽ là các dịch chuyển tương đối. Trong bối cảnh của bộ tô bóng và chất liệu, các tính chất sau đây là những cái ở các ổ cắm đầu vào. Nhuốm Màu -- Tinge Giá Trị -- Value Giá trị là độ sáng tổng thể của hình ảnh. Giảm/Tăng các giá trị sẽ dịch chuyển độ sáng/tối của một hình ảnh. 