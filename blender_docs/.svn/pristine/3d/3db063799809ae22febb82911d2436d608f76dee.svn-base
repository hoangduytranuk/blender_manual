
*******************
Workflow & Examples
*******************

Simple Drivers can be configured from the pop-over that appears when adding a new Driver.

When adding multiple Drivers or for more advanced configurations,
it is useful to have open the :doc:`Drivers Editor </editors/drivers_editor>`.


Examples
========

Transform Driver
----------------

Control a property with an object's transform.
In this example, the Y rotation of Object 2 will be driven by the X position of Object 1.

Starting from a simple setup with two objects:

#. Add a Driver to the *Rotation Y* property of the second object via the context menu or with :kbd:`Ctrl-D`.

   .. figure:: /images/animation_drivers_workflow-examples_transform-driver-1.png

#. Open the *Drivers Editor* and select the *Y Euler Rotation* property in the channels region.
#. Open the Sidebar region and select the *Drivers* tab.
#. Configure the driver to be the *Averaged Value* of a *Transform Channel* of the first object.

   .. figure:: /images/animation_drivers_workflow-examples_transform-driver-2.png

#. Experiment with moving the first object and notice how it affects the Y rotation of the second object.


Scripted Expression - Orbit a Point
-----------------------------------

Orbit an object's position around a point with a custom *Scripted Expression*.
The object's position will change when scrubbing the timeline.

Using trigonometry, circular motion can be defined in 2D using the sinus and cosine functions.
(See `Unit Circle <https://en.wikipedia.org/wiki/Unit_circle>`__).

In this example, the current frame is used as the variable that induces the motion.
``frame`` is a :ref:`Simple Expression <drivers-simple-expressions>` that corresponds to
``bpy.context.scene.frame_current``.

.. figure:: /images/animation_drivers_workflow-examples_object-rotation.png

#. Add a driver to the X Location property.

   #. Set the *Driver Type* to *Scripted Expression*.
   #. Add the expression ``0 + (sin(frame / 8) * 4)``, where:

      - ``frame/8`` : is the current frame of the animation, divided by 8 to slow the orbit down.
      - ``(sin( )*4)`` : multiplies the result of ``sin(frame/8)`` by 4 for a bigger circle.
      - ``0 +`` : is used to control the offset to the orbit center point.

#. Add a driver to the Y Location property with the expression ``0 + (cos(frame / 8) * 4)``.
#. Scrub the timeline to see the effect. Experiment with the variables to control the size and center of the orbit.


Custom Function - Square Value
------------------------------

Make a custom function to get the square of a value (i.e. value\ :sup:`2`).
Adding the function to the *Driver Namespace* allows it to be used from driver expressions.

The *Driver Namespace* has a list of built-in functions for use in driver expressions,
as well as constants such as π and e.
These can be inspected via the Python Console::

   >>> bpy.app.driver_namespace[' <tab>
                                 acos']
                                 acosh']
                                 asin']
                                 asinh']
                                 atan']
                                 ...

To add a new function to the *Driver Namespace*, the function itself needs to be implemented
and then added to the ``bpy.app.driver_namespace``.

#. Add the following to the Text Editor inside Blender and press *Run Script*. ::

      import bpy

      def square(val):
         """Returns the square of the given value"""
         return val * val

      # Add function to driver_namespace
      bpy.app.driver_namespace['square'] = square

#. Add a driver with a *Scripted Expression* such as ``square(frame)``.
#. Observe the effect when scrubbing the timeline.

There are more custom function examples available in Blender's Text Editor
:menuselection:`Templates > Python > Driver Functions`.


Shape Key Driver
----------------

This example is a shape key driver. The driver was added to the shape key Value.

.. TODO2.8 Replace screenshots (ui appearance changes):

.. figure:: /images/animation_drivers_workflow-examples_shape-key.png
   :width: 400px

   Shape key driver example.

This example uses the Armature Bone "b" 's Z Rotation to control the Value of a Shape Key.
The bone rotation mode is set to XYZ Euler.

The Driver F-curve is mapped like so:

- Bone Z Rotation 0.0 (0.0): Shape Key value 0.0
- Bone Z Rotation -2.09 (-120.0): Shape Key value 1.0

This kind of driver can also be setup with the Variable Type Rotational Difference.

See :doc:`Shape Keys </animation/shape_keys/index>` for more info.


Drivers and Multiple Relative Shape Keys
========================================

The following screenshots illustrate combining shape keys, bones, and
drivers to make multiple chained relative shape keys sharing a single root.
While it lacks the convenience of the single Evaluation Time of an absolute shape key,
it allows you to have more complex relationships between your shape keys.

.. TODO2.8 Replace screenshots (ui appearance changes):

.. list-table::

   * - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-shape-base.png
          :width: 320px

          Basis shape key.

     - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-shape-1.png
          :width: 320px

          Key1 shape key.

   * - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-shape-2a.png
          :width: 320px

          Key2A shape key.

     - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-shape-2b.png
          :width: 320px

          Key2B shape key.

The Basis shape key has the stacks fully retracted. Key1 has the base fully extended.
Key2A has the left stack fully extended. Key2B has the right stack fully extended.
Key2A and Key2B are both relative to Key1
(as you can see in the field in the bottom right of the Shape Keys panel).

.. TODO2.8 Replace screenshots (ui appearance changes):

.. list-table::

   * - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-key1.png
          :width: 320px

          Key1 must handle conflicting values from the two bones.

     - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-key2a.png
          :width: 320px

          Key2A has different generator coefficients so it is activated in a different range of the bone's position.

     - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-key2b.png
          :width: 320px

          Key2B is the same as Key2A, but is controlled by the second bone.

The value of Key1 is bound to the position of bones by a driver with two variables.
Each variable uses the world Z coordinate of a bone and
uses the maximum value to determine how much the base should be extended.
The generator polynomial is crafted such that the top of
the dominant stack should line up with the bone for that stack.

The value of Key2A is bound to the position of "Bone.L".
Its generator parameters are crafted such that when Key1's value reaches 1,
the value of Key2A starts increasing beyond zero. In this way,
the top of the left stack will move with bone.L (mostly).

The value of Key2B is bound to the position of "Bone.R".
Its generator parameters are similar to Key2A so that
the top of the right stack will move with bone.R (mostly).

.. TODO2.8 Replace screenshots (ui appearance changes):

.. list-table::

   * - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-retracted.png
          :width: 320px

          When both bones are low, Key2B and Key2A are deactivated and Key1 is at low influence.

     - .. figure:: /images/animation_drivers_workflow-examples_for-multiple-shape-keys-extended.png
          :width: 320px

          Extended.

Since it is quite easy for bone.L and bone.R to be in positions that
indicate conflicting values for Key1 there will be times
when the bones do not line up with the tops of their respective stacks.
If the driver for Key1 was to use Average or Minimum instead of Maximum to
determine the value of the shape key then "conflicts" between bone.L
and bone.R would be resolved differently. You will choose according to
the needs of your animation.

.. vimeo:: 173408647
