/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import base.Common;
import base.Document;
import com.htran.Comparators.DocumentPathComparator;
import com.htran.Events.ProcessDocAction;
import com.htran.Events.ProcessDocEvent;
import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.TreeSet;

/**
 *
 * @author htran
 */
public class ProcessDocuments {

    TreeSet<Document> left_doc_list = new TreeSet<Document>(new DocumentPathComparator());
    TreeSet<Document> right_doc_list = new TreeSet<Document>(new DocumentPathComparator());

    String left_dir = "/home/htran/tmp/back/blender-trans-git/blender-internationalisation/blender_docs/locale/vi/LC_MESSAGES/";
    String right_dir = "/home/htran/blender_documentations/translation_manual/locale/vi/LC_MESSAGES/";

    static String DOC_DIR = "DOC_DIR";

    String from_path = null;
    String to_path = null;
    String doc_path = null;
    String manual_path = null;
    String system_file_sep = null;
    List<Path> from_po_file_list = null;
    List<Path> to_po_file_list = null;
    //Common common = null;

    Document to_doc_list = null;
    List<ProcessDocAction> actionListenerList = null;
    List<ProcessDocAction> endActionListenerList = null;
    List<ProcessDocAction> beginActionListenerList = null;
    private List<ProcessDocAction> preActionListenerList = null;
    private List<ProcessDocAction> postActionListenerList = null;

    public ProcessDocuments() {
        //common = Common.getInstance();
/*
        //doc_path = System.getenv("DOC_DIR");
        doc_path = "/home/htran/blender-trans-git/blender-internationalisation/blender_docs/locale";
        system_file_sep = File.separator;

        from_path = doc_path + system_file_sep + "en/LC_MESSAGES";
        to_path = doc_path + system_file_sep + "vi/LC_MESSAGES";
         */
        //to_path = Common.doc_dir;
        Common.getInstance();

        actionListenerList = new ArrayList<ProcessDocAction>();
        endActionListenerList = new ArrayList<ProcessDocAction>();
        beginActionListenerList = new ArrayList<ProcessDocAction>();
        preActionListenerList = new ArrayList<ProcessDocAction>();
        postActionListenerList = new ArrayList<ProcessDocAction>();
    }

    public void AddActionListener(ProcessDocAction a) {
        this.actionListenerList.add(a);
    }

    public void RemoveActionListener(ProcessDocAction a) {
        this.actionListenerList.remove(a);
    }

    public void AddEndActionListener(ProcessDocAction a) {
        this.endActionListenerList.add(a);
    }

    public void RemoveEndActionListener(ProcessDocAction a) {
        this.endActionListenerList.remove(a);
    }

    public void AddPreActionListener(ProcessDocAction a) {
        this.preActionListenerList.add(a);
    }

    public void RemovePreActionListener(ProcessDocAction a) {
        this.preActionListenerList.remove(a);
    }

    public void AddPostActionListener(ProcessDocAction a) {
        this.postActionListenerList.add(a);
    }

    public void RemovePostActionListener(ProcessDocAction a) {
        this.postActionListenerList.remove(a);
    }

    public void ProcessActions(Document from, Document to) {
        for (int i = actionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = actionListenerList.get(i);
            ProcessDocEvent e = new ProcessDocEvent(this, i, null);
            e.setFromDocument(from);
            e.setToDocument(to);
            a.actionPerformed(e);
        }//end for
    }//end routine

    public void ProcessPreActions(Document from, Document to) {
        for (int i = preActionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = preActionListenerList.get(i);
            ProcessDocEvent e = new ProcessDocEvent(this, i, null);
            e.setFromDocument(from);
            e.setToDocument(to);
            a.actionPerformed(e);
        }//end for
    }//end routine

    public void ProcessPostActions(Document from, Document to) {
        for (int i = postActionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = postActionListenerList.get(i);
            ProcessDocEvent e = new ProcessDocEvent(this, i, null);
            e.setFromDocument(from);
            e.setToDocument(to);
            a.actionPerformed(e);
        }//end for
    }//end routine

    public void ProcessEndActions() {
        for (int i = endActionListenerList.size() - 1; i >= 0; i--) {
            ProcessDocAction a = endActionListenerList.get(i);
            ProcessDocEvent e = new ProcessDocEvent(this, i, null);
            e.setFromDocument(null);
            e.setToDocument(null);
            a.actionPerformed(e);
        }//end for
    }//end routine

    private boolean isDocumentLoaded(TreeSet<Document> list, Path path_to_find) {
        Document d = new Document(path_to_find);
        boolean is_there = list.contains(d);
        return (is_there);
    }//end routine

    private boolean isDocumentLoaded(TreeSet<Document> list, Document doc) {
        boolean is_there = list.contains(doc);
        return (is_there);
    }//end routine

    private Document searchTree(TreeSet<Document> list, Path path_to_find) {
        Document d = new Document(path_to_find);
        Document ceil = list.ceiling(d);
        Document floor = list.floor(d);
        Document result = (ceil == floor ? ceil : null);
        return result;
    }//end routine

    private Document getRightDoc(Path r_path, Document left_doc) {
        Path left_path = left_doc.getPoPath();
        int left_index = left_dir.length();
        String common_part = left_path.toString().substring(left_index);
        Path right_path = Paths.get(r_path.toString(), common_part);
        File right_file = right_path.toFile();
        if (!right_file.exists()) {
            System.out.println("Could not find: " + right_path);
            return null;
        }

        Document right_doc = null;
        right_doc = new Document(right_path);
        right_doc.LoadDocument(false);

        return right_doc;
    }//end routine

    public void Process() throws Exception {

        Document vipo_doc = new Document(Common.vi_po_file);
        //Document vipo_doc = new Document(Common.test_file);
        vipo_doc.LoadDocument(true);
        //Common.LOGGER.info(vipo_doc.toString());
/*
        File r_file = new File(right_dir);
        Path r_path = r_file.toPath();
*/
        POFileList from_po_file_list = new POFileList(Common.vi_manual_dir);

/*
        POFileList from_po_file_list = new POFileList(left_dir);
*/
        from_po_file_list.GetFileList();
        Collections.sort(from_po_file_list);
        int count = 0;
        //Common.LOGGER.info(from_po_file_list.toString());
        for (Path left_path : from_po_file_list) {
            Document left_doc, right_doc;

            left_doc = new Document(left_path);
            left_doc.LoadDocument(false);

            right_doc = this.getRightDoc(r_path, left_doc);

            boolean is_diff = left_doc.isDiff(right_doc);
            if (is_diff) {
                left_doc_list.add(left_doc);
                right_doc_list.add(right_doc);
            }//end if

            ProcessPreActions(left_doc, right_doc);
        }//end for

        for (Document left_doc : left_doc_list) {
            Document right_doc = this.getRightDoc(r_path, left_doc);
            ProcessActions(left_doc, right_doc);
            //Common.LOGGER.info(man_doc.getPath().toString());
            //Common.LOGGER.info("--------------------");
            //Common.LOGGER.info("Document after changes:\n" + man_doc.toString());

            //Common.LOGGER.info("=================");
            //Common.LOGGER.info(man_doc.toString());
            //Common.LOGGER.info("=================");
        }//end for

        for (Document left_doc : left_doc_list) {
            Document right_doc = this.getRightDoc(r_path, left_doc);
            ProcessPostActions(left_doc, right_doc);
        }//end for
        ProcessEndActions();
    }//end routine
/*
    public void Process() throws Exception {
        POFileList from_po_file_list = new POFileList(from_path);
        from_po_file_list.GetFileList();

        POFileList to_po_file_list = new POFileList(to_path);
        to_po_file_list.GetFileList();

        for (Path from_path : from_po_file_list) {
            Document from_doc = new Document(from_path);
            from_doc.LoadDocument(false);

            Path relative_file = from_po_file_list.RelativePath(from_path);
            Path to_path = to_po_file_list.FindSubPath(relative_file);
            //there might be new files added
            if (to_path == null){
                continue;
            }//end if
            Document to_doc = new Document(to_path);
            to_doc.LoadDocument(false);


            ProcessActions(from_doc, to_doc);
        }//end for
    }//end routine
     */

    /**
     * @return the endActionListenerList
     */
    public List<ProcessDocAction> getEndActionListenerList() {
        return endActionListenerList;
    }

    /**
     * @param endActionListenerList the endActionListenerList to set
     */
    public void setEndActionListenerList(List<ProcessDocAction> endActionListenerList) {
        this.endActionListenerList = endActionListenerList;
    }

    /**
     * @return the beginActionListenerList
     */
    public List<ProcessDocAction> getBeginActionListenerList() {
        return beginActionListenerList;
    }

    /**
     * @param beginActionListenerList the beginActionListenerList to set
     */
    public void setBeginActionListenerList(List<ProcessDocAction> beginActionListenerList) {
        this.beginActionListenerList = beginActionListenerList;
    }

    /**
     * @return the preActionListenerList
     */
    public List<ProcessDocAction> getPreActionListenerList() {
        return preActionListenerList;
    }

    /**
     * @param preActionListenerList the preActionListenerList to set
     */
    public void setPreActionListenerList(List<ProcessDocAction> preActionListenerList) {
        this.preActionListenerList = preActionListenerList;
    }

    /**
     * @return the postActionListenerList
     */
    public List<ProcessDocAction> getPostActionListenerList() {
        return postActionListenerList;
    }

    /**
     * @param postActionListenerList the postActionListenerList to set
     */
    public void setPostActionListenerList(List<ProcessDocAction> postActionListenerList) {
        this.postActionListenerList = postActionListenerList;
    }
}//end class
