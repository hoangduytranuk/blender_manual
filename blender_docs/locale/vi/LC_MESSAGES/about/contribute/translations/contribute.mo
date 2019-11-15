��    "      ,              <     =  i   I  :  �     �  
   	       �   .  ?   �       
   1  t   <     �     �     �  ;   �  /   '  B   W    �     �  K   �  C     3   [  k   �  .   �  V   *	  �   �	  �   
     �
  �   �
  �   V     �  {     .   �  �  �  5   w  i   �  -    ;   E     �  F   �  �   �  t   �  .   L     {  �   �  l     ,   �     �  �   �  U   R  �   �  r  =  .   �  �   �  n   �  ^     �   p  >     �   Q  �   �  �   �  3   �  �   �    �  :   �    �  D   �   A PO Editor A guide how to add a new language can be found in the :doc:`/about/contribute/translations/add_language`. As the original manual changes, the templates will need updating. Note, doing this is not required, as administrator usually update the files for all languages at once. This allows all languages to be on the same version of the manual. However, if you need to update the files yourself, it can be done as follows:: Building with Translations Contribute Editing Translation Files First of all, it is assumed that you have the manual already building. If you have not done this already go back too the :ref:`Getting Started <about-getting-started>` section. From the directory containing your checkout of the manual run:: Generated PO File Installing Instructions on this page are based on `Sphinx Intl documentation <http://www.sphinx-doc.org/en/stable/intl.html>`__ Keeping Track of Fuzzy Strings Language Files Maintenance Now you can build the manual with the translation applied:: Now you can edit the PO translation files, e.g: Now you will have a build of the manual with translations applied. On this page French (``fr``) is used for examples. However, it can be replaced with other `languages codes <https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html>`__. So, be sure to change the ``/fr`` suffixes in this guide to the language you are translating! Original RST File Otherwise you will get a warning: ``'locale' is not under version control`` The modified ``.po`` files can be edited and committed back to svn. The updated templates can then be committed to svn. This is optional, translations are automatically built online, e.g: https://docs.blender.org/manual/fr/dev/ This will create a ``locale/fr`` subdirectory. This will only give a quick summary however, you can get more information by running:: To make edit the PO files you will need to install a PO editor. We recommended that you use `Poedit <https://poedit.net/>`__ however, any PO editor will do. To see which languages are currently available, you can browse the repository: https://developer.blender.org/diffusion/BMT/browse/trunk/blender_docs/locale Updating PO Files When running subversion from the command line (such as updating or committing), you will need to change directory to ``locale/fr`` first. When the manual is updated, those translations which are outdated will be marked as fuzzy. To keep track with that, you can use a tool we created for that task. You can do this by running:: You should get a list of all the files with information about the number of empty and fuzzy strings. For more options see:: You should have a directory layout like this:: Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-18 15:55-0400
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Trình Soạn Thảo Định Dạng PO -- A PO Editor A guide how to add a new language can be found in the :doc:`/about/contribute/translations/add_language`. Khi các bản hướng dẫn sử dụng gốc thay đổi, các bản mẫu cũng sẽ cần phải được cập nhật. Lưu ý, điều này không cần thiết, vì quản trị viên thường cập nhật các tập tin cho tất cả các ngôn ngữ cùng một lúc. Việc này cho phép tất cả các ngôn ngữ được tồn tại trên cùng một phiên bản của bản hướng dẫn sử dụng. Đương nhiên, nếu bạn cần phải tự cập nhật các tập tin thì việc đó có thể được thực hiện như sau:: Biên Tập các Bản Dịch -- Building with Translations Đóng Góp -- Contribute Biên Soạn các Tập Tin Phiên Dịch -- Editing Translation Files Trước hết, chúng tôi giả định là bạn đã biên tập và kiến dựng bản hướng dẫn rồi. Nếu bạn chưa làm điều này, thì hãy quay lại phần :ref:`Khởi Đầu -- Getting Started <about-getting-started>`. Từ thư mục có chứa phiên bản trích xuất của bạn về bản hướng dẫn sử dụng, thi hành:: Tập Tin РО Sinh Tạo -- Generated PO File Cài Đặt -- Installing Hướng dẫn trên trang này dựa trên bản `Tài Liệu về Sphinx Intl <http://www.sphinx-doc.org/en/stable/intl.html>`__ Theo Dõi các Đoạn Văn được Đánh Dấu là **Fuzzy : Mơ Hồ** -- Keeping Track of Fuzzy Strings Tập Tin về Ngôn Ngữ -- Language Files Bảo Quản -- Maintenance Bây giờ, bạn có thể xây dựng bản hướng dẫn sử dụng với phần phiên dịch được áp dụng vào đó:: Giờ đây, bạn có thể chỉnh sửa các tập tin phiên dịch PO, ví dụ: Bây giờ bạn sẽ có một bản xây dựng của hướng dẫn sử dụng trong máy, với các phần phiên dịch được lồng vào. Trên trang này, tiếng Pháp (``fr`` : French) được sử dụng làm các ví dụ. Đương nhiên, nó có thể được thay thế bằng các  `mã ngôn ngữ <https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html>`__ khác. Do đó, hãy đổi hậu tố ``/fr`` trong hướng dẫn này sang ngôn ngữ mà bạn đang dịch! Bản Tập Tin RST Gốc -- Original RST File Nếu không, bạn sẽ nhận được cảnh báo: ``'locale' is not under version control -- 'locale' chưa được đặt dưới sự quản lý về thay đổi trong các phiên bản`` Các tập tin ``.po`` đã soạn có thể được chỉnh sửa và chuyển giao trở lại nguồn svn. Các bản mẫu được cập nhật sau đó có thể được chuyển giao vào kho svn. Cái này chỉ là tùy chọn mà thôi, bản dịch sẽ được tự động kiến tạo trực tuyến, ví dụ: https://docs.blender.org/manual/fr/dev/ Việc này sẽ kiến tạo thư mục nhánh ``locale/fr``. Lệnh này sẽ chỉ cung cấp cho bạn một báo cáo vắn tắt mà thôi, dĩ nhiên, bạn có thể lấy thêm thông tin bằng cách thi hành:: Để chỉnh sửa các tập tin PO, bạn cần phải cài đặt Trình Soạn Thảo PO -- `PO editor`. Chúng tôi đề cử là bạn nên sử dụng `Poedit <https://poedit.net/>`__ song, bất kỳ trình soạn thảo PO nào cũng được. Để xem ngôn ngữ nào hiện đã có sẵn, bạn có thể duyệt qua kho lưu trữ: https://developer.blender.org/diffusion/BMT/browse/trunk/blender_docs/locale Cập Nhật các Tập Tin PO -- Updating PO Files Khi thi hành subversion trong dòng lệnh (chẳng hạn như cập nhật hoặc chuyển giao thay đổi), bạn cần phải chuyển sang thư mục ``locale/fr`` trước đã. Khi bản hướng dẫn sử dụng được cập nhật, những phiên dịch lỗi thời sẽ được đánh dấu là ``fuzzy`` (mờ ám). Để theo dõi cái này, bạn có thể sử dụng công cụ mà chúng tôi đã tạo cho nhiệm vụ đó. Bạn có thể làm điều này bằng cách thi hành:: Bạn sẽ nhận được một danh sách tất cả các tập tin với thông tin về số lượng các dòng trống rỗng (chưa phiên dịch) và các dòng được đánh dấu là ``fuzzy`` -- mờ ám. Để biết thêm các tùy chọn khác, hãy xem:: Bạn sẽ có một bố trí thư mục trông giống thế này: 