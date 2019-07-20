
******************
Weight Paint Tools
******************

Draw
   Paints a specified weight over the object.

Blur
   Smooths out the weighting of adjacent vertices. In this mode the Weight
   Value is ignored. The strength defines how much the smoothing is applied.

Average
   Smooths weights by painting the average resulting weight from all weights under the brush.

Smear
   Smudges weights by grabbing the weights under the brush and "dragging" them.
   This can be imagined as a finger painting tool.

Gradient
   Applies a linear/radial weight gradient;
   this is useful at times when painting gradual changes in weight becomes difficult.
   Blends the weights of selected vertices with unselected vertices.

   .. figure:: /images/sculpt-paint_weight-paint_weight-tools_gradient.png

      Example of the Gradient tool being used with selected vertices.

   Weight
      The gradient starts at the current selected weight value, blending out to nothing.
   Strength
      Lower values can be used so the gradient mixes in with the existing weights (just like with the brush).
   Type
      - Linear: :kbd:`Alt-LMB` and drag.
      - Radial: :kbd:`Ctrl-Alt-LMB` and drag.

Sample
   Weights
      Sets the brush *Weight* as the weight selected under the cursor.
   Vertex Group
      Displays a list of possible vertex groups to select that are under the cursor.

:ref:`Annotate <tool-annotate>`
   Draw free-hand annotation.

   Annotate Line
      Draw straight line annotation.
   Annotate Polygon
      Draw a polygon annotation.
   Annotate Eraser
      Erase previous drawn annotations.
