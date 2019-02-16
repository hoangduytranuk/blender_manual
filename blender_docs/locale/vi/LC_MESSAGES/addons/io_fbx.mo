��    p      �                        "  6   (     _     h     w  �   �  	          �   +  R  �     
     !
     -
     <
     L
  	   b
  V   l
     �
     �
     �
     �
     �
  
          �     �   �  }   �  2   5     h  O  q     �  �   �     _  A   d     �     �  l   �     2  %   A  4   g     �  �   �  
   e     p     �     �  
   �     �     �     �     �     �     �          %     <  �   J                    )     .     A  7   G          �  
   �  L   �     �  W   �  t   N     �  |   �  4   R     �  	   �     �  
   �     �     �     �     �     �     t     �  �   �  �   y  	   U  w   _  
   �     �     �  �  �  q   �  �             	     &     <  B   M  ~   �  P        `     h  Q   ~  /  �  3       T   4   �  �      R"  �  i"     !$     &$  S   ,$     �$  &   �$  ,   �$  �   �$     �%  0   &    5&  �  K'  2   �)  #   *  4   2*  )   g*  <   �*     �*  �   �*     �+     �+  1   �+  C   	,  -   M,  0   {,     �,  <  �,  �  �-  �   v/  2   U0     �0  /  �0  %   �2  �   �2     �3  `   �3  3   &4  /   Z4  �   �4  &   =5  k   d5  I   �5     6  K  +6      w7  ?   �7  K   �7  =   $8     b8     |8  ,   �8  '   �8     �8  '   �8  A   &9  &   h9  A   �9     �9  h  �9  3   Y;     �;  &   �;     �;  2   �;     <  �   !<  /   �<     �<     �<  �   =     �=  �   �=  �   J>  .   0?  �   _?  Q   (@     z@  (   �@  <   �@     �@     A  '   3A  4   [A     �A  �   �A  0   B     �B  �  �B  �  �D     hF  �   �F  )   -G     WG  +   vG  �  �G  �   �L  L  AM     �N  j   �N  D   O  )   SO  w   }O  �   �O  �   �P     OQ  #   gQ  �   �Q  �  R  N   �S  �   8T  �  �T  -   �V   2.79 3.9.1 :menuselection:`File --> Import/Export --> FBX (.fbx)` Absolute Add Leaf Bones All Actions Animated fluid simulation -- FBX does not support this kind of animation. You can however use the OBJ exporter to write a sequence of files. Animation Animation Offset Animation support is minimal currently, we read all curves as if they were 'baked' ones (i.e. a set of close keyframes with linear interpolation). Animations (FBX AnimStacks, Blender actions) **are not linked** to their object, because there is no real way to know which stack to use as 'active' action for a given object, mesh or bone. This may be enhanced to be smarter in the future, but it's not really considered urgent, so for now you'll have to link actions to objects manually. Apply Modifiers Apply Scale Apply Scalings Apply Transform Armature FBXNode Type Armatures Armatures’ instances (through e.g. dupli or group instancing) **are not supported**. Authors Auto Autodesk FBX Automatic Bone Orientation Baked Animation Batch Mode Blender Blender uses Y Forward, Z Up (since the front view looks along the +Y direction). For example, its common for applications to use Y as the up axis, in that case -Z Forward, Y Up is needed. Bones would need to get a correction to their orientation (FBX bones seems to be -X aligned, Blender’s are Y aligned), this does not affect skinning or animation, but imported bones in other applications will look wrong. Bones' orientation importing is complex, you may have to play a bit with related settings until you get the expected results. Campbell Barton, Bastien Montagne, Jens Restemeier Category Choose whether to batch export groups or scenes to files. Note, when Group/Scene is enabled, you cannot use the animation option *Current Action* since that uses scene data and groups are not attached to any scenes. Also note, when Group/Scene is enabled you must include the armature objects in the group for animated actions to work. Compatibility Constraints -- The result of using constraints is exported as a keyframe animation however the constraints themselves are not saved in the FBX. Copy Copy the file on exporting and reference it with a relative path. Custom Properties Decal Offset Dupli-objects -- At the moment dupli-objects are only written in static scenes (when animation is disabled). Embed Textures Empty/Camera/Lamp/Armature/Mesh/Other Enable/Disable exporting of respective object types. Export Export all actions compatible with the selected armatures start/end times which are derived from the keyframe range of each action. When disabled only the currently assigned action is exported. FBX format Force Connect Children Force Start/End Keying Forward / Up Axis Geometries Group/Scene Ignore Leaf Bones Image Search Import Import Animation Import Enums As Strings Import Normals Import User Properties Import-Export Imported actions are linked to their related object, bone or shape key, on a 'first one wins' basis. If you export a set of them for a single object you'll have to reassign them yourself. Key All Bones Location Loose Edges Main Manual Orientation Match Material textures -- only texface images are supported. Mesh: shape keys. Missing NLA Strips NURBS surfaces, text3D and metaballs are converted to meshes at export time. Name Note that the importer is a new addition and lacks many features the exporter supports. Object instancing -- exported objects do not share data, instanced objects will each be written with their own data. Only Deform Bones Only export the selected objects. Otherwise export all objects in the scene. Note, this does not apply when batch exporting. Only write the filename and omit the path component. Own Dir Path Mode Primary/Secondary Bone Axis Properties Relative Sampling Rate Saving Just Animations Scale Scale the exported data by this value. 10 is the default because this fits best with the scale most applications import FBX to. Selected Objects Simplify Since many applications use a different axis for 'Up', these are axis conversion for these settings, Forward and Up axes -- By mapping these to different axes you can convert rotations between applications default up and forward axes. Since many applications use a different axis for 'Up', these are axis conversions for Forward and Up axes -- By mapping these to different axes you can convert rotations between applications default up and forward axes. Smoothing Some of the following features are missing because they are not supported by the FBX format, others may be added later. Strip Path TODO. Tangent Space The FBX file format supports files that only contain takes. It is up to you to keep track of which animation belongs to which model. The animation that will be exported is the currently selected action within the Action editor. To reduce the file size, turn off the exporting of any parts you do not want and disable *All Actions*. For armature animations typically you just leave the armature enabled which is necessary for that type of animation. Reducing what is output makes the export and future import much faster. Normally each action will have its own name but the current or only take can be forced to be named "Default Take". Typically, ensure that this option remains off. The exporter can bake mesh modifiers and animation into the FBX so the final result looks the same as in Blender. This format is mainly use for interchanging character animations between applications and is supported by applications such as Cinema4D, Maya, Autodesk 3ds Max, Wings3D and engines such as Unity3D, Unreal Engine 3/UDK and Unreal Engine 4. Usage Use Modifiers Render Setting Use Pre/Post Rotation Uses full paths. Uses relative / absolute paths based on the paths used in Blender. Uses relative paths for files which are in a subdirectory of the exported location, absolute for any directories outside that. Uses relative paths in every case (except when on a different drive on windows). Version Version 7.1 or newer. Vertex shape keys -- FBX supports them but this exporter does not write them yet. When enabled, each file is exported into its own directory, this is useful when using the *Copy Images* option. So each directory contains one model with all the images it uses. Note, this requires a full Python installation. If you do not have a full Python installation, this button will not be shown. When enabled, export each group or scene to a file. When enabled, the mesh will be from the output of the modifiers applied to the mesh. When referencing paths in exported files you may want some control as to the method used since absolute paths may only be correct on your own system. Relative paths, on the other hand, are more portable but mean that you have to keep your files grouped when moving about on your local file system. In some cases, the path doesn't matter since the target application will search a set of predefined paths anyway so you have the option to strip the path too. binary FBX files only. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-02 17:31+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 2.79 3.9.1 :menuselection:`Tập Tin (File) --> Nhậpt/Xuất (Import/Export) --> FBX (.fbx)` Tuyệt Đối -- Absolute Thêm Xương Ngọn -- Add Leaf Bones Toàn Bộ các Hành Động -- All Actions Hoạt họa mô phỏng chất lỏng (*Animated fluid simulation*) -- FBX không hỗ trợ loại hoạt họa này, Tuy nhiên, bạn có thể sử dụng trình xuất khẩu OBJ để viết thành một trình tự (*chuỗi*) các tập tin. Hoạt Hình -- Animation Vị Trí của Hoạt Họa -- Animation Offset Hỗ trợ về hoạt hình hiện tại có rất ít. Phần mềm sẽ đọc tư liệu của tất cả các đường cong như thể chúng đã được 'nướng' vậy (tức là một tập hợp các khung hình chính (*khung khóa*) có nội suy tuyến tính). Các hoạt hình (Ngăn Xếp Hoạt Họa của FBX (*FBX AnimStacks*), các họa họa trong Blender) **không liên kết** (not linked) với vật thể của chúng, bởi vì không có cách nào thực sự để biết ngăn xếp nào sử dụng làm hành động đang 'hoạt động' đối với một vật thể đã cho cả, khung lưới hoặc xương. Cái này có thể được phát triển để nó thông minh hơn trong tương lai, nhưng hiện giờ vấn đề này không phải thực sự khẩn cấp, vì thế, bạn sẽ phải liên kết các hành động với các đối tượng một cách thủ công. Áp Dụng Bộ Điều Chỉnh -- Apply Modifiers Áp Dụng Tỷ Lệ -- Apply Scale Áp Dụng Biến Đổi Tỷ Lệ -- Apply Scalings Áp Dụng Biến Hóa -- Apply Transform Thể loại nút FBXNode cho Cốt -- Armature FBXNode Type Cốt -- Armatures Các thực thể của Cốt (Armatures) (thông qua quá trình thực thể hóa bản sao (dupli) hoặc thực thể hóa nhóm chẳng hạn) sẽ **không được hỗ trợ** (*not supported*). Tác Giả -- Authors Tự Động -- Auto Định Dạng FBX của Autodesk -- Autodesk FBX Tự Động Định Hướng Xương -- Automatic Bone Orientation Hoạt Hình đã Nướng -- Baked Animation Chế Độ Thi Hành Hàng Loạt -- Batch Mode Blender Blender sử dụng Y Hướng về Trước, Z Lên (vì mặt trước trông dọc theo hướng trục +Y). Ví dụ, việc các ứng dụng sử dụng Y làm trục lên là một việc phổ biến, trong trường hợp đó, -Z Hướng về Trước (*Forward*), Y Lên (*Up*) là điều cần thiết. Các xương sẽ cần phải được chỉnh sửa hướng của chúng (các xương trong FBX hình như sắp xếp theo hướng -X, trong khi Blender thì căn chỉnh theo hướng Y). Cái này không ảnh hưởng đến quá trình bóc vỏ hành (*skinning*) hoặc hoạt hình, nhưng các xương được nhập trong các ứng dụng khác sẽ trông không đúng. Việc nhập định hướng của các xương khá phức tạp, bạn có thể phải thử nghiệm một chút với các sắp đặt liên quan, cho đến khi bạn nhận được kết quả mình mong đợi. Campbell Barton, Bastien Montagne, Jens Restemeier Hạng Mục -- Category Chọn xem có xuất các nhóm hoặc các cảnh hàng loạt ra các tập tin. Lưu ý, khi Nhóm/Cảnh được kích hoạt, bạn không thể sử dụng tùy chọn Hoạt họa *Hành Động Hiện Tại* (*Current Action*) vì cái đó sử dụng dữ liệu cảnh, trong khi các nhóm không được gắn liền vào bất kỳ cảnh nào cả. Cũng lưu ý, khi Group/Scene được kích hoạt, bạn phải bao gồm các vật thể cốt (*armature objects*) trong nhóm để các hành động trong hoạt hình hoạt động. Tính Tương Thích -- Compatibility Ràng buộc -- Kết quả của việc sử dụng các ràng buộc được xuất dưới dạng hoạt hình khung khóa, song các ràng buộc sẽ không được lưu trong FBX. Sao Chép -- Copy Sao chép tập tin khi xuất và tham chiếu tập tin bằng đường dẫn tương đối. Các Tính Chất Tùy Chỉnh -- Custom Properties Dịch Chuyển của Đề-Can -- Decal Offset Các vật thể sao chép (*Dupli-objects*) -- Hiện thời các vật thể sao chép chỉ được viết trong các cảnh tĩnh (*static scenes*) (khi hoạt họa tắt). Nhúng Chất Liệu -- Embed Textures Vật Thể Rỗng/Máy Ảnh/Đèn/Cốt/Khung Lưới/Cái Khác -- Empty/Camera/Lamp/Armature/Mesh/Other Bật/Tắt khả năng xuất các loại đối tượng tương ứng. Xuất -- Export Xuất tất cả các hành động tương thích với các khoảng thời gian bắt đầu/kết thúc của cốt đã chọn, bắt nguồn từ phạm vi khung khóa của mỗi hành động. Khi bị tắt (*vô hiệu hóa*), chỉ hành động hiện được gán cho (*assigned*) là sẽ được xuất mà thôi. Định dạng FBX -- FBX format Ép Buộc Kết Nối với Con Cái -- Force Connect Children Bắt Buộc Khóa Hóa Khởi Đầu/Kết Thúc -- Force Start/End Keying Trục Hướng về Trước/Lên Trên -- Forward / Up Axis Hình Học -- Geometries Nhóm/Cảnh -- Group/Scene Bỏ Qua Xương Ngọn -- Ignore Leaf Bones Tìm Kiếm Hình Ảnh -- Image Search Nhập -- Import Nhập Hoạt Họa -- Import Animation Nhập Enum như các Chuỗi Ký Tự -- Import Enums As Strings Nhập Pháp Tuyến -- Import Normals Nhập các Tính Chất Người Dùng -- Import User Properties Nhập-Xuất -- Import-Export Hành động đã nhập sẽ được liên kết với vật thể liên quan, như xương hoặc hình mẫu (*shape key*) của chúng, trên cơ sở 'ưu tiên cho cái nào đến trước'. Nếu bạn đã xuất một tập hợp của chúng cho một đơn vật thể nào đó rồi thì bạn sẽ phải tự đặt chúng lại (*reassign*). Khóa Hóa Toàn Bộ các Xương -- Key All Bones Vị Trí -- Location Các Cạnh Rời Rạc -- Loose Edges Chủ Yếu -- Main Định Hướng Thủ Công -- Manual Orientation Khớp -- Match Các chất liệu của nguyên liệu -- chỉ hỗ trợ các hình ảnh của chất liệu bề mặt (*texface images*) mà thôi. Khung Lưới: các hình mẫu (*shape keys*). Còn thiếu -- Missing Dải NLA -- NLA Strips Các bề mặt NURBS, Văn Bản 3D (*text3D*) và các Siêu Cầu (*metaballs*) sẽ được chuyển đổi thành khung lưới tại thời điểm xuất khẩu. Tên -- Name Lưu ý rằng trình nhập khẩu là một bổ sung mới và còn thiếu nhiều tính năng mà trình xuất khẩu hỗ trợ. Thực thể hóa vật thể (*Object instancing*) -- các vật thể xuất khẩu sẽ không sử dụng chung dữ liệu, các đối tượng đã thực thể hóa sẽ được ghi với dữ liệu riêng của chúng. Duy Xương Biến Dạng -- Only Deform Bones Chỉ xuất các đối tượng đã chọn mà thôi. Nếu không, xuất tất cả các đối tượng trong cảnh. Lưu ý, cái này sẽ không áp dụng trong khi cho xuất hàng loạt. Chỉ viết tên tập tin mà thôi và bỏ qua thành phần đường dẫn. Thư Mục Riêng -- Own Dir Chế Độ Đường Dẫn -- Path Mode Trục xương chính / phụ -- Primary/Secondary Bone Axis Tính Chất -- Properties Tương Đối -- Relative Tần Số Mẫu Vật -- Sampling Rate Duy Lưu các Hoạt Hình -- Saving Just Animations Tỷ Lệ -- Scale Đổi tỷ lệ của các vật thể đã nhập bằng giá trị này. 10 là giá trị mặc định, bởi vì giá trị này phù hợp nhất với tỷ lệ mà hầu hết các ứng dụng nhập FBX vào. Các Vật Thể đã Chọn -- Selected Objects Đơn Giản Hóa -- Simplify Vì nhiều ứng dụng sử dụng trục khác cho hướng 'Lên' cho nên đây là phương pháp để chuyển đổi trục trong những sắp đặt này, Trục Hướng về Trước và Lên Trên (Forward and Up axis) -- Bằng cách ánh xạ các trục này đến trục khác, bạn có thể chuyển đổi sự xoay chiều giữa các sắp đặt mặc định về trục Hướng về Trước và Lên Trên của các ứng dụng. Vì nhiều ứng dụng sử dụng trục khác cho hướng 'Lên' cho nên đây là phương pháp để chuyển đổi trục trong những sắp đặt này, Trục Hướng về Trước và Lên Trên (Forward and Up axis) -- Bằng cách ánh xạ các trục này đến trục khác, bạn có thể chuyển đổi sự xoay chiều giữa các sắp đặt mặc định về trục Hướng về Trước và Lên Trên của các ứng dụng. Làm Mịn -- Smoothing Một số tính năng sau đây bị thiếu là do chúng không được định dạng FBX hỗ trợ, một số khác có thể sau này sẽ được cho thêm vào. Loại Bỏ Đường Dẫn -- Strip Path Nội dung cần viết thêm. Không Gian Tiếp Tuyến -- Tangent Space Định dạng tập tin FBX hỗ trợ các tập tin chỉ có chứa các đoạn đã quay mà thôi. Việc kiểm soát sự bố trí các hoạt hình nào trực thuộc về mô hình nào là hoàn toàn tùy thuộc vào bạn. Hoạt hình sẽ được xuất ra là hành động hiện được chọn trong Trình Biên Soạn Hành Động (*Action editor*). Để giảm cỡ của tập tin, xin bạn hãy tắt khả năng xuất bất kỳ phần nào mà bạn không muốn và tắt sắp đặt *Toàn Bộ các Hành Động* (*All Actions*) đi. Đối với các hoạt hình của cốt thì thông thường bạn chỉ cần để cốt ở tình trạng kích hoạt (*enabled*), tức cái cần thiết cho thể loại hoạt hình này. Việc thuyên giảm số lượng các vật cho xuất ở đầu ra sẽ làm cho việc xuất khẩu và nhập khẩu trong tương lai nhanh hơn nhiều. Thông thường, mỗi hành động sẽ có tên riêng của nó, nhưng đoạn quay hiện tại, hoặc đoạn quay duy nhất, thì bị buộc phải đặt tên là "Cảnh Quay Mặc Định" (*Default Take*). Thông thường thì nên để tùy chọn này là tắt (*giải hoạt*) (*off*). Trình xuất khẩu có thể nướng các bộ điều chỉnh khung lưới và hoạt hình thành FBX, hầu cho kết quả cuối cùng trông giống tương tự như trong Blender. Định dạng này chủ yếu được sử dụng để tráo đổi các hoạt hình của nhân vật giữa các ứng dụng khác nhau và được hỗ trợ bởi các ứng dụng như Cinema4D, Maya, Autodesk 3ds Max, Wings3D và các động cơ (máy trò chơi) như Unity3D, Unreal Engine 3/UDK và Unreal Engine 4. Sử Dụng -- Usage Sử Dụng Sắp Đặt về Kết Xuất của các Bộ Điều Chỉnh -- Use Modifiers Render Setting Dùng Sự Xoay Chiều (Tiền/Hậu) Kỳ -- Use Pre/Post Rotation Sử dụng đường dẫn đầy đủ. Sử dụng đường dẫn tương đối / tuyệt đối dựa trên các đường dẫn sử dụng trong Blender. Sử dụng đường dẫn tương đối cho các tập tin nằm trong thư mục nhánh của vị trí đã xuất. Sử dụng đường dẫn tuyệt đối cho bất kỳ thư mục nào nằm ngoài đó. Sử dụng đường dẫn tương đối trong mọi trường hợp (trừ khi nằm trên một ổ đĩa khác trên Windows). Phiên Bản -- Version Phiên bản 7.1 hoặc mới hơn. Các hình mẫu điểm đỉnh (*Vertex shape keys*) -- FBX hỗ trợ chúng, song trình xuất khẩu này vẫn chưa viết chúng. Khi được bật, mỗi tập tin sẽ được xuất vào thư mục riêng của nó. Điều này rất hữu ích khi sử dụng tùy chọn *Sao Chép Hình Ảnh* (*Copy Images*). Vì thế, mỗi thư mục chứa một mô hình, với tất cả các hình ảnh mà nó sử dụng. Lưu ý, cái này đòi hỏi phải cài đặt Python đầy đủ. Nếu bạn không cài đặt Python đầy đủ, nút này sẽ không hiển thị lên đâu. Khi được bật thì xuất mỗi nhóm hoặc cảnh vào một tập tin. Khi được bật, khung lưới sẽ được lấy từ đầu ra của các bộ điều chỉnh đã được áp dụng cho khung lưới. When referencing paths in exported files you may want some control as to the method used since absolute paths may only be correct on your own system. Relative paths, on the other hand, are more portable but mean that you have to keep your files grouped when moving about on your local file system. In some cases, the path doesn't matter since the target application will search a set of predefined paths anyway so you have the option to strip the path too. Duy các tập tin FBX nhị phân mà thôi. 