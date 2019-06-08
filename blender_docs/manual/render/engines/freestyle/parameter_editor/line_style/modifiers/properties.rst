
**********
Properties
**********

There are several modifiers for stroke vertex properties
(i.e. line color, alpha transparency and thickness) available.
As with other modifier stacks in Blender, they are applied from top to bottom.


Common Options
==============

Mix
   The modifier output can be mixed with the base property using the usual methods
   (see for example the :doc:`Mix compositing node </compositing/types/color/mix>`
   for further discussion of this topic).
Influence
   How much the result of this modifier affects the current property.


Mapping
-------

Mapping between the defined range and the range input of the modifier.
e.g. a range of crease values.


Color
^^^^^

Color Ramp
   A :ref:`color ramp <ui-color-ramp-widget>` that maps the property to a stroke color.


Alpha
^^^^^

Mapping
   Either a linear progression (from 0.0 to 1.0),
   or a custom mapping :ref:`curve <ui-curve-widget>`.

   .. note::

      Note the linear non-inverted option is equivalent to "do nothing",
      as original values from materials are already in the (0.0 to 1.0) range.
      That is the case for: Crease Angle, 3D Curvature, Material, Noise, Tangent.

Invert
   Inverts the *Mapping*.


Thickness
^^^^^^^^^

Min Thickness and Max Thickness
   The minimum and maximum assigned thickness.
Mapping
   Either a linear progression (from *Min Thickness* to *Max Thickness*),
   or a custom mapping curve (on the same range).
Invert
   Inverts the *Mapping*.


Types
=====

.. _bpy.types.LineStyle*Modifier_AlongStroke:

Along Stroke
------------

The *Along Stroke* modifier alters the base property with a new one from
a given range mapped along each stroke's length. In other words,
it applies a gradient along each stroke.


.. _bpy.types.LineStyleThicknessModifier_Calligraphy:

Calligraphy
-----------

The *Calligraphy* modifier (thickness only) mimics some broad and flat pens for calligraphy.
It generates different thickness based on the orientation of the stroke.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_thickness-calligraphy.png

Orientation
   The angle (orientation) of the virtual drawing tool, from the vertical axis of the picture.
   For example, an angle of 0.0 mimics a pen aligned with the vertical axis.
   Hence, the thickest strokes will be the vertical ones i.e. stroke's direction is aligned with the angle, and
   the thinnest will be the horizontal ones i.e. stroke's direction is perpendicular to the angle.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_thickness-calligraphy-example.png
   :width: 430px

   Calligraphy modifier demo by T.K.
   `File:Toycar_Calligraphy.zip <https://wiki.blender.org/wiki/File:Toycar_Calligraphy.zip>`__.


.. _bpy.types.LineStyle*Modifier_CreaseAngle:

Crease Angle
------------

A modifier based on the Crease Angle (angle between two adjacent faces).
If a stroke segment does not lie on a crease (i.e. the edge does not have the *Crease Angle nature*),
its properties are not touched by the modifier.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_alpha-crease-angle.png

   Alpha Modifier.

Min Angle and Max Angle
   The range of input values to the mapping.
   Out-of-range crease angle values will be clamped by
   the Min and Max angles and their corresponding property values.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_color-crease-angle-example.png
   :width: 430px

   Crease Angle modifier demo by T.K.
   `File:Render_freestyle_modifier_crease_angle.blend
   <https://wiki.blender.org/uploads/b/b4/Render_freestyle_modifier_crease_angle.blend>`__.


.. _bpy.types.LineStyle*Modifier_Curvature_3D:

Curvature 3D
------------

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_color-curvature-3d-example.png
   :width: 430px

   Curvature 3D modifier demo by T.K.
   `File:Render_freestyle_modifier_curvature_3d.blend
   <https://wiki.blender.org/wiki/File:Render_freestyle_modifier_curvature_3d.blend>`__.

A modifier based on radial curvatures of the underlying 3D surface.
The `curvature <https://en.wikipedia.org/wiki/Curvature>`__ of a 2D curve
at a point is a measure of how quickly the curve turns at the point.
The quicker the turn is, the larger the curvature is at the point.
The curvature is zero if the curve is a straight line.
Radial curvatures are those computed for a 2D curve that appears at the cross section
between the 3D surface and a plane defined by the view point (camera location)
and the normal direction of the surface at the point.

For radial curvatures to be calculated (and therefore for this modifier to have any effect),
the *Face Smoothness* option has to be turned on and the object needs to have *Smooth Shading*.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_alpha-curvature-3d.png

   Alpha Modifier.

Min Curvature and Max Curvature
   The limits of the mapping.
   If the current point of the stroke is at *Min Curvature* or less from the target,
   it will take the start point of the mapping, and conversely,
   if it is at *Max Curvature* or more from the target, it will take the end-point value of the mapping.


.. _bpy.types.LineStyle*Modifier_DistanceFromCamera:
.. _bpy.types.LineStyle*Modifier_DistanceFromObject:

Distance from Camera/Object
---------------------------

The *Distance from Camera* or *Distance from Object* modifier alters the base property with a new one
from a given range using the distance to the active *camera* or to a given *object* as the parameter.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_alpha-distance-from-object.png

   Distance from Object: Alpha Modifier.

Target
   The object to measure distance from (Distance from Object only).
Range Min and Range Max
   The limits of the mapping from "distance to camera" to "property in mapping".
   If the current point of the stroke is at *Range Min* or less from the active camera or the object,
   it will take the start value, and conversely,
   if it is at *Range Max* or more from the camera/object, it will take the end value.
   These values are in the current scene's units, not in pixels!
Fill Range by Selection
   Set the min/max range values from the distances between the current selected mesh vertices and
   the camera or the target.


.. _bpy.types.LineStyle*Modifier_Material:

Material
--------

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_color-material.png

   Color Modifier.

The *Material* modifier alters the base property with a new one taken from a given range mapped on
the current material under the stroke.

You can use various properties of the materials, among which many are mono-component
(i.e. give B&W results). In this case for the color modifier, an optional color ramp can be used to
map these gray-scale values to colored ones.

In the reverse case properties of the materials, which are multi-components
(i.e. give RGB results) the mean value will be used for Alpha and Thickness modifiers.

If used with the *Split by Material* option in the *Stroke* tab,
the result will not be blurred between materials along the strokes.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_color-material-example.png
   :width: 430px

   Material modifiers demo by T.K.
   `File:Lilies_Color_Material.zip <https://wiki.blender.org/wiki/File:Lilies_Color_Material.zip>`__.


.. _bpy.types.LineStyle*Modifier_Noise:

Noise
-----

The *Noise* modifier uses a pseudo-random number generator to variably distribute the property along the stroke.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_thickness-noise.png

   Thickness Modifier.

Amplitude
   The maximum value of the noise. A higher amplitude means a less transparent (more solid) stroke.
Period
   The period of the noise. This means how quickly the property value can change.
   A higher value means a more smoothly changing color along the stroke.
Seed
   Seed used by the pseudo-random number generator.
Asymmetric
   Thickness only -- Allows the thickness to be distributed unevenly at every point.
   Internally, the stroke is represented as a backbone with a thickness to the right and left side.
   All other thickness shaders make sure that the left and right thickness values are equal.
   For the Noise shader however, a meaningful (and good-looking) result
   can be created by assigning different values to either side of the backbone.

.. figure:: /images/render_freestyle_parameter-editor_line-style_modifiers_properties_thickness-noise-example.png
   :width: 430px

   Effect generated with a noise thickness modifier using asymmetric thickness.


.. _bpy.types.LineStyle*Modifier_Tangent:

Tangent
-------

This modifier bases its effect on the traveling direction of the stroke evaluated at the stroke's vertices.
