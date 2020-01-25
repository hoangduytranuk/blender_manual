
*******
Options
*******

.. figure:: /images/sculpt-paint_weight-paint_options_options-panel.png
   :align: right

   Paint options.

The Weight Paint Options modify the overall brush behavior:

Auto Normalize
   Ensures that all deforming vertex groups add up to one while painting.
   When this option is turned off, then all weights of a vertex can have any value between 0.0 and 1.0.
   However, when Vertex Groups are used as Deform Groups for character animation
   then Blender always interprets the weight values relative to each other.
   That is, Blender always does a normalization over all deform bones.
   Hence in practice it is not necessary to maintain a strict normalization and
   further normalizing weights should not affect animation at all.

   This option works most intuitively when used to maintain normalization while
   painting on top of weights that are already normalized with some other tool.
Multi-Paint
   Paint on all selected Vertex Groups simultaneously, in a way that preserves their relative influence.
   This can be useful when tweaking weights in an area that is affected by more than three bones at once,
   e.g. certain areas on a character's face.

   This option is only useful in the Armature tab, where you can select multiple
   Vertex Groups by selecting multiple Pose bones. Once at least two Vertex
   Groups are selected, viewport colors and paint logic switch to Multi-Paint Mode,
   using the sum of the selected groups' weights if Auto Normalize is enabled,
   and the average otherwise. Any paint operations aimed at this collective weight are applied to
   individual Vertex Group weights in such way that their ratio stays the same.

   Since the ratio is undefined if all weights are zero, Multi-Paint cannot operate on
   vertices that do not have any weight assigned to the relevant Vertex Groups.
   For this reason it also does not allow reducing the weight all the way to zero.
   When used with X Mirror, it only guarantees completely a symmetrical result
   if weights are initially symmetrical.

   .. tip::

      While Multi-Paint cannot directly paint on zero-weight vertices,
      it is possible to use the *Smooth Weight* tool to copy a reasonable non-zero
      weight distribution from adjacent vertices without leaving Multi-Paint Mode
      or changing bone selection.

      To do that, enable vertex selection, select target vertices, and apply one
      iteration of the tool using vertex groups from *Selected Pose Bones* with low Factor.
      After that simply paint on top to set the desired collective weight.

Restrict
   This option limits the influence of painting to vertices (even with weight 0)
   belonging to the selected vertex group.
X Mirror
   Use the X Mirror option for mirrored painting on groups that have symmetrical names,
   like with extension ".R"/ ".L" or "_R" / "_L". If a group has no mirrored counterpart,
   it will paint symmetrically on the active group itself.
   You can read more about the naming convention in
   :ref:`Editing Armatures: Naming conventions <armature-editing-naming-conventions>`.
   The convention for armatures/bones apply here as well.
Topology Mirror
   Use topology-based mirroring, for when both sides of a mesh have matching mirrored topology.
   See :ref:`here <modeling_meshes_editing_topology-mirror>` for more information.


.. seealso::

   See the :ref:`Brush Display <sculpt-paint-brush-display>` options.
