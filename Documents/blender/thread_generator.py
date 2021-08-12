import bpy
from math import *

def createMeshFromData(name, origin, verts, edges, faces):
	# Create mesh and object
	me = bpy.data.meshes.new(name+'Mesh')
	ob = bpy.data.objects.new(name, me)
	ob.location = origin
	ob.show_name = False
	# Link object to scene and make active
	scn = bpy.context.scene
	scn.objects.link(ob)
	scn.objects.active = ob
	ob.select = True
	# Create mesh from given verts, faces.
	me.from_pydata(verts, edges, faces)
	# Update mesh with new data
	me.update()

# Parameters
VerticesPerLoop = 256
Loops = 2
R = 32.5 # Outer radius
r = 30 # Inner radius
# thread profile (h1, h2, h3, h4 of the 4 points defining the profile)
h1 = 2
h2 = 0.5
h3 = 2
h4 = 0.5
falloffRate = 5

# Code
H = h1 + h2 + h3 + h4

#build array of profile points
ProfilePoints = []
ProfilePoints.append( [r, 0, 0] )
ProfilePoints.append( [R, 0, h1] )
if h2 > 0:
	ProfilePoints.append( [R, 0, h1 + h2] )
ProfilePoints.append( [r, 0, h1 + h2 + h3] )
if h4 > 0:
	ProfilePoints.append( [r, 0, h1 + h2 + h3 + h4] )

N = len(ProfilePoints)
verts = [[0, 0, 0] for _ in range(N * (VerticesPerLoop + 1)  * Loops)]
faces = [[0, 0, 0, 0] for _ in range(( N - 1) * VerticesPerLoop * Loops) ]

# go around a cirle. for each point in ProfilePoints array, create a vertex
angle = 0
for i in range(VerticesPerLoop * Loops + 1):
	for j in range(N):
		angle = i * 2 * pi / VerticesPerLoop
		# falloff applies to outer rings only
		u = i / (VerticesPerLoop * Loops)
		radius = r + (R - r) * (1 - 6*(pow(2 * u - 1, falloffRate * 4)/2 - pow(2 * u - 1, falloffRate * 6)/3)) if ProfilePoints[j][0] == R else r

		x = radius * cos(angle)
		y = radius * sin(angle)
		z = ProfilePoints[j][2] + i / VerticesPerLoop * H

		verts[N*i + j][0] = x
		verts[N*i + j][1] = y
		verts[N*i + j][2] = z
# now build face array
for i in range(VerticesPerLoop * Loops):
	for j in range(N - 1):
		faces[(N - 1) * i + j][0] = N * i + j
		faces[(N - 1) * i + j][1] = N * i + 1 + j
		faces[(N - 1) * i + j][2] = N * (i + 1) + 1 + j
		faces[(N - 1) * i + j][3] =  N * (i + 1) + j

createMeshFromData( 'Thread', [0, 0, 0], verts, [], faces )
