/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import com.htran.CommonUtils.BlockList;
import com.htran.CommonUtils.Common;
import com.htran.CommonUtils.DocumentBase;
import com.htran.CommonUtils.FileIO;
import com.htran.Comparators.MSGIDFlatTextComparator;
import java.io.File;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
//import org.apache.commons.codec.digest.DigestUtils;

/**
 *
 * @author htran
 */
public class Document extends ArrayList<TextBlock> implements DocumentBase {

    /**
     * @return the dirty
     */
    public boolean isDirty() {
        return dirty;
    }

    /**
     * @param dirty the dirty to set
     */
    public void setDirty(boolean dirty) {
        this.dirty = dirty;
    }
    private boolean dirty=false;

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
     * @return the po_path
     */
    public Path getPoPath() {
        return po_path;
    }

    /**
     * @param po_path the po_path to set
     */
    public void setPoPath(Path po_path) {
        this.po_path = po_path;
    }

    public String path = null;
    public Path po_path = null;

    /**
     * Absolute path is required
     *
     * @param path
     */
    public Document(String path) {
        this.path = path;
        File f = new File(this.getPath());
        po_path = f.toPath();
    }

    /**
     * Absolute path is required
     *
     * @param path
     */
    public Document(Path path) {
        this.po_path = path;
        this.path = po_path.toString();
    }

    public void LoadDocument(boolean is_flat) {
        try {
            List<String> lines = FileIO.getInstance().readFile(this.po_path);

            BlockList blk_list = new BlockList(lines);
            blk_list.toBlocks();

            int documentCurrentLine = 0;
            for (Object blk : blk_list) {
                List<String> block_text = (List<String>) blk;
                TextBlock txt_blk = new TextBlock(block_text, documentCurrentLine);
                txt_blk.setDocument(this);
                txt_blk.setTextBlock(txt_blk);
                txt_blk.parseBlock();
                //System.out.println("txt_blk: " + txt_blk.toString());
                if (is_flat) {
                    txt_blk.setFlatText();
                }

                this.add(txt_blk);
                int block_size = block_text.size() + 1; //add one for space
                documentCurrentLine += block_size;
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        setDocument(this);
    }//end loadDocument

    public void setFlat() {
        for (TextBlock blk : this) {
            blk.setFlatText();
        }//end for
    }//end

    public void SortInMSGIDOrder() {
        try {
            this.sort(MSGIDFlatTextComparator.getInstance());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }//end routine

    public boolean SimpleValidation(Document other) {
        boolean valid = false;
        try {
            valid = (this.size() == other.size());
            if (!valid) {
                throw new RuntimeException("Different in number of blocks, from: " + other.size() + " To:" + this.size() + "\n");
            }

            //MesssageDigest md = null;
/*
            valid = this.CompageMD5Digest(other);
            if (!valid) {
                System.out.println("MD5 digest different: " + this.path + "\n" + other.path);
            }
             */
            for (int i = 0; i < this.size(); i++) {
                TextBlock blk_from = this.get(i);
                TextBlock blk_to = other.get(i);
                String from_elem_list = blk_from.toString();
                String to_elem_list = blk_to.toString();
                valid = (from_elem_list.compareTo(to_elem_list) == 0);
                if (!valid) {
                    throw new RuntimeException("Block elements are different\nFrom:\n" + blk_from.toString() + "\n\nTo:\n" + blk_to.toString() + "\n");
                }
            }//end for
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return valid;
    }//end SimpleValidation
/*
    public String MD5Digest() {
        String md5_digest = null;
        try {
            String path = this.getPath();
            File f = new File(path);
            FileInputStream stream = new FileInputStream(f);
            md5_digest = DigestUtils.md5Hex(stream);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return md5_digest;
    }//end md5Digist

    public boolean CompageMD5Digest(Document other) {
        int compare = -1;
        String md5_this_doc = this.MD5Digest();
        String md5_other_doc = other.MD5Digest();
        try {
            compare = md5_this_doc.compareTo(md5_other_doc);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return (compare == 0);
    }
     */
    /**
     *
     * @return String version, including the filePath
     */
    public String docToString() {
        StringBuilder bld = new StringBuilder();
        bld.append(this.getPath());
        bld.append(Common.NEW_LINE);
        bld.append(Common.sparator_line);
        bld.append(Common.NEW_LINE);
        bld.append(this.toString());
        bld.append(Common.NEW_LINE);
        return bld.toString();
    }//end routine

    @Override
    public String toString() {
        StringBuilder bld = new StringBuilder();
        for (TextBlock block : this) {
            String blk_string = block.toString();
            bld.append(blk_string);
        }//end routine
        return bld.toString();
    }//end routine

    public String toStringExcludeHeader() {
        StringBuilder bld = new StringBuilder();
        for (int i=1; i < this.size(); i++) {
            TextBlock block = this.get(i);
            String blk_string = block.toString();
            bld.append(blk_string);
        }//end routine
        return bld.toString();
    }//end routine

    public boolean isDiff(Document other){
        try{
            String this_text = this.toStringExcludeHeader();
            String other_text = other.toStringExcludeHeader();
            int comp = (this_text.compareTo(other_text));
            return (comp != 0);
        }catch(Exception ex){
            ex.printStackTrace();
            return false;
        }
    }//end routine

    @Override
    public Document getDocument() {
        return this;
    }

    @Override
    public void setDocument(Document doc) {

    }

    @Override
    public TextBlock getTextBlock() {
        return null;
    }

    @Override
    public void setTextBlock(TextBlock txt_block) {

    }
}//end class
