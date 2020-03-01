��          �               �  j   �  9   H     �     �  �  �  g   v     �     �  
   �       �     �   �     �  p  �     P  r   \  9   �  �   		  ;   �	  E   
  6   [
  �   �
  �   !  �  �  $   y  7   �  �   �  �  �  �   q  �   ]  3   �  2     �  L  �   �     �      �     �     �  �    >  �  H   �  �  (  #     �   2  p     Z  �  �   �  }   m  {   �  �   g     V!  �  i"  A   L%  f   �%  �  �%   A happy feeling -- you guessed it -- add yellow (equal parts red and green, no blue) for bright and sunny. A startling event may be sharpened and contrast-enhanced. An example of a composition. An example of color correction. Compositing Nodes allow you to assemble and enhance an image (or movie). Using composition nodes, you can glue two pieces of footage together and colorize the whole sequence all at once. You can enhance the colors of a single image or an entire movie clip in a static manner or in a dynamic way that changes over time (as the clip progresses). In this way, you use composition nodes to both assemble video clips together and enhance them. Dust and airborne dirt are often added as a cloud texture over the image to give a little more realism. Examples Getting Started Image Size Introduction It is recommended to pay attention to image resolution and color depth when mixing and matching images. Aliasing (rough edges), color *flatness*, or distorted images can all be traced to mixing inappropriate resolutions and color depths. Raw footage from a foreground actor in front of a blue screen, or a rendered object doing something, can be layered on top of a background. Composite both together, and you have composited footage. Saving your Composite Image So each node in a composite can operate on different sized images as defined by its inputs. Only the *Composite* output node has a fixed size, as defined by the settings in Properties Editor :menuselection:`Render --> Dimensions`. The *Viewer* node always shows the size from its input, but when not linked (or linked to a value) it shows a small 320×256 pixel image. Term: Image The composite is centered by default, unless a translation has been assigned to a buffer using a *Translate* node. The first/top Image input socket defines the output size. The term *Image* may refer to a single picture, a picture in a numbered sequence of images, or a frame of a movie clip. The Compositor processes one image at a time, no matter what kind of input you provide. To convey a flashback or memory, the image may be softened. To convey hatred and frustration, add a red tinge or enhance the red. To make an image 'feel' colder, a blue tinge is added. To process your image, you use nodes to import the image into Blender, change it, optionally merge it with other images, and finally, save it. To save a composition as a movie clip (all frames in a single file), use an ``AVI`` or ``Quicktime`` format, and use the *Animation* button and its settings. To save a sequence of images, for example, if you input a movie clip or used a Time node with each frame in its own file, use the *Animation* button and its settings. If you might want to later overlay them, be sure to use an image format that supports an Alpha channel (such as ``PNG``). If you might want to later arrange them front to back or create a depth of field effect, use a format that supports a Z-depth channel (such as ``EXR``). You can change the mood of an image: You can do just about anything with images using nodes. You now have your first node setup, from here you can add and connect many types of :doc:`Compositing Nodes </compositing/index>`, in a sort of map layout, to your heart's content (or physical memory constraints, whichever comes first). Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-11-04 02:53+0000
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Một cảm giác vui vẻ - chắc bạn đoán được rồi - thì thêm màu vàng vào (cho lượng màu đỏ và màu xanh lá cây non bằng nhau, không có màu lam vào) để làm sáng lên và tràn đầy ánh nắng. Một sự kiện đáng kinh ngạc có thể được tăng cường độ rõ nét và độ tương phản lên (để nêu bật). Một ví dụ về một quá trình tổng hợp. Một ví dụ về sự chỉnh sửa màu sắc. Sự Tổng Hợp các Nút cho phép bạn lắp ráp và nâng cấp hình ảnh (hoặc phim). Bằng việc sử dụng sự tổng hợp các nút, bạn có thể nối hai đoạn phim lại với nhau và tô màu toàn bộ chuỗi phim cùng một lúc. Bạn có thể tăng cường màu sắc của một hình ảnh đơn lẻ hoặc toàn bộ một đoạn phim theo cách xử lý cố định, hoặc theo phương pháp năng động, thay đổi theo thời gian (theo sự tiến triển của đoạn phim). Bằng cách này, bạn sử dụng sự tổng hợp các nút để vừa lắp ráp các đoạn video lại với nhau, vừa nâng cấp chúng lên. Bụi bẩn và bụi bay trong không khí thường được thêm vào như một chất liệu mây mù che phủ hình ảnh để tạo cảm quan chân thực hơn. Ví Dụ -- Examples Khởi Đầu -- Getting Started Khổ Ảnh -- Image Size Giới Thiệu -- Introduction Bạn nên chú ý đến độ phân giải hình ảnh và độ sâu màu (*color depth*) khi pha trộn và ghép các hình ảnh với nhau. Sự gai góc (các cạnh thô thiển), màu sắc *nhạt nhẽo* (*flatness*) hoặc hình ảnh bị méo mó đều có thể lần rò ra được nguyên nhân là do độ phân giải và độ sâu màu khi pha trộn không phù hợp. Đoạn phim thô về một diễn viên nằm ở đằng trước màn hình màu xanh lam, hoặc một đối tượng được kết xuất đang làm gì đó, đều có thể được chồng tầng (*layered*) trên nền. Tổng hợp cả hai lại với nhau và bạn có một đoạn phim tổng hợp. Lưu Hình Ảnh Tổng Hợp của bạn -- Saving your Composite Image Vì vậy, mỗi nút trong một tổng hợp có thể hoạt động trên các hình ảnh có kích thước khác nhau như được xác định bởi các nguồn đầu vào của nó. Chỉ nút đầu ra của *Tổng Hợp* (Composite) là có kích thước cố định, như được xác định bởi các thiết lập trong Trình Biên Soạn Tính Chất :menuselection:`Kết Xuất (Render) --> Kích Thước (Dimensions)`. Nút *Xem Hình* (Viewer) luôn luôn hiển thị kích thước từ nguồn đầu vào của nó, nhưng khi không được kết nối (hoặc được liên kết với một giá trị nào đó), nó sẽ hiển thị một hình ảnh nhỏ với cỡ 320×256 điểm ảnh (pixel). Thuật Ngữ: Hình Ảnh -- Image Bản tổng hợp sẽ được đặt ở trung tâm (*centered*) theo mặc định, trừ khi có một sự dịch chuyển nào đó đã được gán cho bộ đệm (*buffer*) bằng nút *Dịch Chuyển* (Translate). Ổ cắm đầu vào của Hình ảnh đầu tiên/trên cùng sẽ xác định kích thước ở đầu ra. Thuật ngữ *Hình Ảnh* có thể ám chỉ đơn cử một hình ảnh, một hình ảnh trong một trình tự của nhiều hình ảnh, hoặc một khung hình của một đoạn phim. Trình Tổng Hợp -- `Compositor` -- sẽ xử lý lần lượt từng hình ảnh một, bất kể loại đầu vào bạn cung cấp là gì. Để truyền tải một hồi tưởng hoặc một kỷ niệm, hình ảnh có thể được làm nhòe đi một cách mềm mại. Để truyền đạt lòng hận thù và sự khó chịu, hãy cho thêm màu đỏ hoặc tăng cường màu đỏ lên. Để làm cho hình ảnh có 'cảm giác' lạnh hơn, một chuyển sắc màu xanh lam có thể được thêm vào. Để xử lý hình ảnh của bạn, bạn phải sử dụng các nút để nhập hình ảnh vào Blender, thay đổi nó, ngoài ra còn tùy thích hợp nhất nó với các hình ảnh khác, và cuối cùng, lưu nó lại. Để lưu một tổng hợp thành một đoạn phim (movie clip) (tất cả các khung hình nằm trong một tập tin), thì xin sử dụng định dạng ``AVI`` hoặc ``Quicktime``, và sử dụng nút *Hoạt Họa* (Animation) và các sắp đặt của nó. Để lưu một trình tự hình ảnh, ví dụ: nếu bạn nhập một đoạn phim (movie clip) hoặc sử dụng nút Thời Gian (Time node) với mỗi khung hình trong tập tin riêng của nó, thì hãy sử dụng nút *Hoạt Họa* (Animation) và các cài đặt của nó. Nếu như sau này bạn muốn phủ chồng (overlay) lên chúng, thì nên nhớ sử dụng định dạng hình ảnh nào có hỗ trợ kênh Alpha (chẳng hạn như ``PNG``). Nếu như sau này bạn muốn sắp xếp chúng từ trước đến sau hoặc muốn tạo độ sâu trường ảnh, thì hãy sử dụng định dạng hỗ trợ kênh chiều sâu Z (Z-depth channel) (chẳng hạn như định dạng ``EXR``). Bạn có thể thay đổi tâm trạng của một hình ảnh: Bạn có thể làm bất cứ điều gì với các hình ảnh bằng cách sử dụng các nút. Bây giờ bạn đã thiết lập nút đầu tiên. Từ đây, bạn có thể cho thêm và kết nối nhiều loại :doc:`Các Nút Tổng Hợp -- Compositing Nodes </compositing/index>`, trong cách bố trí giống như bản đồ, cho đến khi mãn nguyện thì thôi (hoặc cho đến điểm tới hạn của bộ nhớ, cái nào xảy ra trước còn tùy hoàn cảnh). 