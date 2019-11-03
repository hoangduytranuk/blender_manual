.. _objects-types:

************
Object Types
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Add`
   :Hotkey:    :kbd:`Shift-A`

New objects can be created with the *Add* menu in the 3D View's header.

Mesh
   :doc:`Meshes </modeling/meshes/introduction>` are objects
   composed of Polygonal Faces, Edges and/or Vertices, and
   can be edited extensively with Blender's mesh editing tools.
   See :doc:`Mesh Primitives </modeling/meshes/primitives>`.
Curve
   :doc:`Curves </modeling/curves/introduction>` are mathematically defined objects
   which can be manipulated with control handles or control points
   (instead of vertices), to manage their length and curvature.
   See :doc:`Curves Primitives </modeling/curves/primitives>`.
Surface
   :doc:`Surfaces </modeling/surfaces/introduction>` are patches that are
   also manipulated with control points. These are useful for simple rounded forms
   and organic landscapes.
   See :doc:`Surfaces Primitives </modeling/surfaces/primitives>`.
Metaball
   :doc:`Meta Objects </modeling/metas/introduction>` (or Metaballs) are objects
   formed by a mathematical function (with no control points or vertices)
   defining the 3D volume in which the object exists. Meta Objects have a liquid-like quality
   where when two or more Metaballs are brought together,
   they merge by smoothly rounding out the connection, appearing as one unified object.
   See :doc:`Meta Primitives </modeling/metas/primitives>`.
Text
   :doc:`Text objects </modeling/texts/introduction>`
   create a two-dimensional representation of a string of characters.
Grease Pencil
   :doc:`Grease Pencil Objects </grease_pencil/primitives>` are objects
   created by painting strokes.

Armature
   :doc:`Armatures </animation/armatures/index>` are used for rigging 3D models
   in order to make them poseable and animateable.
Lattice
   :doc:`Lattices </animation/lattice>` are non-renderable wireframes,
   commonly used for taking additional control over other objects
   with help of the :doc:`Lattice Modifier </modeling/modifiers/deform/lattice>`.

Empty
   :doc:`Empties </modeling/empties>` are null objects
   that are simple visual transform nodes that do not render.
   They are useful for controlling the position or movement of other objects.
Image
   Images are :doc:`empty </modeling/empties>` objects that display images
   in the 3D Viewport. These images can be used to support modeling and animating.

Light
   :doc:`Lights </render/lights/light_object>` for lighting the scene in
   renders.
Light Probe
   :doc:`Lights </render/eevee/lightprobes/introduction>` are used by
   the Eevee render engine and record lighting information for indirect lighting.

Camera
   This is the virtual camera that is used to determine what appears in the render.
   See Cameras in :doc:`Cycles </render/cameras>`.

Speaker
   :doc:`Speaker </render/output/audio/speaker>` brings a source of sound to the scene.

Force Field
   :doc:`Force Fields </physics/forces/force_fields/index>` are used in physical simulations.
   They give simulations external forces, creating movement, and
   are represented in the 3D Viewport as small control objects.

Collection Instance
   Lets you select from a list of existing collections. Once selected, an Empty object will be created,
   with an instance of the selected collection (collection instancing active).
   See :doc:`/scene_layout/object/properties/instancing/collection`.


.. _object-common-options:

Common Options
==============

You can change the options of the object in the :ref:`ui-undo-redo-adjust-last-operation` panel
just after creating it:

Type
   Some objects let you change their type after creation with a selector.
Radius/Size
   Sets the starting size.

Align
   Rotates the new object so that it is aligned in one of the following manners:

   World
      Aligns the object to the global space axes, i.e. the object's front faces the negative Y axis (default).
   View
      Aligns the object to the view space axes, i.e. the object's front faces the viewport's point of view.
   3D Cursor
      Aligns the object to match the rotation of the :doc:`3D Cursor </editors/3dview/3d_cursor>`.

Location
   Objects are placed, by default, at the position of the 3D Cursor.
   These values let you place the object in an other position.
Rotation
   Values let you rotate the object so that default rotation is overridden.
