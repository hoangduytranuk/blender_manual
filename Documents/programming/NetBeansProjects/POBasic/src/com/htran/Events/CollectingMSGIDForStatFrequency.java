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
import com.htran.Comparators.BasicTextCaseComparator;
import java.awt.event.ActionEvent;
import java.util.TreeMap;

/**
 *
 * @author htran
 */
public class CollectingMSGIDForStatFrequency extends ProcessDocAction {

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;

            Document manual = doc_event.getToDocument();
            String flat_msgid, flat_msgstr;
            boolean is_a_repeat, has_msgid, has_msgstr;
            int old_count, new_count;

            if (Common.word_stat == null) {
                Common.word_stat = new TreeMap<>(BasicTextCaseComparator.getInstance());
            }//end if
            int count = 0;
            for (TextBlock blk : manual) {
                count++;
                
                boolean is_first_block = (count == 1);
                if (is_first_block) continue;
                
                TextBlockComponent msgid = blk.getMsgid();
                TextBlockComponent msgstr = blk.getMsgstr();

                flat_msgid = (msgid != null) ? msgid.getFlatText() : null;
                flat_msgstr = (msgstr != null) ? msgstr.getFlatText() : null;

                has_msgid = (!(flat_msgid == null || flat_msgid.isEmpty()));
                has_msgstr = (!(flat_msgstr == null || flat_msgstr.isEmpty()));

                is_a_repeat = (has_msgid && Common.word_stat.containsKey(flat_msgid));
                if (is_a_repeat) {
                    old_count = Common.word_stat.get(flat_msgid);
                    new_count = (has_msgstr ? old_count : old_count + 1);
                    Common.word_stat.replace(flat_msgid, new_count);
                } else {
                    if (! has_msgstr){
                        Common.word_stat.put(flat_msgid, 1);
                    }//end if
                }//end if                
            }//end for
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end switch/case        
    }//end routine
}//end class
