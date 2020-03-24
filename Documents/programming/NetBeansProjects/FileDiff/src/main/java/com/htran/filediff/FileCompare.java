/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.filediff;

import com.github.difflib.DiffUtils;
import com.github.difflib.patch.Delta;
import com.github.difflib.patch.DeltaType;
import com.github.difflib.patch.Patch;
import com.github.difflib.text.DiffRow;
import com.github.difflib.text.DiffRow.Tag;
import com.github.difflib.text.DiffRowGenerator;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.function.BiPredicate;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Hoang Duy Tran <hoangduytran@gmail.com>
 */
public class FileCompare extends FileBase {

    public static enum CompareOption {
        MERGING_FILES,
        COMPARE_MSGID,
        COMPARE_MSGSTR,
        COMPARE_MSGCTX,
        COMPARE_COMMENTS,
        SOURCE_FILE_SET,
        TARGET_FILE_SET,
        MERGE_FILE_SET,
        DEBUGGING,
        DO_NOTHING

    };

    public static String[] patterns = {
        null,
        "^msgid.*$", //tieng Anh
        "^msgstr.*$", //tieng Viet\
        "^msgctxt.*$", //context
        "^#[\\.\\,].*$", //comments
        null,
        null,
        null,
        null,
        null
    };

    private static String[] header_list = {
        "# Blender's translation file",
        "# Copyright",
        "# This file is distributed",
        "# HỒ NHỰT CHÂU",
        "\"Project-Id-Version:",
        "\"Report-Msgid-Bugs-To:",
        "\"POT-Creation-Date:",
        "\"PO-Revision-Date:",
        "\"Last-Translator:",
        "\"Language-Team:",
        "\"Language:",
        "\"MIME-Version:",
        "\"Content-Type:",
        "\"Content-Transfer-Encoding:",
        "\"X-Generator:"
    };

    private static boolean is_sorted = false;
    private StartWithComparator startWithComp = null;
    List<String> orig_list = null;
    List<String> my_list = null;
    List<String> changed_list = null;
    private String origFile = null; //"/home/htran/blender-svn/bf-translations/trunk/po/vi.po";
    private String myFile = null; //"/home/htran/blender-trans-git/blender-internationalisation/trunk/po/vi.po";
    //String my_file = "/home/htran/vi.po";
    private String out_file = "/home/htran/test_vi.po";
    private String comparePattern = null;
    String[] p = {"#.", "#:", "#,"};
    private boolean debugging = false;
    private CompareOption compareOption = CompareOption.DO_NOTHING;

    /*    
    String en_line_pattern = "^msgid.*$";  //tieng Anh
    String en_line_pattern = "^msgstr.*$"; //tieng Viet\
    String en_line_pattern = "^msgctxt.*$"; //context
    String en_line_pattern = "^#[\\.\\,]*$"; //references
     */
    private void init() {
        orig_list = readFile(getOrigFile());
        my_list = readFile(getMyFile());
        clearFileContent(getOutFile());
        prepareListsForComparingOptions();
        changed_list = new ArrayList<>();
    }

    private void prepareListsForComparingOptions() {

        switch (compareOption) {
            case COMPARE_MSGID:
            case COMPARE_MSGSTR:
            case COMPARE_MSGCTX:
            case COMPARE_COMMENTS:
                orig_list = selectiveList(comparePattern, orig_list);
                my_list = selectiveList(comparePattern, orig_list);
                break;
            default:
                break;
        }//end switch
    }

    private List<String> defaultMode() {
        //BiPredicate<String, String> source_ref_comparer = (x, y) -> ((x.startsWith(p[0]) && y.startsWith(p[0])) || (x.startsWith(p[1]) && y.startsWith(p[1])) && (x.compareTo(y) == 0));
        changed_list = new ArrayList<>();
        try {
            Patch<String> patch = DiffUtils.diff(orig_list, my_list);

            changed_list = new ArrayList<>();
            int line_no = 0;
            String first_line = null;
            for (Delta delta : patch.getDeltas()) {
                DeltaType type = delta.getType();
                List<String> orig_list = this.unormalizeString(delta.getOriginal().getLines());
                List<String> my_list = this.unormalizeString(delta.getRevised().getLines());
                boolean check_header = (line_no <= 4);
                boolean is_header_list = false;

                switch (type) {
                    case DELETE:
                        changed_list.addAll(orig_list);
                        break;
                    case INSERT:
                        //remove, this is the line in my file and no longer in the orig list
                        break;
                    case CHANGE:
                        first_line = orig_list.get(0);
                        if (check_header) {
                            is_header_list = (check_header)
                                    && (first_line.startsWith("Project-Id")
                                    || first_line.startsWith("POT-Creation-Date")
                                    || first_line.startsWith("X-Generator"));
                        }
                        boolean is_translation_line = first_line.startsWith("msgstr");
                        if (is_header_list || is_translation_line) {
                            changed_list.addAll(my_list);
                        } else {
                            changed_list.addAll(orig_list);
                        }
                        break;
                    case EQUAL:
                        changed_list.addAll(my_list);
                        break;
                }//end switch
                System.out.println(type.toString() + "|" + orig_list.toString() + "|" + my_list.toString());
                line_no++;
            }//end for        
        } catch (Exception ex) {
            Logger.getLogger(FileBase.class.getName()).log(Level.SEVERE, null, ex);
        }
        return changed_list;
    }

    private List<String> generatorMode() {

        try {
            DiffRowGenerator generator = DiffRowGenerator.create()
                    .showInlineDiffs(false)
                    .inlineDiffByWord(false)
                    .oldTag(f -> "~")
                    .newTag(f -> "**")
                    .build();
            List<DiffRow> rows = generator.generateDiffRows(orig_list, my_list);

            if (this.isDebugging()) {
                System.out.println(this.toString());
                System.out.println("tag|original|new|");
                System.out.println("tag|--------|---|");                
            }//end if
            
            int line_no = 1;
//            int debug_lino = 85424;
//            int debug_count = 8;
            for (DiffRow row : rows) {
                Tag tag = row.getTag();
                String orig_line = unormalizeString(row.getOldLine());
                String my_line = unormalizeString(row.getNewLine());
                boolean check_header = (line_no <= 20);

                switch (tag) {
                    case DELETE:
                        changed_list.add(orig_line);
                        break;
                    case INSERT:
                        //- this is in my_file, which has been deleted from original, so ignore
                        //
                        break;
                    case CHANGE:
//                        boolean is_debug_line = (line_no >= debug_lino) && (line_no <= debug_lino+debug_count);
//                        if (is_debug_line){
//                            System.out.println("******DEBUG_LINE" + line_no);
//                            System.out.println("******" + row);
//                        }
                        boolean is_header_area = (line_no < 19);
                        if (is_header_area){
                            changed_list.add(my_line);
                            break;
                        }
                        
                        boolean is_my_line_empty = (my_line == null || my_line.trim().isEmpty());
                        boolean is_orig_line_empty = (orig_line == null || orig_line.trim().isEmpty());   
                        
                        boolean is_use_my_line = (is_orig_line_empty && !is_my_line_empty);
                        if (is_use_my_line){
                            changed_list.add(my_line);
                            break;
                        }
                        
                        boolean is_use_orig_line = (is_my_line_empty && !is_orig_line_empty);
                        if (is_use_orig_line){
                            changed_list.add(orig_line);
                            break;
                        }
                        
                        //both are not empty, we have to choose
                        boolean is_msgstr_line = (orig_line.startsWith("msgstr"));
                        if (is_msgstr_line) {
                            changed_list.add(my_line);
                        } else {
                            changed_list.add(orig_line);
                        }
                        break;
                    case EQUAL:
                        changed_list.add(my_line);
                        break;
                    default:
                        System.out.println(line_no + "|DEFAULT|" + orig_line + "|" + my_line);
                        break;
                }
                if (this.isDebugging()) {
                    System.out.println(line_no + "|" + tag.toString() + "|" + orig_line + "|" + my_line);
                }
                
                line_no++;
            }
        } catch (Exception ex) {
            Logger.getLogger(FileBase.class.getName()).log(Level.SEVERE, null, ex);
        }
        return changed_list;
    }
/*
    private boolean isUseMyLine(int line_number, String orig_line, String my_line) {
        
        boolean is_empty_line = trimmed_line.endsWith("\"\"") || trimmed_line.isEmpty();
        boolean is_non_empty_msgstr = trimmed_line.startsWith("msgstr") && !is_empty_line;
        boolean is_my_line_empty = (my_line == null) || my_line.isEmpty();
        return (is_header || is_non_empty_msgstr) && (! is_my_line_empty);
    }
*/
    public void run() {
        init();
        //defaultMode();
        generatorMode();
        writeFile(getOutFile(), changed_list);
    }

    private boolean isHeader(String line) {
        if (!is_sorted) {
            Arrays.sort(header_list);
            startWithComp = new StartWithComparator();
            is_sorted = true;
        }//end sorting list
        int index = Arrays.binarySearch(header_list, line, startWithComp);
        boolean is_header = (index >= 0);
//        if (!is_header)
//            System.out.println("Not header:" + line);
        return is_header;
    }

    private List<String> unormalizeString(List<String> lst) {
        lst.forEach(item -> unormalizeString(item));
        return lst;
    }

    private String unormalizeString(String str) {
        return unHtml(str);//.replace("    ", "\t");
    }

    private String unHtml(String str) {
        return str.replace("&lt;", "<").replace("&gt;", ">");
    }

    /**
     * @return the compareOption
     */
    public CompareOption getCompareOption() {
        return compareOption;
    }

    /**
     * @param compareOption the compareOption to set
     */
    public void setCompareOption(CompareOption compareOption) {
        this.compareOption = compareOption;
    }

    /**
     * @return the origFile
     */
    public String getOrigFile() {
        return origFile;
    }

    /**
     * @param origFile the origFile to set
     */
    public void setOrigFile(String origFile) {
        this.origFile = origFile;
    }

    /**
     * @return the myFile
     */
    public String getMyFile() {
        return myFile;
    }

    /**
     * @param myFile the myFile to set
     */
    public void setMyFile(String myFile) {
        this.myFile = myFile;
    }

    /**
     * @return the comparePattern
     */
    public String getComparePattern() {
        return comparePattern;
    }

    /**
     * @param comparePattern the comparePattern to set
     */
    public void setComparePattern(String comparePattern) {
        this.comparePattern = comparePattern;
    }

    /**
     * @return the out_file
     */
    public String getOutFile() {
        return out_file;
    }

    /**
     * @param out_file the out_file to set
     */
    public void setOutFile(String out_file) {
        this.out_file = out_file;
    }

    /**
     * @return the debugging
     */
    public boolean isDebugging() {
        return debugging;
    }

    /**
     * @param debugging the debugging to set
     */
    public void setDebugging(boolean debugging) {
        this.debugging = debugging;
    }

    public String toString() {
        StringBuilder b = new StringBuilder();
        b.append("option: " + this.getCompareOption()).append("\n");
        b.append("pattern: " + this.getComparePattern()).append("\n");
        b.append("original file: " + this.getOrigFile()).append("\n");
        b.append("my file: " + this.getMyFile()).append("\n");
        b.append("output file: " + this.getOutFile()).append("\n");
        b.append("DEBUGGING: " + this.isDebugging()).append("\n");
        return b.toString();
    }//end routine

}//end of class

class StartWithComparator implements Comparator {

    @Override
    public int compare(Object o1, Object o2) {
        //o1 is the line in header_list
        //o2 is the line to be compare
        int value = -1;
        try {
            String s1 = (String) o1; //header list
            String s2 = (String) o2; //line from file
            if (s2.startsWith(s1)) {
                value = 0;
            } else {
                value = s1.compareTo(s2);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return value;
    }
}
