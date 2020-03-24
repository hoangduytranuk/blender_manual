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
 * 20-Feb-2019 17:00:15
 */
public class TextBlockComponent {
    private String ID = null;
    private ArrayList<String>textList = new ArrayList<>();
    private int sourceIndex = -1;    
    @Override
    public String toString(){
        return "You're in TextBlockComponent";
    }//end
}//end class
