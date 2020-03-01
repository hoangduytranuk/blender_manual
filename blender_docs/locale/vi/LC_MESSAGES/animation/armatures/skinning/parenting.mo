��          �               ,     -     ;     Y  �   p     �     �                
  	   $  9  .  �  h     -     D     V  ?  l  �  �     Z     h     �  �   �     !	     5	     K	     `	  N   t	     �	  9  �	      =      -   ^  =   �  ?  �   :kbd:`Ctrl-P` :ref:`weight-painting-bones`. Armature Deform Parent Armature Deform Parenting is a way of creating and setting up an :doc:`Armature Modifier </modeling/modifiers/deform/armature>`. Example Hotkey Menu Mode Object Mode and Pose Mode Reference To use *Armature Deform Parenting* you must first select all the child objects that will be influenced by the armature and then lastly, select the armature object itself. Once all the child objects and the armature are selected, press :kbd:`Ctrl-P` and select *Armature Deform* in the *Set Parent To* pop-up menu. When parenting it will create empty :doc:`vertex groups </modeling/meshes/properties/vertex_groups/index>` on the child objects (if they do not already exist) for and named after each deforming bone in the armature. The newly created vertex groups will be empty. This means they will not have any weights assigned. Vertex groups will only be created for bones which are setup as deforming (:menuselection:`Properties Editor --> Bone --> Deform Panel`). With Automatic Weights With Empty Groups With Envelope Weights Works in a similar way to *With Automatic Weights*. The difference is that the influences are calculated based on the :ref:`Bone Envelopes <armature-bones-envelope>` settings. It will assign a weight to each vertex group the vertices that is inside its bone's influence volume, depending on their distance to this bone. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-01-29 17:18-0500
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 :kbd:`Ctrl-P` :ref:`weight-painting-bones`. -- Armature Deform Parent Armature Deform Parenting is a way of creating and setting up an :doc:`Armature Modifier </modeling/modifiers/deform/armature>`. Ví Dụ -- Example Phím Tắt -- Hotkey Trình Đơn -- Menu Chế Độ -- Mode Chế Độ Vật Thể và Chế Độ Tư Thế -- Object Mode and Pose Mode Tham Chiếu -- Reference To use *Armature Deform Parenting* you must first select all the child objects that will be influenced by the armature and then lastly, select the armature object itself. Once all the child objects and the armature are selected, press :kbd:`Ctrl-P` and select *Armature Deform* in the *Set Parent To* pop-up menu. When parenting it will create empty :doc:`vertex groups </modeling/meshes/properties/vertex_groups/index>` on the child objects (if they do not already exist) for and named after each deforming bone in the armature. The newly created vertex groups will be empty. This means they will not have any weights assigned. Vertex groups will only be created for bones which are setup as deforming (:menuselection:`Trình Biên Soạn Tính Chất (Properties Editor) --> Xương (Bone) --> Bảng Biến Dạng (Deform Panel)`). Với Trọng Lượng Tự Động -- With Automatic Weights Với các Nhóm Trống -- With Empty Groups Với Trọng Lượng từ Vỏ Bao -- With Envelope Weights Works in a similar way to *With Automatic Weights*. The difference is that the influences are calculated based on the :ref:`Bone Envelopes <armature-bones-envelope>` settings. It will assign a weight to each vertex group the vertices that is inside its bone's influence volume, depending on their distance to this bone. 