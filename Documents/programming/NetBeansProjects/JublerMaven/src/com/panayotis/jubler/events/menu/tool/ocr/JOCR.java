/**
 * Copyright @ 2008 Quan Nguyen
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package com.panayotis.jubler.events.menu.tool.ocr;

import static com.panayotis.jubler.i18n.I18N._;
import com.panayotis.jubler.os.DEBUG;
import com.panayotis.jubler.os.RuntimeProcessStreamReader;
import com.panayotis.jubler.subs.CommonDef;
import com.panayotis.jubler.subs.Share;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import static com.panayotis.jubler.subs.CommonDef.NL;

/**
 *
 * @author Quan Nguyen (nguyenq@users.sf.net) && Hoang Duy Tran
 */
public class JOCR implements CommonDef {

    private static final String CMD_LANGUAGE_OPTION = "-l";
    private static final String TESS_OUT_FILE = "JublerTessOutput";
    private static final String TESS_OUT_EXT = ".txt";
    private static String TEMP_IMG_FILE = "tmp";
    private String tesseract_path = null;

    /**
     * Creates a new instance of OCR
     */
    public JOCR(String tesseract_path) {
        this.tesseract_path = tesseract_path;
    }

    public String ocrUsingOriginalImage(File imageFile, String language_code) throws Exception {
        File[] f_list = new File[1];
        f_list[0] = imageFile;
        return performOCR(f_list, language_code, false);
    }

    public String ocrUsingTempFile(File tempImageFile, String language_code) throws Exception {
        File[] f_list = new File[1];
        f_list[0] = tempImageFile;
        return performOCR(f_list, language_code, true);
    }//end public String recognizeText(final File tempImageFile, final String language_code) throws Exception 

    public String performOCR(File[] imgFiles, String language_code, boolean remove_image_file) throws Exception {
        RuntimeProcessStreamReader ins = null, ers = null;
        BufferedReader in = null;
        File tessOutTempFile = File.createTempFile(TESS_OUT_FILE, TESS_OUT_EXT);
        StringBuffer output_str_buffer = new StringBuffer();
        File temp_img_file = null;
        try {
            String tess_output_file_name = Share.getFileNameWithoutExtension(tessOutTempFile);
            List<String> system_command = new ArrayList<String>();
            system_command.add(tesseract_path);
            system_command.add(""); // this is the slot for inputfile, which will be filed later.
            system_command.add(tess_output_file_name);
            system_command.add(CMD_LANGUAGE_OPTION);
            system_command.add(language_code);

            //new instance of the process builder
            ProcessBuilder process_bld = new ProcessBuilder();

            //set the process's directory using the working directory, ie. Jubler's dir.
            process_bld.directory(new File(USER_CURRENT_DIR));


            //Run throught the image list.
            for (File imgFile : imgFiles) {
                //prepare to change image's filename to something without spaces
                //and rename the image file to it.
                String ext = Share.getFileExtension(imgFile);
                String temp_img_filename = TEMP_IMG_FILE + ext;
                temp_img_file = new File(imgFile.getParentFile(), temp_img_filename);

                Share.CopyFile(imgFile, temp_img_file);

                // DEBUG.debug("Change " + imgFile.getAbsolutePath() + " to " + temp_img_file.getAbsolutePath());

                //fillin the input file as the data is now available.
                system_command.set(1, temp_img_file.getPath());

                DEBUG.logger.log(Level.INFO, "OCR command: " + system_command);

                //now set the command to be executed.
                process_bld.command(system_command);

                //redirect the error stream (3) to standard output (1).
                //process_bld.redirectErrorStream(true);



                //Start the process, execute the command line.
                Process process = process_bld.start();
                InputStream inp = process.getInputStream();
                InputStream erp = process.getErrorStream();

                try {
                    ins = new RuntimeProcessStreamReader("stdin", inp);
                    ins.start();
                } catch (Exception e) {
                    ins = null;
                }

                try {
                    ers = new RuntimeProcessStreamReader("stderr", erp);
                    ers.start();
                } catch (Exception e) {
                    ins = null;
                }

                int process_returned_value = process.waitFor();

                DEBUG.logger.log(Level.INFO, _("OCR program returned value: ") + process_returned_value + NL);

                if (remove_image_file) {
                    imgFile.delete();
                }//end if (remove_image_file)


                if (process_returned_value == 0) {
                    in = new BufferedReader(new InputStreamReader(new FileInputStream(tessOutTempFile), "UTF-8"));
                    String str;
                    while ((str = in.readLine()) != null) {
                        output_str_buffer.append(str).append(EOL);
                    }
                } else {
                    StringBuilder bd = new StringBuilder();
                    //String msg = null; //_("OCR program returned value: ") + process_returned_value + NL;
                    //bd.append(msg);

                    String msg = _("Image File: ") + imgFile.getName() + NL;
                    bd.append(msg);

                    if (!Share.isEmpty(ins)) {
                        bd.append(ins.getLine());
                    }
                    if (!Share.isEmpty(ers)) {
                        bd.append(ers.getLine());
                    }

                    String error_msg;
                    switch (process_returned_value) {
                        case 1:
                            error_msg = _("There are errors in accessing image files.");
                            break;
                        case 29:
                            error_msg = _("OCR engine cannot recognize the image.");
                            break;
                        case 31:
                            error_msg = _("Unsupported image format is detected.");
                            break;
                        default:
                            error_msg = _("Some unforeseen errors occurred.");
                    }//end switch (process_returned_value) 
                    bd.append(error_msg);
                    DEBUG.logger.log(Level.WARNING, bd.toString());
                    throw new RuntimeException(bd.toString());
                }//end if (process_returned_value == 0) { / else
            }//end for (File imgFile : imgFiles)
        } catch (Exception ex) {
            throw ex;
        } finally {
            try {
                in.close();
            } catch (Exception e) {
            }
            if (remove_image_file) {
                for (File image : imgFiles) {
                    try {
                        image.delete();
                    } catch (Exception e) {
                    }
                }//for (File image : imgFiles)
            }//end if (remove_image_file)
            try {
                temp_img_file.delete();
            } catch (Exception e) {
            }
            try {
                tessOutTempFile.delete();
            } catch (Exception e) {
            }
            return output_str_buffer.toString();
        }
    }//end public String performOCR(File[] imgFiles, String language_code, boolean remove_image_file) throws Exception
}
