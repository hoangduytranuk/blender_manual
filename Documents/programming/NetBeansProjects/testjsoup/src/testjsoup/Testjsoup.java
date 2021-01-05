/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package testjsoup;

import java.io.File;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@googlemail.com>
 */
public class Testjsoup {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        String html="<html><head><title>First parse</title></head>"
                + "<body><p>Parsed HTML into a doc.</p></body></html>";
        String html_file="/home/htran/blender_documentations/blender_docs/build/rstdoc/advanced/command_line/arguments.html";
        File input_file = new File(html_file);
        try{
            Document doc = Jsoup.parse(input_file, null);
            
            doc.select("paragraph").forEach(System.out::println);
            
////Document doc = Jsoup.parse(html);
//            Elements body = doc.getElementsByTag("title");
//            for (Element e : body) {
//                System.out.println(e.html());
//                String text = e.text();
//                System.out.println(text);
//            }//end for
        }catch(Exception e){
            e.printStackTrace();
        }//end try/catch
        
    }//end main    
}//end class
