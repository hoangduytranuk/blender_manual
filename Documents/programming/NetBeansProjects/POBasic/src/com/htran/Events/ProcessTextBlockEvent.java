/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.Events;

import base.TextBlock;
import java.awt.event.ActionEvent;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class ProcessTextBlockEvent extends ActionEvent {    
    
    /**
     * @return the fromBlock
     */
    public TextBlock getFromBlock() {
        return fromBlock;
    }

    /**
     * @param fromBlock the fromBlock to set
     */
    public void setFromBlock(TextBlock fromBlock) {
        this.fromBlock = fromBlock;
    }

    /**
     * @return the toBlock
     */
    public TextBlock getToBlock() {
        return toBlock;
    }

    /**
     * @param toBlock the toBlock to set
     */
    public void setToBlock(TextBlock toBlock) {
        this.toBlock = toBlock;
    }
    
    private TextBlock fromBlock;
    private TextBlock toBlock;
    
    public ProcessTextBlockEvent(Object source, int id, String command) {
        super(source, id, command);
    }
}//end class
