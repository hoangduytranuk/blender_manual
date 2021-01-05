/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.translationpomaven;

import base.Document;
import java.util.ArrayList;
import javax.swing.table.AbstractTableModel;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class TableTextData extends AbstractTableModel {

    /**
     * @return the thisDoc
     */
    public Document getThisDoc() {
        return thisDoc;
    }

    /**
     * @param thisDoc the thisDoc to set
     */
    public void setThisDoc(Document thisDoc) {
        this.thisDoc = thisDoc;
    }

    /**
     * @return the otherDoc
     */
    public Document getOtherDoc() {
        return otherDoc;
    }

    /**
     * @param otherDoc the otherDoc to set
     */
    public void setOtherDoc(Document otherDoc) {
        this.otherDoc = otherDoc;
    }
    private Document thisDoc = new Document("");
    private Document otherDoc = new Document("");
    private int numRow = 0;
    private ArrayList<String> diffLines = new ArrayList<>();

    /**
     * @return the numRow
     */
    public int getNumRow() {
        return numRow;
    }

    /**
     * @param numRow the numRow to set
     */
    public void setNumRow(int numRow) {
        this.numRow = numRow;
    }

    
    @Override
    public int getRowCount() {
        return diffLines.size();
    }

    @Override
    public int getColumnCount() {
        //columns: text left, button to right, button to left, text right;
       return 4;
    }

    @Override
    public Object getValueAt(int rowIndex, int columnIndex) {
        String text_line = null;
        int index = Math.max(0, Math.min(rowIndex, diffLines.size()));
        try{
            text_line = diffLines.get(index);
        }catch(Exception ex){
            text_line = null;
        }
        return text_line;
    }
    
    
}//end class
