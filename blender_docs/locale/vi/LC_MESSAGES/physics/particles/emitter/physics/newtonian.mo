��    *      l              �  ,   �  ~   �  �   i     �  �      �     �  	   �     �     �  
   �     �     �     �     �  k   �     d  �   p  .   F	     u	  	   ~	     �	     �	     �	     �	  >   �	  	   �	  �   �	     �
  �   	  	   �  I   �  �     B  �  	   �            %        :  f   A  e   �  �    M   �  ~     �   �     %  �  <    �  "   �     �  "        /     B     Q  U   e     �     �  k   �     I  �   d  .   :     i     �     �     �     �     �  >   �       �   7  ,   4  �   a       I   0  �   z  B  &     i     �     �  %   �     �  f   �  e   L   :menuselection:`Particle System --> Physics` A force that reduces particle velocity in relation to its speed and size (useful in order to simulate air drag or water drag). A tolerance value that allows the number of subframes to vary. It sets the relative distance a particle can move before requiring more subframes. Adaptive Subframes Also known as "2nd order Runge-Kutta". Slower than Euler but much more stable. If the acceleration is constant (no drag for example), it is energy conservative. It should be noted that in example of the bouncing particles, the particles might bounce higher than they started once in a while, but this is not a trend. This integrator is a generally good integrator for use in most cases. Also known as "Forward Euler". Simplest integrator. Very fast but also with less exact results. If no dampening is used, particles get more and more energy over time. For example, bouncing particles will bounce higher and higher each time. Should not be confused with "Backward Euler" (not implemented) which has the opposite feature, the energy decrease over time, even with no dampening. Use this integrator for short simulations or simulations with a lot of dampening where speedy calculations are more important than accuracy. Brownian Collision Collision Group Damp Die on Hit Drag Euler Forces Frame Settings If set, particles collide with objects from the group, instead of using objects that are on the same layer. Integration Integrators are a set of mathematical methods available to calculate the movement of particles. The following guidelines will help to choose a proper integrator, according to the behavior aimed at by the animator. Kill particle when it hits a deflector object. Midpoint Newtonian Newtonian Physics settings. Options Panel RK4 Reduces particle velocity (deceleration, friction, dampening). Reference Short for "4th order Runge-Kutta". Similar to Midpoint but slower and in most cases more accurate. It is energy conservative even if the acceleration is not constant. Only needed in complex simulations where Midpoint is found not to be accurate enough. Size Deflect Specify the amount of Brownian motion. Brownian motion adds random motion to the particles based on a Brownian noise field. This is nice to simulate small, random wind forces. Subframes The amount of simulation time (in seconds) that passes during each frame. The number of simulation steps per frame. Subframes to simulate for improved stability and finer granularity in simulations. Use higher values for faster-moving particles. The particles will move according to classical (Newtonian) mechanics. Particles start their life with the specified initial velocities and angular velocities, and move according to external forces. The response to environment and to forces is computed differently, according to the given integrator chosen by the animator. Threshold Timestep Type Use the particle size in deflections. Verlet Very fast and stable integrator, energy is conserved over time with very little numerical dissipation. When this checkbox without a label is enabled Blender will automatically set the number of subframes. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :menuselection:`Hệ Thống Hạt (Particle System) --> Vật Lý (Physics)` A force that reduces particle velocity in relation to its speed and size (useful in order to simulate air drag or water drag). A tolerance value that allows the number of subframes to vary. It sets the relative distance a particle can move before requiring more subframes.  -- Adaptive Subframes Also known as "2nd order Runge-Kutta". Slower than Euler but much more stable. If the acceleration is constant (no drag for example), it is energy conservative. It should be noted that in example of the bouncing particles, the particles might bounce higher than they started once in a while, but this is not a trend. This integrator is a generally good integrator for use in most cases. Also known as "Forward Euler". Simplest integrator. Very fast but also with less exact results. If no dampening is used, particles get more and more energy over time. For example, bouncing particles will bounce higher and higher each time. Should not be confused with "Backward Euler" (not implemented) which has the opposite feature, the energy decrease over time, even with no dampening. Use this integrator for short simulations or simulations with a lot of dampening where speedy calculations are more important than accuracy. Chuyển Động Brown -- Brownian Va Đập -- Collision Nhóm Va Đập -- Collision Group Lực Hãm -- Damp  -- Die on Hit Lực Cản -- Drag Euler (tên họ của nhà toán học Leonhard Euler, người Thụy Sĩ) -- Euler Lực -- Forces -- Frame Settings If set, particles collide with objects from the group, instead of using objects that are on the same layer. Tích Phân -- Integration Integrators are a set of mathematical methods available to calculate the movement of particles. The following guidelines will help to choose a proper integrator, according to the behavior aimed at by the animator. Kill particle when it hits a deflector object. Trung Điểm -- Midpoint Newton -- Newtonian Newtonian Physics settings. Tùy Chọn -- Options Bảng -- Panel RK4 Reduces particle velocity (deceleration, friction, dampening). Tham Chiếu -- Reference Short for "4th order Runge-Kutta". Similar to Midpoint but slower and in most cases more accurate. It is energy conservative even if the acceleration is not constant. Only needed in complex simulations where Midpoint is found not to be accurate enough. Đi Lệch Do Kích Thước -- Size Deflect Specify the amount of Brownian motion. Brownian motion adds random motion to the particles based on a Brownian noise field. This is nice to simulate small, random wind forces. Khung Hình Phủ -- Subframes The amount of simulation time (in seconds) that passes during each frame. The number of simulation steps per frame. Subframes to simulate for improved stability and finer granularity in simulations. Use higher values for faster-moving particles. The particles will move according to classical (Newtonian) mechanics. Particles start their life with the specified initial velocities and angular velocities, and move according to external forces. The response to environment and to forces is computed differently, according to the given integrator chosen by the animator. Giới Hạn -- Threshold Bước Thời Gian -- Timestep Thể Loại -- Type Use the particle size in deflections. Verlet Very fast and stable integrator, energy is conserved over time with very little numerical dissipation. When this checkbox without a label is enabled Blender will automatically set the number of subframes. 