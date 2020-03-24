/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import java.awt.event.ActionEvent;
import base.Document;

/**
 *
 * @author htran
 */
public class ProcessDocEvent extends ActionEvent{

    /**
     * @return the fromDocument
     */
    public Document getFromDocument() {
        return fromDocument;
    }

    /**
     * @param fromDocument the fromDocument to set
     */
    public void setFromDocument(Document fromDocument) {
        this.fromDocument = fromDocument;
    }

    /**
     * @return the toDocument
     */
    public Document getToDocument() {
        return toDocument;
    }

    /**
     * @param toDocument the toDocument to set
     */
    public void setToDocument(Document toDocument) {
        this.toDocument = toDocument;
    }
    
    private Document fromDocument = null;
    private Document toDocument = null;
    
    public ProcessDocEvent(Object source, int id, String command) {
        super(source, id, command);
    }
    
    
}
