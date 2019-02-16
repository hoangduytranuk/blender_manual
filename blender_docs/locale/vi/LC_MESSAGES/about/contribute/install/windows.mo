��          �               �  0   �  w     O   �  Q   �  �   (  �   �  L   5  U   �  L   �  >   %  j   d  L   �  �     n   �  )  9     c     ~  -   �  �   �     b	  T   y	      �	  L   �	  '   <
  A   d
  0   �
  #   �
  �  �
  X   �  �     ^   �  j     �   �  �   :  ~     �   �  f   X  a   �  �   !  �   �  /  b  �   �  �  @  :   �  '   &  c   N  �   �  @   �     �  M   Z  �   �  3   ,  �   `  f   �  O   I   All other settings can remain as set by default. Click *OK* -- the repository will now be downloaded which may take a few minutes depending on your internet connection. Continue with the next step: :doc:`Building </about/contribute/build/windows>`. Download `TortoiseSVN <https://tortoisesvn.net/downloads.html>`__ for MS-Windows. Download the `Python installation package <https://www.python.org/downloads/>`__ for MS-Windows. In this guide version 3.6.x is used. During the setup, some warnings may be shown, but do not worry about them. However, if any errors occur, they may cause some problems. Enter the ``blender_docs`` folder which was just added by the SVN checkout:: Every now and then you may want to make sure your dependencies are up to date using:: If all goes well, you should see the following message when it is finished:: In the *Checkout directory* field, enter: ``C:\blender_docs``. In the *URL of repository* field, enter: ``https://svn.blender.org/svnroot/bf-manual/trunk/blender_docs``. In this guide, we will use TortoiseSVN though any Subversion client will do. Inside that folder is a file called ``requirements.txt`` which contains a list of all the dependencies we need. Install all the dependencies using Python's ``pip`` command:: Install Python with the installation wizard. Please make sure that you enable the "Add Python to PATH" option: Install TortoiseSVN with the installation wizard. When choosing which features will be installed, it is recommended that you enable *command line client tools* to give you access to SVN from the command line (there is no harm in doing this, and it may be helpful if you ever run into any trouble). Installation on MS-Windows Installing Python Installing SVN and Downloading the Repository Once the installation has finished, create a new folder that will contain everything related to the Blender Manual. In this guide, we will use ``C:\blender_docs``. Open a Command Prompt. Open the new folder, right-click and choose *SVN Checkout...* from the context menu. Setting up the Build Environment The option must be enabled so you can build the manual with the make script. This guide covers the following topics: `Installing Python`_ (used to "convert" the source files to HTML) `Installing SVN and Downloading the Repository`_ `Setting up the Build Environment`_ Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-05 00:17+0000
PO-Revision-Date: 2018-12-05 02:12+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Tất cả các cài đặt khác có thể vẫn để như sắp đặt mặc định. Nhấp vào *OK* - kho lưu trữ hiện sẽ được tải xuống, có thể mất vài phút, tùy thuộc vào chất lượng đường kết nối Internet của bạn. Tiếp tục với bước tiếp theo: :doc:`Biên Dịch </about/contribute/build/windows>`. Tải xuống máy bản `TortoiseSVN <https://tortoisesvn.net/downloads.html>`__ -- dành cho MS-Windows. Tải xuống máy `Gói cài đặt Python <https://www.python.org/downloads/>`__ -- dành cho MS-Windows. Trong hướng dẫn này phiên bản 3.6.x sẽ được sử dụng. Trong khi thiết lập, một số cảnh báo có thể xuất hiện, nhưng đừng lo lắng về chúng. Đương nhiên, nếu có bất kỳ lỗi nào xảy ra, chúng có thể gây ra một số rắc rối. Bước vào thư mục ``blender_docs`` vừa được kiến tạo và bổ sung bởi việc kiểm xuất (checkout) SVN:: Thỉnh thoảng, bạn có thể muốn đảm bảo là các thư viện phụ thuộc của bạn được cập nhật với những thay đổi gần đây nhất, bằng cách sử dụng:: Nếu mọi việc xảy ra trôi chảy thì bạn sẽ thấy thông báo sau khi nó hoàn thành:: Trong ô *Thư mục kiểm xuất -- Checkout directory*, làm ơn điền: ``C:\blender_docs``. Trong ô *Địa chỉ của kho lưu trữ - URL of repository*, làm ơn điền: ``https://svn.blender.org/svnroot/bf-manual/trunk/blender_docs``. Trong hướng dẫn này, chúng tôi sẽ sử dụng TortoiseSVN, mặc dù bất kỳ trình khách ứng dụng Subversion nào cũng có thể sử dụng được. Bên trong thư mục đó có một tập tin với cái tên ``requirements.txt``, và trong đó có chứa một danh sách tất cả các phần mềm phụ thuộc mà chúng ta cần phải có. Để cài đặt các phụ thuộc này, chúng ta có thể sử dụng lệnh ``pip`` như sau:: Cài đặt Python bằng trình hướng dẫn cài đặt. Xin vui lòng đảm bảo rằng bạn đã bật tùy chọn ``Thêm Python vào PATH -- Add Python to PATH``: Cài đặt TortoiseSVN bằng trình hướng dẫn cài đặt. Khi chọn các tính năng sẽ được cài đặt, bạn nên cho bật *công cụ trình khách dòng lệnh -- command line client tools* để cho phép mình truy cập vào SVN từ dòng lệnh (thực hiện việc này không có gì hại cả, và ngược lại, có thể rất hữu ích nếu bạn gặp phải bất kỳ rắc rối nào). Cài đặt trên MS-Windows -- Installation on MS-Windows Cài Đặt Python -- Installing Python Cài Đặt SVN và Tải về Máy Kho Lưu Trữ -- Installing SVN and Downloading the Repository Sau khi cài đặt xong, hãy tạo một thư mục mới để chứa tất cả mọi thứ liên quan đến Bản Hướng Dẫn Sử Dụng Blender. Trong hướng dẫn này, chúng ta sẽ sử dụng ``C:\blender_docs``. Mở một Cửa Sổ Bàn Giao Tiếp -- Open a Command Prompt. Mở thư mục mới, nhấp chuột phải và chọn *SVN Checkout ... -- Kiểm Xuất SVN* từ trình đơn ngữ cảnh. Thiết Lập Môi Trường Biên Dịch -- Setting up the Build Environment Tùy chọn phải được bật để bạn có thể biên dịch bản hướng dẫn sử dụng bằng tập lệnh ``make``. Hướng dẫn này bao gồm các chủ đề sau: `Cài đặt Python -- Installing Python`_ (được sử dụng để "chuyển đổi" các tập tin nguồn sang dạng HTML) `Cài Đặt SVN và Tải Kho Lưu Trữ về Máy -- Installing SVN and Downloading the Repository`_ `Thiết Lập Môi Trường Biên Tập -- Setting up the Build Environment`_ 