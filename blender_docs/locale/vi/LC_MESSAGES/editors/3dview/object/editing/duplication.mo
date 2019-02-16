��    *      l              �  �   �     f     s  ,   �  -   �  C   �  <   !  H   ^  A  �  �   �  �   k  	   �     	          +     4    ;  �   O  �   �  c   �	  �   �	     �
     �
     �
     �
     �
     �
     �
  	   �
  I   �
     3  &   S  �   z  �        �  x   T  T  �  �   "  ~   �    p  �   �  �  !  �   �     �     �  ,   �  -   �  C   �  <   =  H   z  A  �  �     �   �          2     K     a     {    �  �   �  �   H  c   �  �   H     �  0   �     ,     G     \  &   p     �     �  I   �       &   +  �   R  �   �     �  x   ,   T  �   �   �!  ~   �"    H#  �   f%   :doc:`Linked Libraries </data_system/linked_libraries>` are also a form of duplication. Any object or data-block in other blend-files can be reused in the current file. :kbd:`Alt-D` :kbd:`Shift-D` :menuselection:`Object --> Duplicate Linked` :menuselection:`Object --> Duplicate Objects` :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate Linked` :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate` :ref:`data-system-datablock-make-single-user` for unlinking data-blocks. A common table has a top and four legs. Model one leg, and then make linked duplicates three times for each of the remaining legs. If you later make a change to the mesh, all the legs will still match. Linked duplicates also apply to a set of drinking glasses, wheels on a car... anywhere there is repetition or symmetry. As a mesh is edited in *Edit Mode* in one object, the same occurs in the other cube as well. The mesh data are links, not copies. As in the previous example, the newly created cube has inherited the material of the original cube. The material properties are linked, not copied. Duplicate Duplication Edit and Object Modes Examples Hotkey If you want to make changes to an object in the new linked duplicate independently of the original object, you will have to manually make the object a "single-user" copy by :kbd:`LMB` the number in the *Object Data* panel of the Properties editor. (See :ref:`ui-data-block`). If you want transform properties (i.e. object data-blocks) to be "linked", see the page on :doc:`parenting </editors/3dview/object/properties/relations/parents>`. In contrast, if one of these two cubes is rotated or rescaled in Object Mode, the other remains unchanged. The transform properties are copied, not linked. In the *Duplicate Objects* Operator panel the *Linked* checkbox is checked unlike with *Duplicate*. Likewise, if one cube is edited in Object Mode, the other cube remains unchanged. The new object's transform properties or data-block is a copy, not linked. Linked Linked Duplicates Linked Library Duplication Menu Mode Object Mode Panel Reference See above if you want separate copies of the data-blocks normally linked. The Cube object was duplicated. The Cube object was linked duplicated. The object ``Cube`` was duplicated, using :kbd:`Shift-D`. Both these cubes has separate meshes with unique names: ``Cube`` and ``Cube.001``. The object ``Cube`` was linked duplicated, using :kbd:`Alt-D`. Though both these cubes are separate objects with unique names: ``Cube`` and ``Cube.001``, the single mesh named ``Cube``, is shared by both. The original left cube is being edited, the duplicated right cube remains unchanged. The mesh data has been copied, not linked. There are two types of object duplication, being `Duplicate`_ and `Linked Duplicates`_ which instance their Object Data. This copy is a new object, which shares some data-blocks with the original object (by default, all the Materials, Textures, and F-Curves), but which has copied others, like the mesh, for example. This is why this form of duplication is sometimes called "shallow link", because not all data-blocks are shared; some of them are "hard copied"! This will create a visually-identical copy of the selected object(s). The copy is created at the same position as the original object and you are automatically placed in *Grab* mode. See the examples below. When the cube was duplicated, it inherited the material of the original cube. The material properties were linked, not copied. You also have the choice of creating a *Linked Duplicate* rather than a *Duplicate*; this is called a deep link. This will create a new object with **all** of its data linked to the original object. If you modify one of the linked objects in *Edit Mode*, all linked copies are modified. Transform properties (object data-blocks) still remain copies, not links, so you still can rotate, scale, and move freely without affecting the other copies. Reference Expl. :ref:`Duplicate Example <expl-object-link-duplicate>` for the discussions below. You can choose which types of data-block will be linked or copied when duplicating: in the :ref:`User Preferences <prefs-editing-duplicate-data>`. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-14 21:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :doc:`Linked Libraries </data_system/linked_libraries>` are also a form of duplication. Any object or data-block in other blend-files can be reused in the current file. :kbd:`Alt-D` :kbd:`Shift-D` :menuselection:`Object --> Duplicate Linked` :menuselection:`Object --> Duplicate Objects` :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate Linked` :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate` :ref:`data-system-datablock-make-single-user` for unlinking data-blocks. A common table has a top and four legs. Model one leg, and then make linked duplicates three times for each of the remaining legs. If you later make a change to the mesh, all the legs will still match. Linked duplicates also apply to a set of drinking glasses, wheels on a car... anywhere there is repetition or symmetry. As a mesh is edited in *Edit Mode* in one object, the same occurs in the other cube as well. The mesh data are links, not copies. As in the previous example, the newly created cube has inherited the material of the original cube. The material properties are linked, not copied. Sao Chép -- Duplicate Sao Chép -- Duplication Edit and Object Modes Các Ví Dụ -- Examples Phím Tắt -- Hotkey If you want to make changes to an object in the new linked duplicate independently of the original object, you will have to manually make the object a "single-user" copy by :kbd:`LMB` the number in the *Object Data* panel of the Properties editor. (See :ref:`ui-data-block`). If you want transform properties (i.e. object data-blocks) to be "linked", see the page on :doc:`parenting </editors/3dview/object/properties/relations/parents>`. In contrast, if one of these two cubes is rotated or rescaled in Object Mode, the other remains unchanged. The transform properties are copied, not linked. In the *Duplicate Objects* Operator panel the *Linked* checkbox is checked unlike with *Duplicate*. Likewise, if one cube is edited in Object Mode, the other cube remains unchanged. The new object's transform properties or data-block is a copy, not linked. Kết Nối -- Linked Bản Sao Chép Kết Nối -- Linked Duplicates Linked Library Duplication Trình Đơn -- Menu Chế Độ -- Mode Chế Độ Vật Thể -- Object Mode Bảng -- Panel Tham Chiếu -- Reference See above if you want separate copies of the data-blocks normally linked. The Cube object was duplicated. The Cube object was linked duplicated. The object ``Cube`` was duplicated, using :kbd:`Shift-D`. Both these cubes has separate meshes with unique names: ``Cube`` and ``Cube.001``. The object ``Cube`` was linked duplicated, using :kbd:`Alt-D`. Though both these cubes are separate objects with unique names: ``Cube`` and ``Cube.001``, the single mesh named ``Cube``, is shared by both. The original left cube is being edited, the duplicated right cube remains unchanged. The mesh data has been copied, not linked. There are two types of object duplication, being `Duplicate`_ and `Linked Duplicates`_ which instance their Object Data. This copy is a new object, which shares some data-blocks with the original object (by default, all the Materials, Textures, and F-Curves), but which has copied others, like the mesh, for example. This is why this form of duplication is sometimes called "shallow link", because not all data-blocks are shared; some of them are "hard copied"! This will create a visually-identical copy of the selected object(s). The copy is created at the same position as the original object and you are automatically placed in *Grab* mode. See the examples below. When the cube was duplicated, it inherited the material of the original cube. The material properties were linked, not copied. You also have the choice of creating a *Linked Duplicate* rather than a *Duplicate*; this is called a deep link. This will create a new object with **all** of its data linked to the original object. If you modify one of the linked objects in *Edit Mode*, all linked copies are modified. Transform properties (object data-blocks) still remain copies, not links, so you still can rotate, scale, and move freely without affecting the other copies. Reference Expl. :ref:`Duplicate Example <expl-object-link-duplicate>` for the discussions below. You can choose which types of data-block will be linked or copied when duplicating: in the :ref:`User Preferences <prefs-editing-duplicate-data>`. 