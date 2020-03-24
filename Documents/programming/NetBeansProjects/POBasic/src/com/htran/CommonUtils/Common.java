/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.htran.CommonUtils;

import java.io.IOException;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;
import java.util.function.BiConsumer;
import java.util.logging.FileHandler;
import java.util.logging.Logger;


/**
 *
 * @author Hoang Duy Tran <hoangduytran1960@gmail.com>
 */
public class Common {

    //public static String COMMENT = "#";
    public static String COMMENT="#";
    public static String MSGID="msgid";
    public static String MSGCTXT="msgctxt";
    public static String MSGSTR="msgstr";
    public static String SPACE=" ";
    public static String QUOTE="\"";
    public static String NEWLINE =  System.lineSeparator();
    public static String FUZZY="#, fuzzy";
    public static String DOT=".";
    public static String COLLON=":";
    public static String DASH="-";
    public static String PO_EXT=".po";
    public static String RST_EXT=".rst";
    public static String COMMENTED_LINE= "#~";
    public static String KEYBOARD=":kbd:";
    public static String B_SLASH="\\";
    public static String PERCENTAGE="%";
    public static String STAR="*";
    public static String BLEND_FILE=".blend";
    public static String COLON=":";
    public static String TODO_LOWER="\btodo\b";
    public static String TODO_TRANSLATED="Nội dung cần viết thêm";

    public static String RE_COMMENTED_LINE = "^#~";
    public static String RE_COMMENT="^#";
    public static String RE_COMMENT_UNUSED="#~";
    public static String RE_MSGID="^msgid";
    public static String RE_MSGCTXT="^msgctxt";
    public static String RE_MSGSTR="^msgstr";
    public static String RE_EMPTYSTR="";
    public static String RE_TWO_MORE_RETURN="\n\n";
    public static String RE_ONE_RETURN="\n";
    public static String RE_LEADING_SPACES = "^[\ |\t]+?";
    public static String RE_RST_UNDERLINED = "^[\#|*|=|\-|^|\"]+?$";
    public static String RE_RST_SPECIAL = "^[\.|:|`|\#]+?";
    public static String RE_IS_ALPHA = "^[A-Za-z]+.*$";
    public static String RE_LEADING_HYPHENS="^(-- ).*$";
    public static String RE_ENDING_DOT="^(.*?)\.$";
    public static String RE_KEYBOARD="(:kbd:`)(.*?)(`)";
    public static String RE_NUMBER="\d+";
    public static String RE_BRACKET=r"[\(\[\{]+";
    public static String RE_XXX=r".*X{3}.*";
    public static String RE_DOTDOT=r".*\.\..*";
    public static String RE_HYPHEN=r".*\-.*";
    public static String RE_XRAY=r".*X-Ray.*";
    public static String RE_DD=r".*([23][Dd]).*";
    public static String RE_REF=":ref:";
    public static String RE_MENU=":menuselection:";
    public static String RE_URL="http";
    public static String RE_MOUSE_BUTTON="[(RMB)+|(LMB)+|(MMB)+]";
    public static String RE_DOC=":doc:";
    public static String RE_TODO=r"(\btodo\b)";
    public static String RE_QUOTED_WELL=r"^\"(.*)\"$";
    public static String RE_QUOTED_STRING = "(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)";
    public static String QUOTED_STRING_RE = re.compile(r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")

    public static String[] RST_HEADER=["#", "*", "=", "-", "^", "\""];

    end_char_list=set(['.','!',')', ',', '>', ':','*','`',])
    COMMENT_FLAG="#: "
    LANGUAGE_SEPARATOR=" -- "

    ignore_list=[
        "OBJ","PLY","STL","SVG","Web3D","Linux",
        "Apple macOS","Microsoft Windows",
        "OpenVDB","Alembic","Collada","OpenGL","CUDA","OpenCL","BSDF","Alpha","iTaSC",
        "Tab","PYTHONPATH","Python","Blender", "Arch Linux", "Redhat/Fedora", 
        "Gamma", "RGB", "X", "Y", "Z", "XYZ", "Alpha", "X, Y", "Debian/Ubuntu", "UVs",
        "NURBS", "UV", "H.264", "MPEG", "Xvid", "QuickTime", "Ogg Theora", "X/Y",
        "AVI Jpeg", "OpenEXR", "Bézier", "Euler", "Verlet", "RK4", "CUDA", "OpenMP", "MS-Windows",
        "macOS", "Sigma", "X, Y, Z", "2D", "Nabla", "Musgrave", "Stucci", "Voronoi", "Lennard-Jones",
        "B-Spline", "CPU", "BSSRDF", "Boolean", "OpenSubdiv", "Nabla", "Python", "Blender", "PYTHONPATH",
        "MS-Windows", "YCbCr", "Catmull-Clark", "Blosc", "Zip", "OpenAL", "GLSL", "SDL", "Mono"
        "GGX", "Christensen-Burley", "Blackman-Harris", "Sobol", "DOF", "FSAA", "HDRI", "MIS", "NURBS",
        "glTF 2.0", "Catmull-Rom", "Mitch", "Laplace", "Sobel", "Prewitt", "Kirsch", "Doppler", 
        "Alpha :kbd:`Ctrl-H`", "VD16", "HSV/HSL", "Mono", "GGX", "RRT", "Windows", "Laptops",
        "bpy.context", "bpy.data", "bpy.ops"
    ]


    COMMON_KEYS = ["ctrl", "alt", "windows", "tab", "shift", "spacebar", "enter", "delete", "pgup", "pageup",
                   "pgdown", "pagedown", "end", "esc", "return","backspace", "home", 
                   "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]

    ALPHABET = r"(\w){1}"

    # , ""
    ignore_start_with_list = [
        "bpy", "def", "bpy", "def", "for", "while", "print", "if", "bl_info", "class", "return", "paths", "dx"
    ]
    RE_NONTRANS="^([\ |\t]?-- ).*$"
    RE_KEYBOARD=r"(:kbd:`)(.*?)(`)"

    public Common() {
        FileHandler fh;
        try {

            // This block configure the logger with handler and formatter  
            fh = new FileHandler(logger_file_path);
            LOGGER.addHandler(fh);
            //SimpleFormatter formatter = new SimpleFormatter();
            //fh.setFormatter(formatter);

            // the following statement is used to log any messages  
            Calendar today = Calendar.getInstance();
            /*            
            today.clear(Calendar.HOUR);
            today.clear(Calendar.MINUTE);
            today.clear(Calendar.SECOND);
             */
            Date todayDate = today.getTime();
            /*
            String zone_diff = ZoneId.of("Europe/London") // Specify a time zone.
                    .getRules() // Get the object representing the rules for all the past, present, and future changes in offset used by the people in the region of that zone.
                    .getOffset(Instant.now()) // Get a `ZoneOffset` object representing the number of hours, minutes, and seconds displaced from UTC. Here we ask for the offset in effect right now.
                    .toString();
             */
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mmZ");
            timeNow = sdf.format(todayDate);
            //zone_diff = zone_diff.replace(":", "");
            //timeNow += zone_diff;

//            LOGGER.info(timeNow);

            this.LoadDict();

            changed_list = new ArrayList<>();

        } catch (SecurityException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static Common getInstance() {
        if (instance == null) {
            instance = new Common();
        }
        return instance;
    }

    public static void PrintDocumentPath(){
        if (current_doc == last_doc)
            return;
        
        if (! doc_path_printed){
            System.out.println("File: " + Common.current_doc.getPath() + "\n" + Common.sparator_line);
            doc_path_printed = true;
        }//end if
    }//end routine
    
    public void LoadDict() {
        boolean is_empty = false;
        Common.dict = FileIO.getInstance().LoadPropertiesFromXML(Common.dictionaryPath);
        is_empty = Common.dict.isEmpty();
        if (!is_empty) {
            dict_map = sortingDict();
            LOGGER.info("Properties are LOADED OK!\n" + dict_map.toString());
            LOGGER.info("OK!");
        } else {
            dict_map = loadingDefaultList();
            Common.dict.clear();
            Common.dict = this.mapToProperties(dict_map);
            LOGGER.info("Properties are NOT LOADED (possibly there are errors in the XML file dictionary.properties. CHECK! Using default internal list.");
            //FileIO.getInstance().WritePropertiesAsXML(Common.dictionaryPath, Common.dict);
        }//end if
    }//end routine

    public TreeMap<String, String> loadingDefaultList() {
        TreeMap<String, String> map = new TreeMap<>(BasicTextNoneCaseComparator.getInstance());
        for (String elem[] : Common.msg_list) {
            String pattern = elem[0];
            String repl = elem[1];
            map.put(pattern, repl);
        }//end while
        return map;
    }//end routine

    public TreeMap<String, String> sortingDict() {
        TreeMap<String, String> map = new TreeMap<>(BasicTextNoneCaseComparator.getInstance());
        Common.dict.forEach(new BiConsumer<Object, Object>() {
            public void accept(Object key, Object value) {
                String pattern = (String) key;
                String repl = (String) value;
                map.put(pattern, repl);
            }//end routine
        });
        return map;
    }//end routine

    public Properties mapToProperties(Map<String, String> map) {
        Properties p = new Properties();
        Set<Map.Entry<String, String>> set = map.entrySet();
        for (Map.Entry<String, String> entry : set) {
            p.put(entry.getKey(), entry.getValue());
//            LOGGER.info("putting key:" + entry.getKey() + " value:" + entry.getValue());
//            LOGGER.info("p sofar:\n" + p.toString());
        }
        return p;
    }//end routine

    public Map<String, String> propertiesToMap(Properties props) {
        HashMap<String, String> hm = new HashMap<String, String>();
        Enumeration<Object> e = props.keys();
        while (e.hasMoreElements()) {
            String s = (String) e.nextElement();
            hm.put(s, props.getProperty(s));
        }
        return hm;
    }
    /*
    public static boolean textContain(String text, String find_pattern) {
        find_pattern = "FIRST AUTHOR";

        Pattern p = Pattern.compile(find_pattern, Pattern.DOTALL | Pattern.MULTILINE);
        LOGGER.info("Pattern p: [" + p + "] find_pattern: [" + find_pattern + "]\n");
        Matcher m = p.matcher(text);
        LOGGER.info("matcher: [" + m + "] for text: [" + text + "]\n");
        boolean is_contain = (m.matches());

        boolean text_is_contain = text.contains(find_pattern);
        if (is_contain) {
            LOGGER.info("textContain - find_pattern: [" + find_pattern + "] m: [" + m + "]\n");
        }else if (text_is_contain){
            LOGGER.info("text_is_contain - find_pattern: [" + find_pattern + "] m: [" + text + "]\n");
        }else{
            LOGGER.info("UNFOUND find_pattern: [" + find_pattern + "] text: [" + text + "]\n");
        }
        return (text_is_contain || is_contain);
    }
     */
}//end class

