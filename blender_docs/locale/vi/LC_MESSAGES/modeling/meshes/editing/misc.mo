��    &      L              |     }  *   �  /   �  %   �       b        z  0   �     �  	   �  #   �     �     �          
     &  �   +  	   �  �   �  	   �     �     �     �  ,     2   2     e  j   s  v   �  "  U  Z   x     �  4   �    "	  �   =
  �   �
     n     z  �  �     >  *   G  /   r  %   �     �  b   �  "   ?  0   b  +   �  %   �  #   �     	          :     O     n  �   �     ?  �   _     N     h      �     �  ,   �  2   �       j   +  v   �  "    Z   0     �  4   �    �  �   �  �   }  (   &  (   O   :kbd:`P` :menuselection:`Mesh --> Sort Elements...` :menuselection:`Mesh --> Vertices --> Separate` :ref:`Joining objects <object-join>`. All Loose Parts At some point, you will come to a time when you need to cut parts away from a mesh to be separate. By Material Creates separate mesh objects for each material. Cursor Distance Edit Mode Enabling the Display Indices Option Hotkey Material Menu Miscellaneous Editing Tools Mode Move all selected elements to the beginning (or end, if *Reverse* enabled), without affecting their relative orders. Warning: This option will also affect **unselected** elements' indices! Randomize Randomizes indices of selected elements (*without* affecting those of unselected ones). The seed option allows you to get another randomization -- the same seed over the same mesh/set of selected elements will always give the same result! Reference Reverse Selected Separate Separates the mesh in its unconnected parts. Simply reverse the order of the selected elements. Sort Elements Sort along the active view's X axis, from left to right by default (again, there is the *Reverse* option). Sort along the active view's Z axis, from farthest to nearest by default (use *Reverse* if you want it the other way). Sort faces, and faces only, from those having the lowest material's index to those having the highest. Order of faces inside each of those "material groups" remains unchanged. Note that the *Reverse* option only reverses the order of the materials, *not* the order of the faces inside them. Sort from nearest to farthest away from the 3D cursor position (*Reverse* also available). Suzanne dissected neatly. This option separates the selection to a new object. This tool (available from the *Specials*, *Vertices*, *Edges* and *Faces* menus) allows you to reorder the matching selected mesh elements, following various methods. Note that when called from the *Specials* menu, the affected element types are the same as the active select modes. To separate an object, the vertices (or faces) must be selected and then separated, though there are several different ways to do this. Type ``bpy.app.debug = True`` into the Python Console and a checkbox will appear in the Properties region under :menuselection:`Mesh Display --> Edge Info --> Indices`. View X Axis View Z Axis Project-Id-Version: Blender 2.79 Manual 2.79
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
 :kbd:`P` :menuselection:`Mesh --> Sort Elements...` :menuselection:`Mesh --> Vertices --> Separate` :ref:`Joining objects <object-join>`.  -- All Loose Parts At some point, you will come to a time when you need to cut parts away from a mesh to be separate. Theo Nguyên Liệu -- By Material Creates separate mesh objects for each material. Khoảng Cách Con Trỏ -- Cursor Distance Chế Độ Biên Soạn -- Edit Mode Enabling the Display Indices Option Phím Tắt -- Hotkey Nguyên Liệu -- Material Trình Đơn -- Menu -- Miscellaneous Editing Tools Chế Độ -- Mode Move all selected elements to the beginning (or end, if *Reverse* enabled), without affecting their relative orders. Warning: This option will also affect **unselected** elements' indices! Ngẫu Nhiên Hóa -- Randomize Randomizes indices of selected elements (*without* affecting those of unselected ones). The seed option allows you to get another randomization -- the same seed over the same mesh/set of selected elements will always give the same result! Tham Chiếu -- Reference Đảo Ngược -- Reverse Cái Được Chọn -- Selected Phân Rã -- Separate Separates the mesh in its unconnected parts. Simply reverse the order of the selected elements. -- Sort Elements Sort along the active view's X axis, from left to right by default (again, there is the *Reverse* option). Sort along the active view's Z axis, from farthest to nearest by default (use *Reverse* if you want it the other way). Sort faces, and faces only, from those having the lowest material's index to those having the highest. Order of faces inside each of those "material groups" remains unchanged. Note that the *Reverse* option only reverses the order of the materials, *not* the order of the faces inside them. Sort from nearest to farthest away from the 3D cursor position (*Reverse* also available). Suzanne dissected neatly. This option separates the selection to a new object. This tool (available from the *Specials*, *Vertices*, *Edges* and *Faces* menus) allows you to reorder the matching selected mesh elements, following various methods. Note that when called from the *Specials* menu, the affected element types are the same as the active select modes. To separate an object, the vertices (or faces) must be selected and then separated, though there are several different ways to do this. Type ``bpy.app.debug = True`` into the Python Console and a checkbox will appear in the Properties region under :menuselection:`Mesh Display --> Edge Info --> Indices`. Trục X của Góc Nhìn -- View X Axis Trục Z của Góc Nhìn -- View Z Axis 