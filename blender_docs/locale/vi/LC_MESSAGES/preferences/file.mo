��    X      �              �     �  6   �  O   �     (     9     @     O  	   g     q  �   �  {  Q  �   �  �   e	    9
  Z   M     �      �  /   �  3     0   ;    l  j   t  �   �          �  
   �     �     �     �     �     �       ,     g   E  z   �     (  H   6       �   �     p     }  J   �  O   �  C      :   d  �   �  _   �     �     �                     ,     @     N     V     c     s     z     �     �     �  �   �  3   =  .   q  9   �  K   �  m   &  �   �    @  �   I  �         �  @   �  '   %  ^   M     �     �     �     �     �     �     �     �     �     �  4     �  6     �  6   �  O   )  +   y     �  (   �  E   �     )  J   6  �   �  {  G   �   �!  �   ["    /#  Z   C$     �$      �$  /   �$  3   %  0   C%    t%  j   |&  �   �&     �'     �'  '   �'     �'  6   �'     "(     2(  5   P(  <   �(  ,   �(  g   �(  z   X)     �)  H   �)  /   .*  �   ^*  +   B+     n+  J   �+  O   �+  C   &,  :   j,  �   �,  _   �-  *   �-  0   .     K.     \.     n.  6   }.  '   �.     �.     �.  )   �.     "/  (   6/     _/  -   h/     �/  �   �/  3   J0  .   ~0  9   �0  K   �0  m   31  �   �1    M2  �   V4  �   5     �5  @   6  '   B6  ^   j6     �6     �6     �6     �6     �6     �6     �6     7     7     7  4   7   ... :doc:`Python Security </advanced/scripting/security>`. An additional location to search for Python scripts. See `Scripts Path`_ below. Animation Player Author Auto Execution Auto Run Python Scripts Auto Save Auto Save Temporary Files Automatically loads the ``quit.blend`` file after re-starting Blender. This file is always saved on quit, regardless of this option. See :ref:`Recover Last Session <troubleshooting-file-recovery>`. Be sure that you have the right privileges for running the executable accessing the path defined. On MS-Windows for instance, if the option "Run this program as an administrator" is enabled for the executable, it will lead to a failure to open the editor due to a limitation within the OS User Account Control. Running a program with elevated privileges is potentially dangerous! Blend-files in these folders will *not* automatically run Python scripts. This can be used to define where blend-files from untrusted sources are kept. By activating this, the file region in the File Browser will only show appropriate files (i.e. blend-files when loading a complete Blender setting). The selection of file types may be changed in the file region. By default Blender looks in several directories (OS dependent) for scripts. By setting a user script path in the preferences an additional directory is looked in. This can be used to store certain scripts/templates/presets independently of the currently used Blender Version. By default, external files use a :doc:`relative path </data_system/files/relative_paths>`. Compress File Compress blend-file when saving. Default location when searching for font files. Default location when searching for image textures. Default location when searching for sound files. Default setting is to load the Window layout (the :doc:`Screens </interface/window_system/screens>`) of the saved file. This can be changed individually when loading a file from the *Open blend-file* panel of the :doc:`File Browser </editors/file_browser/index>`. Display a thumbnail of images and movies when using the :doc:`File Browser </editors/file_browser/index>`. Enables :doc:`Auto Save </troubleshooting/recover>`. Tells Blender to *automatically* save a backup copy of your work-in-progress files to the :ref:`temp-dir`. Excluded Paths File File Paths File extension filter. Filter File Extensions Fonts Hide Dot File/Data-blocks Hide Recent Locations Hide System Bookmarks Hide System Bookmarks in the *File Browser*. Hide file which start with ``.`` on file browsers (in Linux and Apple systems, ``.`` files are hidden). Hide the *Recent* panel of the :doc:`File Browser </editors/file_browser/index>` which displays recently accessed folders. I18n Branches If these folders do not exist, they will *not* be created automatically. Image Editor Inside the specified folder, specific subfolders have to be created to tell Blender what to look for where. This folder structure has to mirror the structure of the scripts folder found in the installation directory of Blender: Keep Session Load UI Locations for various external files can be set for the following options: Name that will be used in exported files when the format supports such feature. Number of files displayed in :menuselection:`File --> Open Recent`. Number of versions created for the same file (for backup). Previews of images and materials in the :doc:`File Browser </editors/file_browser/index>` are created on demand. To save these previews into your blend-file, enable this option (at the cost of increasing the size of your blend-file). Python scripts (including driver expressions) are not executed by default for security reasons. Recent Files Relative Paths Render Cache Render Output Save & Load Save Preview Images Save Versions Scripts Scripts Path Show Thumbnails Sounds Tabs as Spaces Temp Text Editor Textures The *File* tab in *User Preferences* allows you to configure auto-save preferences and set default file paths for blend-files, rendered images, and more. The location where cached render images are stored. The location where temporary files are stored. The path to an external program to use for image editing. The path to an external program to use for playback of rendered animations. The path to the ``/branches`` directory of your local svn-translation copy, to allow translating from the UI. This option may slow down Blender when you quit, or under normal operation when Blender is saving your backup files. Using this option traces processor time for file size. This option tells Blender to keep the indicated number of saved versions of your file in your current working directory when you manually save a file. These files will have the extension: ``.blend1``, ``.blend2``, etc., with the number increasing to the number of versions you specify. Older files will be named with a higher number. e.g. With the default setting of 2, you will have three versions of your file: ``*.blend`` (your last save), ``*.blend1`` (your second last save) and ``*.blend2`` (your third last save). This option will compact your files whenever Blender is saving them. Dense meshes, large packed textures or lots of elements in your scene will result in a large blend being created. This specifies the number of minutes to wait between each :doc:`Auto Save </troubleshooting/recover>`. The default value of the Blender installation is 2 minutes. The minimum is 1, and the Maximum is 60 (save every hour). Timer When hitting :kbd:`Tab` the tabs get written as keyboard spaces. Where rendered images/videos are saved. You may choose to ignore these security issues and allow scripts to be executed automatically. add-ons camera cloth interface_theme modules operator presets render scripts startup templates Not all of the folders have to be present. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 ... :doc:`Python Security </advanced/scripting/security>`. An additional location to search for Python scripts. See `Scripts Path`_ below. Máy Chơi Hoạt Họa -- Animation Player Tác Giả -- Author Thi Hành Tự Động -- Auto Execution Tự Động Thi hành Tập Lệnh Python -- Auto Run Python Scripts -- Auto Save Tự Động Lưu các Tập Tin Tạm Thời -- Auto Save Temporary Files Automatically loads the ``quit.blend`` file after re-starting Blender. This file is always saved on quit, regardless of this option. See :ref:`Recover Last Session <troubleshooting-file-recovery>`. Be sure that you have the right privileges for running the executable accessing the path defined. On MS-Windows for instance, if the option "Run this program as an administrator" is enabled for the executable, it will lead to a failure to open the editor due to a limitation within the OS User Account Control. Running a program with elevated privileges is potentially dangerous! Blend-files in these folders will *not* automatically run Python scripts. This can be used to define where blend-files from untrusted sources are kept. By activating this, the file region in the File Browser will only show appropriate files (i.e. blend-files when loading a complete Blender setting). The selection of file types may be changed in the file region. By default Blender looks in several directories (OS dependent) for scripts. By setting a user script path in the preferences an additional directory is looked in. This can be used to store certain scripts/templates/presets independently of the currently used Blender Version. By default, external files use a :doc:`relative path </data_system/files/relative_paths>`. Nén Tập Tin -- Compress File Compress blend-file when saving. Default location when searching for font files. Default location when searching for image textures. Default location when searching for sound files. Default setting is to load the Window layout (the :doc:`Screens </interface/window_system/screens>`) of the saved file. This can be changed individually when loading a file from the *Open blend-file* panel of the :doc:`File Browser </editors/file_browser/index>`. Display a thumbnail of images and movies when using the :doc:`File Browser </editors/file_browser/index>`. Enables :doc:`Auto Save </troubleshooting/recover>`. Tells Blender to *automatically* save a backup copy of your work-in-progress files to the :ref:`temp-dir`.  -- Excluded Paths Tập Tin -- File Đường Dẫn Tập Tin -- File Paths File extension filter. Thanh Lọc Đuôi Tập Tin -- Filter File Extensions Phông -- Fonts  -- Hide Dot File/Data-blocks Giấu Vị Trí Gần Đây -- Hide Recent Locations Giấu Ghi Nhớ của Hệ Thống -- Hide System Bookmarks Hide System Bookmarks in the *File Browser*. Hide file which start with ``.`` on file browsers (in Linux and Apple systems, ``.`` files are hidden). Hide the *Recent* panel of the :doc:`File Browser </editors/file_browser/index>` which displays recently accessed folders.  -- I18n Branches If these folders do not exist, they will *not* be created automatically. Trình Biên Soạn Hình Ảnh -- Image Editor Inside the specified folder, specific subfolders have to be created to tell Blender what to look for where. This folder structure has to mirror the structure of the scripts folder found in the installation directory of Blender: Duy Trì Phiên Sử Dụng -- Keep Session Nạp Giao Diện -- Load UI Locations for various external files can be set for the following options: Name that will be used in exported files when the format supports such feature. Number of files displayed in :menuselection:`File --> Open Recent`. Number of versions created for the same file (for backup). Previews of images and materials in the :doc:`File Browser </editors/file_browser/index>` are created on demand. To save these previews into your blend-file, enable this option (at the cost of increasing the size of your blend-file). Python scripts (including driver expressions) are not executed by default for security reasons. Số Tập Tin Gần Đây -- Recent Files Đường Dẫn Tương Đối -- Relative Paths  -- Render Cache  -- Render Output -- Save & Load Lưu Hình Ảnh Duyệt Thảo -- Save Preview Images Số Phiên Bản Lưu -- Save Versions  -- Scripts -- Scripts Path Hiển Thị Hình Tem -- Show Thumbnails Âm Thanh -- Sounds Tab thành dấu cách -- Tabs as Spaces  -- Temp Trình Biên Soạn Văn Bản -- Text Editor Chất Liệu -- Textures The *File* tab in *User Preferences* allows you to configure auto-save preferences and set default file paths for blend-files, rendered images, and more. The location where cached render images are stored. The location where temporary files are stored. The path to an external program to use for image editing. The path to an external program to use for playback of rendered animations. The path to the ``/branches`` directory of your local svn-translation copy, to allow translating from the UI. This option may slow down Blender when you quit, or under normal operation when Blender is saving your backup files. Using this option traces processor time for file size. This option tells Blender to keep the indicated number of saved versions of your file in your current working directory when you manually save a file. These files will have the extension: ``.blend1``, ``.blend2``, etc., with the number increasing to the number of versions you specify. Older files will be named with a higher number. e.g. With the default setting of 2, you will have three versions of your file: ``*.blend`` (your last save), ``*.blend1`` (your second last save) and ``*.blend2`` (your third last save). This option will compact your files whenever Blender is saving them. Dense meshes, large packed textures or lots of elements in your scene will result in a large blend being created. This specifies the number of minutes to wait between each :doc:`Auto Save </troubleshooting/recover>`. The default value of the Blender installation is 2 minutes. The minimum is 1, and the Maximum is 60 (save every hour). Đồng Hồ -- Timer When hitting :kbd:`Tab` the tabs get written as keyboard spaces. Where rendered images/videos are saved. You may choose to ignore these security issues and allow scripts to be executed automatically. add-ons camera cloth interface_theme modules operator presets render scripts startup templates Not all of the folders have to be present. 