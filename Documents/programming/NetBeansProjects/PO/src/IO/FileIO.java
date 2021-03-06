/*
 * Copyright (C) 2019 Hoang Duy Tran <hoangduytran1960@googlemail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package IO;

import document.Document;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 * 20-Feb-2019 18:33:13
 */
public class FileIO {

public static List<String> readFile(Path path) {
        List<String> string_list = new ArrayList<String>();

        try (Stream<String> stream = Files.lines(path)) {
            string_list = stream.collect(Collectors.toList());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return string_list;
    }//end method

    public static void writeFile(String filename, String content, boolean is_append) throws IOException {
        //overwrite existing, do not append
        FileWriter fileWriter = new FileWriter(filename, is_append);
        BufferedWriter writer = new BufferedWriter(fileWriter);
        writer.append(content);
        writer.close();
    }
    
    public static void writeFile(String filename, Document doc, boolean is_append) throws IOException {
        String content = doc.toString();
        FileIO.writeFile(filename, content, is_append);
    }//end method

    public static void writeFile(Document doc) throws IOException {
        String content = doc.toString();
        FileIO.writeFile(doc.getPath(), content, false);
    }//end method

    
    
    public static List<Path> FileList(String root_path, ListPathEvent event_handler) {
        Path path = Paths.get(root_path);
        List<Path> files = new ArrayList<>();
        try {
            Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
                    
                    if (file.startsWith("."))
                        return FileVisitResult.CONTINUE;
                   
                    boolean valid_handler = (event_handler != null) && (event_handler instanceof ListPathEvent );
                    if (! valid_handler)
                        throw new IOException("Invalid event handler for FileList");
                    
                    event_handler.setVars(root_path, file, attrs);
                    FileVisitResult result = event_handler.run();
                    return result;
                    //return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        return files;
    }

    /*
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
    }//end routine

    public void WriteProperties(String filename, Properties prop) {
        try {
            File f = new File(filename);
            OutputStream out = new FileOutputStream(f);
            prop.store(out, Common.dictionaryName + " : " + Common.timeNow);
            out.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine

    public void WritePropertiesAsXML(String filename, Properties prop) {
        try {
            File f = new File(filename);
            OutputStream out = new FileOutputStream(f);
            prop.storeToXML(out, Common.dictionaryName + " : " + Common.timeNow);
            out.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine
*/
    public Properties LoadProperties(String filename) {
        Properties prop = new Properties();
        InputStream is = null;

        try {
            File f = new File(filename);
            is = new FileInputStream(f);
        } catch (Exception ex) {
            ex.printStackTrace();
            is = null;
        }

        try {
            if (is == null) {
                is = this.getClass().getResourceAsStream(filename);
            }
            prop.load(is);
            is.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return prop;
    }//end routine

    public Properties LoadPropertiesFromXML(String filename) {
        Properties prop = new Properties();
        InputStream is = null;
        /*
        try {
            File f = new File(filename);
            is = new FileInputStream(f);
        } catch (Exception ex) {
            ex.printStackTrace();
            is = null;
        }
         */
        try {
            //if (is == null) {
            is  = this.getClass().getResourceAsStream("/" + filename);
            //is  = this.getClass().getClassLoader().getResourceAsStream(filename);
            //}//end if
            prop.loadFromXML(is);
//            Common.LOGGER.info("LOADED:\n" + prop.toString());
            //is.close();
        } catch (Exception ex) {
            ex.printStackTrace();
            //Common.LOGGER.info(ex.toString());
            if (is != null) {
                try {
                    is.close();
                } catch (Exception e) {
                }
            }//end if
            System.exit(0);
        }
        return prop;
    }//end routine

    /**
     * Exclude root_dir element, return ./../../filename
     *
     * @param p
     * @return
     */
    public static Path RelativePath(Path root_path, Path p) {
        Path subpath = null;
        int start_index = root_path.toString().length();
        String subpath_str = p.toString().substring(start_index);
        File f = new File(subpath_str);        
        subpath = f.toPath();
        //String str = subpath.toString();
        //System.out.println(str);
        return subpath;
    }//end RelativePath
    
}//end 
