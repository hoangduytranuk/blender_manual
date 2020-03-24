/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author htran
 */
public class BlockList extends ArrayList {    
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
        List<String> block = new ArrayList<String>();
        boolean is_done = false;        
        for(String line : lines){
            boolean is_done_block = line.trim().isEmpty();
            if (is_done_block){
                if (! block.isEmpty()){
                    this.add(block);
                    block = new ArrayList<String>();
                }//end if
            }else{
                block.add(line);
            }//end if            
        }//end for
        if (! block.isEmpty()){
            this.add(block);
        }//end if
    }//end block
}//end class
