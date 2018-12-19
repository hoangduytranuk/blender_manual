.. _bpy.types.MaskModifier:

*************
Mask Modifier
*************

The Mask Modifier allows vertices of an object to be hidden dynamically based on vertex groups.


Options
=======

Mode
   The Mask Modifier can hide parts of a mesh based on two different modes, selectable from this select menu.

   Vertex Group
      When the *Vertex Group* option is selected,
      all vertices belonging to the chosen Vertex Group (with a weight above zero) will be visible,
      and all other vertices will be hidden.

      .. figure:: /images/modeling_modifiers_generate_mask_vertex-group.png
         :width: 350px

         Vertex Group.

   Armature
      When in Pose Mode,
      vertices belonging to the Vertex Group associated with the active bone (same names) will be visible.
      Vertices not in that group will be hidden.

      .. figure:: /images/modeling_modifiers_generate_mask_armature.png
         :width: 350px

         Armature.

Inverse
   Normally, vertices belonging to the selected Vertex Group (or group associated with the active pose bone)
   will be shown. The *Invert* toggle allows you to reverse this behavior, instead showing all vertices
   which do not belong to the Vertex Group, and hiding those that do.
