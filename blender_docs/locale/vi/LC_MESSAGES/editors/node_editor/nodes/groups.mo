��    :      �              �     �     �     �  %   �  '     %   B  '   h  %   �  "   �  0   �  	   
  n        �  �  �  0  z     �  ,   �  
   �     �     �  "   	     +	  �   8	     �	     �	  �  �	  �  �  �   q  j   +     �     �     �  	   �  
   �     �     �     �  ,   �       _       y     �  	   �  �   �  	   E  �   O  �  �     �  ,   �  �      �   �  '   q  �  �     �  B   �  �  �  9  ^  �  �     P     ]     k  I   �  N   �  B      C   c  ;   �  6   �  S      (   n   �   �   2   K!  �  ~!  �  ]$     8&  :   J&      �&     �&     �&  %   �&  &   '    +'     3(     I(  u  _(  �  �*  �   �-  �   �.  -   6/     d/     �/     �/     �/     �/     �/     �/  6   0     I0  &  c0     �2     �2     �2     �2     �3  �   
4  �  �4  7   �7  .   �7  
  !8  T  ,9  ,   �:  �  �:     ?>  �   T>  q  �>  y  UA   :kbd:`Alt-G` :kbd:`Ctrl-G` :kbd:`Tab`, :kbd:`Ctrl-Tab` :menuselection:`File --> Link/Append` :menuselection:`Go to Parent Node Tree` :menuselection:`Group --> Edit Group` :menuselection:`Group --> Group Insert` :menuselection:`Group --> Make Group` :menuselection:`Group --> Ungroup` :menuselection:`Properties region --> Interface` All Modes Also nested node groups are supported. I.e. a node group can be inserted or created inside another node group. Appending Node Groups As an example: If you have created a material that you would like to use with different inputs e.g. diffuse color: red plastic, green plastic. You could create different materials with *Make Single User* for each different color with a copy of the tree part describing the plastic material. If you like to edit the material you would need to redo the edit on all materials. A better method of reuse is to create node groups, exposing only the variable inputs (e.g. diffuse color). Conceptually, grouping nodes allows you to specify a *set* of nodes that you can treat as though it were "just one node". Node groups are similar to functions in programming. You can then reuse them inside, which are then called "NodeGroups", or in other blend-file(s), when appending called "NodeTrees". Copy Copy to parent node tree, keep group intact. Edit Group Editor Example of a node group. Example of an expanded node group. Group Insert Grouping nodes can simplify a node tree by allowing instancing and hiding parts of the tree. Both material and composite nodes can be grouped. Header Hotkey If during node group development an additional parameter needs to be passed into the group, an additional socket must be added to the *Group Input* node. This is easily done by adding a connection from the hollow socket on the right side of the *Group Input* node to the desired input socket on the node requiring input. The process is similar for the *Group Output* regarding data you want to be made available outside the group. If you have multiple inputs or outputs, they can be re-ordered by selecting the socket in the list and then moving it up or down with the arrow buttons on the right side of the panel. The larger plus sign buttons below the list will add an unconnected socket of the same type as the selected socket or a value socket if there is no selection. The small circled plus sign at the bottom of the list has filtering functions to facilitate finding nodes if the group has a large number of sockets. If you include a source node in your group, you will end up having the source node appearing *twice*: once inside the group, and once outside the group in the new material node-network. If you include an output node in the group, there will not be an output socket available *from* the group! Info Editor Input nodes Interactively Interface Make Group Menu Mode Move Move to parent node tree, remove from group. Node Groups Once you have appended a Node Tree to your blend-file, you can make use of it in the Node editor by pressing :kbd:`Shift-A`, :menuselection:`Add --> Group`, then selecting the appended group. The "control panel" of the Group include the individual controls for the grouped nodes. You can change them by working with the Group node like any other node. Output node Panel Recursion Recursive node groups are prohibited for all the current node systems to prevent infinite recursion. A node group can never contain itself (or another group that contains it). Reference Remember that the essential idea is that a group should be an easily-reusable, self-contained software component. Material node groups should **not** include: Selecting a set of nodes, ending with the destination group node, and pressing :menuselection:`Group --> Group Insert` will move those nodes into that group. The moved nodes are collected into a group of their own to preserve their connection context, having their own group input and output nodes. The group's existing input and output nodes are updated with new sockets, if any, from the new nodes. The node group must be edited to contain a single *Group Input* and a single *Group Output* node. Separate :kbd:`P` Separate selected nodes from the node group. Sockets can be added, re-ordered, or removed, descriptive names can be added and the details of the input data value defined here. The :kbd:`Alt-G` tool removes the group and places the individual nodes into your editor workspace. No internal connections are lost, and now you can thread internal nodes to other nodes in your workspace. The interface panel for editing groups. To create a node group, in the Node editor, select the nodes you want to include, then press :kbd:`Ctrl-G`, :menuselection:`Group --> Make Group`. A node group will have a green title bar. All of the selected nodes will now be contained within the node group. Default naming for the node group is "NodeGroup", "NodeGroup.001" etc. There is a name field in the node group you can click into to change the name of the group. Change the name of the node group to something meaningful. When appending node groups from one blend-file to another, Blender does not make a distinction between material node groups or composite node groups, so it is recommended to use some naming convention that will allow you to easily distinguish between the two types. Ungroup What **not** to include in your groups (all modes of Node editors) When a node group is created, new *Group Input* and *Group Output* nodes are generated to represent the data flow into and out of the group. When created, connections to input sockets coming from unselected nodes will become attached to new sockets on the *Group Input* node. Similarly, outgoing connections to input sockets of unselected nodes will become attached to the new *Group Output* node. With a node group selected, :kbd:`Tab` expands the node to a frame, and the individual nodes within it are shown. You can move them around, play with their individual controls, re-thread them internally, etc. just like you can if they were a normal part of the editor view. You will not be able, though, to thread them to a node outside the group; you have to use the external sockets on the side of the node group. To add or remove nodes from the group, you need to ungroup them. While :kbd:`Tab` can be used to both enter and exit a group, :kbd:`Ctrl-Tab` only exits. Project-Id-Version: Blender 2.79 Manual 2.79
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
 :kbd:`Alt-G` :kbd:`Ctrl-G` :kbd:`Tab`, :kbd:`Ctrl-Tab` :menuselection:`Tập Tin (File) --> Kết Nối/Bổ Sung (Link/Append)` :menuselection:`Chuyển về Cây Nút Phụ Huynh -- Go to Parent Node Tree` :menuselection:`Nhóm (Group) --> Biên Soạn Nhóm (Edit Group)` :menuselection:`Nhóm (Group) --> Chèn Thêm Nhóm (Group Insert)` :menuselection:`Nhóm (Group) --> Tạo Nhóm (Make Group)` :menuselection:`Nhóm (Group) --> (Rã Nhóm) Ungroup` :menuselection:`Vùng Tính Chất (Properties region) --> Giao Diện (Interface)` Toàn Bộ các Chế Độ -- All Modes Các nhóm nút lồng nhau cũng được hỗ trợ nữa, chẳng hạn, một nhóm nút có thể được chèn vào hoặc được tạo bên trong một nhóm nút khác. Bổ Sung các Nhóm Nút -- Appending Node Groups Một ví dụ: Nếu bạn đã tạo một nguyên liệu mà bạn muốn sử dụng với các yếu tố đầu vào khác nhau, ví dụ: màu khuếch tán: nhựa màu đỏ, nhựa màu xanh lá cây, thì bạn có thể tạo các nguyên liệu riêng biệt bằng nút *Biến thành Đơn Người Dùng* (*Make Single User*) cho mỗi màu khác nhau, với bản sao của phần cây mô tả vật liệu nhựa. Nếu bạn muốn chỉnh sửa nguyên liệu, thì bạn cần phải chỉnh sửa lại tất cả các nguyên liệu. Một phương pháp tốt hơn để tái sử dụng là tạo các nhóm nút, chỉ cho lộ ra các tham số đầu vào (ví dụ: màu khuếch tán) (*diffuse color*). Nói một cách khái niệm, việc nhóm các nút lại cho phép bạn chỉ định một *tập hợp* các nút mà bạn có thể coi như là \một đơn nút\. Các nhóm nút tương tự như các hàm trong lập trình vậy. Sau đó, bạn có thể tái sử dụng chúng bên trong, cái mà sau đó được gọi là \Nhóm Nút (NodeGroups)\ hoặc trong các tập tin blend khác, khi chèn thêm vào, được gọi là \Cây Nút (NodeTrees)\. Sao Chép -- Copy Sao chép vào cây nút phụ huynh, giữ nguyên nhóm. Biên Soạn Nhóm -- Edit Group Trình Biên Soạn -- Editor Ví dụ về nhóm nút. Ví dụ về nhóm nút mở rộng. Chèn Thêm vào Nhóm -- Group Insert Việc nhóm các nút có thể đơn giản hóa một cây nút bằng cách cho phép việc tạo một thực thể và ẩn dấu các phần của cây. Cả hai loại nút, nút chất liệu và nút tổng hợp, đều có thể nhóm lại được. Tiêu Đề -- Header Phím Tắt -- Hotkey Nếu trong quá trình phát triển nhóm nút, một tham số bổ sung cần phải được đưa vào nhóm thì một ổ cắm cần phải được bổ sung vào phần *Đầu Vào của Nhóm* (Group Input). Điều này có thể dễ dàng thực hiện bằng cách cho thêm một kết nối từ ổ cắm rỗng ở phía bên phải của *Đầu Vào của Nhóm* (Group Input) vào ổ cắm đầu vào mong muốn trên nút yêu cầu đầu vào. Đối với dữ liệu mà bạn muốn cung cấp ra khỏi nhóm, làm tương tự như quá trình này trên *Đầu Ra của Nhóm* (Group Output). Nếu bạn có nhiều đầu vào hoặc đầu ra thì chúng có thể được sắp xếp lại bằng cách chọn ổ cắm trong danh sách và sau đó di chuyển nó lên hoặc xuống bằng các nút mũi tên ở bên phải của bảng điều khiển. Các nút dấu cộng lớn hơn bên dưới danh sách sẽ cộng thêm một ổ cắm không kết nối cùng loại như ổ cắm được chọn, hoặc một ổ cắm giá trị, nếu không có lựa chọn nào. Dấu cộng nhỏ được khoanh tròn ở dưới cùng của danh sách có một số chức năng thanh lọc để tạo thuận lợi cho việc tìm kiếm các nút nếu nhóm có một số lượng lớn các ổ cắm. Nếu bạn bao gồm một nút nguồn trong nhóm của bạn thì kết quả sẽ là bạn có nút nguồn xuất hiện *hai lần*: một nằm bên trong nhóm và một nằm bên ngoài nhóm trong mạng lưới nút nguyên liệu mới. Nếu bạn bao gồm một nút đầu ra trong nhóm thì bạn sẽ không có một ổ cắm đầu ra có *từ* (ra khỏi) nhóm! Trình Biên Soạn Thông Tin -- Info Editor Nút Đầu Vào -- Input nodes Tương Tác -- Interactively Giao Diện -- Interface Tạo Nhóm -- Make Group Trình Đơn -- Menu Chế Độ -- Mode Di Chuyển -- Move Chuyển về cây nút phụ huynh, xóa khỏi nhóm Nhóm Nút -- Node Groups Một khi bạn đã bổ sung thêm một cây nút vào tập tin blend của mình, bạn có thể sử dụng nó trong Trình Biên Soạn Nút (Node editor) bằng cách nhấn phím :kbd:`Shift-A`, :menuselection:`Thêm (Add) --> Nhóm (Group)`, sau đó chọn nhóm đã bổ sung. \Bảng điều khiển\ (control panel) của Nhóm bao gồm cá nhân các điều khiển cho các nút đã được nhóm lại. Bạn có thể thay đổi chúng bằng cách làm việc với nút Nhóm giống như với bất kỳ nút nào khác. Nút Đầu Ra -- Output node Bảng -- Panel Đệ Quy -- Recursion Các nhóm nút đệ quy sẽ bị cấm hoạt động đối với toàn bộ hệ thống nút hiện tại, nhằm ngăn chặn sự đệ quy vô hạn. Một nhóm nút không bao giờ có thể chứa chính bản thân nó (hoặc nhóm khác có chứa chính bản thân nó). Tham Chiếu -- Reference Hãy nhớ rằng điều thiết yếu là một nhóm phải là một thành phần phần mềm dễ tái sử dụng, khép kín. Nhóm nút nguyên liệu **không nên** bao gồm: Chọn một tập hợp các nút, kết thúc bằng nút nhóm đích và nhấn vào :menuselection:`Nhóm (Group) --> Chèn Thêm vào Nhóm (Group Insert)` để di chuyển các nút ấy vào nhóm đó. Các nút đã di chuyển sẽ được thu thập thành một nhóm của riêng chúng, để bảo vệ bối cảnh kết nối của chúng, bao gồm có các nút đầu vào và đầu ra của riêng mình. Các nút đầu vào và đầu ra hiện tại của nhóm sẽ được cập nhật với các ổ cắm mới, nếu có, từ các nút mới. Nhóm nút phải được biên soạn để chỉ chứa một đơn *Đầu Vào của Nhóm* (Group Input) và một đơn *Đầu Ra của Nhóm* (Group Output) mà thôi. Phân Tách (Separate) -- :kbd:`P` -- Separate :kbd:`P` Tách các nút đã chọn khỏi nhóm nút. Các ổ cắm có thể được thêm vào, được sắp xếp lại hoặc bị loại bỏ. Các tên có tính diễn giải có thể được cho thêm vào và các chi tiết của giá trị dữ liệu đầu vào sẽ được xác định tại đây. Công cụ :kbd:`Alt-G` loại bỏ nhóm và đặt các nút riêng biệt vào không gian làm việc của trình biên soạn của bạn. Các kết nối nội bộ đều được bảo tồn và bây giờ bạn có thể kéo dây mắc nối các nút nội bộ sang các nút khác trong địa phận làm việc của bạn. Bảng giao diện để biên soạn nhóm. Để tạo một nhóm nút, trong trình biên soạn Nút (Node editor), chọn các nút bạn muốn bao gồm vào, sau đó nhấn :kbd:`Ctrl-G`, :menuselection:`Nhóm (Group) --> Tạo Nhóm (Make Group)`. Nhóm nút sẽ có thanh tiêu đề màu lục. Lúc này, tất cả các nút đã chọn sẽ nằm trong nhóm nút. Đặt tên mặc định cho nhóm nút là \NodeGroup\, \NodeGroup.001\ v.v. Có một ô tên trong nhóm nút mà bạn có thể bấm vào để thay đổi tên của nhóm. Hãy đổi tên của nhóm nút thành một cái gì đó có ý nghĩa. Khi bổ sung các nhóm nút từ một tập tin blend sang một cái khác, Blender không phân biệt giữa nhóm nút nguyên liệu hoặc nhóm nút kết hợp, cho nên, chúng tôi khuyên bạn nên sử dụng một số quy ước đặt tên, cho phép bạn dễ dàng phân biệt giữa hai loại. Rã Nhóm -- Ungroup Những cái **không** nên bao gồm trong các nhóm của bạn (trong tất cả các chế độ của những Trình Biên Soạn Nút) Khi một nhóm nút được kiến tạo, các nút *Đầu Vào của Nhóm* (Group Input) và *Đầu Ra của Nhóm* (Group Output) mới sẽ được sinh tạo ra để biểu thị luồng chảy của dữ liệu vào và ra khỏi nhóm. Khi được kiến tạo, các kết nối đến ổ cắm đầu vào đến từ các nút không được chọn sẽ được gắn vào các ổ cắm mới trên nút *Đầu Vào của Nhóm*. Tương tự, các kết nối ra ngoài đến các ổ cắm đầu vào của các nút không được chọn sẽ được gắn vào nút *Đầu Ra của Nhóm* mới. Với một nhóm nút được chọn, phím :kbd:`Tab` sẽ mở rộng nút ra một khung cửa sổ, và cá nhân các nút trong đó sẽ được hiển thị. Bạn có thể di chuyển chúng xung quanh, thử nghiệm với các cá nhân điều khiển của chúng, thay đổi sự kết nối nội bộ của chúng v.v.. giống như bạn có thể làm nếu chúng là một phần bình thường trong khung nhìn của trình biên soạn. Song, bạn sẽ không thể kết nối chúng vào một nút bên ngoài nhóm;  bạn phải sử dụng các ổ cắm bên ngoài, ở trên mép của nhóm nút. Để cho thêm hoặc loại bỏ các nút trong nhóm, bạn cần phải rã nhóm chúng trước đã. Trong khi phím :kbd:`Tab` có thể được sử dụng để nhập hoặc thoát nhóm, :kbd:`Ctrl-Tab` chỉ dùng để thoát mà thôi. 