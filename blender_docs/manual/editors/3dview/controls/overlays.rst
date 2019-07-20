
*****************
Viewport Overlays
*****************

Using the Viewport Overlays pop-over settings for the overlays can be configured.
There is a switch to turn off all overlays for the 3D View.

The options that are visible in the pop-over depends on the mode that the 3D View is in.


Object Mode
===========

The next options are always present, independent the current mode.


Guides
------

Grid
   Show grid in orthographic side view.
Floor
   Show the ground plane.

   X/Y/Z
      Show the X and/or Y and/or Z axis line.

Scale
   The distance between lines in the grid/floor.
Subdivision
   The number of subdivisions between grid lines.

Text Info
   Show text overlay.
3D Cursor
   Show the 3D Cursor overlay.
Annotations
   Show the annotation overlay.


Objects
-------

Extra
   Show details of objects including empty wires, cameras and other visual guides.
Relationship Lines
   Show dashed lines indicating parents or constraint relationships.
Outline Selected
   Show an outline highlight around selected objects.
Bones
   Show Bones. Disable to only show their motion path.
Motion Paths
   Show the motion path overlay.
Origin
   Show the object origin of the active object.
Origin (All)
   Show the object origin of all objects.


Geometry
--------

Wireframe
   Show the face edges overlay.

   Wireframe
      Adjust the number of wires to display. 1.0 means show all wires.

Face Orientation
   Show the face orientation overlay. In the face orientation overlay
   all faces where the face normal point towards the camera are colored blue.
   All faces where the face normal point away from the camera are colored red.
   With this overlay it is easy to detect the orientation of the face normals.


Motion Tracking
---------------

Show the motion tracking overlay.

Camera Path
   Show the reconstruction camera path.
Marker Names
   Show the names for reconstructed track objects.

Tracks
   Change the display of the reconstructed tracks.

   - Plain Axes
   - Arrows
   - Single Arrow
   - Circle
   - Cube
   - Sphere
   - Cone

Size
   Change the display size of the recontructed tracks.


.. _3dview-overlay-mesh_edit_mode:

Mesh Edit Mode
==============

The next options are available when in Edit Mesh Mode.

Edges
   Highlighted selected and partially selected edges.

   *Only affects vertex and face selection mode (as edges are always highlighted in edge-selection mode).*
Faces
   Highlight faces using a face overlay that applies to both selected and unselected faces.

   *Affects all selection modes.*
Center
   Show face-center points in solid shading modes.

   *Only affects face-select mode.*
Creases
   Display edges marked with a crease
   for the :doc:`Subdivision Surface Modifier </modeling/modifiers/generate/subdivision_surface>`.
Sharp
   Display sharp edges, used with the edge split modifier.
Bevel
   Display weights created for the :doc:`Bevel Modifier </modeling/modifiers/generate/bevel>`.
Seams
   Display the UV unwrapping seams.
Edge Marks and Face Marks
   Used by Freestyle.


Shading
-------

Hidden Wire
   Show only front-facing wireframes.
   This is useful for a re-topology workflow.

   .. tip::

      Optimally this could be combined with the *X-Ray* display setting.

Vertex Groups Weights
   Display weights in Edit Mode.

   Zero Weights
      Display unweighted vertices:

      :None:
      :Active: Show vertices with no weights in the active group.
      :All: Show vertices with no weights in any group.


Mesh Analysis
-------------

Show the mesh analysis overlay.

See: :ref:`modeling-mesh-analysis`.


Measurement
-----------

Numerical measures of the selected elements on screen as part of the text info overlay.
The :ref:`data-scenes-props-units` can be set in the Scene properties.

Edge Length
   Shows the length of selected edges.
Edge Angle
   Shows the angle of selected edges between two faces.
Face Area
   Show the area of selected faces.
Face Angle
   Show the angle of selected face corners.

.. tip::

   Geometry connected to the selection is shown while transforming,
   allowing you to move a vertex and see the connected edge lengths for example.

.. note::

   These values respect :ref:`Global/Local <modeling-mesh-transform-panel>`.

   Use *Global* if you want the Object's scale to be applied to the measurements.


.. _mesh-display-normals:

Normals
-------

- Display vertex normals
- Display face normals at vertices (split normals)
- Display face normals

Size
   The size to show the selected normals.


Developer
---------

Indices
   Display the indices of selected vertices, edges and faces.


Freestyle
---------

Edge Marks
   Display Freestyle edge marks, used with the Freestyle renderer.
Face Marks
   Display Freestyle face marks, used with the Freestyle renderer.


Sculpt Mode
===========

Show Diffuse Color
   Show diffuse color of object and overlay sculpt mask on top of it.

Mask
   Show mask as overlay on object. The opacity of the overlay can be controlled.


Vertex Paint
============

Opacity
   The opacity of the overlay.
Show Wire
   Use wireframe display in paint modes.


Weight Paint
============

Opacity
   The opacity of the overlay.
Zero Weights
   Zero Weights
      Display unweighted vertices.

      - None
      - Active: Show vertices with no weights in the active group.
      - All: Show vertices with no weights in any group.
Show Weight Contours
   Show contour lines formed by points with the same interpolated weight.
Show Wire
   Use wireframe display in paint modes.


Texture Paint
=============

Opacity
   The opacity of the overlay.


Pose Mode
=========

Fade Geometry
   Show the bones on top and face other geometry to the back.
   The opacity can be controlled with the slider.


.. _3dview-overlay-grease-pencil:

Grease Pencil
=============

Onion Skin
   Show ghosts of the keyframes before and after the current frame.
Canvas
   Display a grid over Grease Pencil drawing plane. The opacity of the grid can be controlled with a slider.
Fade 3D Objects
   Cover all viewport with a full color layer to improve visibility while drawing over complex scenes.
   The opacity of the color layer can be adjusted.
Fade Layers
   Decreases the opacity of all the layers in the object other than the active one.
Edit Lines
   Show edit lines when editing strokes.
Show Edit Lines only in multiframe
   Only show edit lines while in multiframe edition.
Vertex Opacity
   Opacity for edit vertices (points).
