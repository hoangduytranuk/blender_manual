
******
Layers
******

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties region --> Grease Pencil Layers`

Grease Pencil sketches are organized in layers,
much like the image layers in the GIMP or Photoshop\ :sup:`®`.
These layers are not related to any of the other layer systems in Blender.

The layers' main purpose is to gather sketches that are related in some
meaningful way (e.g. "blocking notes", "director's comments on blocking", or "guidelines").
For this reason, all the strokes on a layer (not just those made after a particular change)
are affected by that layer's color, opacity, and stroke thickness settings.

Layers are managed in the *Grease Pencil Panel* of the *Properties region* :kbd:`N` shown here.

.. figure:: /images/interface_grease-pencil_drawing_layers_list.png

   Grease Pencil panel.


Grease Pencil Data
==================

Use the following controls to Add, Remove or adjust the position of a layer in the list.

Source
   Scene
      Grease Pencil data attached to the current scene is used,
      unless the active object already has Grease Pencil data (i.e. old files).
   Object
      Grease Pencil data attached to the active object is used.
      This is required when using pre 2.73 add-ons.

Grease Pencil
   Used to select the Grease Pencil data-block to use for layers. For controls see :ref:`ui-data-block`.

Active Layer
   A :ref:`ui-list-view` of layers attached to each scene or object.

   Parent (bone icon)
      Indicates that a parent has been set for the layer.
   Lock (padlock icon)
      Locks the ability to edit the current layers layer.
   Hide (eye icon) :kbd:`H`
      Hides the current layer in the drawing region.
   Unlock Color (color wheel with arrow icon)
      Unprotects selected colors from further editing and/or frame changes.

   Isolate (padlock icon) :kbd:`NumpadAsterix`
      To restrict editing to the active layer only.
   Isolate (visible) (eye icon)
      An option of *Isolate* to also affect the visibility.

   Specials
      Duplicate Layer
         Creates a copy of the current layer.
      Show All :kbd:`Alt-H`
         Makes all hidden layers visible.
      Hide Others :kbd:`Shift-H`
         Hides all non-selected layers.
      Lock/Unlock All
         Locks/Unlocks all of the layers. This can be useful to prevent unwanted editing.
      Merge Down
         Merges the current layer with the layer below it.

.. note::

   By default, most operations occur only on the *active* layer highlighted in the list.


Appearance Settings
===================

These settings can be used to change how the active layer appears.

Opacity
   The transparency of the layer.
X-Ray
   Makes the lines visible when they pass behind other objects in the scene.
Show Points
   Draws the start/end points that make up the stroke.

Tint
   Color
      The color to tint the layer.
   Factor
      The amount that the *Tint Color* has on the layer.

Thickness Change
   A relative change in pixels to apply to the thickness of all stroke in the active layer
   (works like a modifier).

   Apply (hand and bulged in blue line icon)
      If the apply button is pressed, the thickness change is applied and
      the value is reset to zero.


Animation
=========

Parent
   A :ref:`ui-data-id` to select the :term:`parent` object.
   The strokes of the layer will follow parent transformations.

   Type
      Type of :doc:`parent relation </editors/3dview/object/properties/relations/parents>`.

      Object, Armature, Bone

Lock Frame
   Locks the current frame displayed by layer.
Delete Frame
   Deletes the active frame for the active Grease Pencil Layer.


.. _grease-pencil-onion:

Onion Skinning
--------------

Onion-skinning, also known as ghosting, helps an animator by displaying the neighboring frames as a faded trail.

.. figure:: /images/interface_grease-pencil_drawing_layers_onion.png

   Grease Pencil Onion Skinning.

Onion Skinning
   Checkbox to enable onion skinning.
Always Show (camera icon)
   If enabled ghosts are displayed when scrubbing the view, playing back animation and/or in the OpenGL renders.
   There are two use cases where this is quite handy:

   - For creating a cheap motion-blur effect, especially when the before/after values are also animated.
   - If you've animated a shot with onion skinning enabled, the poses may end up looking odd
     if the ghosts are not shown (as you may have been accounting for the ghosts when making the compositions).
Use Custom Colors (color wheel icon)
   Toggles to use the *Before* and *After* controls to change the color of the ghosted frames.

Before/After
   Color
      The color of the strokes before/after the current frame.
   Before/After Range
      The maximum number of ghosts to show before/after the current frame.
      0 will only show the previous/next sketch, and -1 will not show any frames before/after current.
