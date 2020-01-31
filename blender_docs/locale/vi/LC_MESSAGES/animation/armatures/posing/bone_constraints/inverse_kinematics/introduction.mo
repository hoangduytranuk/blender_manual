��    4      �              \  !   ]  ,     F   �  B   �     6  	   =     G     W  	   i     s     �  c  �     �                    (  
   7  �   B  �   �     �	     �	  
   �	     �	     �	     �	     �	     �	     �	     �	     �	  	   �	  	   �	  	   
     
  
   
     "
     )
     2
  	   8
     B
  �   H
  �  ;  �   �  �   �  d  [     �  M   �       W  "  �  z  �  U  !     ,   /  �   \  �   �     z     �     �     �     �     �     �  c     .   d     �     �     �     �     �  �   �  �   �     V     o  $   �     �     �     �  %   �           %      9      S   "   c      �      �      �      �       �      !     #!     9!     S!  �   r!  �  e"  �   %  �   �%  d  �&     �(  M   )  )   S)  W  })  �  �*   :abbr:`DLS (Damped Least Square)` :abbr:`SDLS (Selective Damped Least Square)` :menuselection:`Properties editor --> Armature --> Inverse Kinematics` :menuselection:`Properties editor --> Bone --> Inverse Kinematics` Always Animation Arm Rig Example Armature IK Panel Auto Step Automatic IK Bone IK Panel Coefficient on end effector position error to set corrective joint velocity. The time constant of the error correction is the inverse of this value. However, this parameter has little effect on the dynamic of the armature since the algorithm evaluates the target velocity in any case. Setting this parameter to 0 means 'opening the loop': the solver tracks the velocity but not the position; the error will accumulate rapidly. Setting this value too high means an excessive amount of correction and risk of instability. The value should be in the range 20-100. Default value is 20, which means that tracking errors are corrected in a typical time of 100-200ms. The feedback coefficient is the reason why the armature continues to move slightly in Simulation mode even if the target has stopped moving: the residual error is progressively suppressed frame after frame. Control Rotation Damping Epsilon Damping Max Feedback IK Constraints IK Stretch IK is mostly done with bone constraints. They work by the same method but offer more choices and settings. Please refer to these pages for detail about the settings for the constraints: If the :ref:`iTaSC IK Solver <rigging-armatures_posing_bone-constraints_ik_model_itasc>` is used, the bone IK panel changes to add these additional parameters. Initial Introduction Iterations Limit Lock Max Max Velocity Min Mode Never Panel Pose Mode Precision Reference Reiteration Simulation Solver Standard Steps Stiffness TODO. The Simulation mode is the stateful mode of the solver: it estimates the target's velocity, operates in a 'true time' context, ignores rotation from keyframes (except via a joint rotation constraint) and builds up a state cache automatically. The length of the chain is increased (if there is a connected parent available to add to it) with :kbd:`Ctrl-PageUp` or :kbd:`Ctrl-WheelDown`, and decreased with :kbd:`Ctrl-PageDown` or :kbd:`Ctrl-WheelUp`. However, the initial chain length is 0, which effectively means follow the connections to parent bones as far as possible, with no length limit. So pressing :kbd:`Ctrl-PageUp` the first time sets the chain length to 1 (move only the selected bone), and pressing :kbd:`Ctrl-PageDown` at this point sets it back to 0 (unlimited) again. Thus, you have to press :kbd:`Ctrl-PageUp` *more than once* from the initial state to set a finite chain length greater than 1. This arm uses two bones to overcome the twist problem for the forearm. IK locking is used to stop the forearm from bending, but the forearm can still be twisted manually by pressing :kbd:`R Y Y` in *Pose Mode*, or by using other constraints. This panel is used to select the IK Solver type for the armature: *Standard* or *iTaSC*. Most the time people will use the *Standard* IK solver. Use this option if you want to let the solver set how many substeps should be executed for each frame. A substep is a subdivision on the time between two frames for which the solver evaluates the IK equation and updates the joint position. More substeps means more processing but better precision on tracking the targets. The auto step algorithm estimates the optimal number of steps to get the best trade-off between processing and precision. It works by estimation of the nonlinearity of the pose and by limiting the amplitude of joint variation during a substep. It can be configured with next two parameters: Weight `IK Arm Example <https://wiki.blender.org/wiki/File:IK_Arm_Example.blend>`__. iTaSC Solver iTaSC accepts a mix of constraints, and multiple constraints per bone: the solver computes the optimal pose according to the respective weights of each constraint. This is a major improvement from the current constraint system where constraints are solved one by one in order of definition so that conflicting constraints overwrite each other. iTaSC uses a different method to compute the Jacobian, which makes it able to handle other constraints than just end effectors position and orientation: iTaSC is a generic multi-constraint IK solver. However, this capability is not yet fully exploited in the current implementation, only two other types of constraints can be handled: Distance in the Cartesian space, and Joint Rotation in the joint space. The first one allows maintaining an end effector inside, at, or outside a sphere centered on a target position, the second one is the capability to control directly the rotation of a bone relative to its parent. Those interested in the mathematics can find a short description of the method used to build the Jacobian here. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-01-31 01:35+0000
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 :abbr:`DLS (Damped Least Square)` :abbr:`SDLS (Selective Damped Least Square)` :menuselection:`Trình Biên Soạn Tính Chất (Properties editor) --> Cốt (Armature) --> Động Học Ngược (IK) (Inverse Kinematics)` :menuselection:`Trình Biên Soạn Tính Chất (Properties editor) --> Xương (Bone) --> Động Học Ngược (IK) (Inverse Kinematics)` Luôn Luôn -- Always Hoạt Họa -- Animation -- Arm Rig Example -- Armature IK Panel -- Auto Step -- Automatic IK -- Bone IK Panel Coefficient on end effector position error to set corrective joint velocity. The time constant of the error correction is the inverse of this value. However, this parameter has little effect on the dynamic of the armature since the algorithm evaluates the target velocity in any case. Setting this parameter to 0 means 'opening the loop': the solver tracks the velocity but not the position; the error will accumulate rapidly. Setting this value too high means an excessive amount of correction and risk of instability. The value should be in the range 20-100. Default value is 20, which means that tracking errors are corrected in a typical time of 100-200ms. The feedback coefficient is the reason why the armature continues to move slightly in Simulation mode even if the target has stopped moving: the residual error is progressively suppressed frame after frame. Điều Khiển Độ Xoay -- Control Rotation -- Damping Epsilon -- Damping Max Phản Hồi -- Feedback -- IK Constraints Kéo Giãn IK -- IK Stretch IK is mostly done with bone constraints. They work by the same method but offer more choices and settings. Please refer to these pages for detail about the settings for the constraints: If the :ref:`iTaSC IK Solver <rigging-armatures_posing_bone-constraints_ik_model_itasc>` is used, the bone IK panel changes to add these additional parameters. Khởi Đầu -- Initial Giới Thiệu -- Introduction Số Lần Lặp Lại -- Iterations Giới Hạn -- Limit Khóa -- Lock Lớn Nhất -- Max Vận Tốc Tối Đa -- Max Velocity Nhỏ Nhất -- Min Chế Độ -- Mode Không Bao Giờ -- Never Bảng -- Panel Chế Độ Tư Thế -- Pose Mode Chuẩn Xác -- Precision Tham Chiếu -- Reference Tái Lặp -- Reiteration Mô Phỏng -- Simulation Trình Giải Nghiệm -- Solver Chuẩn -- Standard Số Bước -- Steps Độ Cứng -- Stiffness Nội dung cần viết thêm. The Simulation mode is the stateful mode of the solver: it estimates the target's velocity, operates in a 'true time' context, ignores rotation from keyframes (except via a joint rotation constraint) and builds up a state cache automatically. The length of the chain is increased (if there is a connected parent available to add to it) with :kbd:`Ctrl-PageUp` or :kbd:`Ctrl-WheelDown`, and decreased with :kbd:`Ctrl-PageDown` or :kbd:`Ctrl-WheelUp`. However, the initial chain length is 0, which effectively means follow the connections to parent bones as far as possible, with no length limit. So pressing :kbd:`Ctrl-PageUp` the first time sets the chain length to 1 (move only the selected bone), and pressing :kbd:`Ctrl-PageDown` at this point sets it back to 0 (unlimited) again. Thus, you have to press :kbd:`Ctrl-PageUp` *more than once* from the initial state to set a finite chain length greater than 1. This arm uses two bones to overcome the twist problem for the forearm. IK locking is used to stop the forearm from bending, but the forearm can still be twisted manually by pressing :kbd:`R Y Y` in *Pose Mode*, or by using other constraints. This panel is used to select the IK Solver type for the armature: *Standard* or *iTaSC*. Most the time people will use the *Standard* IK solver. Use this option if you want to let the solver set how many substeps should be executed for each frame. A substep is a subdivision on the time between two frames for which the solver evaluates the IK equation and updates the joint position. More substeps means more processing but better precision on tracking the targets. The auto step algorithm estimates the optimal number of steps to get the best trade-off between processing and precision. It works by estimation of the nonlinearity of the pose and by limiting the amplitude of joint variation during a substep. It can be configured with next two parameters: Trọng Lượng -- Weight `IK Arm Example <https://wiki.blender.org/wiki/File:IK_Arm_Example.blend>`__. Bộ Giải Nhiệm iTaSC -- iTaSC Solver iTaSC accepts a mix of constraints, and multiple constraints per bone: the solver computes the optimal pose according to the respective weights of each constraint. This is a major improvement from the current constraint system where constraints are solved one by one in order of definition so that conflicting constraints overwrite each other. iTaSC uses a different method to compute the Jacobian, which makes it able to handle other constraints than just end effectors position and orientation: iTaSC is a generic multi-constraint IK solver. However, this capability is not yet fully exploited in the current implementation, only two other types of constraints can be handled: Distance in the Cartesian space, and Joint Rotation in the joint space. The first one allows maintaining an end effector inside, at, or outside a sphere centered on a target position, the second one is the capability to control directly the rotation of a bone relative to its parent. Those interested in the mathematics can find a short description of the method used to build the Jacobian here. 