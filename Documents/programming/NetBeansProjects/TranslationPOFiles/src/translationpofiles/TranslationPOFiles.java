/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package translationpofiles;

import java.nio.file.Path;
import java.util.List;
import translationpofiles.CommonUtils.FileIO;

/**
 *
 * @author htran
 */
public class TranslationPOFiles {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {        
        String doc_dir="/home/htran/blender-trans-git/blender-internationalisation/blender_docs/locale/vi/LC_MESSAGES";
        FileIO io = new FileIO();
        List<Path> file_list = io.FileList(doc_dir);
        System.out.println("Number of files: " + file_list.size());
        
        Path p = file_list.get(0);        
        List<String> list = io.readFile(p);
        
        
        // TODO code application logic here
        System.out.println("File: " + p.toString() + " read number of lines: " + list.size());
    }
    
    
    
}
