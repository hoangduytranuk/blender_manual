��                        �  b   �  �   P  7   '  |   _  y   �  �  V  	   (  �   2                     *     2  C   R     �  
   �     �  T   �     
               0     <      Y  A   z  �  �    A  	   R  �  \  b     �   w  7   N  |   �  y     �  }  &   O  �   v  /   D     t  %   �     �     �  C   �     &  $   E     j  T   �     �     �  4   
     ?     O      l  A   �  �  �    T     e   :term:`Constraints <Constraint>` (also known as joints) for rigid bodies connect two rigid bodies. Additional parameters appear in the *Rigid Body Constraint* panel of the *Physics* tab in the Properties editor for the selected *Empty* object or the one of the two constrained objects with the created constraint. Allows constrained objects to pass through one another. Allows constraint to break during simulation. Disabled for the *Motor* constraint. This can be used to simulate destruction. Allows to make constraints stronger (more iterations) or weaker (less iterations) than specified in the rigid body world. Also you can create *Rigid Body Constraint* on one of the two constrained objects with *Rigid Body Constraint* button of the *Physics* tab in the Properties editor. This constraint is dependent on the object location and rotation on which it was created. This way, there are no *Empty* object created for the constraint. The role of the *Empty* object is put on this object. The constrained object can be then set as *Passive* type for better driving the constrain. Breakable By using limits you can constrain objects even more by specifying a translation/rotation range on/around respectively one axis (see below for each one individually). To lock one axis, set both limits to 0. Common Options Connect Disable Collisions Enabled First object to be constrained. Impulse strength that needs to be reached before constraint breaks. Introduction Iterations Limits Number of constraint solver iterations made per simulation step for this constraint. Object 1 Object 2 Override Iterations Physics Tab Rigid Body Constraint panel. Second object to be constrained. Specifies whether the constraint is active during the simulation. The physics constraints are meant to be attached to an :term:`Empty` object. The constraint then has fields which can be pointed at the two physics-enabled object which will be bound by the constraint. The *Empty* object provides a location and axis for the constraint distinct from the two constrained objects. The location of the entity hosting the physics constraint marks a location and set of axes on each of the two constrained objects. These two anchor points are calculated at the beginning of the animation and their position and orientation remain fixed in the *local* coordinate system of the object for the duration of the animation. The objects can move far from the constraint object, but the constraint anchor moves with the object. If this feature seems limiting, consider using multiple objects with a non-physics *Child of* constraint and animate the relative location of the child. The quickest way to constrain two objects is to select both and click the *Connect* button in the *Physics* tab of the *Tool Shelf*. This creates a new *Empty* object (named "Constraint") with a physics constraint already attached and pointing at the two selected objects. Threshold Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-07 02:04+0000
PO-Revision-Date: 2018-12-07 02:06+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :term:`Constraints <Constraint>` (also known as joints) for rigid bodies connect two rigid bodies. Additional parameters appear in the *Rigid Body Constraint* panel of the *Physics* tab in the Properties editor for the selected *Empty* object or the one of the two constrained objects with the created constraint. Allows constrained objects to pass through one another. Allows constraint to break during simulation. Disabled for the *Motor* constraint. This can be used to simulate destruction. Allows to make constraints stronger (more iterations) or weaker (less iterations) than specified in the rigid body world. Also you can create *Rigid Body Constraint* on one of the two constrained objects with *Rigid Body Constraint* button of the *Physics* tab in the Properties editor. This constraint is dependent on the object location and rotation on which it was created. This way, there are no *Empty* object created for the constraint. The role of the *Empty* object is put on this object. The constrained object can be then set as *Passive* type for better driving the constrain. Có Thể Bị Phá Hủy -- Breakable By using limits you can constrain objects even more by specifying a translation/rotation range on/around respectively one axis (see below for each one individually). To lock one axis, set both limits to 0. Các Tùy Chọn Phổ Thông -- Common Options Kết Nối -- Connect Tắt Va Đập -- Disable Collisions Bật -- Enabled First object to be constrained. Impulse strength that needs to be reached before constraint breaks. Giới Thiệu -- Introduction Số Lần Lặp Lại -- Iterations Giới Hạn -- Limits Number of constraint solver iterations made per simulation step for this constraint. Vật Thể 1 -- Object 1 Vật Thể 2 -- Object 2 Đổi Số Lần Lặp Lại -- Override Iterations  -- Physics Tab Rigid Body Constraint panel. Second object to be constrained. Specifies whether the constraint is active during the simulation. The physics constraints are meant to be attached to an :term:`Empty` object. The constraint then has fields which can be pointed at the two physics-enabled object which will be bound by the constraint. The *Empty* object provides a location and axis for the constraint distinct from the two constrained objects. The location of the entity hosting the physics constraint marks a location and set of axes on each of the two constrained objects. These two anchor points are calculated at the beginning of the animation and their position and orientation remain fixed in the *local* coordinate system of the object for the duration of the animation. The objects can move far from the constraint object, but the constraint anchor moves with the object. If this feature seems limiting, consider using multiple objects with a non-physics *Child of* constraint and animate the relative location of the child. The quickest way to constrain two objects is to select both and click the *Connect* button in the *Physics* tab of the *Tool Shelf*. This creates a new *Empty* object (named "Constraint") with a physics constraint already attached and pointing at the two selected objects. Giới Hạn -- Threshold 