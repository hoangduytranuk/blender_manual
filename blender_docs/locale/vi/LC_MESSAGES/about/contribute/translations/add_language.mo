��    !      $              ,     -  l   ?  v   �  @   #  >   d     �  �   �  ?   a  ,   �  O   �       >   4  T   s  3   �  �   �  �  �  �     �   �  {   �	  M   K
     �
  \   �
  $     3   (  ^   \  J  �  0     3   7  7   k  L   �  H   �  c   9  �  �  2   U  �   �  �   (  F   �  Z   �     U  �   u  >   I  j   �  w   �     k  N   �  Y   �  m   2  �   �    G  �   K  ?  +  �   k  o        x  l   �  N     @   Q  p   �  �    U   �  I   �  �   G  q   �  o   N   �   �    Adding a Language Bring your local repository up to the most recent version of changes, including the one you have just done:: Change the current working directory to the directory of ``blender_docs``, where the instance of ``Makefile`` resides. Check out the current translation repository using the command:: Convert all the ``rst`` files into ``pot`` translation files:: Create ``html`` files:: Create an entry for the language in the html menu by opening file ``./resources/theme/js/version_switch.js`` (assuming you are at the ``blender_docs`` subdirectory). Creating a new set of translation language from English source. Creating the Language Entry in the HTML Menu Ensure the previous instance of ``build`` directory is removed, if any exists:: Enter your password:: Find the table for the languages in ``var all_langs = {..};``. From the ``blender_docs`` directory to generate a set of files for ``fr`` language:: Generating the Set of Files for the Target Language Goto ``https://developer.blender.org`` to create an account for yourself and become a developer/translator for the Blender organization. If the language you want to translate has not been started by someone else already and you wish to create a set of new files for the desired language, say 'fr' (French), then you must first use the environment you have created, as guided in :ref:`Getting Started <about-getting-started>`, in particular :doc:`/about/contribute/install/index` and :doc:`/about/contribute/build/index` sections. It is recommended you make two environment variables for these directories, in the ``.bashrc`` to make it more convenient for changing or scripting batch/shell commands for the process of translation and reviewing results:: Login the account and create a task with ``todo`` type, addressing an administrator in the *Subscribers* field, requesting for a committer right in order to transfer changes to the central repository of the translation team. Open a text editor to enter the following texts, change the language code to whatever the language you will be translating: Open an instance of the console application, such as Gnome-Terminal emulator. Preparations Save this file as ``conf.py`` in the ``blender_docs`` directory, where ``Makefile`` resides. Setting the Local Configuration File Submit new set of files to the central repository:: Tells ``svn`` to ignore this file when performing operations by executing this shell command:: This will download all language sets available in the repository into the ``locale`` directory of your drive. You can go to the ``locale`` directory to see the hidden subdirectory ``.svn`` within it, together with directories of languages. You'll need to add your own set of files for the language you're trying to translating to. This will give you a foundation environment for: To find out about changes in the local repository:: Trying the Make Process to Create HTML Files In English Update changes in English texts which have been added by other contributors. We will download this new set of language as guided in the next section. You don't need all other languages being there, so remove the locale directory for the time being:: Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-27 20:49+1000
PO-Revision-Date: 2019-03-23 14:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Thêm Một Ngôn Ngữ Mới -- Adding a Language Nâng cấp kho lưu trữ cục bộ của bạn lên phiên bản thay đổi gần đây nhất, bao gồm cả thay đổi bạn vừa thực hiện xong:: Chuyển thư mục từ thư mục làm việc hiện tại vào thư mục ``blender_docs``, nơi có bản ``Makefile`` nằm ở đó. Xuất kho bản dịch hiện tại bằng cách sử dụng lệnh:: Chuyển đổi tất cả các tập tin ``rst`` thành tập tin phiên dịch ``pot``:: Tạo các tập tin ``html``:: Tạo một trình mục cho ngôn ngữ trong trình đơn ``html`` bằng cách mở tập tin ``./resources/theme/js/version_switch.js`` (giả định là bạn đang ở thư mục nhánh ``blender_docs``). Tạo một bộ phiên dịch mới từ nguồn tiếng Anh. Tạo Trình Mục cho Ngôn Ngữ trong Trình Đơn HTML -- Creating the Language Entry in the HTML Menu Hãy đảm bảo rằng cá thể trước đây của thư mục ``build`` được xóa đi, nếu nó tồn tại:: Điền mật mã của bạn Tìm bảng về các ngôn ngữ trong biến số ``var all_langs = {..};``. từ thư mục ``blender_docs`` để tạo bộ các tập tin cho ngôn ngữ ``fr``:: Sinh Tạo Bộ Tập Tin cho Ngôn Ngữ Dự Định -- Generating the Set of Files for the Target Language Vào trang ``https://developer.blender.org`` để tạo tài khoản cho chính bản thân và trở thành nhà phát triển/dịch giả cho tổ chức Blender. Nếu ngôn ngữ bạn muốn dịch chưa được bắt đầu bởi người khác và bạn muốn tạo một tập hợp các tập tin mới cho ngôn ngữ mong muốn, chẳng hạn 'fr' (tiếng Pháp), thì trước tiên bạn phải sử dụng môi trường bạn đã tạo, như được hướng dẫn trong bản :ref:`Bắt đầu -- Getting Started <about-getting-started>`, với cụ thể là các phần về :doc:`/about/contribute/install/index` và :doc:`/about/contribute/build/index`. It is recommended you make two environment variables for these directories, in the ``.bashrc`` to make it more convenient for changing or scripting batch/shell commands for the process of translation and reviewing results:: Đăng nhập vào tài khoản và tạo một tác vụ với thể loại ``todo``, liên lạc với một quản trị viên trong trường *Người đăng ký -- Subscribers*, xin có quyền nhập kho (committer right) để chuyển các thay đổi sang kho lưu trữ trung tâm của nhóm dịch thuật. Mở trình soạn thảo văn bản để nhập các văn bản sau, thay đổi mã ngôn ngữ thành mã ngôn ngữ nào mà bạn sẽ phiên dịch: Mở một cửa sổ dòng lệnh, chẳng hạn như trình giả lập Đầu Cuối Gnome (Gnome-Terminal). Chuẩn Bị -- Preparations Lưu tập tin này thành ``conf.py`` trong thư mục ``blender_docs``, nơi tập tin ``Makefile`` nằm. Tạo tập tin cấu hình cục bộ -- Setting the Local Configuration File Nhập kho bộ tập tin mới vào kho lưu trữ trung tâm:: Yêu cầu ``svn`` bỏ qua tập tin này khi thực hiện các thao tác bằng cách thi hành lệnh này:: Việc làm này sẽ tải tất cả các bộ ngôn ngữ có sẵn trong kho lưu trữ xuống thư mục ``locale`` của ổ đĩa của bạn. Bạn có thể vào thư mục ``locale`` để xem thư mục con ẩn ``.svn`` nằm bên trong đó cùng với các thư mục ngôn ngữ. Bạn sẽ cần cho thêm tập hợp tập tin của riêng mình cho ngôn ngữ bạn đang định phiên dịch sang. Việc làm này sẽ cung cấp cho bạn một môi trường cơ bản cho việc: Để tìm xem những thay đổi trong kho lưu trữ địa phương:: Thử Nghiệm Quá Trình Biên Dịch để Tạo các Tập Tin HTML trong Tiếng Anh -- Trying the Make Process to Create HTML Files In English Cập nhật các thay đổi trong văn bản tiếng Anh đã được các cộng tác viên khác thêm vào. Chúng ta sẽ tải xuống bộ ngôn ngữ mới này như được hướng dẫn trong phần tiếp theo. Bạn không cần tất cả các ngôn ngữ khác nằm ở đó, vì vậy hãy tạm thời xóa thư mục ``locale`` đi:: 