#!/bin/bash
IS_LOCAL_MODE=""
function downloadFile()
{
    link=$1
    if [ ! -z $IS_LOCAL_MODE ]; then
        return
    fi
    #wget -c https://builder.blender.org/download//blender-2.80-63ac7c799c8-linux-glibc224-x86_64.tar.bz2
    echo "wget -c $link"
    wget -c $link
}

function uncompressFile()
{
    filename=$1
    echo "tar -xvJf $filename"
    tar -xvJf $filename
}

function removeOldFiles()
{
    old_dir=$1
    echo "rm -fr $old_dir"
    rm -fr $old_dir
}

function relinkFiles()
{
    new_dir=$(find . -maxdepth 1 -type d -name "$prefix$version-*" -print)
    case "$version" in
        2.8*)
            soft_link_dir="blender_2_8_latest"
            ;;
        2.7*)
            soft_link_dir="blender_latest"
            ;;
        *) #default
            soft_link_dir = ""
            ;;
    esac
    if [ ! -z $soft_link_dir ]; then
        echo "ln -sfn $new_dir $soft_link_dir"
        ln -sfn $new_dir $soft_link_dir
    fi
}

function moveZipFileToDownloads()
{
    file_name=$1
    is_in_download=$(echo $file_name | grep "Downloads")
    if [ ! -z $IS_LOCAL_MODE ]; then
        return
    fi
    echo "mv $file_name ~/Downloads"
    mv $file_name ~/Downloads
}

cd $HOME/blender-stuff
link="$1"
if [[ -e $link ]]; then
    IS_LOCAL_MODE="True"
fi
prefix="blender-"
version_pattern="(\d+\.\d+)"
echo "filename: $link"
#version=str(found_list).strip(\"[]\"); print(version);
filename=$(python3 -c "import sys, os; link=\"$1\"; name_index=link.rfind(\"$prefix\"); filename=link[name_index:]; print(filename)")
dirname=
version=$(python3 -c "import re, sys, os; link=\"$1\"; found_list=re.findall(\"$version_pattern\", \"$filename\"); version=found_list[0]; print(version)")
old_dir=$(find . -maxdepth 1 -type d -name "$prefix$version-*" -print)
#echo "version=$version"
echo "filename: $filename, version: $version"
#exit
removeOldFiles $old_dir
downloadFile $link
uncompressFile $filename
relinkFiles $filename $version
moveZipFileToDownloads $filename
