��          �               L    M  	   `  �  j  -      �  .  �   �  �   W  y   �    X     d  }   �     b	     w	  �   �	  .  
  %  C     i  q  n  �  �    �     �  �  �  1   [  �  �  �   4  �   �  y   =    �     �  }   C     �     �  �   �  .  {  %  �     �  q  �   Animating the strengths of various other parameters (a :doc:`Motor's </physics/rigid_body/constraints/types/motor>` Target Velocity, a :doc:`Hinge's </physics/rigid_body/constraints/types/hinge>` limits, etc.) can be used to accomplish a wide variety of interesting results. Animation As with all physics-enabled objects, pay close attention to the *Animated* checkbox in the *Rigid Body* panel of the *Physics* tab in the Properties editor. A common mistake is to use keyframe animation on a *Passive* physics object without checking the *Animated* box. The object will move, but the physics engine will behave as if the *Passive* is still in its starting place, leading to disappointment. Combining Rigid Bodies with Other Simulations Enabling a constraint during the physics simulation often has dramatic results as the physics engine tries to bring into alignment two objects which are often dramatically out of alignment. It is very common for the affected objects to build up enough kinetic energy to bounce themselves out of camera (and into orbit, although the physics engine is not yet capable of simulating a planet's gravity well, so scratch that). If dynamic scaling is not needed, rigid body objects should have the scale applied by using the *Apply Scale* tool :kbd:`Ctrl-A`. In order for this to work, the rigid body object needs to have a Collision Modifier. Simply click on *Collision* in the *Physics* tab. Increasing the number of solver iterations helps making constraints stronger and also improves object stacking stability. It is best to avoid small objects, as they are currently unstable. Ideally, objects should be at least 20 cm in diameter. If it is still necessary, setting the collision margin to 0, while generally not recommended, can help making small object behave more naturally. Rigid body dynamics can be baking to normal keyframes with *Bake To Keyframes* button in the *Physics* tab of the *Tool Shelf*. Rigid body objects can be scaled, also during the simulation. This work well in most cases, but can sometimes cause problems. Scaling Rigid Bodies Simulation Stability Since the rigid body simulation is part of the animation system, it can influence other simulations just like the animation system can. The most common trick is to :term:`keyframe` animate the location or rotation of an *Active* physics object as well as the *Animated* checkbox. When the curve on the *Animated* property switches to disabled, the physics engine takes over using the object's last known location, rotation and velocities. The simplest way of improving simulation stability is to increase the steps per second. However, care has to be taken since making too many steps can cause problems and make the simulation even less stable (if you need more than 1000 steps, you should look at other ways to improve stability). Tips When objects are small and/or move very fast, they can pass through each other. Besides what is mentioned above it's also good to avoid using mesh shapes in this case. Mesh shapes consist of individual triangles and therefore do not really have any thickness, so objects can pass through more easily. You can give them some thickness by increasing the collision margin. Project-Id-Version: Blender 2.79 Manual 2.79
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
 Animating the strengths of various other parameters (a :doc:`Motor's </physics/rigid_body/constraints/types/motor>` Target Velocity, a :doc:`Hinge's </physics/rigid_body/constraints/types/hinge>` limits, etc.) can be used to accomplish a wide variety of interesting results. Hoạt Hình -- Animation As with all physics-enabled objects, pay close attention to the *Animated* checkbox in the *Rigid Body* panel of the *Physics* tab in the Properties editor. A common mistake is to use keyframe animation on a *Passive* physics object without checking the *Animated* box. The object will move, but the physics engine will behave as if the *Passive* is still in its starting place, leading to disappointment.  -- Combining Rigid Bodies with Other Simulations Enabling a constraint during the physics simulation often has dramatic results as the physics engine tries to bring into alignment two objects which are often dramatically out of alignment. It is very common for the affected objects to build up enough kinetic energy to bounce themselves out of camera (and into orbit, although the physics engine is not yet capable of simulating a planet's gravity well, so scratch that). If dynamic scaling is not needed, rigid body objects should have the scale applied by using the *Apply Scale* tool :kbd:`Ctrl-A`. In order for this to work, the rigid body object needs to have a Collision Modifier. Simply click on *Collision* in the *Physics* tab. Increasing the number of solver iterations helps making constraints stronger and also improves object stacking stability. It is best to avoid small objects, as they are currently unstable. Ideally, objects should be at least 20 cm in diameter. If it is still necessary, setting the collision margin to 0, while generally not recommended, can help making small object behave more naturally. Rigid body dynamics can be baking to normal keyframes with *Bake To Keyframes* button in the *Physics* tab of the *Tool Shelf*. Rigid body objects can be scaled, also during the simulation. This work well in most cases, but can sometimes cause problems.  -- Scaling Rigid Bodies  -- Simulation Stability Since the rigid body simulation is part of the animation system, it can influence other simulations just like the animation system can. The most common trick is to :term:`keyframe` animate the location or rotation of an *Active* physics object as well as the *Animated* checkbox. When the curve on the *Animated* property switches to disabled, the physics engine takes over using the object's last known location, rotation and velocities. The simplest way of improving simulation stability is to increase the steps per second. However, care has to be taken since making too many steps can cause problems and make the simulation even less stable (if you need more than 1000 steps, you should look at other ways to improve stability). Ngọn -- Tips When objects are small and/or move very fast, they can pass through each other. Besides what is mentioned above it's also good to avoid using mesh shapes in this case. Mesh shapes consist of individual triangles and therefore do not really have any thickness, so objects can pass through more easily. You can give them some thickness by increasing the collision margin. 