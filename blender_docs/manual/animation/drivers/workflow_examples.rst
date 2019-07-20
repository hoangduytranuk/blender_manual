
*******************
Workflow & Examples
*******************

Simple Drivers can be configured from the pop-over that appears when adding a new Driver.

When adding multiple Drivers or for more advanced configurations,
it is useful to have open the :doc:`Drivers Editor </editors/drivers_editor>`.


Transform Driver
================

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
===================================

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
#. Scrub the timeline to see the effect.
   Experiment with the variables to control the size and center of the orbit.


Custom Function - Square Value
==============================

Create a custom function to get the square of a value (i.e. *value*\ :sup:`2`).
Adding the function to the *Driver Namespace* allows it to be used from driver expressions.

The *Driver Namespace* has a list of built-in functions for use in driver expressions,
as well as constants such as pi and e.
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

      # Add function to driver_namespace.
      bpy.app.driver_namespace['square'] = square

#. Add a driver with a *Scripted Expression* such as ``square(frame)``.
#. Observe the effect when scrubbing the timeline.

There are more custom function examples available in Blender's Text Editor
:menuselection:`Templates > Python > Driver Functions`.



Shape Key Drivers
=================

Improved Mesh Deformation
-------------------------

Fix intersection problems that happen when using armatures and weight painting, specially at joints.
Shape keys can also be used to tweak and refine a rig, for example to suggest muscle formations.
In this example, a shape key is used to improve the deformation at the elbow of a rudimentary arm.

.. figure:: /images/animation_drivers_workflow-examples_shape-key_improved_deformation.png

   Left: Skeletal mesh deformation without correction.
   Right: Corrective shape key applied


Setup
^^^^^

#. Add a mesh (in this example, a cylinder with loop cuts).
#. Add an armature with a chain of bones.
#. Skin the mesh to the armature using weight painting.

   (Note: to parent the mesh to the armature: select the mesh first,
   then the armature and use :kbd:`Ctrl-P` to parent with auto weights.)

Experiment with posing the armature and observe the deformation at the joint.
To fix intersection problems or angles that look unsatisfactory,
you can associate a :doc:`Shape Key </animation/shape_keys/index>` with a pose.


Shape Key
^^^^^^^^^

#. Pose the armature such that the problems are visible.
   Be sure to cover the extreme poses that you want to support for the rig.
#. With the mesh selected, add a new *Shape Key* in addition to the *Basis* key.
   :menuselection:`Properties --> Mesh tab --> Shape Keys`
#. In order to author the shape key on top of the armature deformation,
   enable both *Edit Mode Display* and *Cage Editing* in the armature modifier.
   :menuselection:`Properties --> Modifiers tab --> Armature Modifier --> Header`
#. Enter Edit Mode and select the new shape key in the properties panel.
   Adjust the vertices as desired.
   Select the *Basis* key to toggle between the original mesh and your edits.
   (Note: be careful to apply edits only to your shape and
   not to the original mesh or other existing keys.)


Once you are satisfied with how the deformation looks for the problematic pose,
you'll need to configure a driver to activate the shape smoothly when entering that position.


Driver
^^^^^^

#. Add a driver to the *Value* of the shape key you've created.
#. Open the Drivers Editor and select the driver.


.. rubric:: Method 1 -- Direct mapping to a bone rotation value

A simple way to configure the driver is with a direct correspondence of
the value of a bone's rotation channel to the shape key activation *Value*.
This method has the disadvantage of relying on a single channel of a bone's
rotation which might be insufficient to precisely express the condition under which
the shape key should be activated.

#. In the Drivers tab, select the *Averaged Value* of the rotation of the bone you're posing.

   Understand the rotation axis that you're interested in by enabling axes display
   in the armature or by observing the bone's transform values in the Properties.

   Select the rotation channel and set it to local, meaning, the bone's
   rotation value relative to its parent bone.

   .. figure:: /images/animation_drivers_workflow-examples_shape-key_method1.png

#. Manually set points in the driver curve by selecting a handle and
   dragging it or inserting values in the *F-Curve* tab.
   The Y Axis represents the shape key *Value*, which should go from 0.0 to 1.0.
   The X Axis is usually the frame, but for this driver it represents the rotation value in radians.
   You can have more than two points in the curve and tweak the transitions
   with the handles in the curve view (:kbd:`G` to move).

#. To verify that the driver behaves correctly, deselect the option to
   only show drivers for selected objects. This way, you can pose the armature
   and keep an eye on the driver.


.. rubric:: Method 2 -- Rotational difference to a target bone

This method requires an additional *target* or *corrective* bone, but it better expresses
the spatial condition in 3D space of the bone that is causing the problem.

#. In armature Edit Mode, add a new bone extruded from Bone 1,
   in the position at which Bone 2 should have the shape key active.
   This type of bones usually follow a naming convention such as
   "TAR-" (target) or "COR-" (corrective).

#. In the Drivers tab, select the *Averaged Value* of the rotational difference
   between the bone you're rotating and the target bone.
   A rotational difference is the minimum angle between two objects in world space.
   It is therefore important that the bones have the same root,
   so that the only thing affecting the angle between the bones is the rotation of one of them.
   When the deformation bone (Bone 2) reaches the target rotation (TAR-Bone 2)
   the rotational difference will be 0?.

   .. figure:: /images/animation_drivers_workflow-examples_shape-key_method2.png

#. Manually adjust the driver curve handles so that the shape key *Value*
   (Y axis) is 1.0 when the rotational difference (X axis) is 0?.
   The *Value* should be 0.0 when the arm is extended, at which point
   the rotational difference should be around 90? or more (in radians).

#. See the steps in Method 1 on how to adjust the curve handles and
   confirm that the functionality is working. Pose the armature to
   verify that the ranges are correct.


Chained Relative Shape Keys
---------------------------

Setup a chain of multiple relative shape keys that partially overlap given a certain input.

In this example, different shapes overlap in effect and in the input that drives them.
It is important to remember that
:ref:`relative shape keys mix additively <animation-shapekeys-relative-vs-absolute>`.

While relative shape keys lack the convenience of the single *Evaluation Time* of
absolute shape keys, they allow for more complex relationships between your shape keys.
The following images illustrate combining shape keys, bones, and
drivers to make multiple chained relative shape keys sharing a single root.


Shape Keys
^^^^^^^^^^

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

The images above show a single mesh with shape keys.

*Key1* has the base fully extended as well as the top of both stacks.
*Key2A* and *Key2B* are both relative to *Key1* and extend one stack without affecting the base.


Drivers
^^^^^^^

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

The *Value* of *Key1* is bound to the position of two different bones by a driver with two variables.
Each variable uses the world Z coordinate of a bone and
uses the maximum value to determine how much the base should be extended.
The generator polynomial is crafted such that the top of
the dominant stack should line up with the bone for that stack.

The *Value* of *Key2A* is bound to the position of "Bone.L".
Its generator parameters are crafted such that when *Key1*'s *Value* reaches 1,
the *Value* of *Key2A* starts increasing beyond zero. In this way,
the top of the left stack will move with bone.L (mostly).

The *Value* of *Key2B* is bound to the position of "Bone.R".
Its generator parameters are similar to *Key2A* so that
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
indicate conflicting values for *Key1* there will be times
when the bones do not line up with the tops of their respective stacks.
If the driver for *Key1* was to use Average or Minimum instead of Maximum to
determine the value of the shape key then "conflicts" between bone.L
and bone.R would be resolved differently. You will choose according to
the needs of your animation.

The following video shows a timelapse of this example and the end result at 3:58.

.. vimeo:: 173408647
