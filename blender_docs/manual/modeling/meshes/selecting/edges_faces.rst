
*************
Edges & Faces
*************

Edges
=====

.. figure:: /images/modeling_meshes_selecting_edges-faces_mode-buttons-edge-activated.png

   Buttons for the selection modes.

Edges can be selected in much the same way as vertices and faces
by :kbd:`RMB`-clicking them while Edge Select Mode is activated.
Pressing :kbd:`Shift` while clicking will add/subtract to the existing selection.


.. _modeling-meshes-selecting-edge-loops:

Edge Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode (Mesh)
   :Menu:      :menuselection:`Select --> Edge Loop`
   :Hotkey:    :kbd:`Alt-RMB`, or :kbd:`Shift-Alt-RMB` for modifying existing selection

Edge loops can be selected by first selecting an edge (vertex or edge selection mode),
and then going to :menuselection:`Select --> Edge Loop`. The shortcut :kbd:`Alt-RMB` on an edge
(either vertex or edge select mode) is a quicker and more powerful way of doing so.
More powerful, because you can add/remove loops from an existing selection if you press
:kbd:`Shift` too.

Note, that if you want to select a loop while being in vertex select mode,
you still have to perform the shortcut on an edge -- while you,
for just selecting vertices, would :kbd:`RMB` on a vertex.

.. figure:: /images/modeling_meshes_selecting_edges-faces_edge-loop-example.png

   An edge loop.


Edge Rings
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode (Mesh)
   :Menu:      :menuselection:`Select --> Edge Ring`
   :Hotkey:    :kbd:`Ctrl-Alt-RMB`, or :kbd:`Shift-Ctrl-Alt-RMB` for modifying existing selection

Edge Rings are selected similarly.
Based on the selection of an edge go to :menuselection:`Select --> Edge Ring`.
Or use :kbd:`Ctrl-Alt-RMB` on an edge.

.. figure:: /images/modeling_meshes_selecting_edges-faces_edge-ring-example.png

   An edge ring.

.. note:: Convert Selection to Whole Faces

   If the edge ring selection happened in Edge Select Mode, switching to Face Select Mode will erase the selection.

   This is because none of those faces had all its (four) edges selected,
   just two of them.

   Instead of selecting the missing edges manually or by using :kbd:`Shift-Alt-RMB` twice,
   it is easier to first switch to Vertex Select Mode, which will kind of "flood" the selection.
   A subsequent switch to Face Select Mode will then properly select the faces.


Faces
=====

.. figure:: /images/modeling_meshes_selecting_edges-faces_mode-buttons-face-activated.png

   The Face Select Mode activated.

To select parts of a mesh face-wise, you have to switch to Face Select Mode.
Do this by clicking the button shown above, or press :kbd:`Ctrl-Tab` to spawn a menu.
The selection works as usual with :kbd:`RMB`;
to add/remove to an existing selection, additionally press :kbd:`Shift`.
The Border, Circle and Lasso Selection Tools must intersect the face indicators
usually represented by small pixel squares; one at the center of each face.


.. _modeling-meshes-selecting-face-loops:

Face Loops
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode (Mesh)
   :Hotkey:    :kbd:`Alt-RMB` or :kbd:`Shift-Alt-RMB` for modifying existing selection

Face Loops are pretty much the same as Edge Rings. If you want to select a Face Loop,
there is no menu entry that works based on a selected face. Using :menuselection:`Select --> Edge Ring`
would select a "cross" with the prior selected face as the middle.
If you want to avoid switching to Edge Select Mode to select a Face Loop,
use the :kbd:`Alt-RMB` shortcut.

.. figure:: /images/modeling_meshes_selecting_edges-faces_face-mode-different-loop-selections.png

   Different loop selection operations on a grid in Face Select Mode.

- Just the selected face.
- Select the face, then :menuselection:`Select --> Edge Ring`.
  See, how Blender selects edges, even if being in Face Select Mode.
  If these edges are desired and you want to work on them, switch in Edge Select Mode.
  Switching to Vertex Select Mode would flood the selection and leave you with the 4th image as result,
  after going back to Face Select Mode.
- Select the face, the :menuselection:`Select --> Edge Loop`.
  As in the example above, Blender pretends to be in Edge Select Mode and takes the four edges of the selected face
  as base for the selection operation.
- This selection was created by :kbd:`Alt-RMB` on the left edge of the center face,
  followed by twice :kbd:`Shift-Alt-RMB` on the top edge of the center face. Two times,
  because the first click will remove the selected face loop (in this case, just the original selected face),
  while the second click will add the whole vertical running loop to the selection, creating the cross.


N-gons in Face Select Mode
--------------------------

.. figure:: /images/modeling_meshes_selecting_edges-faces_face-mode-ngon-visual-problem.png

   N-gon face having its center dot inside another face.

As already known, faces are marked with a little square dot in the middle of the face.
With n-gons that can lead in certain cases to a confusing display.
The example shows the center dot of the U-shaped n-gon being inside of the oblong face inside the "U".
It is not easy to say which dot belongs to which face (the orange dot in the image is the object origin).
Luckily, you do not need to care much, because to select a face, you do not have to click the center dot,
but the face itself.

.. tip:: Face selection

   *To select a face*: Click the face, not the dot!
