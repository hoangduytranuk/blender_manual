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
public class COMMENTFlatTextComparator implements Comparator {
    public static COMMENTFlatTextComparator this_instance = null;
    public static COMMENTFlatTextComparator getInstance(){
        if (this_instance == null)
            this_instance = new COMMENTFlatTextComparator();
        return this_instance;
    }//end routine
    
    @Override
    public int compare(Object o1, Object o2) {
        int compare_value = -1;
        try {
            TextBlock tbx1 = (TextBlock) o1;
            TextBlock tbx2 = (TextBlock) o2;
            TextBlockComponent msgcomment_block_1 = tbx1.getComment();
            TextBlockComponent msgcomment_block_2 = tbx2.getComment();

            boolean is_comparable = (msgcomment_block_1 != null && msgcomment_block_2 != null);
            if (is_comparable) {
                String str_1 = msgcomment_block_1.getFlatText();
                String str_2 = msgcomment_block_2.getFlatText();
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
