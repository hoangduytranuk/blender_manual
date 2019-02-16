��    7      �              �  ;   �     �  s   �  o   C  !   �  P   �  >   &     e  ?   j     �     �     �  a   �  �   6  �   (     �             ~  )  v   �	  	   
     )
  t   6
     �
  �   �
    l  �   �     F     V     ]  $   w     �  1   �     �     �          !     >  V   G  �   �  �   P  �   �  �  �  Y   A     �  i   �  "       ;  y   =  ;   �  :   �     .  `   3  a   �  �  �  ;   �     �  s   �  o   r  !   �  P     >   U     �  ?   �     �     �       a   /  �   �  �   �     T  "   h     �  ~  �  v   !     �     �  t   �     E  �   ]       �   !     �!     �!  Q   "  $   Y"     ~"  1   �"     �"      �"     �"      #     8#  V   P#  �   �#  �   Y$  �   �$  �  �%  Y   J'     �'  i   �'  "   $(    G(  y   I)  ;   �)  :   �)     :*  `   O*  a   �*   An icon as a quick visual reference of the modifier's type. Apply Applying a modifier that is not first in the stack will ignore the stack order and could produce undesired results. At the top is the *panel header*. The icons each represent different settings for the modifier (left to right): Below the header are two buttons: Below this header, all of the options unique to each modifier will be displayed. Collapse modifier to show only the header and not its options. Copy Creates a duplicate of the modifier at the bottom of the stack. Deform Delete ``X`` Deletes the modifier. Displays the modified geometry in Edit Mode, as well as the original geometry which you can edit. Each modifier has been brought in from a different part of Blender, so each has its own unique settings and special considerations. However, each modifier's interface has the same basic components, see Fig. :ref:`fig-modifiers-panel-layout`. Every modifier has a unique name per object. Two modifiers on one object must have unique names, but two modifiers on different objects can have the same name. The default name is based off the modifier type. Example Expand (down/right arrow icon) Generate In a modifier stack the order in which modifiers are applied has an effect on the result. Fortunately modifiers can be rearranged easily by clicking the convenient up and down arrow icons. For example, the image below shows :doc:`Subdivision Surface </modeling/modifiers/generate/subsurf>` and :doc:`Mirror </modeling/modifiers/generate/mirror>` modifiers that have switched places. In this example a simple subdivided cube has been transformed into a rather complex object using a stack of modifiers. Interface Introduction Makes the modifier "real" -- converts the object's geometry to match the applied modifier, and deletes the modifier. Modifier Stack example. Modifiers are a series of non-destructive operations which can be applied on top of an object's geometry. They can be applied in just about any order the users chooses. Modifiers are automatic operations that affect an object in a non-destructive way. With modifiers, you can perform many effects automatically that would otherwise be too tedious to do manually (such as subdivision surfaces) and without affecting the base geometry of your object. Modifiers are calculated from top to bottom in the stack. In this example, the desired result (on right) is achieved by first mirroring the object, and then calculating the subdivision surface. Modifiers menu. Modify Move (up/down arrow icon) Moves modifier up/down in the stack. Name Panel layout (Subdivision Surface as an example). Render (camera icon) Show in Edit Mode (box icon) Show in viewport (eye icon) Show on cage (triangle icon) Simulate The *Box* and *Triangle* icons may not be available depending on the type of modifier. The *Deform* group of modifiers only changes the shape of an object without adding new geometry, and are available for meshes, and often texts, curves, surfaces and/or lattices. The *Generate* group of modifiers includes constructive tools that either change the general appearance of or automatically add new geometry to an object. The *Modify* group of modifiers includes tools similar to the *Deform Modifiers* (see below), but which do not directly affect the shape of the object; rather they affect some other data, such as vertex groups. The *Simulate* group of modifiers activates simulations. In most cases, these modifiers are automatically added to the modifiers stack whenever a *Particle System* or *Physics* simulation is enabled. Their only role is to define the place in the modifier stack used as base data by the tool they represent. Generally, the attributes of these modifiers are accessible in separate panels. The Mirror modifier is the last item in the stack and the result looks like two surfaces. The Modifier Stack The Subdivision surface modifier is the last item in the stack and the result is a single merged surface. There are four types of modifiers: They work by changing how an object is displayed and rendered, but not the geometry which you can edit directly. You can add several modifiers to a single object to form `The Modifier Stack`_ and *Apply* a modifier if you wish to make its changes permanent. This kind of functionality is often referred to as a "modifier stack" and is also found in several other 3D applications. Toggles visibility of the modifier's effect in the 3D View. Toggles visibility of the modifier's effect in the render. Type When enabled, the final modified geometry will be shown in Edit Mode and can be edited directly. `Download example file <https://wiki.blender.org/wiki/File:25-Manual-Modifiers-example.blend>`__. Project-Id-Version: Blender 2.79 Manual 2.79
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
 An icon as a quick visual reference of the modifier's type. Áp Dụng -- Apply Applying a modifier that is not first in the stack will ignore the stack order and could produce undesired results. At the top is the *panel header*. The icons each represent different settings for the modifier (left to right): Below the header are two buttons: Below this header, all of the options unique to each modifier will be displayed. Collapse modifier to show only the header and not its options. Sao Chép -- Copy Creates a duplicate of the modifier at the bottom of the stack. Biến Dạng -- Deform Xóa ``X`` -- Delete ``X`` Deletes the modifier. Displays the modified geometry in Edit Mode, as well as the original geometry which you can edit. Each modifier has been brought in from a different part of Blender, so each has its own unique settings and special considerations. However, each modifier's interface has the same basic components, see Fig. :ref:`fig-modifiers-panel-layout`. Every modifier has a unique name per object. Two modifiers on one object must have unique names, but two modifiers on different objects can have the same name. The default name is based off the modifier type. Ví Dụ -- Example  -- Expand (down/right arrow icon) Sinh Tạo -- Generate In a modifier stack the order in which modifiers are applied has an effect on the result. Fortunately modifiers can be rearranged easily by clicking the convenient up and down arrow icons. For example, the image below shows :doc:`Subdivision Surface </modeling/modifiers/generate/subsurf>` and :doc:`Mirror </modeling/modifiers/generate/mirror>` modifiers that have switched places. In this example a simple subdivided cube has been transformed into a rather complex object using a stack of modifiers. Giao Diện -- Interface Giới Thiệu -- Introduction Makes the modifier "real" -- converts the object's geometry to match the applied modifier, and deletes the modifier. Modifier Stack example. Modifiers are a series of non-destructive operations which can be applied on top of an object's geometry. They can be applied in just about any order the users chooses. Modifiers are automatic operations that affect an object in a non-destructive way. With modifiers, you can perform many effects automatically that would otherwise be too tedious to do manually (such as subdivision surfaces) and without affecting the base geometry of your object. Modifiers are calculated from top to bottom in the stack. In this example, the desired result (on right) is achieved by first mirroring the object, and then calculating the subdivision surface. Modifiers menu. Sửa Đổi -- Modify Di Chuyển (biểu tượng mũi tên lên/xuống) -- Move (up/down arrow icon) Moves modifier up/down in the stack. Tên -- Name Panel layout (Subdivision Surface as an example).  -- Render (camera icon)  -- Show in Edit Mode (box icon)  -- Show in viewport (eye icon)  -- Show on cage (triangle icon) Mô Phỏng -- Simulate The *Box* and *Triangle* icons may not be available depending on the type of modifier. The *Deform* group of modifiers only changes the shape of an object without adding new geometry, and are available for meshes, and often texts, curves, surfaces and/or lattices. The *Generate* group of modifiers includes constructive tools that either change the general appearance of or automatically add new geometry to an object. The *Modify* group of modifiers includes tools similar to the *Deform Modifiers* (see below), but which do not directly affect the shape of the object; rather they affect some other data, such as vertex groups. The *Simulate* group of modifiers activates simulations. In most cases, these modifiers are automatically added to the modifiers stack whenever a *Particle System* or *Physics* simulation is enabled. Their only role is to define the place in the modifier stack used as base data by the tool they represent. Generally, the attributes of these modifiers are accessible in separate panels. The Mirror modifier is the last item in the stack and the result looks like two surfaces. -- The Modifier Stack The Subdivision surface modifier is the last item in the stack and the result is a single merged surface. There are four types of modifiers: They work by changing how an object is displayed and rendered, but not the geometry which you can edit directly. You can add several modifiers to a single object to form `The Modifier Stack`_ and *Apply* a modifier if you wish to make its changes permanent. This kind of functionality is often referred to as a "modifier stack" and is also found in several other 3D applications. Toggles visibility of the modifier's effect in the 3D View. Toggles visibility of the modifier's effect in the render. Thể Loại -- Type When enabled, the final modified geometry will be shown in Edit Mode and can be edited directly. `Download example file <https://wiki.blender.org/wiki/File:25-Manual-Modifiers-example.blend>`__. 