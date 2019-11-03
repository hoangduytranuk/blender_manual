��    6      �              |     }  �   �     ]  �   m  V     �   m  %        *  +   0     \  E   q     �  $   �  
   �  C   �  #   2  X   V     �     �     �  �   �
     �  �   �     �  \  �  G       _  A  f     �  N   �  .   �     .     2  	   ;     E  �   N        
   (  �   3  Y   �          1  �   :  �     t   �  \   "       	   �  �  �     �  F  �  V   �  �   6  �  "     �  �  �  ,   w  �   �  �   �   #  K!  5   o"     �"  T   �"  6   #  Y   H#     �#  g   �#     $  �   4$  _   �$  �   %     �%     �%  e  �%  �  Z+     �,  k  �,     j.  6  .  �  �1     �5  i  �5     8  �   *8  >   �8     9     9     39     E9  `  W9     �:     �:  �   �:  �   �;  *   D<     o<  p  �<    �=  �   ?  �   �?     c@     @  �  �@  +   #D  g  OD  �   �F    8G   Add Adding blue to blue keeps it blue, but adding blue to red makes purple. White already has a full amount of blue, so it stays white. Use this to shift a color of an image. Adding a blue tinge makes the image feel colder. Additional uses As you can hopefully see, our original magic monkey was overexposed by too much light. To cure an overexposure, you must both darken the image and enhance the contrast. Below are samples of common mix modes and uses, mixing a color or checker with a mask. Black (0.00) times anything leaves black. Anything times White (1.00) is itself. Use this to mask out garbage, or to colorize a black-and-white image. Checking an image for your watermark. Clamp Combines the two images, averaging the two. Contrast Enhancement Controls the amount of influence the node exerts on the output image. Darken Decoding an Image for your Watermark Difference Embedding your mark in an image using a mark and specific position. Encoding your Watermark in an Image Example node setup showing "Darken", "Enhance Contrast" and "Mix" nodes for composition. Examples Factor First, construct your own personal watermark. You can use your name, a word, or a shape or image not easily replicated. While neutral gray works best using the encoding method suggested, you are free to use other colors or patterns. It can be a single pixel or a whole gradient; it is up to you. In the example below, we are encoding the watermark in a specific location in the image using the *Translate* node; this helps later because we only have to look at a specific location for the mark. We then use the RGB to BW node to convert the image to numbers that the Map Value node can use to make the image subliminal. In this case, it reduces the mark to one-tenth of its original intensity. The Add node adds the corresponding pixels, making the ones containing the mark ever-so-slightly brighter. Here is a small map showing the effects of two other common uses for the RGB Curve: *Darken* and *Contrast Enhancement*. You can see the effect each curve has independently, and the combined effect when they are *mixed* equally. Hue If activated, by clicking on the *Color and Alpha* icon, the Alpha channel of the second image is used for mixing. When deactivated, the default, the icon background is a light gray. The alpha channel of the base image is always used. Image In the old days, a pattern was pressed into the paper mush as it dried, creating a mark that identified who made the paper and where it came from. The mark was barely perceptible except in just the right light. Probably the first form of subliminal advertising. Nowadays, people watermark their images to identify them as personal intellectual property, for subliminal advertising of the author or hosting service, or simply to track their image's proliferation throughout the web. Blender provides a complete set of tools for you to both encode your watermark and to tell if an image has your watermark. In the top RGB curve, *Darken*, only the right side of the curve was lowered; thus, any X input along the bottom results in a geometrically less Y output. The *Enhance Contrast* RGB (S-shaped) curve scales the output such that middle values of X change dramatically; namely, the middle brightness scale is expanded, and thus, whiter whites and blacker blacks are output. To make this curve, simply click on the curve and a new control point is added. Drag the point around to bend the curve as you wish. The Mix node combines these two effects equally, and Suzanne feels much better. Inputs It takes out a color. The color needed to turn Yellow into White is Blue. Use this to compare two very similar images to see what had been done to one to make it the other; sort of like a change log for images. You can use this to see a watermark (see `Watermark images`_) you have placed in an image for theft detection. Lighten Like bleach makes your whites whiter. Used with a mask to lighten up a little. Limit the highest color value to not exceed 1. Mix Mix Node Mix Node. Multiply Of course, if you *want* people to notice your mark, do not scale it so much, or make it a contrasting color. There are also many other ways, using other mix settings and fancier rigs. Feel free to experiment! Outputs Properties Shows you how much of a color is in an image, ignoring all colors except what is selected: makes a monochrome picture (style 'Black & Hue'). Some explanation of the mixing methods above might help you use the Mix node effectively: Standard image output. Subtract Taking Blue away from white leaves Red and Green, which combined make Yellow. Taking Blue away from Purple leaves Red. Use this to desaturate an image. Taking away yellow makes an image bluer and more depressing. The *Mix Node* mixes images by working on the individual and corresponding pixels of the two input images. Called "MixRGB" in the shader and texture context. The Blend types can be selected in the select menu. See :term:`Color Blend Modes` for details on each blending mode. The background image. The image size and resolution sets the dimensions of the output image. The foreground image. Use Alpha Various image compression algorithms lose some of the original; the difference shows as noise. Experiment with different compression settings and marks to see which works best for you by having the encoding map in one scene, and the decoding map in another. Use them while changing Blender's image format settings, reloading the watermarked image after saving, to get an acceptable result. In the example above, the mark was clearly visible all the way up to ``JPEG`` compression of 50%. Watermark Images When you see an image that you think might be yours, use the node map below to compare it to your stock image (pre-watermarked original). In this map, the Mix node is set to Difference, and the Map Value node amplifies any difference. The result is routed to a viewer, and you can see how the original mark clearly stands out. With the colors set here, it's like looking at the world through rose-colored glasses. You can also use this technique, using settings that result in visible effects, in title sequences to make the words appear to be cast on the water's surface, or as a special effect to make words appear on the possessed girl's forearm. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-08-30 20:03-0400
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Cộng Thêm -- Add Việc cộng thêm màu xanh lam vào xanh lam sẽ giữ cho màu là xanh lam, nhưng việc thêm màu xanh lam vào màu đỏ sẽ tạo ra màu tím. Màu trắng vốn dĩ đã có màu xanh lam ở mức cao nhất, nên nó vẫn trắng. Sử dụng điều này để dịch chuyển màu của hình ảnh. Thêm sắc lam vào sẽ làm cho hình ảnh cảm thấy lạnh hơn. Những sử dụng khác -- Additional uses Như bạn có thể thấy, hình đầu khỉ ban đầu bị quá sáng, do quá nhiều ánh sáng chiếu vào. Để chữa sự phơi sáng quá mức, bạn phải vừa làm tối cả hình ảnh và vừa phải tăng độ tương phản. Dưới đây là các mẫu vật của các chế độ hòa trộn phổ biến và công dụng của chúng, trộn màu hoặc hình ô cờ với màn chắn lọc. Màu đen (0,00) nhân với bất cứ cái gì cũng sẽ thành màu đen mà thôi. Bất cứ màu nhân với trắng (1.00) sẽ cho chính màu ấy. Sử dụng tính năng này để loại bỏ những bẩn thỉu (*garbage*) hoặc để tô màu một hình ảnh đen trắng. Kiểm tra thủy ấn trong hình ảnh của bạn. Hạn Định -- Clamp Kết hợp hai hình ảnh lại với nhau, lấy trung bình của cả hai cái. Nâng Cao Độ Tương Phản -- Contrast Enhancement Điều chế lượng ảnh hưởng mà nút tác động đến hình ảnh xuất ra. Làm Tối -- Darken Giải mã một Hình Ảnh để tìm Thủy Ấn của bạn -- Decoding an Image for your Watermark Hiệu -- Difference Gắn dấu hiệu của bạn vào một hình ảnh bằng cách sử dụng một nhãn hiệu và một vị trí cụ thể. Mã hóa Thủy Ấn của bạn trong một Hình Ảnh -- Encoding your Watermark in an Image Thiết lập của nút ví dụ cho thấy các nút "Làm Tối" (*Darken*), "Tăng cường độ tương phản" (*Enhance Contrast*) và "Hòa Trộn" (*Mix*) cho bố cục. Ví Dụ -- Examples Hệ Số -- Factor Trước tiên, hãy kiến tạo thủy ấn cá nhân của riêng mình. Bạn có thể sử dụng tên của mình, một từ, hoặc một hình dạng hoặc hình ảnh không dễ dàng sao chép. Trong khi màu xám trung tính hoạt động tốt nhất khi sử dụng phương pháp mã hóa đề xuất, bạn cũng có thể tùy ý sử dụng các màu hoặc mẫu khác nữa. Nó có thể chỉ là một điểm ảnh đơn lẻ, hoặc là toàn bộ dốc màu (*gradient*); tùy bạn chọn lựa. Trong ví dụ dưới đây, chúng ta sẽ mã hóa một thủy ấn tại một vị trí xác định trong hình ảnh bằng nút *Dịch Chuyển* (*Translate*); làm thế này thì trong tương lai sẽ có lợi sau hơn, bởi vì chúng ta chỉ cần nhìn vào một vị trí cụ thể để tìm dấu hiệu. Sau đó, chúng ta sử dụng nút *RGB Sang Trắng/Đen* (*RGB to BW*) để chuyển đổi hình ảnh thành các con số mà nút *Ánh Xạ Giá Trị* (*Map Value*) có thể sử dụng để làm cho hình ảnh trở nên trầm ẩn. Trong trường hợp này, nó giảm dấu ấn xuống một phần mười (1/10) cường độ ban đầu. Nút *Cộng* (*Add*) bổ sung thêm các điểm ảnh tương ứng, làm cho các điểm ảnh trong vùng của dấu hiệu nhỉnh sáng hơn một chút. Đây là một bản đồ nhỏ cho thấy hiệu ứng của hai cách sử dụng phổ biến khác cho đường cong RGB: *Làm Tối* (*Darken*) và *Tăng Cường Độ Tương Phản* (*Contrast Enhancement*). Bạn có thể thấy hiệu ứng của mỗi đường cong một cách độc lập và hiệu ứng kết hợp khi chúng được trộn lẫn với lượng *bằng nhau*. Sắc Thái -- Hue Nếu được kích hoạt, bằng cách bấm vào biểu tượng *Màu và Alpha*, kênh Alpha của hình ảnh thứ hai sẽ được sử dụng để hòa trộn. Khi bị giải hoạt (tắt), bản mặc định, nền biểu tượng sẽ có màu xám nhạt. Kênh alpha của hình ảnh nền (*base image*) sẽ luôn luôn được sử dụng. Hình Ảnh -- Image Trước đây, khuôn mẫu được ép vào hồ giấy khi nó đang khô, tạo ra một dấu hiệu, xác định ai đã làm giấy và nó đến từ đâu. Dấu ấn hầu như không thể nhận thấy ngoại trừ dưới nguồn ánh sáng vừa đủ. Có lẽ đây là hình thức quảng cáo ngầm đầu tiên. Ngày nay, mọi người thủy ấn hình ảnh của họ để xác định chúng là tài sản trí tuệ cá nhân, để tác giả hoặc dịch vụ tồn tại quảng cáo ngầm, hoặc chỉ đơn giản là để theo dõi mức xâm nhập hình ảnh của họ trên toàn bộ mạng web. Blender cung cấp một bộ công cụ hoàn chỉnh để bạn có thể mã hóa thủy ấn của mình và cho biết hình ảnh có thủy ấn của bạn hay không. Trong đường cong RGB (*RGB curve*) trên cùng, *Làm Tối* (*Darken*), thì chỉ phía bên phải của đường cong là được hạ xuống; do đó, bất kỳ đầu vào X nào dọc theo phía dưới sẽ cho kết quả đầu ra Y ít tính hình học hơn. Đường cong *Tăng Cường Độ Tương Phản* RGB (hình chữ S) tỷ lệ hóa đầu ra sao cho các giá trị trung gian của X thay đổi một cách đáng kể; cụ thể là, các giá trị trung gian được mở rộng, và do đó, làm cho các màu trắng trắng hơn và các màu đen đen hơn là đầu ra. Để làm đường cong này, chỉ cần bấm vào đường cong và một điểm điều khiển mới sẽ được thêm vào. Kéo điểm ở xung quanh nó để uốn cong đường cong theo như bạn muốn. Nút Hòa Trộn (*Mix*) kết hợp hai hiệu ứng này với lượng bằng nhau, và hình Suzanne (*Đầu Khỉ*) dễ nhìn hơn nhiều. Đầu Vào -- Inputs Cái này sẽ tước bỏ một màu sắc nào đó ra khỏi hình ảnh. Màu sắc cần thiết để biến màu vàng thành trắng là màu lam. Sử dụng điều này để so sánh hai hình ảnh khá tương đồng để xem những gì đã được thực hiện cho bản này để làm cho nó trở thành bản khác; tương tự như một bản nhật ký về những thay đổi cho hình ảnh. Bạn có thể sử dụng chức năng này để xem hình thủy ấn (xin xem `Watermark images`_) mà bạn đã đặt trong một hình ảnh để phát hiện hành vi trộm cắp. Làm Sáng -- Lighten Tương tự như thuốc tẩy làm những áo trắng của bạn trắng hơn. Sử dụng với một màn chắn để làm sáng lên một chút. Giới hạn giá trị màu cao nhất không vượt quá 1. Hòa Trộn -- Mix Nút Hòa Trộn -- Mix Node Nút Hòa Trộn. Nhân -- Multiply Tất nhiên, nếu bạn *muốn* mọi người chú ý đến nhãn hiệu của bạn, thì đừng phóng to nó quá nhiều, hoặc làm cho nó có màu tương phản. Còn có rất nhiều cách nữa, bằng cách sử dụng các bố trí hòa trộn khác nhau và dùng những dàn dựng bạo dạn hơn. Hãy tùy ý thử nghiệm! Đầu Ra -- Outputs Tính Chất -- Properties Hiển thị cho bạn thấy lượng một màu có trong hình ảnh, bỏ qua tất cả các màu trừ những gì đã được chọn: tạo một ảnh đơn sắc (kiểu 'Đen & Sắc Thái'). Một số giải thích về các phương pháp trộn ở trên có thể giúp bạn sử dụng nút Hòa Trộn một cách hiệu quả: Đầu ra tiêu chuẩn của hình ảnh. Trừ Khấu -- Subtract Lấy màu lam ra khỏi màu trắng sẽ để lại màu đỏ và xanh lục, tức khi kết hợp lại trở nên màu vàng. Lấy xanh lam ra khỏi màu tím sẽ để lại màu đỏ. Sử dụng điều này để giảm độ bão hòa của một hình ảnh. Lấy màu vàng đi để làm cho một hình ảnh xanh hơn và cảm giác buồn hơn. *Nút Hòa Trộn* hòa nhập các hình ảnh bằng cách hoạt động trên các điểm ảnh riêng biệt và tương đồng của hai hình ảnh đầu vào. Được gọi là "Hòa Trộn RGB -- MixRGB" trong ngữ cảnh của bộ tô bóng và chất liệu. Các kiểu hòa trộn (*Blend types*) có thể được chọn trong trình đơn chọn lựa. Xin xem thêm về :term:`Color Blend Modes` để biết thêm chi tiết về từng chế độ hoà trộn. Hình nền. Kích thước và độ phân giải của hình ảnh thiết lập kích thước của hình ảnh ở đầu ra. Hình ảnh nền trước. Dùng Alpha -- Use Alpha Nhiều thuật toán nén hình ảnh gây mất dữ liệu của bản gốc; sự khác biệt thường được hiển thị thành dữ liệu nhiễu. Việc thử nghiệm với các cài đặt trong chu trình nén và các dấu hiệu (dùng làm thủy ấn) khác nhau để tìm xem cái nào hoạt động tốt nhất cho bạn, bằng cách để sơ đồ mã hóa trong một cảnh, và sơ đồ giải mã trong một cảnh khác, là một việc nên làm. Hãy sử dụng chúng trong khi thay đổi cài đặt định dạng hình ảnh trong Blender, tải lại hình ảnh đã được thủy ấn sau khi đã lưu, để đạt được kết quả khả dĩ, có thể chấp nhận được. Trong ví dụ trên đây, dấu hiệu được hiển thị rõ ràng trong toàn bô quá trình, cho mãi đến khi được nén thành ``JPEG`` với độ nén 50%. Hình Ảnh Thủy Ấn -- Watermark Images Khi bạn nhìn thấy một hình ảnh mà bạn nghĩ có thể là của bạn, hãy sử dụng sơ đồ sắp xếp nút dưới đây để so sánh nó với hình ảnh trong kho của bạn (bản gốc chưa được đánh dấu với thủy ấn). Trong sơ đồ này, nút Hòa Trộn (*Mix*) được nối với nút Hiệu (*Difference*) và nút Ánh Xạ Giá Trị (*Map Value*) để khuếch đại bất kỳ sự khác biệt nào. Kết quả được chuyển đến nút Xem Hình (*Viewer*) và bạn có thể thấy dấu hiệu ban đầu rõ ràng nổi bật lên như thế nào. Với những màu sắc thiết lập ở đây, nó giống như nhìn thế giới qua những chiếc kính màu hoa hồng. Bạn cũng có thể sử dụng kỹ thuật này, dùng các sắp đặt đưa đến hiệu ứng nhìn thấy được, trong các đoạn phim tiêu đề để làm cho các từ xuất hiện như được chiếu trên bề mặt của mặt nước, hoặc một hiệu ứng đặc biệt để làm cho các từ xuất hiện trên cánh tay của cô gái bị ma ám. 