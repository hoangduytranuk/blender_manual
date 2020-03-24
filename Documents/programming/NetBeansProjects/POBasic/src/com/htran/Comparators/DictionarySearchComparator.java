/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Comparators;

import base.TextBlock;
import base.TextBlockComponent;
import java.util.Comparator;

/**
 *
 * @author htran
 */
public class DictionarySearchComparator implements Comparator {
    public static DictionarySearchComparator this_instance = null;
    public static DictionarySearchComparator getInstance(){
        if (this_instance == null)
            this_instance = new DictionarySearchComparator();
        return this_instance;
    }//end routine
    
    @Override
    public int compare(Object o1, Object o2) {
        int compare_value = -1;
        try {
/*            
            TextBlock tbx1 = (TextBlock) o1;
            String tbx2 = (TextBlock) o2;
            TextBlockComponent msgid_block_1 = tbx1.getMsgid();
            TextBlockComponent msgid_block_2 = tbx2.getMsgid();

            boolean is_comparable = (msgid_block_1 != null && msgid_block_2 != null);
            if (is_comparable) {
                String str_1 = msgid_block_1.FlatText();
                String str_2 = msgid_block_2.FlatText();
                compare_value = str_1.compareTo(str_2);
/*                
                //debugging
                if (compare_value != 0){
                    System.out.println("Not equal:");
                    System.out.println("str_1 = [" + str_1 + "]");
                    System.out.println("str_2 = [" + str_2 + "]");
                }//end if debugging

            }else{
                throw new RuntimeException("Unable to compare msgid: [" + tbx1 + "] and: [" + tbx2);
            }//end if
*/
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return compare_value;
    }//end routine
}//end class
