
**************
Vertex Connect
**************

Connect Vertex Path
===================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Vertices --> Connect Vertex Path`
   :Hotkey:    :kbd:`J`

This tool connects vertices in the order they are selected, splitting the faces between them.

When there are only two vertices selected, a cut will be made across unselected faces,
a little like the Knife tool; however, this is limited to straight cuts across connected faces.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_pair-before.png

          Two disconnected vertices.

     - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_pair-after.png

          Result of connecting.

Running a second time will connect the first/last endpoints.

When many vertices are selected, faces will be split by their selected vertices.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_multi-before.png

          Before.

     - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_multi-after.png

          After.

Vertices not connected to any faces will create edges,
so this can be used as a way to quickly connect isolated vertices too.


Connect Vertices
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Vertices --> Connect Vertices`

This tool connects selected vertices by creating edges between them and splitting the face.

This tool can be used on many faces at once.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_before.png
          :width: 180px

          Vertices before connecting.

     - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_after.png
          :width: 180px

          After connecting vertices.

     - .. figure:: /images/modeling_meshes_editing_subdividing_vertex-connect_after-faces.png
          :width: 180px

          Resulting face pair.

The main difference between this tool and `Connect Vertex Path`_
is this tool ignores selection order and connects all selected vertices that share a face.
