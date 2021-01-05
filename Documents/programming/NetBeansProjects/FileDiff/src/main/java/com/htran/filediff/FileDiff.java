/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.filediff;

import java.io.File;
import java.util.Arrays;
import java.util.List;
import java.util.TreeMap;

/**
 *
 * @author Hoang Duy Tran <hoangduytran@gmail.com>
 */
public class FileDiff {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        FileCompare x = parsingArgument(args);
        if (x != null) {
            //System.out.println(x);
            x.run();
        }
    }

    public static String helpMessage() {
        String msg = "java -jar <path>\\FileDiff <options> -f original_po_file -t my_po_file [-o merge_file_output -d]\n"
                + "Where <options> include:\n"
                + "\t--h : \tPrint out this help message\n"
                + "\t-m :\tmerging all differences, all Vietnamese translations required are taken from my file.\n"
                + "\t-id :\tcompare differences in msgid elements only\n"
                + "\t-ctx :\tcomparing differences in msgctx elements only only\n"
                + "\t-cm :\tcomparing differences in comment elements only\n"
                + "\t-str :\tcomparing differences in msgstr elements only\n"
                + "\t-f :\tset the source file - original\n"
                + "\t-t :\tset the target file - my file\n"
                + "\t-o :\tset the output of merge to a file\n"
                + "\t-d:\tdebugging - Output id, ctx, cm in separte files."
                + "Merge output will be set in $HOME/test_vi.po, and parsing results are written to STDOUT";

        return msg;
    }

    public static FileCompare parsingArgument(String[] args) {
        int count = args.length;
        if (count < 3) {
            System.out.println(helpMessage());
            return null;
        }

        TreeMap<FileCompare.CompareOption, String> argList = hashingArguments(args);
        System.out.println(argList);
        FileCompare x = setOption(argList);
        
        return x;
    }//end routine

    private static TreeMap<FileCompare.CompareOption, String> hashingArguments(String[] args) {
        TreeMap<FileCompare.CompareOption, String> arg_list = new TreeMap<FileCompare.CompareOption, String>();
        FileCompare.CompareOption op, store_op;
        //String msg = "java -jar <path>\\FileDiff <options> -f original_po_file -t my_po_file [-o merge_file_output -d]\n"
        try {
            op = store_op = FileCompare.CompareOption.DO_NOTHING;
            for (String arg : args) {
                boolean is_options = arg.startsWith("-");
                if (is_options) { //options
                    String lcase_arg = arg.toLowerCase();
                    switch (lcase_arg) {
                        case "--h":
                            System.out.println(helpMessage());
                            System.exit(0);
                        case "-m":
                            store_op = FileCompare.CompareOption.MERGING_FILES;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-id":
                            store_op = FileCompare.CompareOption.COMPARE_MSGID;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-str":
                            store_op = FileCompare.CompareOption.COMPARE_MSGSTR;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-ctx":
                            store_op = FileCompare.CompareOption.COMPARE_MSGCTX;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-cm":
                        case "-cmt":
                            store_op = FileCompare.CompareOption.COMPARE_COMMENTS;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-d":
                            store_op = FileCompare.CompareOption.DEBUGGING;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, lcase_arg);
                            break;
                        case "-f":
                            op = store_op = FileCompare.CompareOption.SOURCE_FILE_SET;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, null);
                            break;
                        case "-t":
                            op = store_op = FileCompare.CompareOption.TARGET_FILE_SET;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, null);
                            break;
                        case "-o":
                            op = store_op = FileCompare.CompareOption.MERGE_FILE_SET;
                            checkDuplication(store_op, arg_list);
                            arg_list.put(store_op, null);
                            break;
                        default:
                            throw new RuntimeException("Don't understand options: [" + arg + "]");
                    }//end switch                                        
                } else {
                    String file_path = arg;
                    switch (op) {
                        case SOURCE_FILE_SET:
                        case TARGET_FILE_SET:
                        case MERGE_FILE_SET:
                            arg_list.replace(op, file_path);
                            checkFileSanity(file_path, (op == FileCompare.CompareOption.MERGE_FILE_SET));
                            op = FileCompare.CompareOption.DO_NOTHING;
                            break;
                        default:
                            throw new RuntimeException("Illegal input: [" + arg + "]");
                    }//end switch
                }//end if
            }//end for
        } catch (Exception ex) {
            arg_list.clear();
            ex.printStackTrace();
        }
        return arg_list;
    }

    private static void checkDuplication(FileCompare.CompareOption op, TreeMap<FileCompare.CompareOption, String> arg_list) {
        if (arg_list.containsKey(op)) {
            throw new RuntimeException("Duplicate options: [" + op + "]");
        }
        
        FileCompare.CompareOption[] singular_set = {
            FileCompare.CompareOption.COMPARE_COMMENTS, 
            FileCompare.CompareOption.COMPARE_MSGCTX,
            FileCompare.CompareOption.COMPARE_MSGID,
            FileCompare.CompareOption.COMPARE_MSGSTR
        };
        
        
        int occurence_count=0;
        for (FileCompare.CompareOption opt : singular_set) {
            boolean is_there = (arg_list.containsKey(opt));
            if (is_there) 
                occurence_count++;
        }//end for
        if (occurence_count > 1){
            throw new RuntimeException("Option should not occure more than once. Confusing!");
        }//end if
    }

    private static void checkFileSanity(String file_path, boolean is_check_parent_path) {
        //System.out.println("In checkFileSanity");
        if (file_path == null || file_path.trim().isEmpty()){
            throw new RuntimeException("Cannot have NULL/empty file.");
        }
        
        //System.out.println("File is not null/empty [" + file_path + "]");
        boolean is_accessible = false;        
        File f = new File(file_path);
        if (is_check_parent_path) {
            file_path = f.getParent();
            f = new File(file_path);
            is_accessible = (f.canRead() && f.canWrite() && f.canExecute());
            if (!is_accessible) {
                throw new RuntimeException("Directory for output file is INACCESSIBLE by you: [" + f.getAbsolutePath() + "]");
            }
            //System.out.println("Parent directory is accessible [" + file_path + "]");
        }else{
            f = new File(file_path);
            is_accessible = (f.isFile() && f.canRead());
            if (!is_accessible) {
                throw new RuntimeException("File is UNREADBLE: [" + f.getAbsolutePath() + "]");
            }
            //System.out.println("File is accessible [" + file_path + "]");
        }
    }

    private static FileCompare setOption(TreeMap<FileCompare.CompareOption, String> hash_arg) {
        FileCompare x = new FileCompare();
        List<FileCompare.CompareOption> op_list = Arrays.asList(FileCompare.CompareOption.values());
        for (FileCompare.CompareOption op : op_list) {
            String value = hash_arg.get(op);
            if (value == null) {
                continue;
            }
            switch (op) {
                case SOURCE_FILE_SET:
                    x.setOrigFile(value);
                    break;
                case TARGET_FILE_SET:
                    x.setMyFile(value);
                    break;
                case MERGE_FILE_SET:
                    x.setOutFile(value);
                    break;
                case DEBUGGING:
                    x.setDebugging(true);
                    break;
                default:
                    switch (op) {
                        case MERGING_FILES:
                        case COMPARE_MSGID:
                        case COMPARE_MSGCTX:
                        case COMPARE_COMMENTS:
                        case COMPARE_MSGSTR:
                            x.setCompareOption(op);
                            x.setComparePattern(FileCompare.patterns[op.ordinal()]);
                            break;
                    }//end switch
            }//end switch
        }//end for
        return x;
    }//end routine
}//end class
