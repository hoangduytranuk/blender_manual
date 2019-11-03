��          �               �  -   �  �  �     �     �     �     �     �  	   �     �     �                    &     ,     ;  	   B  
   L  �   W  �  -  T        m     �     �  �  �  O   H	  �  �	     y     �  (   �     �     �     �  ,        :  +   U     �     �     �  "   �     �     �        �   /  �    T   �  B   E     �     �   :menuselection:`Particle System --> Emission` A random variation of the lifetime of a given particle. The shortest possible lifetime is *Lifetime* × (1 - *Random*). Values above 1.0 are not allowed. For example with the default *Lifetime* value of 50 a *Random* setting of 0.5 will give you particles with a live span ranging from 50 frames to :math:`50 × (1.0 - 0.5) = 25` frames, and with a *Random* setting of 0.75 you will get particles with live spans ranging from 50 frames to :math:`50 × (1.0 - 0.75) = 12.5` frames. Emission End Even Distribution Faces Grid Hexagonal Invert Grid Jittered Jittering Amount Lifetime Number Panel Particles/Face Random Reference Resolution Take any :doc:`Modifiers </modeling/modifiers/introduction>` above the Particle Modifier in the :ref:`modifier stack <modifier-stack>` into account when emitting particles, else it uses the original mesh geometry. The *Emitter* system works just like its name says: it emits/produces particles for a certain amount of time. In such a system, particles are emitted from the selected object from the *Start* frame to the *End* frame and have a certain lifespan. These particles are rendered default as :ref:`Halos <particle-halo>`, but you may also render these kind of particles as objects (depending on the particle system's render settings, see :doc:`Visualization </physics/particles/emitter/render>`). The buttons in the *Emission* panel control the way particles are emitted over time: Use Modifier Stack Vertices Volume Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-08-08 18:21+0100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 :menuselection:`Hệ Thống Hạt (Particle System) --> Phát Xạ (Emission)` A random variation of the lifetime of a given particle. The shortest possible lifetime is *Lifetime* × (1 - *Random*). Values above 1.0 are not allowed. For example with the default *Lifetime* value of 50 a *Random* setting of 0.5 will give you particles with a live span ranging from 50 frames to :math:`50 × (1.0 - 0.5) = 25` frames, and with a *Random* setting of 0.75 you will get particles with live spans ranging from 50 frames to :math:`50 × (1.0 - 0.75) = 12.5` frames. Phát Xạ -- Emission Kết Thúc -- End Phân Phối Đều -- Even Distribution Bề Mặt -- Faces Đồ Thị -- Grid Lục Giác -- Hexagonal Đảo Nghịch Khung Lưới -- Invert Grid Biến Động -- Jittered Lượng Biến Động -- Jittering Amount Tuổi Thọ -- Lifetime Số -- Number Bảng -- Panel Hạt/Bề Mặt -- Particles/Face Ngẫu Nhiên -- Random Tham Chiếu -- Reference Độ Phân Giải -- Resolution Take any :doc:`Modifiers </modeling/modifiers/introduction>` above the Particle Modifier in the :ref:`modifier stack <modifier-stack>` into account when emitting particles, else it uses the original mesh geometry. The *Emitter* system works just like its name says: it emits/produces particles for a certain amount of time. In such a system, particles are emitted from the selected object from the *Start* frame to the *End* frame and have a certain lifespan. These particles are rendered default as :ref:`Halos <particle-halo>`, but you may also render these kind of particles as objects (depending on the particle system's render settings, see :doc:`Visualization </physics/particles/emitter/render>`). The buttons in the *Emission* panel control the way particles are emitted over time: Dùng Ngăn Xếp của Bộ Điều Chỉnh -- Use Modifier Stack Điểm Đỉnh -- Vertices Thể Tích -- Volume 