/*
 * Copyright (C) 2019 Hoang Duy Tran <hoangduytran1960@googlemail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package IO;

import java.nio.file.FileVisitResult;

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 * 23-Feb-2019 23:30:17
 */
public class FindParentDir extends ListPathEvent{

    private String searchPath = null;
    
    public FindParentDir(String search_path){
        this.searchPath = search_path;
    }
    
    @Override
    public FileVisitResult run() {
        //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        boolean is_dir = this.getAttrib().isDirectory();
        if (! is_dir)
            return FileVisitResult.CONTINUE;
        
        String current_path = this.getCurrentPath().toString();
        boolean is_current_dir = (current_path == ".");
        boolean is_parent_dir = (current_path == "..");
        boolean is_ignore = (is_current_dir || is_parent_dir);
        
        if (is_ignore) return FileVisitResult.CONTINUE;
        
        
        boolean is_found = (current_path.contains(searchPath));
        
        return FileVisitResult.TERMINATE;
    }//end method    
}//end class
