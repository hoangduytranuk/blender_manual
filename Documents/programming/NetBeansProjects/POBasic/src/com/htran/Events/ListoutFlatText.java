/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.Common;
import base.Document;
import java.awt.event.ActionEvent;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class ListoutFlatText extends ProcessDocAction {

    @Override
    public void actionPerformed(ActionEvent e) {
        boolean has_changed, is_changed = false;
        try {
            ProcessDocEvent doc_event = (ProcessDocEvent) e;

            //Document vipo = doc_event.getFromDocument();
            Document manual = doc_event.getToDocument();
            manual.setFlat();
            Common.LOGGER.info(manual.docToString());
        } catch (Exception ex) {
            ex.printStackTrace();
        }//end switch/case
    }//end routine   
}//end class
