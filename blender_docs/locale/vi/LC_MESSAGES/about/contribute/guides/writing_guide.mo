��    6      �              |  .   }  ^   �  0     2   <  j   o  f   �  B   A     �  �   �  �   2  i     )   �  i   �       C   �  o   �  �   K	  I   �	  O   
  �   j
       �        	       9   $  {   ^     �  a   �     E  h   N  �   �  >   W  �   �  �   �  c   g     �     �     �  )   �  D      �   e  T        m  �   z       F     d   a  �   �     Q  @   ^  7   �  P   �     (  �  <  8   �  �   #  S   �  @     �   T  �   '  �   �  >   S     �  z  �  �     1   �  �       �  s   �  �   N   �   '!  o   �!  �   d"  %  #     <$  �  U$     �%  4   &  \   6&    �&     �'  �   �'      c(  �   �(  �   D)  {   &*  �  �*  q  ),  �   �-  '   .  )   D.     n.  M   �.  j   �.  :  D/  |   0     �0  �   	1     �1  l   �1  �   g2    3  9   .5  [   h5  a   �5  c   &6  =   �6   "Blender has 23 different kinds of modifiers." "Enabling previews adds 65536 bytes to the size of each blend-file (unless it is compressed)." "Most people do not use this option because ..." "Reloading the file will probably fix the problem" As a last resort you can add comment (which is not shown in the HTML page, but useful for other editors):: Avoid `weasel words <https://en.wikipedia.org/wiki/Weasel_word>`__ and being unnecessarily vague, e.g: Avoid adding terms not found in Blender's interface or the manual. Avoid documenting bugs. Avoid documenting changes in Blender between releases, that is what the release notes are for. We only need to document the current state of Blender. Avoid duplicating documentation; if explaining the term is the primary focus of another section of the manual (e.g. if the term is the name of a tool), either just link to that section, or avoid creating a glossary entry entirely. Avoid enumerations of similar options, such as listing every preset or every frame rate in a select menu. Avoid including specific details such as: Avoid overly long entries. If an explanation of a complex term is needed, supplement with external links. Avoid product placements, i.e. unnecessarily promoting software or hardware brands. Keep content vendor-neutral where possible. Avoid repeating the term immediately or using it in the definition. Avoid repetition of large portions of text. Simply explain it once, and from then on refer to that explanation. Avoid technical explanations about the mathematical/algorithmic implementation of a feature if there is a simpler way to explain it. Avoid using constructs such as "it is" or "xyz is" before the definition. Avoid writing in first person perspective, about yourself or your own opinions. Blender often has 100's of bugs fixed between releases, so it is not realistic to reference even a fraction of them from the manual, while keeping this list up to date. Complete Computer graphics is an incredibly interesting field, there are many rules, exceptions to the rules and interesting details. Expanding into details can add unnecessary content, so keep the text concise and relevant to the topic at hand. Concise Content Guidelines Define the term before providing any further information. Do not simply copy the tooltips from Blender. -- People will come to the manual to learn *more* than is provided by the UI. Examples For general terminology, consider defining a ``:term:`` in the :doc:`glossary </glossary/index>`. Glossary If you are unsure about how a feature works, ask someone else or find out who developed it and ask them. In order to maintain a consistent writing style within the manual, please keep this page in mind and only deviate from it when you have a good reason to do so. Including why or how an option might be useful is a good idea. Issues which are known to the developers and are not going to be resolved before the next release can be documented as *Known Limitations*. In some cases, it may be best to include them in the :doc:`troubleshooting </troubleshooting/index>` section. Keep in mind that Blender has frequent releases, so try to write content that will not have to be redone the moment some small change is made. This also helps a small documentation community to maintain the manual. Keep sentences short and clear, resulting in text that is easy to read, objective and to the point. Maintainable Primary Goals Rules of thumb: Spell checking is *strongly* recommended. Take care about grammar, appropriate wording and use simple English. Their contents may be summarized or simply omitted. -- Such lists are only showing what is already *obvious* in the interface and end up being a lot of text to read and maintain. These details are not useful for users to memorize and they become quickly outdated. This entry:: This section is specifically about the :doc:`Glossary </glossary/index>` section, where we define common terms in Blender and computer graphics. To be avoided: URL references are to be added at the end, formatted as follows, e.g:: Unless the unit a value is measured in is obscure and unpredictable, there is no need to mention it. Use American English (e.g: modeling and not modelling, color and not colour) also for formatting numbers (e.g: 2,718.28 and not 2 718,28). User Focused Would be written like this instead, putting a definition first:: Would be written more like this, avoiding the "it is":: Would be written more like this, avoiding the immediate repetition of the term:: Writing Style Guide Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-03-06 22:21-0500
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 "Blender có 23 loại bộ điều chỉnh khác nhau." "Việc bật tính năng duyệt thảo sẽ làm tăng thêm 65536 bytes vào kích cỡ của mỗi tập tin blend (trừ phi nó được nén lại)" "Đại đa số người dùng không sử dụng tùy chọn này, bởi vì ..." "Tái nạp tập tin CÓ THỂ sẽ sửa được lỗi lầm" Việc cho thêm nhận xét sẽ chỉ nên sử dụng là phương sách cuối cùng mà thôi (cái này không được hiển thị trong trang HTML, song có lợi cho các trình soạn thảo khác):: Tránh các `lời nói lấp lửng -- weasel words <https://en.wikipedia.org/wiki/Weasel_word>`__ -- và tạo cảm giác mơ hồ không cần thiết, ví dụ: Tránh việc cho thêm các thuật ngữ không có trong giao diện của Blender, hoặc trong bản hướng dẫn sử dụng. Tránh việc viết về các lỗi lầm trong phần mềm. Tránh việc ghi lại những thay đổi trong Blender giữa các bản phát hành, bản thông báo về phát hành đã được sử dụng cho mục đích này. Chúng ta chỉ cần ghi lại trạng thái hiện tại của Blender mà thôi. Tránh việc sao chép tài liệu; Nếu việc giải thích cụm từ này là trọng tâm chính của một phần khác trong bản hướng dẫn sử dụng (ví dụ: nếu cụm từ là tên của một công cụ), thì bạn chỉ nên liên kết đến phần đó mà thôi, và nên tuyệt đối tránh việc tự tạo ra một chú giải thuật ngữ. Tránh liệt kê các tùy chọn tương tự, chẳng hạn như liệt kê mọi giá trị đặt trước, hoặc mọi tốc độ khung hình, trong một trình đơn đã chọn nào đó. Tránh bao gồm các chi tiết cụ thể như: Tránh việc kéo dài các mục quá mức. Nếu việc giải thích một thuật ngữ phức tạp là cần thiết thì hãy bổ sung bằng các liên kết ra các nguồn ở bên ngoài. Tránh việc đề cập đến các sản phẩm, tức là quảng bá phần mềm hoặc thương hiệu phần cứng không cần thiết. Cố gắng giữ góc nhìn khách quan, trung lập đối với các nhà cung cấp sản phẩm, nếu có thể. Tránh việc lặp lại thuật ngữ ngay lập tức, hoặc sử dụng chính từ đó trong định nghĩa. Tránh việc lặp đi, lặp lại các phần của văn bản. Chúng ta chỉ cần đơn giản giải thích nó một lần, rồi từ đó trở đi, tham chiếu đến phần giải thích đó là đủ. Tránh việc đi sâu và giải thích một cách máy móc về phương pháp thực hiện toán học/thuật toán một tính năng nào đó, trong khi có cách giải thích đơn giản hơn. Tránh sử dụng các cấu trúc như "nó là -- it is" hoặc "xyz là -- xyz is" trước định nghĩa. Tránh viết trong ngôi thứ nhất (chẳng hạn dùng chữ 'tôi') trong cuộc hội thoại, hoặc viết về bản thân, hoặc viết ý kiến của riêng mình. Giữa hai bản phát hành, Blender thường sẽ có chừng 100 lỗi được chỉnh sửa, vì vậy, đề cập đến nó trong bản hướng dẫn sử dụng không phải là một điều sát thực trong khi duy trì tính cập nhật của bản hướng dẫn sử dụng. Hoàn Thành -- Complete Đồ họa máy tính là một lĩnh vực vô cùng thú vị, có rất nhiều quy tắc, ngoại lệ đối với các quy tắc và các chi tiết hứng khởi. Việc đào sâu vào các chi tiết có thể dẫn đến việc cho thêm các nội dung không cần thiết, cho nên, hãy cố gắng giữ cho văn bản ngắn gọn và có thích hợp với chủ đề đang xử lý. Ngắn Gọn -- Concise Hướng Dẫn về Nội Dung -- Content Guidelines Định nghĩa thuật ngữ đã, trước khi cung cấp thêm bất kỳ thông tin nào. Đừng chỉ đơn giản sao chép các chú giải công cụ từ Blender. -- Mọi người cần phải tìm đến bản hướng dẫn sử dụng để tìm hiểu *nhiều/lớn hơn -- more*, thay vì những gì đã được cung cấp trên giao diện người dùng. Ví Dụ -- Examples Đối với thuật ngữ nói chung, hãy định nghĩa các ``:term:`` (từ chuyên môn) trong :doc:`bảng thuật ngữ -- glossary </glossary/index>`. Bảng Thuật Ngữ -- Glossary Nếu bạn không chắc chắn về sự hoạt động của một tính năng thì xin hãy hỏi người khác, hoặc lùng tìm người đã phát triển tính năng và hỏi họ. Để duy trì phong cách viết nhất quán trong bản hướng dẫn sử dụng, xin vui lòng ghi nhớ hướng dẫn trong trang này và chỉ làm khác đi khi bạn có lý do chính đáng để làm như vậy. Nhớ cho biết lý do tại sao, hoặc làm thế nào, một tùy chọn trở nên hữu ích là một điều tốt. Các vấn đề được các nhà phát triển biết đến, song, không được giải quyết trước khi bản phát hành tiếp theo, có thể được ghi thành ``Những Hạn Chế Từng Biết Đến -- Known Limitations``. Trong một số trường hợp, tốt nhất nên đưa chúng vào phần :doc:`xử lý sự cố -- troubleshooting </troubleshooting/index>`. Hãy nhớ rằng Blender sẽ phát hành các phiên bản khá thường xuyên, vì vậy hãy cố gắng viết làm sao cho nội dung không phải làm lại từ thời điểm những thay đổi nhỏ được thực hiện. Điều này cũng giúp cho cộng đồng nhỏ quản lý bản tài liệu duy trì bản hướng dẫn sử dụng dễ dàng. Giữ cho các câu ngắn gọn và rõ ràng, dẫn đến văn bản sẽ dễ đọc, khách quan và sát vào vấn đề. Bảo Quản Dễ Dàng -- Maintainable Mục Đích Chủ Yếu -- Primary Goals Quy Luật Thông Thường: Kiểm tra chính tả là điều phải *hết sức -- strongly* để ý. Hãy quan tâm đến ngữ pháp, dùng từ ngữ thích hợp và sử dụng tiếng Anh đơn giản. Nội dung của chúng có thể được tóm tắt lại, hoặc đơn giản là bỏ qua. -- Những danh sách như vậy chỉ hiển thị những gì vốn dĩ đã *hiển nhiên -- obvious* trong giao diện mà thôi và để lại một lượng lớn văn bản cần phải đọc và bảo quản. Những chi tiết này không hữu ích cho người dùng ghi nhớ và chúng sẽ nhanh chóng trở nên lỗi thời. Mục này:: Phần này sẽ đặc chuyên về :doc:`Bảng Thuật Ngữ -- Glossary </glossary/index>`, tức là bản trong đó chúng ta định nghĩa các từ chuyên môn thông dụng trong Blender và trong đồ họa máy tính. Tránh: Tham chiếu URL phải được cho thêm ở phần cuối, với định dạng như sau đây, ví dụ: Trừ khi đơn vị một giá trị nào đó đã được đo lường, song tối nghĩa và bất định, chúng ta không cần phải đề cập đến nó. Sử dụng tiếng Anh Mỹ (ví dụ sự khác biệt về cách đánh vần: ``modeling`` (mô hình hóa) chứ không dùng ``modelling`` (hai chữ ``l``), và dùng ``color`` (màu sắc) chứ không dùng ``colour`` (có thêm chữ 'u')), đồng thời, định dạng hình thức của các con số (chẳng hạn: 2,718.28 mà không dùng 2 718,28, dùng dấu phẩy để tách phân phần nghìn chứ không dùng dấu cách trống, dấu chấm để tách phân phần thập phân, chứ không dùng dấu chấm). Hướng Trọng Tâm vào Người Dùng -- User Focused Thay vào đó, sẽ nên được viết như thế này, đặt định nghĩa trước:: Sẽ được viết giống như thế này hơn, tránh việc sử dụng "nó là -- it is":: Sẽ được viết như thế này hơn, tránh sự lặp lại thuật ngữ ngay lập tức:: Hướng Dẫn về Phong Cách Viết -- Writing Style Guide 