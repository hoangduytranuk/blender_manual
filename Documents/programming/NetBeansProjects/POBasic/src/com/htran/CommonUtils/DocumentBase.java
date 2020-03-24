/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import base.Document;
import base.TextBlock;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public interface DocumentBase {
    public Document documentBase = null;
    public TextBlock textBlockBase = null;
    
    public Document getDocument();
    public void setDocument(Document doc);

    public TextBlock getTextBlock();
    public void setTextBlock(TextBlock txt_block);
}

