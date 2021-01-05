/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.Document;
import base.TextBlock;
import base.TextBlockComponent;
import java.awt.event.ActionEvent;

/**
 *
 * @author htran
 */
public class TranslateOriginalMSGIDToVietnamese extends ProcessDocAction {

    @Override
    public void actionPerformed(ActionEvent e) {
        boolean block_exists = false;
        boolean is_translate = false;
        try {
/*            
            ProcessDocEvent doc_event = (ProcessDocEvent) e;
            Document from_doc = doc_event.getFromDocument();
            Document to_doc = doc_event.getToDocument();
            Translator translator = Translator.getInstance();

            int nblocks = from_doc.size();
            for (int block_index = 0; block_index < nblocks; block_index++) {
                boolean is_first_block = (block_index == 0);
                if (is_first_block) {
                    continue;
                }//end if

                try {
                    TextBlock from_blk = from_doc.get(block_index);
                    TextBlock to_blk = from_doc.get(block_index);
                    String to_msgstr_string = to_blk.getMsgstr().FlatText();
                    String from_msgid_string = from_blk.getMsgid().FlatText();
                    is_translate = (!from_msgid_string.isEmpty()) && to_msgstr_string.isEmpty();
                    if (is_translate) {
                        String vi_translated_text = translator.translate(from_msgid_string, Language.ENGLISH, Language.CHINESE_SIMPLIFIED);
                        System.out.println("English Text: " + from_msgid_string);
                        System.out.println("Translation: " + vi_translated_text);
                    }//end if
                } catch (Exception ex) {
                    continue;
                }
            }//end for
*/
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine
}//end class
