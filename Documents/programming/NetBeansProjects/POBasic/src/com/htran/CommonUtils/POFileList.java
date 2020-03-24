/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import java.io.File;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;

/**
 *
 * @author htran
 */
public class POFileList extends ArrayList<Path> {

    String root_dir = null;
    Path root_path = null;
    int number_of_files = 0;

    public POFileList(String root_dir) {
        this.root_dir = root_dir;
        File f = new File(root_dir);
        root_path = f.toPath();
    }

    public void GetFileList() {
        List<Path> file_list = FileIO.getInstance().FileList(root_dir);
        this.addAll(file_list);
        this.sort(new Comparator() {
            @Override
            public int compare(Object o1, Object o2) {
                int compare_value = -1;
                try {
                    Path p1 = (Path) o1;
                    Path p2 = (Path) o2;
                    compare_value = p1.compareTo(p2);
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
                return compare_value;
            }
        });
    }

    /**
     * Exclude root_dir element, return ./../../filename
     *
     * @param p
     * @return
     */
    public Path RelativePath(Path p) {
        Path subpath = null;
        int start_index = root_path.toString().length();
        int end_index = p.toString().length();
        String subpath_str = p.toString().substring(start_index);
        File f = new File(subpath_str);        
        subpath = f.toPath();
        //String str = subpath.toString();
        //System.out.println(str);
        return subpath;
    }//end RelativePath

    public String extractExtension(Path p) throws Exception {
        String p_copy_unchanged = p.toString();
        int p_copy_unchanged_len = p_copy_unchanged.length();
        int index_of_dot = p_copy_unchanged.indexOf(".");

        String extension = p_copy_unchanged.substring(index_of_dot, p_copy_unchanged_len);
        return extension;
    }

    public Path changeExtension(Path p, String from, String to) throws Exception {
        Path return_path = p;
        try {
            String p_copy_lower = p.toString().toLowerCase();
            String from_lower = from.toLowerCase();
            boolean is_matching_extension = p_copy_lower.endsWith(from_lower);

            if (is_matching_extension) {
                String p_copy_unchanged = p.toString();
                int p_copy_unchanged_len = p_copy_unchanged.length();
                int extension_to_len = to.length();
                int end_index = (p_copy_unchanged_len - extension_to_len) - 1;
                String p_copy_unchanged_without_extension = p_copy_unchanged.substring(0, end_index);
                String p_copy_with_new_extension = p_copy_unchanged_without_extension + to;

                File f = new File(p_copy_with_new_extension);
                return_path = f.toPath();
            } else {
                throw new RuntimeException("Unable to change extension for path: " + p + " from:" + from + "; to:" + to);
            }//end if
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return return_path;
    }//end routine

    /**
     * Get an entry from a subpath by resolving subpath against root_path
     *
     * @param subpath
     * @return
     */
    public Path FindSubPath(Path subpath) throws Exception {
        Path entry = null;
        Path full_path = root_path.resolve(subpath);
//        String full_path_str = full_path.toAbsolutePath().toString();
//        System.out.println(full_path_str);
//            int index = this.indexOf(full_path);

        Path[] this_array = new Path[this.size()];
        Arrays.asList(this.toArray(this_array));
        int entry_index = Arrays.binarySearch(this_array, full_path);

//            System.out.println(entry_index);
        boolean is_found = (entry_index >= 0);
        if (!is_found) {
            throw new RuntimeException("Unable to find sub-path for: " + subpath);
        } else {
            entry = this.get(entry_index);
        }
        return entry;
    }//end FindSubPath
}
