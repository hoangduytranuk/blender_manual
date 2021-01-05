/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package translationpofiles.CommonUtils;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;
import java.util.Vector;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 *
 * @author htran
 */
public class FileIO {

    static String POT_EXT = ".pot";
    static String PO_EXT = ".po";

    static String PO_MSGID = "msgid";
    static String PO_MSGSTR = "msgstr";
    static String PO_MSGCTX = "msgctxt";
    
    public static List<String> readFile(Path path) {
        List<String> string_list = new Vector<String>();

        try (Stream<String> stream = Files.lines(path)) {
            string_list = stream.collect(Collectors.toList());            
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return string_list;
    }//end method

        
    public static List<Path> FileList(String root_path) {
        Path path = Paths.get(root_path);
        List<Path> files = new Vector<>();
        try {
            Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    boolean is_regular_file = (!attrs.isDirectory());

                    if (is_regular_file && isPOFile(file)) {
                        files.add(file);
                    }
                    return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        return files;
    }

    private static boolean isPOFile(Path file) {
        boolean is_right_file = false;
        try {
            //first check for filename's extension
            String filename_in_lowercase = file.getFileName().toString().toLowerCase();
            is_right_file = filename_in_lowercase.endsWith(POT_EXT) || filename_in_lowercase.endsWith(PO_EXT);
            if (!is_right_file) {
                return false;
            }

            //now check to content for any of the main keywords
            Stream<String> stream = Files.lines(file);
            is_right_file = (stream.filter(s -> s.contains(PO_MSGID)) != null)
                    || (stream.filter(s -> s.contains(PO_MSGSTR)) != null)
                    || (stream.filter(s -> s.contains(PO_MSGCTX)) != null);
            //System.out.println("The file: " + file.toString() + " [is_right_file: " + is_right_file + "]");

        } catch (Exception ex) {
            is_right_file = false;
            ex.printStackTrace();
        }
        return is_right_file;
    }
}//end class

