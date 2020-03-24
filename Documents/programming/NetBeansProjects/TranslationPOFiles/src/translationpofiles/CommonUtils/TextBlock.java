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
public class TextBlock {

    private static int ERROR_LINE_NO = -1;
    public enum BlockType {BLOCK_UNDEFINED, BLOCK_COMMENT, BLOCK_MSGID, BLOCK_MSGSTR, BLOCK_MSGCTXT};        
    
    List<String> block = null;
    List<String> text = null;
    
    String COMMENT = "#";
    String MSGID = "msgid";
    String MSGSTR = "msgstr";
    String MSGCTXT = "msgctxt";
    
    TextBlock comment;
    TextBlock msgid;
    TextBlock msgstr;
    TextBlock msgctxt;
    
    BlockType type = BlockType.BLOCK_UNDEFINED;

    int currentLine = ERROR_LINE_NO;
    int totalLine = 0;

    public TextBlock(BlockType type) {
        this.type = type;
    }
    
    public TextBlock(List<String> block) {
        this.block = block;
        currentLine = 0;
        totalLine = block.size();
    }

    public void parseBlock(){
        addComment();
        addMsgCtxt();
        addMsgID();
        addMsgStr();
    }//end block
    
    private void addComment() {
        boolean start_collecting = false;
        boolean end_collecting = true;
        int local_current_line = currentLine;

        while (local_current_line < totalLine) {
            String line = block.get(currentLine);
            if (line.startsWith(COMMENT)) {
                start_collecting = true;
                end_collecting = false;
            }//end if

            if (line.startsWith(MSGID)
                    || line.startsWith(MSGSTR)
                    || line.startsWith(MSGCTXT)) {
                start_collecting = false;
                end_collecting = true;
            }//end if

            if (start_collecting) {
                AddStringToBlock(comment, BlockType.BLOCK_COMMENT, line);
                currentLine += 1;
            }
            
            if (end_collecting) {
                break;
            }
            local_current_line += 1;
        }//end while      
    }//end routine

    

    private void addMsgID() {
        boolean start_collecting = false;
        boolean end_collecting = true;
        int local_current_line = currentLine;

        while (local_current_line < totalLine) {
            String line = block.get(currentLine);
            if (line.startsWith(MSGID)) {
                start_collecting = true;
                end_collecting = false;
            }//end if

            if (line.startsWith(COMMENT)
                    || line.startsWith(MSGSTR)
                    || line.startsWith(MSGCTXT)) {
                start_collecting = false;
                end_collecting = true;
            }//end if

            if (start_collecting) {
                AddStringToBlock(comment, BlockType.BLOCK_MSGID, line);
                currentLine += 1;
            }
            
            if (end_collecting) {
                break;
            }
            
            local_current_line += 1;
        }//end while                
    }//end routine

    private void addMsgStr() {
        boolean start_collecting = false;
        boolean end_collecting = true;
        int local_current_line = currentLine;

        while (local_current_line < totalLine) {
            String line = block.get(currentLine);
            if (line.startsWith(MSGSTR)) {
                start_collecting = true;
                end_collecting = false;
            }//end if

            if (line.startsWith(COMMENT)
                    || line.startsWith(MSGID)
                    || line.startsWith(MSGCTXT)) {
                start_collecting = false;
                end_collecting = true;
            }//end if

            if (start_collecting) {
                AddStringToBlock(comment, BlockType.BLOCK_MSGSTR, line);
                currentLine += 1;
            }
            
            if (end_collecting) {
                break;
            }
            
            local_current_line += 1;
        }//end while                
    }//end routine    

    private void addMsgCtxt() {
        boolean start_collecting = false;
        boolean end_collecting = true;
        int local_current_line = currentLine;

        while (local_current_line < totalLine) {
            String line = block.get(currentLine);
            if (line.startsWith(MSGCTXT)) {
                start_collecting = true;
                end_collecting = false;
            }//end if

            if (line.startsWith(COMMENT)
                    || line.startsWith(MSGID)
                    || line.startsWith(MSGSTR)) {
                start_collecting = false;
                end_collecting = true;
            }//end if

            if (start_collecting) {
                AddStringToBlock(comment, BlockType.BLOCK_MSGCTXT, line);
                currentLine += 1;
            }
            
            if (end_collecting) {
                break;
            }

            local_current_line += 1;            
        }//end while                
    }//end routine

    public void AddStringToBlock(TextBlock block, BlockType type, String line) {
        if (block == null) {
            block = new TextBlock(type);
        }
        block.text.add(line);
    }
}
