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
import com.htran.Comparators.MSGIDFlatTextComparator;
import com.htran.Comparators.MSGIDFlatTextPossibleComparator;
import java.awt.event.ActionEvent;
import java.util.Collections;

/**
 *
 * @author htran
 */
public class TransferTranslatedTextFromVIPOToManualDoc extends ProcessDocAction {
    Document last_doc = null;
    Document this_doc = null;
    
    @Override
    public void actionPerformed(ActionEvent e) {
        boolean is_changed = false;
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;

            Document vipo = doc_event.getFromDocument();
            Document manual = doc_event.getToDocument();
            Common.current_doc = manual;
            Common.doc_changed = false;
            this_doc = manual;

//            System.out.println("vipo: = " + vipo.getPath());
//            System.out.println("manual: = " + manual.getPath());
            vipo.sort(MSGIDFlatTextComparator.getInstance());
            int len = manual.size();
            for (int i = 0; i < len; i++) {
                boolean is_first_block = (i == 0);
                if (is_first_block) {
                    continue;
                }

                TextBlock manual_txt_block = manual.get(i);
                MSGIDFlatTextComparator comparator = MSGIDFlatTextComparator.getInstance();
                MSGIDFlatTextPossibleComparator possible_comparator = MSGIDFlatTextPossibleComparator.getInstance();

                int found_index = Collections.binarySearch(vipo, manual_txt_block, comparator);
                boolean is_found = (found_index >= 0);
                if (is_found) {
                    replaceMatches(vipo, manual_txt_block, found_index);
                } else {
                    found_index = Collections.binarySearch(vipo, manual_txt_block, possible_comparator);
                    is_found = (found_index >= 0);
                    if (is_found) {
                        TextBlock vipo_txt_block = vipo.get(found_index);

                        PossibleMatch possible = PossibleMatch.getInstance();
                        ProcessTextBlockEvent event = new ProcessTextBlockEvent(this, 0, null);
                        event.setFromBlock(vipo_txt_block);
                        event.setToBlock(manual_txt_block);
                        possible.actionPerformed(event);
                    }//end is_found for possible
                }//end if

            }//end for

            if (manual.isDirty()) {
                UpdateCommentBlockText upd_comment = UpdateCommentBlockText.getInstance();
                upd_comment.actionPerformed(e);

                UpdateRevisionTimeOnly upd_revision = UpdateRevisionTimeOnly.getInstance();
                upd_revision.actionPerformed(e);

                if (! Common.changed_list.contains(manual)){
                    System.out.println("Document changed: " + manual.getPath());
                    Common.changed_list.add(manual);
                }
            }//end if
            /*
            if (Common.doc_changed) {
                System.out.println(manual.toString());
            }//end if
            */
            Common.last_doc = Common.current_doc;
            Common.doc_path_printed = false;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine

    private void replaceMatches(Document vipo, TextBlock manual_txt_block, int found_index) {

        
        TextBlockComponent manual_msgstr = manual_txt_block.getMsgstr();
        String manual_msgstr_flat_text = manual_msgstr.getFlatText();
        
        TextBlock vipo_txt_block = vipo.get(found_index);
        TextBlockComponent vi_po_msgid = vipo_txt_block.getMsgid();
        TextBlockComponent vipo_msgstr = vipo_txt_block.getMsgstr();
        String vipo_msgstr_flat_text = vipo_msgstr.getFlatText();
        
        boolean has_been_translated = (manual_msgstr_flat_text.length() > 0);
        boolean has_been_translated_and_identical = (has_been_translated) && (manual_msgstr_flat_text.compareTo(vipo_msgstr_flat_text) == 0);
        boolean is_replace = (!has_been_translated) || (!has_been_translated_and_identical);
        if (is_replace) {

            String combined_msgid_and_msgstr = compbineMSGID_MSGSTR(vipo_txt_block);
            boolean is_ignore = (combined_msgid_and_msgstr == null) || (manual_msgstr_flat_text.compareTo(combined_msgid_and_msgstr) == 0);
            if (is_ignore) {
                return;
            }
            
            
            if (last_doc != this_doc){
                last_doc = this_doc;
                this_doc = manual_txt_block.getDocument();
                System.out.println("manual: = " + this_doc.getPath());
            }
            
            System.out.println("replacing: [" + manual_msgstr_flat_text + "] => " + combined_msgid_and_msgstr);
            manual_txt_block.getMsgstr().clear();
            manual_txt_block.getMsgstr().add(combined_msgid_and_msgstr);
            manual_txt_block.getDocument().setDirty(true);
        }//end if
    }//end routine

    private String compbineMSGID_MSGSTR(TextBlock blk) {
        TextBlockComponent blk_msgid = blk.getMsgid();
        TextBlockComponent blk_msgstr = blk.getMsgstr();
        String msgid = blk_msgid.getFlatText();
        String msgstr = blk_msgstr.getFlatText();

        boolean is_same = (msgid.compareToIgnoreCase(msgstr) == 0);
        if (is_same) {
            return null;
        }

        if (msgid.isEmpty()) {
            return msgstr;
        }

        if (msgstr.isEmpty()) {
            return msgid;
        }

        StringBuilder bld = new StringBuilder();
        bld.append(msgstr);
        bld.append(" -- ");
        bld.append(msgid);
        return bld.toString();

    }//end routine
}//end class
