��          �               �     �     �     �     �     �     �  '  �  �   &                :  
   B     M     \     l     �  7   �  u   �  �  G     �  �     �  �  %   s	  #   �	  �  �	  @   u     �  -   �  /   �     (     C  �  X  >       S  $   i     �     �  #   �     �  &   �  *     G   G  �   �  �  Z  ,     n  ;  s  �  :     ?   Y   Colorizing a BW Image Example Fade In a Title Fade To Black Fade to black. Image In the above example, a Time curve provides the Alpha value to the input socket. The current Render Layer node, which has the title in view, provides the image. As before, the Alpha Over node mixes (using the alpha values) the background swirl and the alpha title to produce the composite image. In the example map to the right, use the *Alpha* value of the Set Alpha node to give a desired degree of colorization. Thread the input image and the Set Alpha node into an Alpha Over node to colorize any black-and-white image in this manner. Inputs No Scene Information Used Outputs Properties Set Alpha Node Set Alpha Node. Standard image input. Standard image output. The *Set Alpha Node* adds an alpha channel to an image. The amount of Alpha can be set for the whole image by using the input field or per pixel by connecting to the socket. This is not, and is not intended to be, a general-purpose solution to the problem of compositing an image that does not contain Alpha information. You might wish to use "Chroma Keying" or "Difference Keying" (as discussed elsewhere) if you can. This node is most often used (with a suitable input being provided by means of the socket) in those troublesome cases when you *cannot*, for some reason, use those techniques directly. This node has no properties. To introduce your animation, you will want to present the title of your animation over a background. You can have the title fly in, or fade it in. To fade it in, use the Set Alpha node with the Time node as shown below. To transition the audience from one scene or shot to another, a common technique is to "fade to black". As its name implies, the scene fades to a black screen. You can also "fade to white" or whatever color you wish, but black is a good neutral color that is easy on the eyes and intellectually "resets" the viewer's mind. The node map below shows how to do this using the Set Alpha node. Using Set Alpha to colorize an image. Using Set Alpha to fade in a title. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-12-27 20:49-0600
PO-Revision-Date: 2019-04-07 00:04+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Tô Màu một Hình Ảnh Trắng/Đen -- Colorizing a BW Image Ví Dụ -- Example Làm Rõ Dần Tiêu Đề -- Fade In a Title Phai Mờ Dần về Màu Đen -- Fade To Black Mờ dần sang màu đen. Hình Ảnh -- Image Trong ví dụ trên, đường cong Thời gian cung cấp giá trị Alpha cho ổ cắm đầu vào. Nút Tầng Kết Xuất (Render Layer) hiện tại, tức cái có tiêu đề nhìn thấy được là nút cung cấp hình ảnh. Như trước đây, nút Alpha Chồng Lên (Alpha Over) pha trộn (sử dụng các giá trị alpha) hình ảnh nền xoáy lốc và alpha của tiêu đề để tạo ra hình ảnh tổng hợp. Ở bên phải sơ đồ ví dụ, sử dụng giá trị *Alpha* của nút Đặt Alpha để cung cấp mức độ màu tô mong muốn. Lồng hình ảnh đầu vào và nút Đặt Alpha vào nút Alpha Chồng Lên (Alpha Over) để tô màu bất kỳ hình ảnh đen trắng nào theo phương pháp này. Đầu Vào -- Inputs Không Sử Dụng Thông Tin Cảnh Đầu Ra -- Outputs Tính Chất -- Properties Nút Đặt Alpha -- Set Alpha Node Nút Đặt Alpha. Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. *Nút Đặt Alpha* cho thêm một kênh alpha vào một hình ảnh. Lượng Alpha có thể đặt cho toàn bộ hình ảnh bằng cách sử dụng trường đầu vào (input field) hoặc bằng mỗi điểm ảnh (pixel) bằng cách kết nối vào ổ cắm. Đây không phải là, và không nhằm mục đích trở thành một giải pháp toàn diện cho vấn đề tổng hợp một hình ảnh không chứa thông tin Alpha. Bạn có thể nên sử dụng phương pháp "Khóa Lọc Màu" (Chroma Keying) hoặc "Khóa Chênh Lệch" (Difference Keying) (như đã được bàn luận ở chỗ khác của bảng hướng dẫn sử dụng) nếu có thể. Nút này thường được sử dụng (với đầu vào thích hợp được cung cấp qua phương tiện ổ cắm) trong những trường hợp rắc rối khi bạn *không thể*, do một số lý do nào đó, sử dụng trực tiếp các kỹ thuật đó. Nút này không có tính chất nào cả. Để giới thiệu hoạt hình của mình, bạn nên trình bày tiêu đề của đoạn hoạt hình của bạn trên một cái nền. Bạn có thể để tiêu đề bay vào, hoặc bạn có thể làm nó rõ dần lên. Để làm rõ dần lên, bạn hãy sử dụng nút Đặt Alpha với nút Thời Gian (Time) như trình bày dưới đây. Để chuyển đối tượng từ cảnh này sang cảnh khác, một kỹ thuật phổ biến thường dùng là "chuyển mờ dần sang màu đen" (fade to black). Đúng như tên gọi của nó, khung cảnh sẽ mờ dần sang một màn hình đen. Bạn cũng có thể "chuyển mờ dần sang màu trắng" (fade to white), hoặc bất kỳ màu nào bạn muốn, nhưng màu đen là màu trung tính tốt, dễ nhìn và về giác quan mà nói, nó "hoàn lại" trí giác của người xem. Sơ đồ bài trí nút dưới đây cho thấy cách thực hiện việc này bằng nút Đặt Alpha. Sử dụng Đặt Alpha để tô màu một hình ảnh. Dùng Đặt Alpha để làm mờ dần một tiêu đề vào 