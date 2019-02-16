��                        �      �  z     	   �  *   �     �     �     �  )  �  <     �   >  3  �     ,     1     :     @  	   G  {   Q  2   �  _      g   `     �  �   �  j   �  m   	  L  �	  /   �  �   	     �  �  �      �  z   �  (   !  *   J     u     �     �  )  �  <   �  �   $  3  �          &     8     H     ]  {   w  2   �  _   &  g   �     �  �      j   �  m   D  L  �  /   �  �   /     �   :menuselection:`Bone --> Deform` A bone property, that controls the global influence of the bone over the deformed object, when using the envelopes method. All Modes Bone influence areas for envelopes method. Deform Distance Envelope Envelopes is the most general skinning method. It works with all available object types for skinning (meshes, lattices, curves, surfaces and texts). It is based on proximity between bones and their geometry, each bone having two different areas of influence, shown in the *Envelope* visualization: In this panel you can set deformation options for each bone. It also excludes the active bone in the automatic weight calculation when the mesh is parented to the armature using the *Armature Deform* tool with the "With Automatic Weights" option. It is only useful for the parts of geometry that are "shared", influenced by more than one bone (generally, at the joints...) -- a bone with a high weight will have more influence on the result than one with a low weight... Note that when set to 0.0, it has the same effect as disabling the *Deform* option. Mode Multiply Panel Radius Reference Set the radius for the head and the tail of envelope bones. Inside this volume, the geometry if fully affected by the bone. Single bone with various different envelope sizes. The 1st with a default radius value, the two others with differing Tail and Head radius values. The :doc:`editing pages </rigging/armatures/bones/editing/transform>` for how to edit these properties. The Deform panel. The Distance defines a volume which is the range within the bone has an influence on vertices of the deformed object. The geometry is less and less affected by the bone as it goes away by following a quadratic decay. The inside area, materialized by the "solid" part of the bone, and controlled by both root and tip radius. The outside area, materialized by the lighter part around the bone, and controlled by the *Distance* setting. This option controls how the two deforming methods interact, when they are both enabled. By default, when they are both active, all vertices belonging to at least one vertex group are only deformed through the vertex groups method. The other "orphan" vertices being handled by the envelopes one. When you enable this option, the "deformation influence" that this bone would have on a vertex (based from its envelope settings) is multiplied with this vertex's weight in the corresponding vertex group. In other words, the vertex groups method is further "weighted" by the envelopes method. Three Armature Bones all using Envelope Weight. Toggling the checkbox in the panel header off, prevents the bone from deforming the geometry at all, overriding any weights that it might have been assigned before; It mutes its influence. Weight Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-14 21:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :menuselection:`Bone --> Deform` A bone property, that controls the global influence of the bone over the deformed object, when using the envelopes method. Toàn Bộ các Chế Độ -- All Modes Bone influence areas for envelopes method. Biến Dạng -- Deform Khoảng Cách -- Distance Vỏ Bao -- Envelope Envelopes is the most general skinning method. It works with all available object types for skinning (meshes, lattices, curves, surfaces and texts). It is based on proximity between bones and their geometry, each bone having two different areas of influence, shown in the *Envelope* visualization: In this panel you can set deformation options for each bone. It also excludes the active bone in the automatic weight calculation when the mesh is parented to the armature using the *Armature Deform* tool with the "With Automatic Weights" option. It is only useful for the parts of geometry that are "shared", influenced by more than one bone (generally, at the joints...) -- a bone with a high weight will have more influence on the result than one with a low weight... Note that when set to 0.0, it has the same effect as disabling the *Deform* option. Chế Độ -- Mode Nhân -- Multiply Bảng -- Panel Bán Kính -- Radius Tham Chiếu -- Reference Set the radius for the head and the tail of envelope bones. Inside this volume, the geometry if fully affected by the bone. Single bone with various different envelope sizes. The 1st with a default radius value, the two others with differing Tail and Head radius values. The :doc:`editing pages </rigging/armatures/bones/editing/transform>` for how to edit these properties. The Deform panel. The Distance defines a volume which is the range within the bone has an influence on vertices of the deformed object. The geometry is less and less affected by the bone as it goes away by following a quadratic decay. The inside area, materialized by the "solid" part of the bone, and controlled by both root and tip radius. The outside area, materialized by the lighter part around the bone, and controlled by the *Distance* setting. This option controls how the two deforming methods interact, when they are both enabled. By default, when they are both active, all vertices belonging to at least one vertex group are only deformed through the vertex groups method. The other "orphan" vertices being handled by the envelopes one. When you enable this option, the "deformation influence" that this bone would have on a vertex (based from its envelope settings) is multiplied with this vertex's weight in the corresponding vertex group. In other words, the vertex groups method is further "weighted" by the envelopes method. Three Armature Bones all using Envelope Weight. Toggling the checkbox in the panel header off, prevents the bone from deforming the geometry at all, overriding any weights that it might have been assigned before; It mutes its influence. Trọng Lượng -- Weight 