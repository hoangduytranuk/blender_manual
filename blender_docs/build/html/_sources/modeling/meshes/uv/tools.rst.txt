
********
UV Tools
********

:ref:`Select <tool-select-tweak>`
   Select or moved.

   :ref:`Select Box <tool-select-box>`
      Select UVs by dragging a box.
   :ref:`Select Circle <tool-select-circle>`
      Select UVs by painting on it.
   :ref:`Select Lasso <tool-select-lasso>`
      Select UVs by drawing a lasso.

Cursor
   Change the location of the 3D Cursor.

Move
   Translation tool.
Rotate
   Rotation tool.
Scale
   Scale tool.

Transform
   Tool to adjust the UVs translation, rotations and scale.

:ref:`Annotate <tool-annotate>`
   Draw free-hand annotation.

   Annotate Line
      Draw straight line annotation.
   Annotate Polygon
      Draw a polygon annotation.
   Annotate Eraser
      Erase previous drawn annotations.

:doc:`Grab </modeling/meshes/uv/uv_sculpt>`
   The Grab brush moves UVs around.
:doc:`Relax </modeling/meshes/uv/uv_sculpt>`
   The Relax brush makes UVs more evenly distributed.
   The algorithm relies on space, not stretch minimization,
   so most probably a minimize stretch will have to be run for optimal results.
   Yet it is great to use after stitching islands,
   or when unwrap produces cluttered results to smooth the distribution of UVs.

   Relaxation Method
      There are two relax algorithms:

      Laplacian, HC
:doc:`Pinch </modeling/meshes/uv/uv_sculpt>`
   The Pinch brush moves UVs toward the brush's center.
   The pinch brush can be inverted by pressing :kbd:`Ctrl-LMB`.
