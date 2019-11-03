��          �               �  #   �  :   �  	     
   &     1  �   =  #   1  	   U  �   _    �     �     �               ,  �   <     9     ?  	   F  	   P  	   Z  	   d     n  r  �     �  �    ?   �	  :   �	  (   7
     `
     |
  �   �
  #        �  �   �  h  D  *   �  &   �     �          2  �   E     B     R     h  "   �     �     �  5   �  r       �   :menuselection:`Bone --> Relations` A :ref:`ui-data-id` to select the bone to set as a parent. All Modes Bone Group Bone Layers Bones relationships also have important consequences on how selections of multiple bones behave when transformed. There are many different situations which may not be included on this list, however, this should give a good idea of the problem: By default, children bones inherit: Connected Exactly like standard children objects. You can modify this behavior on a per-bone basis, using the Relations panel in the *Bones* tab: In the *3D View* editor, use the menu :menuselection:`Armature --> Move Bone To Layer` or :menuselection:`Pose --> Move Bone To Layer` or press :kbd:`M` to show the usual pop-up layers menu. Note that this way, you assign the same layers to all selected bones. Inherit Rotation Inherit Scale Mode Moving Bones between Layers Object Children Obviously, you have to be in *Edit Mode* or *Pose Mode* to move bones between layers. Note that as with objects, bones can lay in several layers at once, just use the usual :kbd:`Shift-LMB` clicks... First of all, you have to select the chosen bone(s)! Panel Parent Parenting Pose Mode Reference Relations Relative Parenting So, when posing a chain of bones, you should always edit its elements from the root bone to the tip bone. This process is known as *forward kinematics* (FK). We will see in a :ref:`later page <bone-constraints-inverse-kinematics>` that Blender features another pose method, called *inverse kinematics* (IK), which allows you to pose a whole chain just by moving its tip. Transformations Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-10-26 00:56+1100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 :menuselection:`Xương (Bone) --> Mối Quan Hệ (Relations)` A :ref:`ui-data-id` to select the bone to set as a parent. Toàn Bộ các Chế Độ -- All Modes Nhóm Xương -- Bone Group -- Bone Layers Bones relationships also have important consequences on how selections of multiple bones behave when transformed. There are many different situations which may not be included on this list, however, this should give a good idea of the problem: By default, children bones inherit: Kết Nối -- Connected Exactly like standard children objects. You can modify this behavior on a per-bone basis, using the Relations panel in the *Bones* tab: In the *3D View* editor, use the menu :menuselection:`Cốt (Armature) --> Di Chuyển Xương vào Tầng Lớp (Move Bone To Layer)` or :menuselection:`Tư Thế (Pose) --> Di Chuyển Xương vào Tầng Lớp (Move Bone To Layer)` or press :kbd:`M` to show the usual pop-up layers menu. Note that this way, you assign the same layers to all selected bones. Thừa Kế Độ Xoay -- Inherit Rotation Thừa Kế Tỷ Lệ -- Inherit Scale Chế Độ -- Mode -- Moving Bones between Layers -- Object Children Obviously, you have to be in *Edit Mode* or *Pose Mode* to move bones between layers. Note that as with objects, bones can lay in several layers at once, just use the usual :kbd:`Shift-LMB` clicks... First of all, you have to select the chosen bone(s)! Bảng -- Panel Phụ Huynh -- Parent Phụ Huynh Hóa -- Parenting Chế Độ Tư Thế -- Pose Mode Tham Chiếu -- Reference Mối Quan Hệ -- Relations Phụ Huynh Hóa Tương Đối -- Relative Parenting So, when posing a chain of bones, you should always edit its elements from the root bone to the tip bone. This process is known as *forward kinematics* (FK). We will see in a :ref:`later page <bone-constraints-inverse-kinematics>` that Blender features another pose method, called *inverse kinematics* (IK), which allows you to pose a whole chain just by moving its tip. -- Transformations 