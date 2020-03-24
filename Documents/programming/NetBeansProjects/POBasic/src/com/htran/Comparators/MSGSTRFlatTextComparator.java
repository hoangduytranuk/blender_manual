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
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class MSGSTRFlatTextComparator implements Comparator {
    public static MSGSTRFlatTextComparator instance = null;
    public static MSGSTRFlatTextComparator getInstance(){
        if (instance == null)
            instance = new MSGSTRFlatTextComparator();
        return instance;
    }//end routine

    @Override
    public int compare(Object o1, Object o2) {
        int compare_value = -1;
        try {
            TextBlock tbx1 = (TextBlock) o1;
            TextBlock tbx2 = (TextBlock) o2;
            TextBlockComponent block1_comp = tbx1.getMsgstr();
            TextBlockComponent block2_comp = tbx2.getMsgstr();

            boolean is_comparable = (block1_comp != null && block2_comp != null);
            if (is_comparable) {
                String str_1 = block1_comp.getFlatText();
                String str_2 = block2_comp.getFlatText();
                compare_value = str_1.compareTo(str_2);
/*
                //debugging
                if (compare_value != 0){
                    System.out.println("Not equal:");
                    System.out.println("str_1 = [" + str_1 + "]");
                    System.out.println("str_2 = [" + str_2 + "]");
                }//end if debugging
*/
            }else{
                throw new RuntimeException("Unable to compare comment: [" + tbx1 + "] and: [" + tbx2);
            }//end if
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return compare_value;
    }//end routine
}//end class