/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.htran.Events;

import base.Common;
import com.htran.Comparators.BasicTextNoneCaseComparator;
import java.awt.event.ActionEvent;
import java.util.TreeMap;
import java.util.function.BiConsumer;

/**
 *
 * @author htran
 */
public class OutputStat extends ProcessDocAction {

    @Override
    public void actionPerformed(ActionEvent e) {
        TreeMap<Integer, String> count_map = new TreeMap<>();
        
        Common.word_stat.forEach(new BiConsumer<String, Integer>() {
            public void accept(String text, Integer count) {
                if (count > 1){
                    count_map.put(count, text);
                }
            }
        });
        
        count_map.forEach(new BiConsumer<Integer, String>() {
            public void accept(Integer count, String text) {
                Common.LOGGER.info(count + "\t[" + text + "]");
            }
        });
                
    }//end routine
}//end class
