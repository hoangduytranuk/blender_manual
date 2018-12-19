
**********************
Texture Blending Modes
**********************

Blending Modes are different methods of controlling how the texture influences material properties.
While a blending mode defines the specific operation performed,
blending factor controls the amount, the overall "strength" of this operation.
For textures such blending factor is set via sliders in the Influence panel.

Blend
   Blending operation to perform. See :term:`Color Blend Modes` for details on each blending mode.
RGB to Intensity
   With this option enabled, an RGB texture (affects color) is used as an intensity texture (affects a value).
Blend Color
   If the texture is mapped to Color,
   what color is blended in according to the intensity of the texture?
Negative
   The effect of the Texture is negated. Normally white means on, black means off, *Negative* reverses that.
Stencil
   The active texture is used as a mask for all following textures.
   This is useful for semitransparent textures and "Dirt Maps".
   Black sets the pixel to "untexturable". The *Stencil* mode works similar to a layer mask in a 2D program.
   The effect of a stencil texture cannot be overridden, only extended. You need an intensity map as input.
Destination Value
   The value (not for RGB) with which the Intensity texture blends with the current value. Two examples:

   - The *Emit* value is normally 0. With a texture mapped to *Emit* you will get maximal effect,
     because *DVar* is 1 by default. If you set *DVar* to 0 no texture will have any effect.
   - If you want transparent material, and use a texture mapped to *Alpha*,
     nothing happens with the default settings, because the *Alpha* value in the *Material* panel is 1.
     So you have to set *DVar* to 0 to get transparent material (and of course *Z Transparency* also).
     This is a common problem for beginners. Or do it the other way round: set *Alpha* to 0 and leave *Dvar* on 1.
     Of course the texture is used inverted then.
