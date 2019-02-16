��    @                      �        �  2   �  2        K     b  	   v    �  	   �     �     �     �     �  k   �     Q  �   n     %     C     U      p     �     �     �     �  F   �     	     	      	     0	  M   A	     �	     �	     �	  �   �	     c
  5  h
     �  	   �     �     �  ?   �  )     �   ,     �                 #   1     U  E   ^     �  =   �  k   �  0   f  a   �  .   �  
   (     3  0   F     w  p   �     �  �     �  �  �   �     Q  2   _  2   �     �  A   �         >  (   O     x  5   �  4   �  d   �  k   `  ]   �  �   *     �  /   �  E   /      u     �     �     �     �  F   �     :     H  3   e     �  M   �     �  I     n   W  �   �     b  5  v     �     �     �     �  ?   �  )   :  �   d  ;   '     c  5   t  G   �  #   �       E   0     v  =   �  k   �  0   8   a   i   .   �      �      !  0   !     L!  p   d!     �!  �   �!   (not available for locked groups) Unassigns the selected Vertices from all groups. After this operation has been performed, the vertices will no longer be contained in any vertex group. :kbd:`Ctrl-G` :menuselection:`Mesh --> Vertex --> Vertex Groups` :menuselection:`Object Data tab --> Vertex Groups` A :ref:`ui-list-view`. Active Vertex Group Add ``+`` Add a Copy of the active Vertex Group as a new Group. The new group will be named like the original group with "_copy" appended at the end of its name. And it will contain associations to exactly the same vertices with the exact same weights as in the source vertex group. All Modes Assign Clear Active Group Copy Vertex Group Copy Vertex Group to Selected Copy Vertex Groups of this Mesh to all linked Objects which use the same mesh data (all users of the data). Copy Vertex Groups to Linked Copy all Vertex Groups to other Selected Objects provided they have matching indices (typically this is true for copies of the mesh which are only deformed and not otherwise edited). Create an empty vertex group. Delete All Groups Delete All Unlocked Groups Deletes the active vertex group. Deselect Editing Vertex Groups Hotkey Invert Group Locks. Lets you select the group that will become the active one (menu only). Lock Lock All Lock Invert All Lock all groups. Locks the group from being editable. You can only rename or delete the group. Menu Mirror Vertex Group Mirror Vertex Group (Topology) Mirror all Vertex Groups, flip weights and/or names, editing only selected vertices, flipping when both sides are selected; otherwise copy from unselected. Mode Multiple objects sharing the same mesh data have the peculiar property that the group names are stored on the object, but the weights in the mesh. This allows you to name groups differently on each object, but take care because removing a vertex group will remove the group from all objects sharing this mesh. Panel Reference Remove Remove ``-`` Remove all Vertex Groups from the Object that are *not* locked. Remove all Vertex Groups from the Object. Remove all assigned vertices from the active Group. The group is made empty. Note that the vertices may still be assigned to other Vertex Groups of the Object. (not available for locked groups). Remove from All Groups Select Set Active Group Sort Vertex Groups Sorts Vertex Groups alphabetically. Specials The :ref:`modeling_meshes_editing_topology-mirror` option is enabled. The Vertex Group panel. The weight value that gets assigned to the selected vertices. To assign the Selected vertices to the active group with the weight as defined in the *Weight* (see below). To deselect all vertices contained in the group. To remove the selected vertices from the active group (and thus also delete their weight values). To select all vertices contained in the group. Unlock All Unlock all groups. Vertex Group Panel in Edit or Weight Paint Mode. Vertex Groups Panel Vertex Groups are maintained within the *Object Data* Properties Editor, and there in the *Vertex Groups* panel. Weight When you switch either to *Edit Mode* or to *Weight Paint Mode* Vertex weights can be edited. The same operations are available in the 3D Views menu :menuselection:`Mesh --> Vertices --> Vertex Groups` or :kbd:`Ctrl-G`. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 (not available for locked groups) Unassigns the selected Vertices from all groups. After this operation has been performed, the vertices will no longer be contained in any vertex group. :kbd:`Ctrl-G` :menuselection:`Mesh --> Vertex --> Vertex Groups` :menuselection:`Object Data tab --> Vertex Groups` A :ref:`ui-list-view`. Nhóm Điểm Đỉnh Đang Hoạt Động -- Active Vertex Group Cộng Thêm ``+`` -- Add ``+`` Add a Copy of the active Vertex Group as a new Group. The new group will be named like the original group with "_copy" appended at the end of its name. And it will contain associations to exactly the same vertices with the exact same weights as in the source vertex group. Toàn Bộ các Chế Độ -- All Modes Chỉ Định -- Assign Xóa Nhóm Đang Hoạt Động -- Clear Active Group Sao Chép Nhóm Điểm Đỉnh -- Copy Vertex Group Sao Chép Nhóm Điểm Đỉnh đến những cái Được Chọn -- Copy Vertex Group to Selected Copy Vertex Groups of this Mesh to all linked Objects which use the same mesh data (all users of the data). Sao Chép Nhóm Điểm Đỉnh sang những cái Kết Nối -- Copy Vertex Groups to Linked Copy all Vertex Groups to other Selected Objects provided they have matching indices (typically this is true for copies of the mesh which are only deformed and not otherwise edited). Create an empty vertex group. Xóa Toàn Bộ các Nhóm -- Delete All Groups Xóa Toàn bộ các Nhóm Không Khóa -- Delete All Unlocked Groups Deletes the active vertex group. Hủy Chọn -- Deselect  -- Editing Vertex Groups Phím Tắt -- Hotkey Invert Group Locks. Lets you select the group that will become the active one (menu only). Khóa -- Lock Khóa Toàn Bộ -- Lock All Đảo Nghịch Khóa Toàn Bộ -- Lock Invert All Lock all groups. Locks the group from being editable. You can only rename or delete the group. Trình Đơn -- Menu Phản Chiếu Đối Xứng Nhóm Điểm Đỉnh -- Mirror Vertex Group Phản Chiếu Đối Xứng Nhóm Điểm Đỉnh (Cấu Trúc Liên Kết) -- Mirror Vertex Group (Topology) Mirror all Vertex Groups, flip weights and/or names, editing only selected vertices, flipping when both sides are selected; otherwise copy from unselected. Chế Độ -- Mode Multiple objects sharing the same mesh data have the peculiar property that the group names are stored on the object, but the weights in the mesh. This allows you to name groups differently on each object, but take care because removing a vertex group will remove the group from all objects sharing this mesh. Bảng -- Panel Tham Chiếu -- Reference Xóa -- Remove Xóa -- Remove ``-`` Remove all Vertex Groups from the Object that are *not* locked. Remove all Vertex Groups from the Object. Remove all assigned vertices from the active Group. The group is made empty. Note that the vertices may still be assigned to other Vertex Groups of the Object. (not available for locked groups). Xóa Khỏi Toàn Bộ các Nhóm -- Remove from All Groups Chọn -- Select Đặt Nhóm Đang Hoạt Động -- Set Active Group Sắp Xếp Thứ Tự các Nhóm Điểm Đỉnh -- Sort Vertex Groups Sorts Vertex Groups alphabetically. Đặc Biệt -- Specials The :ref:`modeling_meshes_editing_topology-mirror` option is enabled. The Vertex Group panel. The weight value that gets assigned to the selected vertices. To assign the Selected vertices to the active group with the weight as defined in the *Weight* (see below). To deselect all vertices contained in the group. To remove the selected vertices from the active group (and thus also delete their weight values). To select all vertices contained in the group. -- Unlock All Unlock all groups. Vertex Group Panel in Edit or Weight Paint Mode.  -- Vertex Groups Panel Vertex Groups are maintained within the *Object Data* Properties Editor, and there in the *Vertex Groups* panel. Trọng Lượng -- Weight When you switch either to *Edit Mode* or to *Weight Paint Mode* Vertex weights can be edited. The same operations are available in the 3D Views menu :menuselection:`Mesh --> Vertices --> Vertex Groups` or :kbd:`Ctrl-G`. 