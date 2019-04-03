.. _objects-types:

************
Object Types
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Tool Shelf --> Create --> Add Primitive`
   :Menu:      :menuselection:`Add`
   :Hotkey:    :kbd:`Shift-A`

New objects can be created with the *Add* menu in the 3D View's header.

Mesh
   :doc:`Meshes </modeling/meshes/introduction>` are objects composed of Polygonal Faces, Edges and/or Vertices,
   and can be edited extensively with Blender's mesh editing tools.
   See :doc:`Mesh Primitives </modeling/meshes/primitives>`.
Curve
   :doc:`Curves </modeling/curves/introduction>` are mathematically defined objects
   which can be manipulated with control handles or control points (instead of vertices),
   to manage their length and curvature. See :doc:`Curves Primitives </modeling/curves/primitives>`.
Surface
   :doc:`Surfaces </modeling/surfaces/introduction>` are patches that are also manipulated with control points.
   These are useful for simple rounded forms and organic landscapes.
   See :doc:`Surfaces Primitives </modeling/surfaces/primitives>`.
Metaball
   :doc:`Meta Objects </modeling/metas/introduction>` (or Metaballs) are objects formed by a mathematical function
   (with no control points or vertices) defining the 3D volume in which the object exists.
   Meta Objects have a liquid-like quality, where when two or more Metaballs are brought together,
   they merge by smoothly rounding out the connection, appearing as one unified object.
   See :doc:`Meta Primitives </modeling/metas/primitives>`.
Text
   :doc:`Text objects </modeling/texts/introduction>`
   create a two-dimensional representation of a string of characters.
Armature
   :doc:`Armatures </rigging/armatures/index>` are used for :doc:`rigging </rigging/introduction>`
   3D models in order to make them poseable and animateable.
Lattice
   :doc:`Lattices </rigging/lattice>` are non-renderable wireframes, commonly used for taking additional control
   over other objects with help of the :doc:`Lattice Modifier </modeling/modifiers/deform/lattice>`.
Empty
   :doc:`Empties </modeling/empties>` are null objects that are simple visual transform nodes that do not render.
   They are useful for controlling the position or movement of other objects.
Speaker
   :doc:`Speaker </render/audio/speaker>` brings a source of sound to the scene.
Camera
   This is the virtual camera that is used to determine what appears in the render.
   See Cameras in :doc:`Cycles </render/cycles/camera>`.
Lamp
   These are used to place light sources in the scene.
   See Lamps in :doc:`General Settings </render/lighting/index>`,
   :doc:`Cycles </render/cycles/lamps>`.
Force Field
   :doc:`Force Fields </physics/force_fields/index>` are used in physical simulations.
   They give simulations external forces, creating movement,
   and are represented in the 3D View editor as small control objects.
Group Instance
   Lets you select from a list of existing object groups.
   Once selected, an Empty object will be created, with an instance of the selected group (group duplication active).
   See :doc:`/editors/3dview/object/properties/duplication/dupligroup`.


.. _object-common-options:

Common Options
==============

You can change the options of the object in the Operator panel just after creating it:

Type
   Some objects let you change their type after creation with a selector.
Radius/Size
   Sets the starting size.

   .. from the center to what? compare plane to circle (3 vertices)

Align to View
   By default objects are aligned to the global space axes.
   This option rotates the new object so that it is aligned to the view space.
Location
   Objects are placed, by default, at the position of the 3D Cursor.
   These values let you place the object in an other position.
Rotation
   Values let you rotate the object so that default rotation is overridden.
