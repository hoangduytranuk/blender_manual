/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.Common;
import base.Document;
import base.TextBlock;
import base.TextBlockComponent;
import java.awt.event.ActionEvent;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class UpdateCommentBlockText extends ProcessDocAction {
    static UpdateCommentBlockText instance = null;
    
    public static UpdateCommentBlockText getInstance(){
        if (instance == null){
            instance = new UpdateCommentBlockText();
        }
        return instance;
    }
    
    public UpdateCommentBlockText(){}    

    String revision_date_time = "\"PO-Revision-Date: " + Common.timeNow + "\\n" + Common.QUOTE;
    String[][] comment_group = {
        {"FIRST AUTHOR", "# Hoang Duy Tran <hoangduytran1960@gmail.com>"},
        {"Last-Translator", "\"Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>\\n\""},
        {"Language-Team", "\"Language-Team: London, UK <hoangduytran1960@googlemail.com>\\n\""},
        {"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE", revision_date_time}};

    String language_vi_insert = "\"Language: vi\\n\"";


    /*
    time_now  = ""
    date_to  = "PO-Revision-Date: " + time_now    
     */
    @Override
    public void actionPerformed(ActionEvent e) {
        boolean has_changed, is_changed = false;
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;

            //Document vipo = doc_event.getFromDocument();
            Document manual = doc_event.getToDocument();            

            String content_string = manual.toString();

            int len = manual.size();
            TextBlock manual_txt_block = manual.get(0);
            has_changed = ReplaceComment(manual_txt_block);
            if (has_changed) {
                is_changed = true;
            }
            
            /*
            boolean is_changed = false;
            for (String elem[] : msg_list) {
                String pattern = elem[0];
                String repl = elem[1];
                
                Pattern p = Pattern.compile(pattern);
                Matcher m = p.matcher(content_string);
                if (m.matches()){
                    content_string = m.replaceAll(repl);
                    is_changed = true;
                }//end if
            }//end for
            if (is_changed){
                Common.LOGGER.info("block replaced: " + content_string);
            }//end if
             */
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end switch/case
    }//end routine

    private boolean ReplaceComment(TextBlock blk) {
        boolean is_changed, is_in_msgstr, is_in_comment, is_changed_comment, is_changed_msgstr;

        is_changed = is_in_msgstr = is_in_comment = is_changed_comment = is_changed_msgstr = false;

        TextBlock old = blk.clone();

        //String manual_txt_block_msgid = msgid.getFlatText();
        for (String elem[] : comment_group) {
            String pattern = elem[0];
            String repl = elem[1];
            String comment_str = blk.getComment().getFlatText();
            String msgstr_str = blk.getMsgstr().getFlatText();

            is_in_msgstr = is_in_comment = is_changed_comment = is_changed_msgstr = false;

            is_in_comment = comment_str.contains(pattern);
            if (is_in_comment) {
                is_changed_comment = ReplaceCommentString(blk.getComment(), pattern, repl);
            }//end if
            is_in_msgstr = msgstr_str.contains(pattern);
            if (is_in_msgstr) {
                is_changed_msgstr = ReplaceCommentString(blk.getMsgstr(), pattern, repl);
            }//end if

            is_changed = (is_changed_comment || is_changed_msgstr);
        }//end for
        String language_team_string = this.comment_group[2][0];
        TextBlockComponent new_msgstr = InsertStringToList(blk.getMsgstr(), language_team_string, language_vi_insert, true);
        if (new_msgstr != null) {
            blk.setMsgstr(new_msgstr);
            is_changed = true;
        }//end if
        if (is_changed) {
            //Common.LOGGER.info("block BEFORE:\n" + old.toString());
            //Common.LOGGER.info("block replaced:\n" + blk.toString() + "\n========================================");
        }
        return is_changed;
    }//end routine

    private boolean ReplaceCommentString(TextBlockComponent comp, String pattern, String repl) {
        boolean is_changed = false;
        //Common.LOGGER.info("old: " + list.toString());
        int len = comp.size();
        for (int i = 0; i < len; i++) {
            String line = comp.get(i);
            boolean is_found = line.contains(pattern);

            //Common.LOGGER.info("pattern: " + pattern + " replace: " + repl);
            //Common.LOGGER.info("line: " + line);
            //Common.LOGGER.info("is_found: " + is_found);
            if (is_found) {
                comp.set(i, repl);
                is_changed = true;
            }//end if            
        }//end for 
        return is_changed;
    }//end routine

    private TextBlockComponent InsertStringToList(TextBlockComponent msgstr, String find_line, String insert_line, boolean is_after) {
        boolean is_changed = false;

        String list_content = msgstr.getFlatText();

        TextBlockComponent comp = new TextBlockComponent();
        String non_quoted_insert_line = comp.RemoveSurroundingQuote(insert_line);
        boolean has_insert_line = (list_content.contains(non_quoted_insert_line));
        if (has_insert_line) {
            //Common.LOGGER.info("DUPLICATE: " + insert_line);
            return null;
        }

        TextBlockComponent new_msgstr = msgstr.clone();
        new_msgstr.clear();

        //Common.LOGGER.info("old: " + msgstr.toString());
        int len = msgstr.size();
        for (int i = 0; i < len; i++) {
            String line = msgstr.get(i);
            boolean is_found = line.contains(find_line);

            //Common.LOGGER.info("pattern: " + pattern + " replace: " + repl);
            //Common.LOGGER.info("line: " + line);
            //Common.LOGGER.info("is_found: " + is_found);
            if (is_found) {
                if (is_after) {
                    new_msgstr.add(line);
                    new_msgstr.add(insert_line);
                } else {
                    new_msgstr.add(insert_line);
                    new_msgstr.add(line);
                }//end if
                is_changed = true;
            } else {
                new_msgstr.add(line);
            }//end if            
        }//end for 
        return new_msgstr;
    }//end routine

}//end class
