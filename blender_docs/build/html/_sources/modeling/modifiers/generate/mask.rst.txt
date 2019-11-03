.. _bpy.types.MaskModifier:

*************
Mask Modifier
*************

The *Mask* modifier allows vertices of an object to be hidden dynamically based on vertex groups.


Options
=======

Mode
   The Mask Modifier can hide parts of a mesh based on two different modes, selectable from this select menu.

   Vertex Group
      When the *Vertex Group* option is selected,
      all vertices belonging to the chosen Vertex Group (with a weight above zero) will be visible,
      and all other vertices will be hidden.

      .. list-table::
         The Mask modifier, Vertex Group mode.

         *  - .. figure:: /images/modeling_modifiers_generate_mask_vertex-group.png

            - .. figure:: /images/modeling_modifiers_generate_mask_panel-vertex-group.png

   Armature
      When in Pose Mode,
      vertices belonging to the Vertex Group associated with the active bone (same names) will be visible.
      Vertices not in that group will be hidden.

      .. list-table::
         The Mask modifier, Armature mode.

         *  - .. figure:: /images/modeling_modifiers_generate_mask_armature.png

            - .. figure:: /images/modeling_modifiers_generate_mask_panel-armature.png

Inverse
   Normally, vertices belonging to the selected Vertex Group (or group associated with the active pose bone)
   will be shown. The *Invert* toggle allows you to reverse this behavior, instead only showing vertices
   which do not belong to the Vertex Group.

Threshold
   Vertices with weights less or equal to this value will be hidden.
