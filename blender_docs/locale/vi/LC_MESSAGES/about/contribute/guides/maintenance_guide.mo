��          T               �      �   �   �      �  Y   �  ,   �  �     �  �  P   �  �  �     �  �   �  S   =  \  �   Adding/Removing/Moving Files It is best to avoid moving/renaming files as this breaks URLs and without this script translators will lose all their work in these files. Please ask an administrator if you think something should be renamed/moved. Maintenance RST-files can then be freely moved and the remap script will move the locale file after:: This script also works for image file names. When RST-files are added or removed the corresponding locale files are added or removed automatically by the update script. However, if files need to be moved please use this Python script:: Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2020-04-12 10:34+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Tạo Thêm/Xóa Bỏ/Di Chuyển các Tập Tin -- Adding/Removing/Moving Files Tốt nhất là nên tránh di chuyển/đổi tên các tập tin, vì điều này sẽ phá hỏng các địa chỉ URL và nếu không có tập lệnh này thì tất cả công việc của các phiên dịch viên trong các tập tin này sẽ bị mất đi. Xin vui lòng kiểm tra với quản trị viên nếu bạn cho rằng có một cái gì đó cần phải được đổi tên/di chuyển, trước khi làm. Bảo Quản -- Maintenance Các tập tin RST sau đó có thể được tự do di chuyển và tập lệnh ``remap`` sẽ di chuyển tập tin ở thư mục ``locale`` sau khi:: Tập lệnh này cũng hoạt động với các tên tập tin hình ảnh nữa. Khi các tập tin RST được cho thêm vào hoặc bị loại bỏ đi thì các tập tin địa phương tương ứng cũng sẽ được thêm vào hoặc gỡ bỏ một cách tự động bởi tập lệnh cập nhật. Tuy nhiên, nếu các tập tin cần được di chuyển thì xin vui lòng sử dụng tập lệnh Python này:: 