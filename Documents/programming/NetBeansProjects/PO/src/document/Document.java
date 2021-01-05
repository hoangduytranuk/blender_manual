package document;


import java.util.ArrayList;

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

/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 * 20-Feb-2019 17:32:58
 */
public class Document {
    private String path = null;
    private boolean isFlat = false;
    private boolean isChanged = false;
    private boolean isUnique = false;
    private boolean isSorted = false;
    private boolean titlePrinted = false;
    private ArrayList<TextBlock> block_list = new ArrayList<>();
    
    @Override
    public String toString(){
        return "You're in Document";
    }//end

    /**
     * @return the path
     */
    public String getPath() {
        return path;
    }

    /**
     * @param path the path to set
     */
    public void setPath(String path) {
        this.path = path;
    }

    /**
     * @return the isFlat
     */
    public boolean isIsFlat() {
        return isFlat;
    }

    /**
     * @param isFlat the isFlat to set
     */
    public void setIsFlat(boolean isFlat) {
        this.isFlat = isFlat;
    }

    /**
     * @return the isChanged
     */
    public boolean isIsChanged() {
        return isChanged;
    }

    /**
     * @param isChanged the isChanged to set
     */
    public void setIsChanged(boolean isChanged) {
        this.isChanged = isChanged;
    }

    /**
     * @return the isUnique
     */
    public boolean isIsUnique() {
        return isUnique;
    }

    /**
     * @param isUnique the isUnique to set
     */
    public void setIsUnique(boolean isUnique) {
        this.isUnique = isUnique;
    }

    /**
     * @return the isSorted
     */
    public boolean isIsSorted() {
        return isSorted;
    }

    /**
     * @param isSorted the isSorted to set
     */
    public void setIsSorted(boolean isSorted) {
        this.isSorted = isSorted;
    }

    /**
     * @return the titlePrinted
     */
    public boolean isTitlePrinted() {
        return titlePrinted;
    }

    /**
     * @param titlePrinted the titlePrinted to set
     */
    public void setTitlePrinted(boolean titlePrinted) {
        this.titlePrinted = titlePrinted;
    }

    /**
     * @return the block_list
     */
    public ArrayList<TextBlock> getBlock_list() {
        return block_list;
    }

    /**
     * @param block_list the block_list to set
     */
    public void setBlock_list(ArrayList<TextBlock> block_list) {
        this.block_list = block_list;
    }
}//end class
