/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package translationpofiles.CommonUtils;

import java.util.List;
import java.util.Vector;

/**
 *
 * @author htran
 */
public class BlockList extends Vector {
    List<String> comment = null;
    List<String> msgid = null;
    List<String> msgstr = null;
    List<String> msgctxt = null;
    
    List<String> lines = null;
    int currentLine = -1;
    int totalLines = 0;
    boolean isEndOfFile = false;
    
    public BlockList(List<String> text_lines) {
        this.lines = text_lines;
        if (this.lines != null){
           this.currentLine = 0;
           this.totalLines = lines.size();
        }
    }
    
    /**
     * split list to blocks by empty
     */
    public void toBlocks(){
        List<String> block = new Vector<String>();
        boolean is_done = false;
        while (! is_done){
            is_done = (currentLine >= totalLines);
            if (is_done)
                break;
            
            String new_line = lines.get(currentLine).trim();
            boolean is_done_block = new_line.isEmpty();
            if (is_done_block){
                this.add(block);                
            }else{
                block.add(new_line);                
            }//end if                        
            currentLine += 1;
        }
    }//end block        
}//end class
