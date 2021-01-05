/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import com.htran.CommonUtils.Common;
import com.htran.CommonUtils.Common.BlockType;
import com.htran.CommonUtils.DocumentBase;
import java.util.List;
import java.util.regex.Pattern;

/**
 *
 * @author htran
 */
public class TextBlock implements Cloneable, DocumentBase {

    private static int ERROR_LINE_NO = -1;
    private List<String> original_text_block = null;
    private int currentLine = ERROR_LINE_NO;
    private int documentCurrentLine = ERROR_LINE_NO;

    private TextBlockComponent comment = null;
    private TextBlockComponent msgctxt = null;
    private TextBlockComponent msgid = null;
    private TextBlockComponent msgstr = null;
    private TextBlockComponent current = null;
    private BlockType blkType = BlockType.UNDEFINED;

    private boolean flatText = false;
    private Document document = null;
    
    public TextBlock() {
    }//end routine

    public TextBlock(List<String> block, int documentCurrentLine) {
        this();
        this.original_text_block = block;
        currentLine = 0;
        this.documentCurrentLine = documentCurrentLine;
    }//end routine

    public TextBlock(TextBlock other) {
        this.original_text_block = other.original_text_block;
        this.documentCurrentLine = other.documentCurrentLine;
        currentLine = other.currentLine;
        try {
            if (other.comment != null) {
                this.comment = other.comment.clone();
            }
            if (other.msgctxt != null) {
                this.msgctxt = other.msgctxt.clone();
            }
            if (other.msgid != null) {
                this.msgid = other.msgid.clone();
            }
            if (other.msgstr != null) {
                this.msgstr = other.msgstr.clone();
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine

    public void parseBlock() {
        int block_line_start = -1;
        setCurrentLine(0);
        this.current = null;
        blkType = BlockType.UNDEFINED;
        for (String line : original_text_block) {

            boolean is_comment = Pattern.compile(Common.RE_COMMENT).matcher(line).matches();
            boolean is_comment_removal = Pattern.compile(Common.RE_COMMENT_REMOVAL).matcher(line).matches();
            boolean is_msgctxt = Pattern.compile(Common.RE_MSGCTXT).matcher(line).matches();
            boolean is_msgid = Pattern.compile(Common.RE_MSGID).matcher(line).matches();
            boolean is_msgstr = Pattern.compile(Common.RE_MSGSTR).matcher(line).matches();

            boolean is_remove_id = false;
            String ID = null;
            if (is_comment_removal) {
                blkType = BlockType.UNDEFINED;
                continue;
            }//end if
            if (is_comment) {
                ID = Common.COMMENT;
                blkType = BlockType.COMMENT;
            }//end if
            if (is_msgctxt) {
                ID = Common.MSGCTXT;
                blkType = BlockType.MSGCTXT;
                is_remove_id = true;
            }//end if
            if (is_msgid) {
                ID = Common.MSGID;
                blkType = BlockType.MSGID;
                is_remove_id = true;
            }//end if
            if (is_msgstr) {
                ID = Common.MSGSTR;
                blkType = BlockType.MSGSTR;
                is_remove_id = true;
            }//end if

            if (!is_comment_removal) {
                this.addStringToBlock(ID, line, currentLine + documentCurrentLine, is_remove_id);
                setCurrentLine(currentLine + 1);
            }//end if
        }
        //Common.LOGGER.log(Level.INFO, this.toString());
    }//end routine

    private TextBlockComponent addStringToBlock(String ID, String line, int start_line, boolean is_remove_id) {
        boolean is_comment, is_msgctxt, is_msgid, is_msgstr;
        if (ID != null) {
            switch (blkType) {
                case COMMENT:
                    if (this.comment == null) {
                        this.comment = new TextBlockComponent(this.document, this, blkType, ID, start_line);
                    }
                    current = this.comment;
                    break;
                case MSGCTXT:
                    if (this.msgctxt == null) {
                        this.msgctxt = new TextBlockComponent(this.document, this, blkType, ID, start_line);
                    }
                    current = this.msgctxt;
                    break;
                case MSGID:
                    if (this.msgid == null) {
                        this.msgid = new TextBlockComponent(this.document, this, blkType, ID, start_line);
                    }
                    current = this.msgid;
                    break;
                case MSGSTR:
                    if (this.msgstr == null) {
                        this.msgstr = new TextBlockComponent(this.document, this, blkType, ID, start_line);
                    }
                    current = this.msgstr;
                    break;
                default: //UNDEFINED
                    break;
            }//end switch
        }//end if

        if (is_remove_id) {
            line = Pattern.compile(ID).matcher(line).replaceAll(Common.EMPTYSTR);
            //Common.LOGGER.log(Level.INFO, "line before trim [" + line + "]");
            line = line.trim();
            //Common.LOGGER.log(Level.INFO, "line AFTER trim [" + line + "]");
        }//end if
        current.add(line);
        return current;
    }//end routine

    public void setFlatText() {
        if (this.comment != null) {
            this.comment.setFlatText();
        }
        if (this.msgctxt != null) {
            this.msgctxt.setFlatText();
        }
        if (this.msgid != null) {
            this.msgid.setFlatText();
        }
        if (this.msgstr != null) {
            this.msgstr.setFlatText();
        }
        setFlatText(true);
    }//end routine

    private String checkAndFixString(TextBlockComponent comp) {
        boolean valid = (comp != null && comp.size() != 0);
        if (!valid) {
            return null;
        }
        String line = comp.toString();
        boolean is_adding_new_line = (!line.endsWith(Common.NEW_LINE));
        if (is_adding_new_line) {
            line = line + Common.NEW_LINE;
        }
        return line;
    }

    @Override
    public String toString() {
        StringBuilder bld = new StringBuilder();
        String line = checkAndFixString(getComment());
        if (line != null) {
            bld.append(line);
        }
        line = checkAndFixString(getMsgctxt());
        if (line != null) {
            bld.append(line);
        }
        line = checkAndFixString(getMsgid());
        if (line != null) {
            bld.append(line);
        }
        line = checkAndFixString(getMsgstr());
        if (line != null) {
            bld.append(line);
        }
        bld.append(Common.NEW_LINE);
        return bld.toString();
    }//end routine

    @Override
    public TextBlock clone() {
        TextBlock new_instance = new TextBlock(this);
        return new_instance;
    }//end routine


    /**
     * @return the original_text_block
     */
    public List<String> getOriginal_text_block() {
        return original_text_block;
    }

    /**
     * @param original_text_block the original_text_block to set
     */
    public void setOriginal_text_block(List<String> original_text_block) {
        this.original_text_block = original_text_block;
    }

    /**
     * @return the currentLine
     */
    public int getCurrentLine() {
        return currentLine;
    }

    /**
     * @param currentLine the currentLine to set
     */
    public void setCurrentLine(int currentLine) {
        this.currentLine = currentLine;
    }

    /**
     * @return the documentCurrentLine
     */
    public int getDocumentCurrentLine() {
        return documentCurrentLine;
    }

    /**
     * @param documentCurrentLine the documentCurrentLine to set
     */
    public void setDocumentCurrentLine(int documentCurrentLine) {
        this.documentCurrentLine = documentCurrentLine;
    }

    /**
     * @return the comment
     */
    public TextBlockComponent getComment() {
        return comment;
    }

    /**
     * @param comment the comment to set
     */
    public void setComment(TextBlockComponent comment) {
        this.comment = comment;
    }

    /**
     * @return the msgctxt
     */
    public TextBlockComponent getMsgctxt() {
        return msgctxt;
    }

    /**
     * @param msgctxt the msgctxt to set
     */
    public void setMsgctxt(TextBlockComponent msgctxt) {
        this.msgctxt = msgctxt;
    }

    /**
     * @return the msgid
     */
    public TextBlockComponent getMsgid() {
        return msgid;
    }

    /**
     * @param msgid the msgid to set
     */
    public void setMsgid(TextBlockComponent msgid) {
        this.msgid = msgid;
    }

    /**
     * @return the msgstr
     */
    public TextBlockComponent getMsgstr() {
        return msgstr;
    }

    /**
     * @param msgstr the msgstr to set
     */
    public void setMsgstr(TextBlockComponent msgstr) {
        this.msgstr = msgstr;
    }

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

    @Override
    public Document getDocument() {
        return document;
    }

    @Override
    public void setDocument(Document doc) {
        this.document = doc;
    }

    @Override
    public TextBlock getTextBlock() {
        return this;
    }

    @Override
    public void setTextBlock(TextBlock txt_block) {
        
    }
}//end class
