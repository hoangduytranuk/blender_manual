��          �               �  }   �     K  8   O  �   �     q          �  G   �     �      �       	   
            (   !     J  
   R     ]  ,   f     �  H   �  �   �  �   �     �     �  8   �  �  �  �   �     i	  �   }	  �  
  -   �     �     �  z        }  ,   �     �  %   �     �       <   #     `     u     �  :   �     �  �   �  e  �  �  �     �     �  d   �   A generated rectangular mask merged with the input mask. The created mask is the size of the current scene render dimensions. Add An optional mask to use as the base for mask operations. Any area covered by both the input mask and the generated mask becomes black. Areas covered by the generated mask that are black on the input mask become the specified *Value*. Areas uncovered by the generated mask remain unchanged. Box Mask Node Box Mask Node. Height Height of the box as a fraction of the total image *width*, not height. Inputs Intensity of the generated mask. Mask Mask Type Multiply Not Operation to use against the input mask. Outputs Properties Rotation Rotation of the box around its center point. Subtract The *Box Mask* node creates an image suitable for use as a simple matte. This yields the *intersection* of this generated mask and the input mask: Values of the input mask are multiplied by the specified *Value* for the area covered by the generated mask. All other areas become black. This yields the *union* of the input mask and the generated mask: Areas covered by the generated mask are set to the specified *Value*. Other parts of the input masked are passed through unchanged, or set to black if there is no input mask. Value Width Width of the box as a fraction of the total image width. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
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
 Màn chắn hình chữ nhật đã sinh tạo sẽ được hội nhập với màn chắn đầu vào. Màn chắn tạo nên sẽ là cỡ của kích thước bản kết xuất cảnh hiện tại. Cộng Thêm -- Add Một chắn lọc tùy chọn (không bắt buộc) để sử dụng làm cơ sở cho các thao tác (phép toán) chắn lọc. Bất cứ khu vực nào được bao trùm bởi cả hai, màn chắn đầu vào và màn chắn đã sinh tạo sẽ trở thành màu đen. Những khu vực mà màn chắn sinh tạo bao trùm là màu đen trên màn chắn đầu vào sẽ trở thành *Giá Trị* (Value) chỉ định. Những khu vực không được màn chắn sinh tạo bao trùm sẽ được giữ nguyên, không thay đổi. Nút Màn Chắn Hình Hộp -- Box Mask Node Nút Màn Chắn Hình Hộp. Chiều Cao -- Height Chiều cao của hình hộp như một hệ số của tổng *chiều rộng* (width), chứ không phải chiều cao. Đầu Vào -- Inputs Cường độ của màn chắn sinh tạo. Màn Chắn -- Mask Thể Loại Màn Chắn -- Mask Type Nhân -- Multiply Đảo Nghịch -- Not Phép toán để sử dụng với màn chắn đầu vào. Đầu Ra -- Outputs Tính Chất -- Properties Xoay Chiều -- Rotation Xoay chiều hình hộp chung quanh trung tâm của nó. Trừ Khấu -- Subtract Nút *Màn Chắn Hình Hộp* kiến tạo một hình ảnh thích hợp để sử dụng nó như một lớp lồng đơn giản. Cái này sẽ cho ra khoảng *giao cắt* (intersection) giữa màn chắn đã sinh tạo này và màn chắn ở đầu vào: Các giá trị của màn chắn đầu vào được nhân với *Giá Trị* (Value) đã chỉ định cho diện tích mà màn chắn sinh tạo bao trùm. Toàn bộ những khu vực khác sẽ trở thành màu đen. Cái này sẽ tạo ra một *kết hợp* (union) của màn chắn đầu vào và màn chắn do máy sinh tạo ra: Khu vực được màn chắn do máy sinh tạo bao phủ sẽ được đặt thành *Giá Trị* (Value) đã chỉ định. Những bộ phận khác của màn chắn đầu vào sẽ được truyền qua nguyên vẹn, không thay đổi, hoặc sẽ được đặt thành màu đen nếu không có màn chắn đầu vào. Giá Trị -- Value Chiều Rộng -- Width Chiều rộng của hình hộp như một hệ số của tổng chiều rộng của hình ảnh. 