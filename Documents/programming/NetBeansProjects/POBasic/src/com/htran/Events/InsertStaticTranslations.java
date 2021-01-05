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
import java.util.Enumeration;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class InsertStaticTranslations extends ProcessDocAction {

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
            for (TextBlock manual_txt_block : manual) {
                has_changed = ReplaceBlockMSGSTR(manual_txt_block);
                if (has_changed) {
                    is_changed = true;
                }
            }//end for

            if (manual.getDocument().isDirty()) {
                UpdateCommentBlockText upd_comment = UpdateCommentBlockText.getInstance();
                upd_comment.actionPerformed(e);

                UpdateRevisionTimeOnly upd_revision = UpdateRevisionTimeOnly.getInstance();
                upd_revision.actionPerformed(e);
                
                if (! Common.changed_list.contains(manual)){
                    System.out.println("Document changed: " + manual.getPath());
                    Common.changed_list.add(manual);
                }
            }//end if
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end switch/case
    }//end routine

    private boolean ReplaceBlockMSGSTR(TextBlock blk) {
        boolean changed = false;
        Enumeration<String> dict_keys = null;

        TextBlock old = blk.clone();
        dict_keys = (Enumeration<String>) Common.dict.propertyNames();

        String flat_msgid = blk.getMsgid().getFlatText();
        String flat_msgstr = blk.getMsgstr().getFlatText();
        boolean is_found_en_text = Common.dict_map.containsKey(flat_msgid);
        boolean has_been_translated = !((flat_msgstr == null) || flat_msgstr.isEmpty());
        boolean is_replace = (is_found_en_text && !has_been_translated);
        if (is_replace) {
            String repl = Common.dict_map.get(flat_msgid);
            ReplaceBlockText(blk.getMsgid(), blk.getMsgstr(), flat_msgid, repl);
            changed = true;
        }else{
            boolean is_debug = (flat_msgid.contains("These settings are common"));
            if (is_debug){
                //Common.LOGGER.info("STOP HERE");
            }
        }//end if
        return changed;
    }//end routine

    private void ReplaceBlockText(TextBlockComponent msgid, TextBlockComponent msgstr, String pattern, String repl) {
        StringBuilder bld = new StringBuilder();
        boolean is_add_start_quote = !repl.startsWith(Common.QUOTE);
        if (is_add_start_quote) {
            bld.append(Common.QUOTE);
        }

        bld.append(repl);

        boolean is_add_end_quote = !repl.endsWith(Common.QUOTE);
        if (is_add_end_quote) {
            bld.append(Common.QUOTE);
        }
        repl = bld.toString();

        System.out.println("Replacing: [" + msgstr.getFlatText() + "]=>[" + repl + "]");
        msgstr.clear();
        msgstr.add(repl);
        msgid.getDocument().setDirty(true);
        
//            Common.LOGGER.info("REPLACED - msgid: " + msgid.toString());
//            Common.LOGGER.info("REPLACED - msgstr: " + msgstr.toString());
    }//end routine
}//end class
