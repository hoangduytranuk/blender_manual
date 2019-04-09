.. _bpy.types.bpy_struct:
.. _bpy.ops.wm.properties:

*****************
Custom Properties
*****************

.. figure:: /images/data-system_custom-properties_add.png
   :align: right

   Custom Properties panel.

Custom properties are a way to store your own metadata in Blender's data-blocks
which can be used for rigging (where bones and objects can have custom properties driving other properties),
and Python scripts, where it's common to define new settings not available in Blender.

Only certain data supports custom properties:

- All :ref:`data-blocks types <data-system-datablock-types>`.
- Bones and Pose-Bones.
- Sequence strips.

To add a custom property, find the *Custom Properties* panel,
found at the bottom of most :doc:`Properties Editor </editors/properties_editor>` or Properties region, and hit *Add*.


Editing Properties
==================

User Interface
--------------

Custom properties can be edited using the panel available for data types that support it.

.. figure:: /images/data-system_custom-properties_edit.png
   :align: right

   Custom Properties edit pop-up.

Property Name
   The name of the custom property.
Property Value
   This does two things: first it sets the current value of the custom property, and
   second, it defines the data type of the property.
   For example, custom properties can either be of type: Integers, Floats, or Booleans.
   See the table below for a list of examples for each:

   :Integers: 1, 2, 3, 4...
   :Floats: 3.141, 5.0, 6.125,
   :Booleans: ``True``, ``False``

   .. note::

      Booleans are handled very similar to integers and only work
      when using Min/Max values that are integers and that are no more than 1 apart.

      At this point, the booleans will still look like integers but behave like
      booleans having one lower, off, value and a higher, on, value.
Default Value
   This sets the default value of the property used by the Reset to Default Value operator.

   .. warning::

      Default values are used as the basis of :ref:`NLA blending <nla-blend-modes>`,
      and a nonsensical default (e.g. 0 for a property used for scaling) on a property intended for
      being keyframed is likely to cause issues.
Min
   The minimum value the custom property can take.
Max
   The maximum value the custom property can take.
Use Soft Limits
   Enables limits that the *Property Value* slider can be adjusted to
   without having to input the value numerically.

   Soft Min
      The minimum value for the soft limit.
   Soft Max
      The maximum value for the soft limit.
Is Statically Overridable
   Specifies if the property can be overridden via the Static Overrides system
   (with an additional performance overhead).
Tooltip
   Allows you to write a custom :doc:`Tooltip </getting_started/help>` for your property.


Python Access
-------------

Custom properties can be accessed in a similar way to
`dictionaries <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>`__,
with the constraints that keys can only be strings,
and values can only be strings, numbers, arrays and nested properties.

See the `API documentation
<https://www.blender.org/api/blender_python_api_current/info_quickstart.html#custom-properties>`__
for details.
