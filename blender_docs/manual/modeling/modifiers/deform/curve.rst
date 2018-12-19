.. _bpy.types.CurveModifier:

**************
Curve Modifier
**************

The Curve Modifier provides a simple but efficient method of deforming a mesh along a curve object.

The Curve Modifier works on a (global) dominant axis, X, Y, or Z.
This means that when you move your mesh in the dominant direction (by default, the X axis),
the mesh will traverse along the curve. Moving the mesh perpendicularly to this axis,
the object will move closer or further away from the curve.

When you move the object beyond the curve endings the object will continue
to deform based on the direction vector of the curve endings.

If the curve is 3D, the *Tilt* value of its control points will be used to twist the deformed object.
And the *Radius* property controls the size of the object as well.

In the :menuselection:`Properties editor --> Curve tab --> Shape panel`
under :ref:`Path/Curve-Deform <curve-shape-path-curve-deform>`
are options that influence the modifier.


Options
=======

.. _fig-modifier-curve-panel:

.. figure:: /images/modeling_modifiers_deform_curve_panel.png

   Curve Modifier.

Object
   The name of the curve object that will affect the deformed object.
Vertex Group
   A vertex group name within the deformed object. The modifier will only affect vertices assigned to this group.
Deformation Axis
   This is the axis that the curve deforms along.

   X, Y, Z, -X, -Y, -Z


Example
=======

Let us make a simple example:

- Remove the default cube object from the scene and add a Monkey
  with :menuselection:`Add --> Mesh --> Monkey`.
- Now add a curve with :menuselection:`Add --> Curve --> Bézier Curve`.
- While in Edit Mode, move the control points of the curve as shown in Fig. :ref:`fig-modifier-curve-edit`,
  then exit Edit Mode :kbd:`Tab`.
- Select the Monkey :kbd:`RMB` in *Object Mode* and add the Curve Modifier.
- Assign the Bézier curve to the modifier, as shown in Fig. :ref:`fig-modifier-curve-panel`.
  The Monkey should be positioned on the curve.

.. list-table::

   * - .. _fig-modifier-curve-edit:

       .. figure:: /images/modeling_modifiers_deform_curve_example-edit-curve.png
          :width: 300px

          Edit curve.

     - .. figure:: /images/modeling_modifiers_deform_curve_example-monkeyoncurve1.png
          :width: 300px

          Monkey on a curve.

     - .. figure:: /images/modeling_modifiers_deform_curve_example-monkeyoncurve2.png
          :width: 300px

          Monkey deformations.

- Now if you select the Monkey, and move it in the Y direction :kbd:`G Y`,
  the monkey will deform nicely along the curve.
- In the image above you can see the Monkey at different positions along the curve.
  To get a cleaner view over the deformation, a :doc:`Subdivision Surface </modeling/modifiers/generate/subsurf>`
  Modifier with two subdivision levels was applied,
  and :ref:`smooth <modeling-meshes-editing-normals-shading>` shading was used.
