/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.translationpomaven;

import com.htran.CommonUtils.ProcessDocuments;
import com.htran.Events.InsertStaticTranslations;
import com.htran.Events.TransferTranslatedTextFromVIPOToManualDoc;

/**
 *
 * @author htran
 */
public class TranslationPOFiles {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*
        String doc_dir="/home/htran/blender-trans-git/blender-internationalisation/blender_docs/locale/vi/LC_MESSAGES";
        FileIO io = new FileIO();
        List<Path> file_list = io.FileList(doc_dir);
        System.out.println("Number of files: " + file_list.size());

        Path p = file_list.get(0);
        List<String> list = io.readFile(p);


        // TODO code application logic here
        System.out.println("File: " + p.toString() + " read number of lines: " + list.size());
        */

        ProcessDocuments px = new ProcessDocuments();
        try{
            //px.AddActionListener(new TransferOriginalMSGIDOver());
            //px.AddEndActionListener(new OutputStat());
            //px.AddPostActionListener(new CollectingMSGIDForStatFrequency());
            //px.AddEndActionListener(new WriteChangesToFiles());
            px.AddActionListener(new InsertStaticTranslations());
            px.AddActionListener(new TransferTranslatedTextFromVIPOToManualDoc());
            //px.AddPostActionListener(new ListoutFlatText());
            px.Process();
        }catch(Exception ex){
            ex.printStackTrace();
        }
    }



}
