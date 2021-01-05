/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Comparators;

import base.Common;
import base.TextBlock;
import base.TextBlockComponent;
import com.htran.Events.ProcessDocAction;
import com.htran.Events.ProcessTextBlockEvent;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 *
 * @author htran
 */
public class MSGIDFlatTextComparator implements Comparator {
    public static MSGIDFlatTextComparator this_instance = null;

    public static MSGIDFlatTextComparator getInstance() {
        if (this_instance == null) {
            this_instance = new MSGIDFlatTextComparator();
        }
        return this_instance;
    }//end routine

/*

    private List<ProcessDocAction> matchActionListenerList = null;
    private List<ProcessDocAction> possibleMatchActionListenerList = null;
    
    public MSGIDFlatTextComparator(){
        matchActionListenerList = new ArrayList<ProcessDocAction>();
        possibleMatchActionListenerList = new ArrayList<ProcessDocAction>();        
    }
    
    public void AddMatchActionListener(ProcessDocAction a) {
        this.matchActionListenerList.add(a);
    }

    public void RemoveMatchActionListener(ProcessDocAction a) {
        this.matchActionListenerList.remove(a);
    }

    public void AddPossibleMatchActionListener(ProcessDocAction a) {
        this.possibleMatchActionListenerList.add(a);
    }

    public void RemovePossibleMatchActionListener(ProcessDocAction a) {
        this.possibleMatchActionListenerList.remove(a);
    }
    
    public void ProcessMatchActions(TextBlock from, TextBlock to) {
        for (int i = matchActionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = matchActionListenerList.get(i);
            ProcessTextBlockEvent e = new ProcessTextBlockEvent(this, i, null);
            e.setFromBlock(from);;
            e.setFromBlock(to);
            a.actionPerformed(e);
        }//end for        
    }//end routine

    public void ProcessPossibleMatchActions(TextBlock from, TextBlock to) {
        for (int i = possibleMatchActionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = possibleMatchActionListenerList.get(i);
            ProcessTextBlockEvent e = new ProcessTextBlockEvent(this, i, null);
            e.setFromBlock(from);;
            e.setFromBlock(to);
            a.actionPerformed(e);
        }//end for        
    }//end routine
*/
    
    @Override
    public int compare(Object o1, Object o2) {
        String str_1, str_2;

        TextBlock tbx1, tbx2;
        TextBlockComponent msgid_block_1, msgid_block_2;

        int compare_value = -1;
        
        boolean is_bigger = (o1 != null) && (o2 == null);
        boolean is_smaller = (o1 == null) && (o2 != null);
        
        if (is_bigger)
            return 1;
        if (is_smaller)
            return -1;
        
        boolean valid = !(o1 == null || o2 == null);
        if (!valid) {
            return -1;
        }

        try {
            tbx1 = (TextBlock) o1;
            tbx2 = (TextBlock) o2;
            msgid_block_1 = tbx1.getMsgid();
            msgid_block_2 = tbx2.getMsgid();
            
            boolean is_comparable = (msgid_block_1 != null && msgid_block_2 != null);
            if (is_comparable) {
                str_1 = msgid_block_1.getFlatText();
                str_2 = msgid_block_2.getFlatText();
                compare_value = str_1.compareTo(str_2);                
            }//end if
        } catch (Exception ex) {
            ex.printStackTrace();
            Common.LOGGER.info((ex.toString()));
            System.exit(0);
        }
        return compare_value;
    }//end routine
}//end class
