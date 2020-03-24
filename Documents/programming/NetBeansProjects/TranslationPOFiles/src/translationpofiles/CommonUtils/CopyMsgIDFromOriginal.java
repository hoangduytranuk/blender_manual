/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package translationpofiles.CommonUtils;

import java.io.File;

/**
 *
 * @author htran
 */
public class CopyMsgIDFromOriginal {
    static String DOC_DIR = "DOC_DIR";
    
    String from_path = null;
    String to_path = null;
    String doc_path = null;
    String system_path_sep = null;
    
    public CopyMsgIDFromOriginal(){
        doc_path = System.getenv(DOC_DIR);
        system_path_sep = File.pathSeparator;
        
        from_path = doc_path + system_path_sep + "build/locale";
        to_path = doc_path + system_path_sep + "locale/vi/LC_MESSAGE";
    }
    
    public void Process(){
        
    }//end routine
}//end class
