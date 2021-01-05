/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import java.util.ArrayList;
import java.util.regex.Pattern;


/**
 *
 * @author htran
 */
public class TextBlockComponent extends ArrayList<String> implements Cloneable, Comparable{    
    private String ID = null;
    private boolean is_flat = false;
    private ArrayList<String> text_list = new ArrayList<String>();
    private Document document = null;
    private TextBlock block = null;

    private String getTextListAsString(){
        StringBuilder sb = new StringBuilder();
        String system_sep = System.lineSeparator();
        for(String text_line : text_list){
            String trimmmed = text_line.trim();
            sb.append(trimmmed).append(system_sep);
        }//end for
        return sb.toString();
    }//end
    
    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
        String system_sep = System.lineSeparator();
        if (ID != null){
            sb.append(ID).append(" ");
        }//end if
        sb.append(getTextListAsString());
        return sb.toString();
    }//end 

    
    public String debugString(){
        StringBuilder sb = new StringBuilder();
        String system_sep = System.lineSeparator();
        if (ID != null){
            sb.append(ID).append(" ");
        }//end if

        sb.append("is_flat:").append(is_flat).append(system_sep);        
        sb.append("text_list:").append(getTextListAsString());
        sb.append("document:").append(document.path).append(system_sep);        
        return sb.toString();
    }//end 
    
    @Override
    public Object clone(){
        TextBlockComponent new_inst = new TextBlockComponent();
        new_inst.ID =  this.ID;
        new_inst.text_list = new ArrayList<String>(this.text_list);
        new_inst.document = this.document;
        new_inst.block = this.block;
        return new_inst;
    }//end
    
    public boolean isNone(){
        return this.text_list == null;
    }//end

    public boolean isEmpty(){
        return (! isNone()) && (this.text_list.size() == 0);
    }//end
    
    public boolean isConsideredEmpty(){
        return (isEmpty()) && (this.text_list.size() == 0);
    }//end
    
    
    /**
     * Extract all text lines and join them into one massive string, only
     * keeping a single pair of quotes ("") for beginning and ending
     *
     * @return null if there is no text, otherwise one long line of all text
     * joined. Useful for comparison for similarities.
     */
    public String getFlatText() {
        StringBuilder bld = new StringBuilder();
        for (String text_line : this) {
            String new_line = RemoveSurroundingQuote(text_line);
            bld.append(new_line);
        }//end for
        String return_string = bld.toString();
        this.setFlatText(true);
        return return_string;
    }//end routine
    
    /**
     * @return the flatText
     */
    public boolean isFlatText() {
        return flatText;
    }

    /**
     * @param flatText the flatText to set
     */
    public void setFlatText(boolean flatText) {
        this.flatText = flatText;
    }

    private int startLine = -1;
    private String ID = null;
    private boolean flatText = false;
    
    public TextBlockComponent() {
    }

    public TextBlockComponent(TextBlockComponent old) {
        this.startLine = old.startLine;
        this.ID = old.ID;
        for (String line : old) {
            this.add(new String(line));
        }//end for
    }//end routine

    public TextBlockComponent(String ID, String text_line) {
        this.ID = ID;
        this.add(text_line);
    }//end routine

    public TextBlockComponent(Document doc, TextBlock txt_block, BlockType blkType, String ID, int start_line) {
        this.ID = ID;
        this.startLine = start_line;
        this.blkType = blkType;
        this.document = doc;
        this.textBlock = txt_block;
    }//end routine

    public TextBlockComponent(String ID, String text_line, int start_line) {
        this.ID = ID;
        this.add(text_line);
        this.startLine = start_line;
    }//end routine

    public TextBlockComponent(String ID, ArrayList<String> text_list) {
        this.ID = ID;
        this.addAll(text_list);
    }//end routine        

    /**
     * @return the startLine
     */
    public int getStartLine() {
        return startLine;
    }//end routine

    /**
     * @param startLine the startLine to set
     */
    public void setStartLine(int startLine) {
        this.startLine = startLine;
    }//end routine

    /**
     * @return the ID
     */
    public String getID() {
        return ID;
    }

    /**
     * @param ID the ID to set
     */
    public void setID(String ID) {
        this.ID = ID;
    }

    public boolean isCommentBlock(){
        return (this.blkType == BlockType.COMMENT);
    }

    private String gatherTextLines(){        
        StringBuilder bld = new StringBuilder();        
        int len = this.size();
        for (int i = 0; i < len; i++) {
            String text_line = this.get(i);
            bld.append(text_line);
            boolean is_last_line = (i == len - 1);
            boolean is_insert_new_line = (!is_last_line);            
            if (is_insert_new_line) {
                bld.append(Common.NEW_LINE);
            }//end if
        }//end for
        return bld.toString();
    }//end routine
    
    @Override
    public String toString() {
        if (this.isEmpty()) {
            return "";
        }
        String text_lines = gatherTextLines();
        
        if (isCommentBlock()) {            
            return text_lines;
        }
        
        
        StringBuilder bld = new StringBuilder();
        bld.append(ID).append(Common.SPACE);

        boolean leading_with_quote = text_lines.startsWith(Common.QUOTE);        
        boolean ending_with_quote = text_lines.endsWith(Common.QUOTE);
        
        if (! leading_with_quote) {
                bld.append(Common.QUOTE);
        }//end if
        
        bld.append(text_lines);
        
        if (! ending_with_quote) {
            bld.append(Common.QUOTE);
        }//end if
        
        return bld.toString();
    }//end routine

    public String RemoveLeadingQuote(String line) {
        String new_line = Pattern.compile(Common.RE_LEADING_QUOTE).matcher(line).replaceAll(Common.EMPTYSTR);
        return new_line;
    }//end routine

    public String RemoveEndingQuote(String line) {
        String new_line = Pattern.compile(Common.RE_ENDING_QUOTE).matcher(line).replaceAll(Common.EMPTYSTR);
        return new_line;
    }//end routine

    public String RemoveSurroundingQuote(String line) {
        String new_line = this.RemoveLeadingQuote(line);
        new_line = this.RemoveEndingQuote(new_line);
        return new_line;
    }


    public void setFlatText() {
        String flat_text = this.getFlatText();
        this.clear();
        this.add(flat_text);
    }//end routine

    @Override
    public TextBlockComponent clone() {
        TextBlockComponent comp = new TextBlockComponent(this);
        return comp;
    }//end routine

    /**
     * @return the blkType
     */
    public BlockType getBlkType() {
        return blkType;
    }

    /**
     * @param blkType the blkType to set
     */
    public void setBlkType(BlockType blkType) {
        this.blkType = blkType;
    }

    @Override
    public Document getDocument() {
        return this.document;
    }

    @Override
    public void setDocument(Document doc) {
        this.document=doc;
    }

    @Override
    public TextBlock getTextBlock() {
        return this.textBlock;
    }

    @Override
    public void setTextBlock(TextBlock txt_block) {
        this.textBlock = txt_block;
    }

    @Override
    public int compareTo(Object o) {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
}//end class
