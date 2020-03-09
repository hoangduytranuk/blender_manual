
********************
Connect Vertex Pairs
********************

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

The main difference between this tool and :doc:`/modeling/meshes/editing/vertex/connect_vertex_path`
is this tool ignores selection order and connects all selected vertices that share a face.
