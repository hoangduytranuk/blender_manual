��    )      d              �  6   �  :   �          ,  "   :  )   ]  A   �     �     �     �     �     �       �   !  x  �  R   %     x     �     �     �  
   �     �     �     �     �     �     �       	        !     4  �   ;     �               !     >  @  ]  >   �	  �   �	  �  r
  6      :   W     �     �  >   �  )   �  A        X  (   h      �  8   �  A   �     -  �   C  x  �  R   G  =   �  !   �     �       "   #  4   F     {  V   �  &   �  .        >  ,   U     �  5   �  	   �  �   �     �  0   �  2   �  `     a   z  @  �  >     �   \   :doc:`Curve Deform </modeling/modifiers/deform/curve>` :doc:`Lattice Deform </modeling/modifiers/deform/lattice>` :kbd:`Alt-P` :kbd:`Ctrl-P` :menuselection:`Object --> Parent` :ref:`Follow Path <curve-path-animation>` Blender supports many different types of parenting, listed below: Bone Bone Parent Clear Parent Clear Parent Inverse Clear and Keep Transformation Hotkey If you want to follow along with the above description here is the blend-file used to describe *Object (Keep Transform)* parenting method: In *Object Mode*, select the child/children and then the parent object. :kbd:`Tab` into *Edit Mode* and on the parent object select either one vertex that defines a single point, or select three vertices that define an area (the three vertices do not have to form a complete face; they can be any three vertices of the parent object), and then press :kbd:`Ctrl-P` and confirm. It is in fact a sort of "reversed" :doc:`hook </modeling/modifiers/deform/hooks>`. Known Limitations Make Parent Menu Mode Move Child Non-Uniform Scale Object Object (Keep Transform) Parent Object Mode Object Parent Options Parenting Objects Reference Relative Parenting Setups The *Set Parent To* pop-up menu is context-sensitive, which means the number of entries it displays can change depending on what objects are selected when the :kbd:`Ctrl-P` shortcut is used. Vertex Vertex (Triangle) Vertex Parent Vertex Parent from Edit Mode Vertex Parent from Object Mode You can *move* a child object to its parent by clearing its origin. The relationship between the parent and child is not affected. Select the child object and press :kbd:`Alt-O`. By confirming the child object will snap to the parent's location. Use the *Outliner* view to verify that the child object is still parented. You can *remove* a parent-child relationship via :kbd:`Alt-P`. `File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend <https://wiki.blender.org/wiki/File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend>`__. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-04-24 16:51-0400
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 :doc:`Curve Deform </modeling/modifiers/deform/curve>` :doc:`Lattice Deform </modeling/modifiers/deform/lattice>` :kbd:`Alt-P` :kbd:`Ctrl-P` :menuselection:`Vật Thể (Object) --> Phụ Huynh (Parent)` :ref:`Follow Path <curve-path-animation>` Blender supports many different types of parenting, listed below: Xương -- Bone Phụ huynh của xương -- Bone Parent Xóa Phụ Huynh -- Clear Parent Đảo Nghịch Xóa Phụ Huynh -- Clear Parent Inverse Xóa nhưng Duy Trì Biến Hóa -- Clear and Keep Transformation Phím Tắt -- Hotkey If you want to follow along with the above description here is the blend-file used to describe *Object (Keep Transform)* parenting method: In *Object Mode*, select the child/children and then the parent object. :kbd:`Tab` into *Edit Mode* and on the parent object select either one vertex that defines a single point, or select three vertices that define an area (the three vertices do not have to form a complete face; they can be any three vertices of the parent object), and then press :kbd:`Ctrl-P` and confirm. It is in fact a sort of "reversed" :doc:`hook </modeling/modifiers/deform/hooks>`. Những Hạn Chế Từng Biết Đến -- Known Limitations Đặt Phụ Huynh -- Make Parent Trình Đơn -- Menu Chế Độ -- Mode Di Chuyển Con Cái -- Move Child Đổi Tỷ Lệ Đồng Đều -- Non-Uniform Scale Vật Thể -- Object Phụ Huynh của Vật Thể (Duy Trì Biến Hóa) -- Object (Keep Transform) Parent Chế Độ Vật Thể -- Object Mode Phụ Huynh của Vật Thể -- Object Parent Tùy Chọn -- Options Vật Thể Phụ Huynh -- Parenting Objects Tham Chiếu -- Reference Phụ Huynh Hóa Tương Đối -- Relative Parenting -- Setups The *Set Parent To* pop-up menu is context-sensitive, which means the number of entries it displays can change depending on what objects are selected when the :kbd:`Ctrl-P` shortcut is used. Điểm Đỉnh -- Vertex Điểm Đỉnh (Tam Giác) -- Vertex (Triangle) Phụ Huynh của Điểm Đỉnh -- Vertex Parent Phụ Huynh của Điểm Đỉnh trong Chế Độ Biên Soạn -- Vertex Parent from Edit Mode Phụ Huynh của Điểm Đỉnh trong Chế Độ Vật Thể -- Vertex Parent from Object Mode You can *move* a child object to its parent by clearing its origin. The relationship between the parent and child is not affected. Select the child object and press :kbd:`Alt-O`. By confirming the child object will snap to the parent's location. Use the *Outliner* view to verify that the child object is still parented. You can *remove* a parent-child relationship via :kbd:`Alt-P`. `File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend <https://wiki.blender.org/wiki/File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend>`__. 