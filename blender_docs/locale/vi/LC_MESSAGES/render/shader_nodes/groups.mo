��    &      L              |     }     �  %   �  '   �  '   �  "     	   @  n   J     �  �  �  0  �     �  
   �     �     �  "        4  �   A     �     �  �  �  j   �	     �	     
  	   
  
   
     '
     ,
     1
     6
     B
     N
  �   T
  	     �        �  �  �  �  C     �     	  I   %  M   o  H   �  6     (   =  �   f  -     �  H  �  '                5     S  %   m  &   �    �     �     �  u  �  �   d     �          ,     E     _     t     �     �     �     �     �       �        �  q  �   :kbd:`Ctrl-G` :kbd:`Tab`, :kbd:`Ctrl-Tab` :menuselection:`File --> Link/Append` :menuselection:`Go to Parent Node Tree` :menuselection:`Group --> Group Insert` :menuselection:`Group --> Ungroup` All Modes Also nested node groups are supported. I.e. a node group can be inserted or created inside another node group. Appending Node Groups As an example: If you have created a material that you would like to use with different inputs e.g. diffuse color: red plastic, green plastic. You could create different materials with *Make Single User* for each different color with a copy of the tree part describing the plastic material. If you like to edit the material you would need to redo the edit on all materials. A better method of reuse is to create node groups, exposing only the variable inputs (e.g. diffuse color). Conceptually, grouping nodes allows you to specify a *set* of nodes that you can treat as though it were "just one node". Node groups are similar to functions in programming. You can then reuse them inside, which are then called "NodeGroups", or in other blend-file(s), when appending called "NodeTrees". Copy Edit Group Editor Example of a node group. Example of an expanded node group. Group Insert Grouping nodes can simplify a node tree by allowing instancing and hiding parts of the tree. Both material and composite nodes can be grouped. Header Hotkey If during node group development an additional parameter needs to be passed into the group, an additional socket must be added to the *Group Input* node. This is easily done by adding a connection from the hollow socket on the right side of the *Group Input* node to the desired input socket on the node requiring input. The process is similar for the *Group Output* regarding data you want to be made available outside the group. If you include an output node in the group, there will not be an output socket available *from* the group! Input nodes Interactively Interface Make Group Menu Mode Move Node Groups Output node Panel Recursive node groups are prohibited for all the current node systems to prevent infinite recursion. A node group can never contain itself (or another group that contains it). Reference Remember that the essential idea is that a group should be an easily-reusable, self-contained software component. Material node groups should **not** include: Ungroup When a node group is created, new *Group Input* and *Group Output* nodes are generated to represent the data flow into and out of the group. When created, connections to input sockets coming from unselected nodes will become attached to new sockets on the *Group Input* node. Similarly, outgoing connections to input sockets of unselected nodes will become attached to the new *Group Output* node. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-12-27 20:49-0600
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 :kbd:`Ctrl-G` :kbd:`Tab`, :kbd:`Ctrl-Tab` :menuselection:`Tập Tin (File) --> Kết Nối/Bổ Sung (Link/Append)` :menuselection:`Chuyển về Cây Nút Phụ Huynh (Go to Parent Node Tree)` :menuselection:`Nhóm (Group) --> Chèn Thêm vào Nhóm (Group Insert)` :menuselection:`Nhóm (Group) --> Rã Nhóm (Ungroup)` Toàn Bộ các Chế Độ -- All Modes Các nhóm nút lồng nhau cũng được hỗ trợ nữa, chẳng hạn, một nhóm nút có thể được chèn vào hoặc được tạo bên trong một nhóm nút khác. Bổ Sung Nhóm Nút -- Appending Node Groups Một ví dụ: Nếu bạn đã tạo một nguyên liệu mà bạn muốn sử dụng với các yếu tố đầu vào khác nhau, ví dụ: màu khuếch tán: nhựa màu đỏ, nhựa màu xanh lá cây, thì bạn có thể tạo các nguyên liệu riêng biệt bằng nút *Biến thành Đơn Người Dùng* (*Make Single User*) cho mỗi màu khác nhau, với bản sao của phần cây mô tả vật liệu nhựa. Nếu bạn muốn chỉnh sửa nguyên liệu, thì bạn cần phải chỉnh sửa lại tất cả các nguyên liệu. Một phương pháp tốt hơn để tái sử dụng là tạo các nhóm nút, chỉ cho lộ ra các tham số đầu vào (ví dụ: màu khuếch tán) (*diffuse color*). Nói một cách khái niệm, việc nhóm các nút lại cho phép bạn chỉ định một *tập hợp* các nút mà bạn có thể coi như là \một đơn nút\. Các nhóm nút tương tự như các hàm trong lập trình vậy. Sau đó, bạn có thể tái sử dụng chúng bên trong, cái mà sau đó được gọi là \Nhóm Nút (NodeGroups)\ hoặc trong các tập tin blend khác, khi chèn thêm vào, được gọi là \Cây Nút (NodeTrees)\. Sao Chép -- Copy Biên Soạn Nhóm -- Edit Group Trình Biên Soạn -- Editor Ví dụ về nhóm nút. Ví dụ về nhóm nút mở rộng. Chèn Thêm vào Nhóm -- Group Insert Việc nhóm các nút có thể đơn giản hóa một cây nút bằng cách cho phép việc tạo một thực thể và ẩn dấu các phần của cây. Cả hai loại nút, nút chất liệu và nút tổng hợp, đều có thể nhóm lại được. Tiêu Đề -- Header Phím Tắt -- Hotkey Nếu trong quá trình phát triển nhóm nút, một tham số bổ sung cần phải được đưa vào nhóm thì một ổ cắm cần phải được bổ sung vào phần *Đầu Vào của Nhóm* (Group Input). Điều này có thể dễ dàng thực hiện bằng cách cho thêm một kết nối từ ổ cắm rỗng ở phía bên phải của *Đầu Vào của Nhóm* (Group Input) vào ổ cắm đầu vào mong muốn trên nút yêu cầu đầu vào. Đối với dữ liệu mà bạn muốn cung cấp ra khỏi nhóm, làm tương tự như quá trình này trên *Đầu Ra của Nhóm* (Group Output). Nếu bạn bao gồm một nút đầu ra trong nhóm thì bạn sẽ không có một ổ cắm đầu ra có *từ* (ra khỏi) nhóm! Nút Đầu Vào -- Input nodes Tương Tác -- Interactively Giao Diện -- Interface Tạo Nhóm -- Make Group Trình Đơn -- Menu Chế Độ -- Mode Di Chuyển -- Move Nhóm Nút -- Node Groups Nút Đầu Ra -- Output node Bảng -- Panel Các nhóm nút đệ quy sẽ bị cấm hoạt động đối với toàn bộ hệ thống nút hiện tại, nhằm ngăn chặn sự đệ quy vô hạn. Một nhóm nút không bao giờ có thể chứa chính bản thân nó (hoặc nhóm khác có chứa chính bản thân nó). Tham Chiếu -- Reference Hãy nhớ rằng điều thiết yếu là một nhóm phải là một thành phần phần mềm dễ tái sử dụng, khép kín. Nhóm nút nguyên liệu **không nên** bao gồm: Rã Nhóm -- Ungroup Khi một nhóm nút được kiến tạo, các nút *Đầu Vào của Nhóm* (Group Input) và *Đầu Ra của Nhóm* (Group Output) mới sẽ được sinh tạo ra để biểu thị luồng chảy của dữ liệu vào và ra khỏi nhóm. Khi được kiến tạo, các kết nối đến ổ cắm đầu vào đến từ các nút không được chọn sẽ được gắn vào các ổ cắm mới trên nút *Đầu Vào của Nhóm*. Tương tự, các kết nối ra ngoài đến các ổ cắm đầu vào của các nút không được chọn sẽ được gắn vào nút *Đầu Ra của Nhóm* mới. 