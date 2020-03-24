/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.Common;
import base.TextBlock;
import base.TextBlockComponent;
import java.awt.event.ActionEvent;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class PossibleMatch extends ProcessDocAction {

    public static PossibleMatch this_instance = null;

    public static PossibleMatch getInstance() {
        if (this_instance == null) {
            this_instance = new PossibleMatch();
        }
        return this_instance;
    }//end routine

    @Override
    public void actionPerformed(ActionEvent e) {

        TextBlock tbx1, tbx2;
        TextBlockComponent msgid_block_1, msgid_block_2;
        String str_1, str_2;
        int compare_value = -1;

        try {
            ProcessTextBlockEvent ev = (ProcessTextBlockEvent) e;
            tbx1 = (TextBlock) ev.getFromBlock();
            tbx2 = (TextBlock) ev.getToBlock();
            boolean ok = (tbx1 != null) && (tbx2 != null);
            if (!ok) {
                return;
            }

            msgid_block_1 = tbx1.getMsgid();
            msgid_block_2 = tbx2.getMsgid();
            boolean is_comparable = (msgid_block_1 != null && msgid_block_2 != null);
            if (is_comparable) {
                str_1 = msgid_block_1.getFlatText();
                str_2 = msgid_block_2.getFlatText();

                boolean is_1_in_2 = str_2.contains(str_1);
                boolean is_2_in_1 = str_1.contains(str_2);
                boolean is_possible = (is_1_in_2 || is_2_in_1);
                if (is_possible) {
                    //plural

                    int plural_1 = str_1.compareTo(str_2 + "s");
                    int plural_2 = new String(str_1 + "s").compareTo(str_2);
                    boolean is_plural = (plural_1 == 0) || (plural_2 == 0);
                    //Node name
                    int node_1 = str_1.compareTo(str_2 + " Node");
                    int node_2 = (str_1 + " Node").compareTo(str_2);
                    boolean is_node = (node_1 == 0) || (node_2 == 0);
                    /*
                    int node_comment_1 = str_1.compareTo(str_2 + " Node.");
                    int node_comment_2 = (str_1 + " Node.").compareTo(str_2);
                    boolean is_node_comment = (node_1 == 0) || (node_2 == 0);
                     */
//                    is_possible = (is_plural || is_node || is_node_comment);
                    is_possible = (is_plural || is_node);
                    if (is_possible) {
                        String msgstr_1 = tbx1.getMsgstr().getFlatText();
                        String msgstr_2 = tbx2.getMsgstr().getFlatText();
                        boolean not_translated = (msgstr_2.isEmpty());
                        String translation = "";
                        if (not_translated) {                            
                            if (is_plural) {
                                translation = msgstr_1 + Common.TRANSLATION_GAP_FILLER + str_2;
                            }
                            if (is_node) {
                                translation = "Nút " + msgstr_1 + Common.TRANSLATION_GAP_FILLER + str_2;
                            }
                            
                            if (!translation.isEmpty()) {
                                Common.PrintDocumentPath();
                                System.out.println("vipo: msgid:[" + str_1 + "] msgstr:[" + msgstr_1 + "]");
                                System.out.println("manual: msgid:[" + str_2 + "] msgstr:[" + translation + "]\n");
                                
                                tbx2.getMsgstr().clear();
                                tbx2.getMsgstr().add(translation);
                                tbx2.getDocument().setDirty(true);
                            }//end if
                            //System.exit(0);
                        }//end if if (not_translated)                        
                    }//end if (is_possible) {
                }//end if (is_possible) {
            }//end if (is_comparable) {
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end try/catch
    }//end routine
}//end class
