#!/bin/bash
declare -a pattern_list=(
	LC_MESSAGES/editors/3dview/display/index.po
	LC_MESSAGES/modeling/meshes/editing/edge
	LC_MESSAGES/modeling/meshes/editing/face
	LC_MESSAGES/modeling/meshes/editing/mesh/knife_project.po
	LC_MESSAGES/modeling/meshes/editing/mesh/snap_symmetry.po
	LC_MESSAGES/modeling/meshes/editing/misc
	LC_MESSAGES/modeling/meshes/editing/vertex
	LC_MESSAGES/modeling/meshes/tools
	LC_MESSAGES/scene_layout/object/editing/apply.po
	LC_MESSAGES/scene_layout/object/editing/clear.po
	LC_MESSAGES/scene_layout/object/editing/convert.po
	LC_MESSAGES/scene_layout/object/editing/delete.po
	LC_MESSAGES/scene_layout/object/editing/duplicate.po
	LC_MESSAGES/scene_layout/object/editing/duplicate_linked.po
	LC_MESSAGES/scene_layout/object/editing/join.po
	LC_MESSAGES/scene_layout/object/editing/make_links.po
	LC_MESSAGES/scene_layout/object/editing/relations.po
	LC_MESSAGES/scene_layout/object/editing/show_hide.po
	LC_MESSAGES/scene_layout/object/editing/snap.po
	LC_MESSAGES/scene_layout/object/editing/transform/align_objects.po
	LC_MESSAGES/scene_layout/object/editing/transform/align_transform_orientation.po
	LC_MESSAGES/scene_layout/object/editing/transform/randomize.po
	LC_MESSAGES/scene_layout/object/properties/relations.po
)

cd $BLENDER_MAN_VI
for f in ${pattern_list[@]};
do
	echo "svn add $f";
	svn add $f;
done