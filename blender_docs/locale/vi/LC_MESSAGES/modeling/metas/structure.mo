��    "      ,              <  W  =  �   �  	    (      \   I  :   �  	   �  9   �  R  %     x  ,   }  +   �  a   �     8  3   >  	   r  	   |     �  `  �  0   �	  #   *
  A   N
  F   �
  �   �
  �   �  �   �  �   C  �   �  /   �     �     �     �  
      �    W  �  �     	  �  ,   �  \   �  >   0  %   o  =   �  R  �     &  ,   :  +   g  a   �     �  7        =     W  ,   p  `  �  0   �  #   /  A   S  F   �  �   �  �   �  �   �  �   H  �   �  3   �     �            
      *Meta* objects are nothing more than mathematical formula that perform logical operations on one another (AND, OR), and that can be added and subtracted from each other. This method is also called *Constructive Solid Geometry* (CSG). Because of its mathematical nature, CSG uses little memory, but requires lots of processing power to compute. :menuselection:`Properties region --> Transform panel --> Type`, :menuselection:`Metaball tab --> Active Element panel --> Type` A more formal definition of a meta object can be given as a *directing structure* which can be seen as the source of a static field. The field can be either positive or negative and hence the field generated by neighboring directing structures can attract or repel. Ball (point, zero-dimensional structure) Blender has five types of metas, each determined by its underlying (or directing) structure. Cube (parallel-epipedal volume, tri-dimensional structure) Edit Mode Ellipsoid (ellipsoidal volume, tri-dimensional structure) In *Edit Mode*, you can change this structure, either using the relevant buttons in the :menuselection:`Metaball tab --> Active Element panel`, or the selector in the *Transform* panel in the Properties region. Depending on the structure, you might have additional parameters, located in both *Transform* panel and *Active Element* panel. Mode Note that by default, the plane is a square. Note that by default, the volume is a cube. Note that by default, the volume is a sphere, producing a spherical meta, as the *Ball* option... Panel Plane (rectangular plane, bi-dimensional structure) Reference Structure Technical Details The implicit surface is defined as the surface where the 3D field generated by all the directing structures assume a given value. For example a meta ball, whose directing structure is a point, generates an isotropic (i.e. identical in all directions) field around it and the surfaces at constant field value are spheres centered at the directing point. The length of the line (and hence, of the tube). The length, width of the rectangle. The length, width, height of the ellipsoid (defaults set to 1.0). The length, width, height of the parallelepiped (defaults set to 1.0). This is a meta which surface is generated by the field produced by a parallel-epipedal volume. This gives a parallel-epipedal surface, with rounded edges. As you might have guessed, it has three additional parameters: This is a meta which surface is generated by the field produced by a rectangular plane. This gives a parallel-epipedal surface, with a fixed thickness, and rounded borders. It has two additional parameters: This is a meta which surface is generated by the field produced by a straight line of a given length. This gives a cylindrical surface, with rounded closed ends. It has one additional parameter: This is a meta which surface is generated by the field produced by an ellipsoidal volume. This gives an ellipsoidal surface. It has three additional parameters: This is the simplest meta, without any additional setting. As it is just a point, it generates an isotropic field, yielding a spherical surface (this is why it is called *Meta Ball* or *Ball* in Blender). Tube (straight line, uni-dimensional structure) Underlying Structure dx dx, dy dx, dy, dz Project-Id-Version: Blender 2.79 Manual 2.79
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
 *Meta* objects are nothing more than mathematical formula that perform logical operations on one another (AND, OR), and that can be added and subtracted from each other. This method is also called *Constructive Solid Geometry* (CSG). Because of its mathematical nature, CSG uses little memory, but requires lots of processing power to compute. :menuselection:`Properties region --> Transform panel --> Type`, :menuselection:`Metaball tab --> Active Element panel --> Type` A more formal definition of a meta object can be given as a *directing structure* which can be seen as the source of a static field. The field can be either positive or negative and hence the field generated by neighboring directing structures can attract or repel.  -- Ball (point, zero-dimensional structure) Blender has five types of metas, each determined by its underlying (or directing) structure.  -- Cube (parallel-epipedal volume, tri-dimensional structure) Chế Độ Biên Soạn -- Edit Mode  -- Ellipsoid (ellipsoidal volume, tri-dimensional structure) In *Edit Mode*, you can change this structure, either using the relevant buttons in the :menuselection:`Metaball tab --> Active Element panel`, or the selector in the *Transform* panel in the Properties region. Depending on the structure, you might have additional parameters, located in both *Transform* panel and *Active Element* panel. Chế Độ -- Mode Note that by default, the plane is a square. Note that by default, the volume is a cube. Note that by default, the volume is a sphere, producing a spherical meta, as the *Ball* option... Bảng -- Panel  -- Plane (rectangular plane, bi-dimensional structure) Tham Chiếu -- Reference Cấu Trúc -- Structure Chi Tiết Kỹ Thuật -- Technical Details The implicit surface is defined as the surface where the 3D field generated by all the directing structures assume a given value. For example a meta ball, whose directing structure is a point, generates an isotropic (i.e. identical in all directions) field around it and the surfaces at constant field value are spheres centered at the directing point. The length of the line (and hence, of the tube). The length, width of the rectangle. The length, width, height of the ellipsoid (defaults set to 1.0). The length, width, height of the parallelepiped (defaults set to 1.0). This is a meta which surface is generated by the field produced by a parallel-epipedal volume. This gives a parallel-epipedal surface, with rounded edges. As you might have guessed, it has three additional parameters: This is a meta which surface is generated by the field produced by a rectangular plane. This gives a parallel-epipedal surface, with a fixed thickness, and rounded borders. It has two additional parameters: This is a meta which surface is generated by the field produced by a straight line of a given length. This gives a cylindrical surface, with rounded closed ends. It has one additional parameter: This is a meta which surface is generated by the field produced by an ellipsoidal volume. This gives an ellipsoidal surface. It has three additional parameters: This is the simplest meta, without any additional setting. As it is just a point, it generates an isotropic field, yielding a spherical surface (this is why it is called *Meta Ball* or *Ball* in Blender).  -- Tube (straight line, uni-dimensional structure) -- Underlying Structure dx dx, dy dx, dy, dz 