
************
Introduction
************

Eevee is not a ray tracing engine and cannot do ray-triangle intersection.
Instead of this, Eevee uses the depth buffer as an approximated scene representation.
This reduces the complexity of scene scale effects and allows high performances.
However, only what is in inside the view can be considered when computing these effects.
Also, since it only uses one layer of depth, only the front-most pixel distance is known.

These limitations creates a few problems:

- The screen space effects disappear when reaching the screen border.
  This can be partially fixed by using the *overscan* feature.
- The screen space effects don't know how deep (or thick) the objects are.
  This is why most effects have a thickness parameter to control how to consider potential intersected pixels.
- Blended surfaces are not considered by these effects.
  They are not part of the depth prepass and do not appear in the depth buffer.
