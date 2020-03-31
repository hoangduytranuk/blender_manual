
*****
Debug
*****

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Performance`

These settings are mainly useful to developers and can be accessed
by setting the :ref:`Debug Value <bpy.ops.wm.debug_menu>` to 256.

Viewport BVH Type
   Dynamic BVH
      Objects can be transformed, added and deleted interactively, at the cost of slower renders.
   Static BVH
      Object modifications require a complete :term:`BVH` rebuild which reduces interactivity but renders faster.
