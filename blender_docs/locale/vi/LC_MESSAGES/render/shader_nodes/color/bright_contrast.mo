��          �               l     m  �   ~     N  
   c     n  �   �  !   "     D     M  �  c                 p       �     �  
   �     �     �     �  �  �     �  E  �  7   
     ;
      [
  8  |
  >   �      �  7     �  M     G     [     p  K  �     �     �     �  :     &   O  *   v   A basic example. A scaling type factor by which to make brighter pixels brighter, but keeping the darker pixels dark. Higher values make details stand out. Use a negative number to decrease the overall contrast in the image. Bright/Contrast Node Brightness Brightness/Contrast Node. By default, it is supposed to work in *premultiplied* alpha. If the *Convert Premul* checkbox is not enabled, it is supposed to work in *straight* alpha. Clamp the values to normal range. Contrast Convert Premultiplied Either of these nodes will scale the values back to normal range. In the example image, we want to amp up the specular pass. The bottom thread shows what happens if we do not clamp the values; the specular pass has valued much less than one in the dark areas; when added to the medium gray, it makes black. Passing the brightened image through either the Map Value or the Color Ramp node produces the desired effect. Example Image Inputs It is possible that this node will put out a value set that has values beyond the normal range, i.e. values greater than one and less than zero. If you will be using the output to mix with other images in the normal range, you should clamp the values using the Map Value node (with the Min and Max enabled), or put through a Color Ramp node (with all normal defaults). Notes Outputs Properties See :term:`Alpha Channel`. Standard image input. Standard image output. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-01-22 23:26+0000
PO-Revision-Date: 2019-03-23 14:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Một ví dụ cơ bản. Một loại hệ số phóng đại dùng để làm cho các điểm ảnh sáng sáng rực hơn, song giữ cho các điểm ảnh đã tối vẫn ở mức độ tối. Giá trị cao sẽ làm cho chi tiết nổi bật lên. Sử dụng số âm hòng để giảm độ tương phản tổng thể trong hình ảnh. Nút Độ Sáng/Tương Phản -- Bright/Contrast Node Độ Sáng Tối -- Brightness Nút Độ Sáng/Tương Phản. Theo mặc định, nó có nghĩa vụ phải hoạt động đối với alpha *nhân trước* (*premultiplied alpha*). Nếu hộp kiểm *Chuyển Đổi Nhân Trước* (*Convert Premul*) không được kích hoạt, thì đúng nghĩa ra, nó sẽ hoạt động trong alpha *thẳng* (*straight alpha*). Hạn định các giá trị trong phạm vi bình thường. Độ Tương Phản -- Contrast Chuyển Đổi Nhân Trước -- Convert Premultiplied Một trong các nút này sẽ tỷ lệ hóa các giá trị để chúng trở lại trong phạm vi bình thường. Trong hình ảnh ví dụ, chúng tôi muốn phóng đại lượt giải quyết về độ lóng lánh (*specular pass*). Luồng dưới cùng cho thấy nếu chúng ta không hạn định các giá trị lại thì điều gì sẽ xảy ra; Lượt giải quyết về độ lóng lánh (*specular pass*) có giá trị ít hơn 1 trong những vùng tối; khi cộng thêm vào màu xám trung bình, nó làm thành màu đen. Việc truyền hình ảnh đã được làm sáng lên qua một trong hai cái, Ánh Xạ Giá Trị (*Map Value*) hoặc Dốc Màu (*Color Ramp*) tạo ra được hiệu ứng mình mong muốn. Ví Dụ -- Example Hình Ảnh -- Image Đầu Vào -- Inputs Có thể nút này sẽ xuất ra một tập hợp các giá trị có độ lớn vượt quá phạm vi bình thường, tức là các giá trị lớn hơn 1 và nhỏ hơn 0. Nếu bạn sử dụng giá trị đầu ra để trộn với các ảnh khác trong phạm vi bình thường thì bạn nên hạn định các giá trị bằng cách sử dụng nút Ánh Xạ Giá Trị (*Map Value*) (với Tối Thiểu (Min) và Tối Đa (Max) được bật), hoặc chuyển qua nút Dốc Màu (*Color Ramp*) (với tất cả các giá trị mặc định thông thường). Ghi Chú -- Notes Đầu Ra -- Outputs Tính Chất -- Properties Xin xem thêm về *Kênh Alpha* -- :term:`Alpha Channel`. Đầu vào hình ảnh tiêu chuẩn. Đầu ra tiêu chuẩn của hình ảnh. 