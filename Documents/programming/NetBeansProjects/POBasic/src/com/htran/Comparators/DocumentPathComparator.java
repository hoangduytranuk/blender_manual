/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Comparators;

import base.Document;
import java.util.Comparator;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class DocumentPathComparator implements Comparator {
    public static DocumentPathComparator instance = null;

    public static DocumentPathComparator getInstance() {
        if (instance == null) {
            instance = new DocumentPathComparator();
        }
        return instance;
    }//end routine

    @Override
    public int compare(Object o1, Object o2) {
        try{
            if (o1 == o2){
                return 0;
            }
            Document d1 = (Document) o1;
            Document d2 = (Document) o2;
            int comp = (d1.getPath().compareTo(d2.getPath()));
            return comp;
        }catch(Exception ex){
            return -1;
        }
    }//end routine
    
}//end class
