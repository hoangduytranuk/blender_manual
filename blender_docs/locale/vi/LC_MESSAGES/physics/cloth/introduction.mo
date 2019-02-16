��          �               �  /   �  7  �         $  .   0  �  _  ]  O  P   �     �  L     V  ]     �	  L   �	  N   
  �   ]
  3     �  ;  _     �    �   
  �   �  l   i     �  9  �  �    /   �  7       9    H  .   T  �  �  ]  s  P   �     "  L   4  V  �     �  L   �  N   D  �   �  3   =  �  q  _   U  �  �  �   @!  �   �!  l   �"  "   #  9  /#   A general process for working with cloth is to: A piece of cloth is any mesh, open or enclosed, that has been designated as cloth. The *Cloth* panels are located in the *Physics* tab and consist of three panels of options. Cloth is either an open or closed mesh and is mass-less, in that all cloth is assumed to have the same density, or mass per square unit. Cloth example. Cloth is commonly modeled as a mesh grid primitive, or a cube, but can also be, for example, a teddy bear. However, Blender's :doc:`soft body system </physics/soft_body/index>` provides better simulation of closed meshes; Cloth is a specialized simulation of fabrics. Cloth on carved wooden men (made by motorsep). Cloth simulation is one of the hardest aspects of CG, because it is a deceptively simple real-world item that is taken for granted, yet actually has very complex internal and environmental interactions. After years of development, Blender has a very robust cloth simulator that is used to make clothing, flags, banners, and so on. Cloth interacts with and is affected by other moving objects, the wind and other forces, as well as a general aerodynamic model, all of which is under your control. Computation of the shape of the cloth at every frame is automatic and done in the background; thus you can continue working while the simulation is computed. However, it is CPU-intensive and depending on the power of your PC and the complexity of the simulation, the amount of CPU needed to compute the mesh varies, as does the lag you might notice. Designate the object as a "cloth" in the *Physics* tab of the Properties editor. Do not jump ahead If desired, give the object particles, such as steam coming off the surface. If you set up a cloth simulation but Blender has not computed the shapes for the duration of the simulation, and if you jump ahead a lot of frames forward in your animation, the cloth simulator may not be able to compute or show you an accurate mesh shape for that frame, if it has not previously computed the shape for the previous frame(s). Introduction Light the cloth and assign materials and textures, UV unwrapping if desired. Make minor edits to the mesh on a frame-by-frame basis to correct minor tears. Model other deflection objects that will interact with the cloth. Ensure the Deflection modifier is last on the modifier stack, after any other mesh deforming modifiers. Model the cloth object as a general starting shape. Once the object is designated as Cloth, a Cloth :doc:`modifier </modeling/modifiers/index>` will be added to the object's modifier stack automatically. As a :doc:`modifier </modeling/modifiers/index>` then, it can interact with other modifiers, such as *Armature* and *Smooth*. In these cases, the ultimate shape of the mesh is computed in accordance with the order of the modifier stack. For example, you should smooth the cloth *after* the modifier computes the shape of the cloth. Optionally age the mesh to some point in the simulation to obtain a new default starting shape. Results of the simulation are saved in a cache, so that the shape of the mesh, once calculated for a frame in an animation, does not have to be recomputed again. If changes to the simulation are made, you have full control over clearing the cache and re-running the simulation. Running the simulation for the first time is fully automatic and no baking or separate step interrupts the workflow. Run the simulation and adjust Options to obtain satisfactory results. The Timeline editors VCR controls are great for this step. So you edit the Cloth settings in two places: use the Physics buttons to edit the properties of the cloth and use the Modifier stack to edit the Modifier properties related to display and interaction with other modifiers. To avoid unstable simulation, ensure that the cloth object does not penetrate any of the deflection objects, Workflow You can *Apply* the Cloth Modifier to freeze, or lock in, the shape of the mesh at that frame, which removes the modifier. For example, you can drape a flat cloth over a table, let the simulation run, and then apply the modifier. In this sense, you are using the simulator to save yourself a lot of modeling time. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-11 06:33+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A general process for working with cloth is to: A piece of cloth is any mesh, open or enclosed, that has been designated as cloth. The *Cloth* panels are located in the *Physics* tab and consist of three panels of options. Cloth is either an open or closed mesh and is mass-less, in that all cloth is assumed to have the same density, or mass per square unit. Cloth example. Cloth is commonly modeled as a mesh grid primitive, or a cube, but can also be, for example, a teddy bear. However, Blender's :doc:`soft body system </physics/soft_body/index>` provides better simulation of closed meshes; Cloth is a specialized simulation of fabrics. Cloth on carved wooden men (made by motorsep). Cloth simulation is one of the hardest aspects of CG, because it is a deceptively simple real-world item that is taken for granted, yet actually has very complex internal and environmental interactions. After years of development, Blender has a very robust cloth simulator that is used to make clothing, flags, banners, and so on. Cloth interacts with and is affected by other moving objects, the wind and other forces, as well as a general aerodynamic model, all of which is under your control. Computation of the shape of the cloth at every frame is automatic and done in the background; thus you can continue working while the simulation is computed. However, it is CPU-intensive and depending on the power of your PC and the complexity of the simulation, the amount of CPU needed to compute the mesh varies, as does the lag you might notice. Designate the object as a "cloth" in the *Physics* tab of the Properties editor. Do not jump ahead If desired, give the object particles, such as steam coming off the surface. If you set up a cloth simulation but Blender has not computed the shapes for the duration of the simulation, and if you jump ahead a lot of frames forward in your animation, the cloth simulator may not be able to compute or show you an accurate mesh shape for that frame, if it has not previously computed the shape for the previous frame(s). Giới Thiệu -- Introduction Light the cloth and assign materials and textures, UV unwrapping if desired. Make minor edits to the mesh on a frame-by-frame basis to correct minor tears. Model other deflection objects that will interact with the cloth. Ensure the Deflection modifier is last on the modifier stack, after any other mesh deforming modifiers. Model the cloth object as a general starting shape. Once the object is designated as Cloth, a Cloth :doc:`modifier </modeling/modifiers/index>` will be added to the object's modifier stack automatically. As a :doc:`modifier </modeling/modifiers/index>` then, it can interact with other modifiers, such as *Armature* and *Smooth*. In these cases, the ultimate shape of the mesh is computed in accordance with the order of the modifier stack. For example, you should smooth the cloth *after* the modifier computes the shape of the cloth. Optionally age the mesh to some point in the simulation to obtain a new default starting shape. Results of the simulation are saved in a cache, so that the shape of the mesh, once calculated for a frame in an animation, does not have to be recomputed again. If changes to the simulation are made, you have full control over clearing the cache and re-running the simulation. Running the simulation for the first time is fully automatic and no baking or separate step interrupts the workflow. Run the simulation and adjust Options to obtain satisfactory results. The Timeline editors VCR controls are great for this step. So you edit the Cloth settings in two places: use the Physics buttons to edit the properties of the cloth and use the Modifier stack to edit the Modifier properties related to display and interaction with other modifiers. To avoid unstable simulation, ensure that the cloth object does not penetrate any of the deflection objects, Quy Trình Làm Việc -- Workflow You can *Apply* the Cloth Modifier to freeze, or lock in, the shape of the mesh at that frame, which removes the modifier. For example, you can drape a flat cloth over a table, let the simulation run, and then apply the modifier. In this sense, you are using the simulator to save yourself a lot of modeling time. 