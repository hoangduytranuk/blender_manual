/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package matchpo;

import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.xml.bind.DatatypeConverter;

/**
 *
 * @author htran
 */
public class BaseClass {
    public String sep_line = "---------------------------";
    public String my_home = System.getenv("HOME");
    public String __po_file = "vi.po";
    public String __po_path = "/home/htran/blender-trans-git/blender-internationalisation/trunk/po/";
    //String __po_file = "test.po";
    //String __po_path = "/home/htran/";
    public String po_file_path = __po_path + __po_file;
    
    
    public List<String> readFile(String path){
        List<String> list = new ArrayList<>();
        try (Stream<String> stream = Files.lines(Paths.get(path))) {
            //1. filter line 3
            //2. convert all content to upper case
            //3. convert it into a List
            list = stream.collect(Collectors.toList());
            stream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //debuging line
        //list.forEach(System.out::println);
        return list;
    }//end routine
    
    public void writeFileWithHeader(String header, String fullPath, List<String> content){
        Path path = Paths.get(fullPath);
        try (BufferedWriter writer = Files.newBufferedWriter(path)) {
            if (! header.isEmpty()){
                writer.write(header);
            }
            
            content.forEach(line -> {
                try {
                    writer.write(line);
                    writer.write(System.lineSeparator());
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            });
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }        
    }//end routine
    
    public void writeFile(String fullPath, List<String> content) {
        Path path = Paths.get(fullPath);
        try (BufferedWriter writer = Files.newBufferedWriter(path)) {
            content.forEach(line -> {
                try {
                    writer.write(line);
                    writer.write(System.lineSeparator());
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            });
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }//end routine

    public void clearFileContent(String fullPath) {
        PrintWriter writer = null;
        File path = new File(fullPath);
        try {
            writer = new PrintWriter(path);
            writer.print("");
            writer.close();
        } catch (Exception ex) {
            ex.printStackTrace();
            if (writer != null){
                writer.close();
                writer = null;
            }//end if
        }
    }//end routine    
    
    public List<Integer> findWord(String find_word, List<String> orig_list){
        List<Integer> find_list = new ArrayList<>();
        
        Pattern p = Pattern.compile(find_word, Pattern.CASE_INSENSITIVE);        
        int list_len = orig_list.size();
        for(int line_count = 0; line_count < list_len; line_count++){
            String text_line = orig_list.get(line_count);
            Matcher m = p.matcher(text_line);
            boolean is_found = m.find();
            if (is_found){
                find_list.add(line_count);
            }//end if
        }//end for loop
        return find_list;
    }//end routine
    
    public void reportBorth(String msg, int orig_line_index, String orig_text_line, int new_line_index, String new_text_line){
        try{
            if (! msg.isEmpty())
                System.out.println(msg);
            System.out.println("Original: " + orig_line_index + orig_text_line.trim());
            System.out.println("New: " + new_line_index + new_text_line.trim());
        }catch(Exception ex){
            ex.printStackTrace();
        }
    }//end routine
    
    public String toHex(String text) throws UnsupportedEncodingException{
        byte[] myBytes = text.getBytes("UTF-8");
        return DatatypeConverter.printHexBinary(myBytes);
    }//end routine

    public List<String> getTextListFromIndex(List<Integer> index_list, List<String> source_list)
    {
        List<String> new_list = new ArrayList<>();        
        try{
            for(int line_index : index_list ){
                String text_line = source_list.get(line_index);
                new_list.add(line_index + ":" + text_line);
            }//end for
        }catch(Exception ex){
            ex.printStackTrace();
        }finally{
            return new_list;
        }        
    }//end routine
}//end class
