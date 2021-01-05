/*
 * OCRAction.java
 *
 * Created on 20-May-2009, 19:26:57
 */

/*
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
 * 
 * This file is part of Jubler.
 * 
 * Jubler is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 2.
 * 
 * 
 * Jubler is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with Jubler; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 * 
 * Contributor(s):
 * 
 */
package com.panayotis.jubler.events.menu.tool.ocr;

import static com.panayotis.jubler.subs.CommonDef.FILE_SEP;
import com.panayotis.jubler.Jubler;
import com.panayotis.jubler.MenuAction;
import com.panayotis.jubler.options.gui.ProgressBar;
import com.panayotis.jubler.os.DEBUG;
import com.panayotis.jubler.subs.Share;
import com.panayotis.jubler.subs.SubEntry;
import com.panayotis.jubler.subs.Subtitles;
import com.panayotis.jubler.subs.loader.ImageTypeSubtitle;
import com.panayotis.jubler.tools.JImage;
import static com.panayotis.jubler.i18n.I18N._;
import com.panayotis.jubler.os.FileCommunicator;
import com.panayotis.jubler.os.SystemDependent;
import com.panayotis.jubler.os.TreeWalker;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.logging.Level;
import javax.swing.JTable;

/**
 * This class performs the OCR action. It runs throught the list of subtitle
 * entries that contain image files and can carry out two actions: <ol> <li>
 * Perform OCR on the original image file of the subtitle entry without any
 * conversions.</li> <li> Perform OCR on an image provided in the
 * subtitle-entry. This image is converted to a B/W image to improve the OCR
 * result.</li> </ol> The options are carried out under the control of the uses
 * the image's filename to write a temporary image in TIFF format to the
 * system's temp directory. It then call the JOCR's recognizeText method to
 * recognise text. The result text is set in the instance of sub-entry. It must
 * know the references of: <ol> <li> Jubler instance currently running, from
 * which it can get the list of subtitles loaded and the table, from where it
 * knows the table's selection.</li> <li> The 'tesseract' executable path.</li>
 * <li> The 3 character code of language where OCR opeation will be based on.
 * </li> <li> The setting of ocrAllList is true when all items from the subtitle
 * list are to be OCR(ed) and false when only the selected items are to be
 * done.</li> </ol>
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 */
public class OCRAction extends MenuAction {

    private String language;
    private boolean ocrAllList = false;
    private boolean usingOriginalImage = false;
    private JTable subTable = null;
    private Subtitles subs = null;
    private int len = 0;
    private int row_count = 0;
    private int selected_row = -1;
    private File workedTessPath = null;
    private File workedTessDataPath = null;
    /**
     * Perform default construction with the addition of setting reference for
     * the {@link Jubler} parent.
     *
     * @param jublerParent The reference to {@link Jubler} running instance.
     */
    public OCRAction(Jubler jublerParent) {
        this.jublerParent = jublerParent;
    }

    /**
     * Carry out the OCR action. It first ask the user to select a language from
     * the available list. The list is drawn by an instance of
     * {@link LanguageSelection}. If a language is selected, a 3 language code
     * is returned and is put towards the OCR thread. There are two ways that
     * the OCR engine can work. <ol> <li>All loaded images are converted to B/W
     * images, written to a temporary file and let the external OCR engine to
     * recognise it. Experiences shown that the B/W images help the OCR egine to
     * produce much better results than the coloured images. The OCR operation
     * will remove the temporary files after it has completed the operation.
     * </li> <li>All original image files are used in the conversion. In this
     * scenario, there are no temporary files produced. The original file is
     * fetch into the external OCR program and the result is returned. </li>
     * </ol>
     *
     * The presence of two methods allows users to compare results and chose it
     * for themselves which method is preferred.
     *
     * To qualify for the OCR, subtitle-entries must implements
     * {@link ImageTypeSubtitle} interface and implemented all its methods.
     *
     * @param evt Event argument
     */
    public void actionPerformed(java.awt.event.ActionEvent evt) {
        try {
            boolean ok = locateTesseractExecutable();
            ok = locateTesseractOCRLanguageData();

            subTable = jublerParent.getSubTable();
            subs = jublerParent.getSubtitles();
            row_count = subTable.getSelectedRowCount();
            len = (isOcrAllList() ? subs.size() : row_count);

            selected_row = subTable.getSelectedRow();

            LanguageSelection lang_sel = new LanguageSelection(jublerParent, workedTessDataPath.getAbsolutePath());

            language = lang_sel.showDialog();
            if (language == null) {
                return;
            }

            Thread ocr_thread = new Thread() {

                @Override
                public void run() {
                    boolean is_image = false;
                    boolean has_image = true;
                    int[] selected;
                    int row;
                    SubEntry sub;
                    ImageTypeSubtitle img_sub;
                    BufferedImage image = null;

                    ProgressBar pb = new ProgressBar();
                    pb.setMinValue(0);
                    pb.setMaxValue(len - 1);
                    pb.on();

                    try {
                        for (int i = 0; i < len; i++) {

                            if (isOcrAllList()) {
                                row = i;
                            } else {
                                selected = subTable.getSelectedRows();
                                row = selected[i];
                            }//end if/else;

                            sub = subs.elementAt(row);

                            is_image = (sub instanceof ImageTypeSubtitle);
                            if (!is_image) {
                                continue;
                            }

                            img_sub = (ImageTypeSubtitle) sub;
                            image = img_sub.getImage();
                            has_image = !(Share.isEmpty(image));
                            if (!has_image) {
                                continue;
                            }

                            File imageFile = img_sub.getImageFile();
                            usingOriginalImage = (imageFile != null);

                            String result = null;
                            String msg = _("OCR:");
                            
                            JOCR ocrEngine = new JOCR(workedTessPath.getAbsolutePath());
                            if (usingOriginalImage) {
                                msg += img_sub.getImageFile().getName();
                                imageFile = img_sub.getImageFile();
                                result = ocrEngine.ocrUsingOriginalImage(imageFile, language);
                            } else {
                                imageFile = JImage.bwConversionToBMPTempFile(image);
                                result = ocrEngine.ocrUsingTempFile(imageFile, language);
                            }//end if

                            pb.setTitle(msg);
                            pb.setValue(i);

                            sub.setText(result.trim());
                            subs.fireTableRowsUpdated(row, row);

                            if (row == selected_row) {
                                jublerParent.getSubeditor().setData(sub);
                            }//end if
                        }//end for(int i=0; i < len; i++)                        
                    } catch (Exception e) {
                        DEBUG.logger.log(Level.WARNING, e.toString());
                    } finally {
                        pb.off();
                    }
                }
            };

            ocr_thread.start();

        } catch (Exception ex) {
            DEBUG.logger.log(Level.WARNING, ex.toString());
        }//end try/catch
    }//public void actionPerformed(java.awt.event.ActionEvent evt)
    private static final String TESSDATA = "TESSDATA_PREFIX";

    private boolean locateTesseractOCRLanguageData() throws Exception {
        boolean ok = false;
        if (! Share.isEmpty(workedTessDataPath)){
            ok = (workedTessDataPath.isDirectory())
                && (workedTessDataPath.canRead());
        }//end if
        
        if (!ok) {
            String err_msg = null;
            String tessDataPath = System.getenv(TESSDATA);
            ok = (!Share.isEmpty(tessDataPath));
            if (ok) {
                workedTessDataPath = new File(tessDataPath);
                ok =    workedTessDataPath.exists() && 
                        workedTessDataPath.isDirectory() && 
                        workedTessDataPath.canRead();
                if (!ok) {
                    err_msg = _("System's environment variable \'" + TESSDATA + "\' is set but the path is inaccessible.");
                }
            } else {
                err_msg = _("System's environment variable \'" + TESSDATA + "\' is NOT set. Unable to locate language data for OCR process.");
            }
            if (ok) {
                DEBUG.logger.log(Level.WARNING, TESSDATA + "=" + this.workedTessDataPath);
            } else {
                workedTessDataPath = null;
                throw new RuntimeException(err_msg);
            }
        }
        return ok;
    }
    private static final String TESSERACT_EXE = "tesseract";

    private boolean locateTesseractExecutable() throws Exception {
        boolean ok = false;
        if (! Share.isEmpty(workedTessPath)){
            ok = (workedTessPath.exists() && workedTessPath.canExecute());
        }//end if
        
        if (! ok) {
            String working_dir = FileCommunicator.getCurrentPath();
            workedTessPath = new File(working_dir, "tesseract" + FILE_SEP + TESSERACT_EXE  + SystemDependent.PROG_EXT);

            ok = workedTessPath.exists() && workedTessPath.canExecute();
            if (!ok) {
                workedTessPath = TreeWalker.searchExecutable(
                        TESSERACT_EXE,
                        null,
                        "imagename outputbase",
                        workedTessPath.getAbsolutePath());
                ok = (!Share.isEmpty(workedTessPath));
            }//end if (!ok)

            if (ok) {
                DEBUG.logger.log(Level.WARNING, "tesseract is found in:  " + workedTessPath);
            } else {
                workedTessPath = null;
                throw new RuntimeException(_("Unable to find executable program \'tesseract\'"));
            }
        }
        return ok;
    }

    /**
     * Gets the 3 characters language code
     *
     * @return The 3 digit language code or null if it has not been set.
     */
    public String getLanguage() {
        return language;
    }

    /**
     * Sets the 3 characters language code.
     *
     * @param language The 3 characters language code.
     */
    public void setLanguage(String language) {
        this.language = language;
    }

    /**
     * Checks to see if OCR action is to perform on the whole list of subtitle
     * images or not.
     *
     * @return true if the OCR operation is to perform on the whole list, false
     * if only the currently selected ones are to be OCR(ed).
     */
    public boolean isOcrAllList() {
        return ocrAllList;
    }

    /**
     * Sets the flag to indicate that OCR action will be performed on the whole
     * list of subtitle images or not.
     *
     * @param ocrAllList true if the OCR operation is to perform on the whole
     * list, false if only the currently selected ones are to be OCR(ed).
     */
    public void setOcrAllList(boolean ocrAllList) {
        this.ocrAllList = ocrAllList;
    }

    /**
     * Checks to see if OCR action will be performed on the original image files
     * instead of the trimmed-down and b/w converted images.
     *
     * @return True if the original image files are used, false if the b/w
     * version of loaded images are used.
     */
    public boolean isUsingOriginalImage() {
        return usingOriginalImage;
    }//end public boolean isUsingOriginalImage()

    /**
     * Sets the flag to indicate whether OCR action will be performed on the
     * original image files or on the b/w converted images.
     *
     * @param usingOriginalImage
     */
    public void setUsingOriginalImage(boolean usingOriginalImage) {
        this.usingOriginalImage = usingOriginalImage;
    }//end public void setUsingOriginalImage(boolean usingOriginalImage) 
}//end public class OCRAction extends MenuAction
