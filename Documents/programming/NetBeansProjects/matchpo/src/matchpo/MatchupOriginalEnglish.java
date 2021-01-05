/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package matchpo;

import java.io.File;
import java.util.Formatter;
import java.util.List;

/**
 *
 * @author htran
 */
public class MatchupOriginalEnglish extends BaseClass{
    String input_en_new_path = null;
    String input_en_orig_path = null;

    private void comparingTwoList(List<Integer> en_new_list, List<String> input_en_new_list, List<Integer> en_orig_list, List<String> input_en_orig_list, int start_index){
        try{
            int input_size = input_en_new_list.size();
            boolean is_end = (start_index >= input_size);
            if (is_end){
                return;
            }//end if
            
            int change_count=0;
            int new_index, orig_index;
            new_index = orig_index = start_index;
            
            int new_count = en_new_list.size();
            int orig_count = en_orig_list.size();
            int loop_count = Math.max(new_count, orig_count);
            
            for(int count = start_index; count < loop_count; count++){
                boolean valid = (new_index < new_count) && (orig_index < orig_count);
                if (! valid) { break; }
                
                int new_line_index = en_new_list.get(new_index);
                int orig_line_index = en_orig_list.get(orig_index);
                
                String new_text_line = input_en_new_list.get(new_line_index);
                String orig_text_line = input_en_orig_list.get(orig_line_index);
                
                int old_line_no = orig_line_index + 1;
                int new_line_no = new_line_index + 1;
                
                boolean is_similar = (new_text_line.trim().toLowerCase().compareTo(orig_text_line.trim().toLowerCase()) == 0);
                boolean is_identical = (new_text_line.trim().compareTo(orig_text_line.trim()) == 0);
                
                if (is_similar && !is_identical){
                    this.reportBorth("is_similar and not is_identical", old_line_no, orig_text_line, new_line_no, new_text_line);
                    input_en_new_list.set(new_line_index,orig_text_line);
                }//end if
                
                boolean is_different = (!(is_similar || is_identical));
                if (is_different){
                    String msg_old = "Differences found: \noriginal:" + this.input_en_orig_path + "\n" + (old_line_no) + ":" + orig_text_line + "\n";
                    String msg_new = "new:" + this.input_en_new_path + "\n" + (new_line_no) + ":" + new_text_line;
                    
                    StringBuilder sbuf = new StringBuilder();
                    sbuf.append(msg_old).append(msg_new);
                    
                    Formatter fmt = new Formatter(sbuf);
                    fmt.format("\n\nHex Representation:\noriginal: [%s]\nnew: [%s]\n", toHex(orig_text_line), toHex(new_text_line));
                    
                    throw new RuntimeException(sbuf.toString());
                }//end if
                new_index += 1;
                orig_index += 1;                
            }//end for loop
            System.out.println("No differences were found!!!");
        }catch(Exception ex){
            ex.printStackTrace();
        }
    }//end routine
    
    public void run(){
        String sep_end_group = "*********************************";
        input_en_new_path = this.po_file_path;

        //input_en_new_path = this.my_home + "/blender-git/blender/release/datafiles/locale/po/vi.po";
        //input_en_orig_path = this.my_home + "/blender-svn/bf-translations/trunk/po/vi.po";
        //input_en_orig_path = this.my_home + "/blender-git/blender/release/datafiles/locale/po/vi.po";
        //input_en_orig_path = this.my_home+"/workspace/potran/src/test.po";
        //input_en_new_path = this.my_home + "/test_vi.po";
        input_en_orig_path = this.my_home + "/test_vi.po";
        
        //System.out.println(input_en_new_path);
        //File f = new File(input_en_new_path);
        //System.out.println("can read file? " + f.canRead());
        //System.exit(0);
        //input_en_orig_path = this.po_file_path;
        //input_en_orig_path = this.my_home + "/blender-svn/bf-translations/trunk/po/vi.po";
        
        List<String> input_en_new_list = this.readFile(input_en_new_path);
        List<String> input_en_orig_list = this.readFile(input_en_orig_path);
        
        String en_line_pattern = "^msgid.*$";  //tieng Anh
        //String en_line_pattern = "^msgstr.*$"; //tieng Viet\
        //String en_line_pattern = "^msgctxt.*$"; //context
        //String en_line_pattern = "^#[\\.\\,]*$"; //references
        List<Integer> en_new_list = findWord(en_line_pattern, input_en_new_list);
        List<Integer> en_orig_list = findWord(en_line_pattern, input_en_orig_list);
        
        List<String> orig_temp_list = getTextListFromIndex(en_orig_list, input_en_orig_list);
        List<String> new_temp_list =getTextListFromIndex(en_new_list, input_en_new_list);

        String orig_temp_path = this.my_home + "/orig_temp_vi.txt";
        String new_temp_path = this.my_home + "/new_temp_vi.txt";
        
        this.writeFileWithHeader(input_en_orig_path + "\n", orig_temp_path, orig_temp_list);
        this.writeFileWithHeader(input_en_new_path + "\n", new_temp_path, new_temp_list);
                
        comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list, 0);
        
    }//end routine
        
}//end class
