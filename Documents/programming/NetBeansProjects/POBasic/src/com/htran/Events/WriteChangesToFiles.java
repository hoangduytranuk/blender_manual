/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.Common;
import base.Document;
import com.htran.CommonUtils.FileIO;
import java.awt.event.ActionEvent;

/**
 *
 * @author htran
 */
public class WriteChangesToFiles extends ProcessDocAction {

    @Override
    public void actionPerformed(ActionEvent e) {
        //ProcessDocEvent doc_event = (ProcessDocEvent) e;
        //Document to_doc = doc_event.getToDocument();        
        for (Document to_doc : Common.changed_list) {
            System.out.println("Writing changes: " + to_doc.getPath());
            try {
                FileIO.writeFile(to_doc);
            } catch (Exception ex) {
                if (to_doc != null) {
                    Common.LOGGER.info("Unable to write to:\n[" + to_doc.getPath() + "]");

                    Common.LOGGER.info(ex.toString());
                    ex.printStackTrace();
                    System.exit(0);
                }//end if
            }//end try/catch
        }//end
    }//end routine
}//end class
