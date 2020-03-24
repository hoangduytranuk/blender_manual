/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Chunk;
import com.github.difflib.patch.Delta;
import com.github.difflib.patch.DeltaType;
import com.github.difflib.patch.Patch;
import base.Document;
import base.TextBlock;
import base.TextBlockComponent;
import com.htran.Comparators.COMMENTFlatTextComparator;
import com.htran.Comparators.MSGIDFlatTextComparator;
import com.htran.Comparators.MSGSTRFlatTextComparator;
import java.awt.event.ActionEvent;
import java.util.List;
import java.util.function.BiPredicate;

/**
 *
 * @author htran
 */
public class TransferOriginalMSGIDOver extends ProcessDocAction {
    Document from_doc = null;
    Document to_doc = null;

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;
            from_doc = doc_event.getFromDocument();
            to_doc = doc_event.getToDocument();

            Patch<TextBlock> patch;
            patch = DiffUtils.diff(from_doc, to_doc, new BiPredicate<TextBlock, TextBlock>() {
                @Override
                public boolean test(TextBlock from_blk, TextBlock to_blk) {
                    TextBlockComponent msgcomment_block = from_blk.getComment();
                    boolean is_first_block = (msgcomment_block != null && msgcomment_block.getStartLine() == 0);
                    if (is_first_block) {
                        return true; //assumed to be equal, do not perform checks
                    }//end if

                    MSGIDFlatTextComparator msgid_comparator = MSGIDFlatTextComparator.getInstance();
                    COMMENTFlatTextComparator msgcomment_comparator = COMMENTFlatTextComparator.getInstance();
                    MSGSTRFlatTextComparator msgstr_comparator = MSGSTRFlatTextComparator.getInstance();

                    int comment_compare_value = msgcomment_comparator.compare(from_blk, to_blk);
                    int msgid_compare_value = msgid_comparator.compare(from_blk, to_blk);
                    int msgstr_compare_value = msgstr_comparator.compare(from_blk, to_blk);

                    boolean is_comment_equal = (comment_compare_value == 0);
                    boolean is_msgid_equal = (msgid_compare_value == 0);
                    boolean is_msgstr_equal = (msgstr_compare_value == 0);

                    boolean is_equal = (is_msgid_equal && is_comment_equal && is_msgstr_equal);

                    //perform transfer changes here, after compared, so debugging should work
                    return is_equal;

                }

                @Override
                public BiPredicate<TextBlock, TextBlock> and(BiPredicate<? super TextBlock, ? super TextBlock> other) {
                    throw new UnsupportedOperationException("and Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                }

                @Override
                public BiPredicate<TextBlock, TextBlock> negate() {
                    throw new UnsupportedOperationException("negate Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                }

                @Override
                public BiPredicate<TextBlock, TextBlock> or(BiPredicate<? super TextBlock, ? super TextBlock> other) {
                    throw new UnsupportedOperationException("or Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                }

            });
            /*
            Patch<TextBlock> patch = DiffUtils.diff(from_doc, to_doc, new Equalizer<TextBlock>(){
                public boolean equals(TextBlock from_blk, TextBlock to_blk) {

                    TextBlockStatus msgcomment_block = from_blk.getBlockByType(TextBlockStatus.BlockType.BLOCK_COMMENT);
                    boolean is_first_block = (msgcomment_block != null && msgcomment_block.getStartLine() == 0);
                    if (is_first_block){
                        return true; //assumed to be equal, do not perform checks
                    }//end if

                    MSGIDFlatTextComparator msgid_comparator = MSGIDFlatTextComparator.getInstance();
                    COMMENTFlatTextComparator msgcomment_comparator = COMMENTFlatTextComparator.getInstance();

                    int comment_compare_value = msgcomment_comparator.compare(from_blk, to_blk);
                    int msgid_compare_value = msgid_comparator.compare(from_blk, to_blk);

                    boolean is_comment_equal = (comment_compare_value == 0);
                    boolean is_msgid_equal = (msgid_compare_value == 0);
                    boolean is_equal = (is_msgid_equal && is_comment_equal);

                    //perform transfer changes here, after compared, so debugging should work
                    return is_equal;
                }//end routine
            });
             */
            int patch_size = patch.getDeltas().size();
            boolean has_patches = (patch_size > 0);
            if (!has_patches) {
                return;
            }
            String from_path, to_path;
            from_path = from_doc.getPath();
            to_path = to_doc.getPath();
            System.out.println("-------------------------------------------------------------------------");
            System.out.println("from document: " + from_path);
            System.out.println("to document: " + to_path);
            System.out.println("-------------------------------------------------------------------------");

            TextBlock from_blk, to_blk;
            Chunk<TextBlock> from_chunk, to_chunk;
            //list out changes for debugging purpose
            for (int i = 0; i < patch.getDeltas().size(); i++) {
                Delta<TextBlock> delta = patch.getDeltas().get(i);
                DeltaType type = delta.getType();
                from_chunk = delta.getOriginal();
                to_chunk = delta.getRevised();
                switch (type) {
                    case CHANGE:
                        List<TextBlock> from_list = from_chunk.getLines();
                        List<TextBlock> to_list = to_chunk.getLines();
                        for (int j = 0; j < from_list.size(); j++) {
                            TextBlock from_block = from_list.get(j);
                            TextBlock to_block = from_list.get(j);
                            TransferBlock(from_block, to_block);
                        }///end for
                        break;
                    case INSERT:
                        break;
                    case DELETE:
                        break;
                    case EQUAL:
                        break;
                }//end switch
                //String delta_string = delta.toString();
                //System.out.println(delta_string);
            }//end for
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine

    private void TransferBlock(TextBlock from_block, TextBlock to_block) {

        TextBlockComponent from_block_comment = from_block.getComment();
        TextBlockComponent from_block_msgctxt = from_block.getMsgctxt();
        TextBlockComponent from_block_msgid = from_block.getMsgid();
        TextBlockComponent from_block_msgstr = from_block.getMsgstr();

        TextBlockComponent to_block_comment = to_block.getComment();
        TextBlockComponent to_block_msgctxt = to_block.getMsgctxt();
        TextBlockComponent to_block_msgid = to_block.getMsgid();
        TextBlockComponent to_block_msgstr = to_block.getMsgstr();

        TransferComponent(from_block_comment, to_block_comment, true);
        TransferComponent(from_block_msgctxt, to_block_msgctxt, true);
        TransferComponent(from_block_msgid, to_block_msgid, true);
        TransferComponent(from_block_msgstr, to_block_msgstr, false);
    }//end routine

    private void TransferComponent(TextBlockComponent from_comp, TextBlockComponent to_comp, boolean is_copy_to_from) {
        boolean is_both_null = (from_comp == null) && (to_comp == null);
        boolean is_to_null = (from_comp != null) && (to_comp == null);
        boolean is_from_null = (from_comp == null) && (to_comp != null);
        boolean is_both_there = (from_comp != null) && (to_comp != null);

        if (is_both_null) {
            return; /// do nothing
        }//end if

        if (is_to_null) {
            return; //do not change from
        }//end if

        if (is_from_null) {
            if (is_copy_to_from) {
                from_comp = to_comp;
                from_doc.setDirty(true);
            } else {
                to_comp = from_comp;
                to_doc.setDirty(true);
            }
        }//end if

        if (is_both_there) {
            String flat_from = from_comp.getFlatText();
            String flat_to = to_comp.getFlatText();
            boolean is_from_empty = (flat_from.length() == 0);
            boolean is_to_empty = (flat_to.length() == 0);
            boolean is_changed = (flat_from.compareTo(flat_to) != 0);

            if (is_changed) {
                if (is_from_empty){
                    from_comp = to_comp;
                    from_doc.setDirty(true);
                }else if (is_to_empty){
                    to_comp = from_comp;
                    to_doc.setDirty(true);
                }else if (is_copy_to_from) {
                    from_comp = to_comp;
                    from_doc.setDirty(true);
                } else {
                    to_comp = from_comp;
                    to_doc.setDirty(true);
                }//end if
            }//end if
        }//end if
    }//end routine
}//end class
