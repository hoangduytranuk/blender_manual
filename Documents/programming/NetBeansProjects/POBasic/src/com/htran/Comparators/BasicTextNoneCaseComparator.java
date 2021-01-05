/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Comparators;

import java.util.Comparator;

/**
 *
 * @author htran
 */
public class BasicTextNoneCaseComparator implements Comparator {

    public static BasicTextNoneCaseComparator this_instance = null;

    public static BasicTextNoneCaseComparator getInstance() {
        if (this_instance == null) {
            this_instance = new BasicTextNoneCaseComparator();
        }
        return this_instance;
    }//end routine

    @Override
    public int compare(Object o1, Object o2) {
        try {
            boolean valid = !(o1 == null || o2 == null);
            if (! valid)
                if (o1 != null && o1 == null) return 1;
                else return -1;
            
            String s1 = (String) o1;
            String s2 = (String) o2;
            int comp = s1.compareToIgnoreCase(s2);
            return comp;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return -1;
    }//end routine
}//end class
