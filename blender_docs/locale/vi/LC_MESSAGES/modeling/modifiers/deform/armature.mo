��    (      \              �  )   �  (   �  *   �  *     )   F     p     �  �   �          "  �   1  f   �  *   !  `   L     �     �  z   �    >  )   V     �     �  p   �            �     �   �  �   q	  6   7
  $   n
  z   �
  D     $   S  (   x  h   �    
     (     5    C  #  J  �  n  )   &  (   P  *   y  *   �  )   �  /   �     )  �   <     �  (   �  �   �  f     *   �  `        r     �  z   �      )   .  .   X     �  p   �       '   %  �   M  �   �  �   �  6   e  $   �  z   �  D   <  $   �  (   �  h   �    8  %   V  &   |    �  #  �   100° rotation, Preserve Volume disabled. 100° rotation, Preserve Volume enabled. 179.9° rotation, Preserve Volume enabled. 180.1° rotation, Preserve Volume enabled. 180° rotation, Preserve Volume disabled. Armature Modifier Armature Modifier. Armature Modifiers can quickly be added to objects using the parenting shortcut :kbd:`Ctrl-P` when the active object is an armature. Bind To Bone Envelopes By adding an armature system to an object, that object can be deformed accurately so that geometry does not have to be animated by hand. Example of Quaternion option effects. Note that the IcoSphere is deformed using the envelopes weights. Example of vertex group's skinning method. For more details on armatures usage, see the :doc:`armature section </rigging/armatures/index>`. Initial state. Invert Inverts the influence set by the vertex group defined in previous setting (i.e. reverses the weight values of this group). Meshes and lattices only -- When enabled, bones of a given name will deform vertices which belong to :doc:`vertex groups </modeling/meshes/properties/vertex_groups/index>` of the same name. e.g. a bone named "forearm", will only affect the vertices in the "forearm" vertex group. Methods to bind the armature to the mesh. Multi Modifier Object Only meaningful when having at least two of these modifiers on the same object, with *Multi Modifier* activated. Options Preserve Volume The Armature Modifier is used for building skeletal systems for animating the poses of characters and anything else which needs to be posed. The influence of one bone on a given vertex is controlled by the weight of this vertex in the relevant group. A much more precise method than *Bone Envelopes*, but also generally longer to set up. The name of a vertex group of the object, the weights of which will be used to determine the influence of this Armature Modifier's result when mixing it with the results from other *Armature* ones. The name of the armature object used by this modifier. The result when posing the armature. The results of the Armature Modifiers are then mixed together, using the weights of the *Vertex Group* as "mixing guides". The same pose, but using envelopes method rather that vertex groups. The weights of the arm vertex group. The weights of the forearm vertex group. Use quaternions for preserving volume of object during deformation. It can be better in many situations. Use the same data as a previous modifier (usually also an Armature Modifier) as input. This allows you to use several armatures to deform the same object, all based on the "non-deformed" data (i.e. this avoids having the second Armature Modifier deform the result of the first one...). Vertex Group Vertex Groups When enabled, bones will deform vertices or control points near them, defined by each bone's envelope radius and distance. Enable/Disable bone :ref:`envelopes <armature-bones-envelope>` defining the deformation (i.e. bones deform vertices in their neighborhood). Without *Preserve Volume*, rotations at joints tend to scale down the neighboring geometry, up to nearly zero at 180 degrees from rest position. With *Preserve Volume*, the geometry is no longer scaled down, but there is a "gap", a discontinuity when reaching 180 degrees from rest position. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 100° rotation, Preserve Volume disabled. 100° rotation, Preserve Volume enabled. 179.9° rotation, Preserve Volume enabled. 180.1° rotation, Preserve Volume enabled. 180° rotation, Preserve Volume disabled. Bộ Điều Chỉnh Cốt -- Armature Modifier Armature Modifier. Armature Modifiers can quickly be added to objects using the parenting shortcut :kbd:`Ctrl-P` when the active object is an armature.  -- Bind To Vỏ Bao của Xương -- Bone Envelopes By adding an armature system to an object, that object can be deformed accurately so that geometry does not have to be animated by hand. Example of Quaternion option effects. Note that the IcoSphere is deformed using the envelopes weights. Example of vertex group's skinning method. For more details on armatures usage, see the :doc:`armature section </rigging/armatures/index>`. Initial state. Đảo Nghịch -- Invert Inverts the influence set by the vertex group defined in previous setting (i.e. reverses the weight values of this group). Meshes and lattices only -- When enabled, bones of a given name will deform vertices which belong to :doc:`vertex groups </modeling/meshes/properties/vertex_groups/index>` of the same name. e.g. a bone named "forearm", will only affect the vertices in the "forearm" vertex group. Methods to bind the armature to the mesh. Nhiều Bộ Điều Chỉnh -- Multi Modifier Vật Thể -- Object Only meaningful when having at least two of these modifiers on the same object, with *Multi Modifier* activated. Tùy Chọn -- Options Duy Trì Thể Tích -- Preserve Volume The Armature Modifier is used for building skeletal systems for animating the poses of characters and anything else which needs to be posed. The influence of one bone on a given vertex is controlled by the weight of this vertex in the relevant group. A much more precise method than *Bone Envelopes*, but also generally longer to set up. The name of a vertex group of the object, the weights of which will be used to determine the influence of this Armature Modifier's result when mixing it with the results from other *Armature* ones. The name of the armature object used by this modifier. The result when posing the armature. The results of the Armature Modifiers are then mixed together, using the weights of the *Vertex Group* as "mixing guides". The same pose, but using envelopes method rather that vertex groups. The weights of the arm vertex group. The weights of the forearm vertex group. Use quaternions for preserving volume of object during deformation. It can be better in many situations. Use the same data as a previous modifier (usually also an Armature Modifier) as input. This allows you to use several armatures to deform the same object, all based on the "non-deformed" data (i.e. this avoids having the second Armature Modifier deform the result of the first one...). Nhóm Điểm Đỉnh -- Vertex Group Nhóm Điểm Đỉnh -- Vertex Groups When enabled, bones will deform vertices or control points near them, defined by each bone's envelope radius and distance. Enable/Disable bone :ref:`envelopes <armature-bones-envelope>` defining the deformation (i.e. bones deform vertices in their neighborhood). Without *Preserve Volume*, rotations at joints tend to scale down the neighboring geometry, up to nearly zero at 180 degrees from rest position. With *Preserve Volume*, the geometry is no longer scaled down, but there is a "gap", a discontinuity when reaching 180 degrees from rest position. 