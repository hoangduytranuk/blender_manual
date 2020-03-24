package IO;

import java.nio.file.FileVisitResult;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 * 20-Feb-2019 19:23:25
 */
public abstract class ListPathEvent {
    private String rootPath = null;
    private Path currentPath = null;
    private BasicFileAttributes attrib = null;

    public ListPathEvent() {}
    
    public ListPathEvent(String root_path, Path current_path, BasicFileAttributes attrib){  
        this.setVars(root_path, current_path, attrib);
    }//end method

    public void setVars(String root_path, Path current_path, BasicFileAttributes attrib){

        this.setRootPath(root_path);
        this.setCurrentPath(current_path);
        this.setAttrib(attrib);        
    }//end method
    
    public abstract FileVisitResult run();

    /**
     * @return the rootPath
     */
    public String getRootPath() {
        return rootPath;
    }

    /**
     * @param rootPath the rootPath to set
     */
    public void setRootPath(String rootPath) {
        this.rootPath = rootPath;
    }

    /**
     * @return the currentPath
     */
    public Path getCurrentPath() {
        return currentPath;
    }

    /**
     * @param currentPath the currentPath to set
     */
    public void setCurrentPath(Path currentPath) {
        this.currentPath = currentPath;
    }

    /**
     * @return the attrib
     */
    public BasicFileAttributes getAttrib() {
        return attrib;
    }

    /**
     * @param attrib the attrib to set
     */
    public void setAttrib(BasicFileAttributes attrib) {
        this.attrib = attrib;
    }
}//end class

