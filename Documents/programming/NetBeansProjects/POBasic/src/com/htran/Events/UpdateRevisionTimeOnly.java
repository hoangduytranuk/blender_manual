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
public class UpdateRevisionTimeOnly extends ProcessDocAction {
    static UpdateRevisionTimeOnly instance = null;
    
    public static UpdateRevisionTimeOnly getInstance(){
        if (instance == null){
            instance = new UpdateRevisionTimeOnly();
        }
        return instance;
    }
    
    public UpdateRevisionTimeOnly(){}    
    
    String revision_date_time = "\"PO-Revision-Date: " + Common.timeNow + "\\n" + Common.QUOTE;

     //do replace of THIS if there are changes in the file
    String po_revision_date_stamped[][] = {{"PO-Revision-Date", revision_date_time}};
    
    @Override
    public void actionPerformed(ActionEvent e) {
        boolean has_changed, is_changed = false;
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;

            //Document vipo = doc_event.getFromDocument();
            Document manual = doc_event.getToDocument();
            //Common.LOGGER.info("FILE: " + manual.getPath() + "\n-------------------------");

            String content_string = manual.toString();

            int len = manual.size();
            TextBlock manual_txt_block = manual.get(0);
            has_changed = ReplaceComment(manual_txt_block);
            if (has_changed) {
                is_changed = true;
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end switch/case
    }//end routine

    private boolean ReplaceComment(TextBlock blk) {
        boolean is_changed, is_in_msgstr, is_in_comment, is_changed_comment, is_changed_msgstr;

        is_changed = is_in_msgstr = is_in_comment = is_changed_comment = is_changed_msgstr = false;

        TextBlock old = blk.clone();

        //String manual_txt_block_msgid = msgid.getFlatText();
        for (String elem[] : po_revision_date_stamped) {
            String pattern = elem[0];
            String repl = elem[1];
            String msgstr_str = blk.getMsgstr().getFlatText();

            is_in_msgstr = is_in_comment = is_changed_comment = is_changed_msgstr = false;

            is_in_comment = msgstr_str.contains(pattern);
            if (is_in_comment) {
                is_changed_comment = ReplaceCommentString(blk.getMsgstr(), pattern, repl);
                if (is_changed_comment)
                    is_changed = true;
            }//end if
        }//end for
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
                String old = new String(comp.get(i));
                comp.set(i, repl);
                is_changed = true;
                //Common.LOGGER.info("Revision TIME has CHANGED from:\n" + old + " to: " + repl);
            }//end if            
        }//end for 
        return is_changed;
    }//end routine    
}//end class
