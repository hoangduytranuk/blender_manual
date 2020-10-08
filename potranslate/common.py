#!/usr/bin/env python3
import os
import html #for escaping html
import sys
home_dir=os.environ['HOME']
po_tran_path = os.path.join(home_dir, 'blender_manual/potranslate')
sys.path.append(po_tran_path)
# sys.path.append('/usr/local/lib/python3.8/site-packages')

# print(f'common sys.path: {sys.path}')

import os
import re
import inspect
import copy as cp
from collections import OrderedDict, defaultdict
from pprint import pprint, pformat
import hashlib
import time
from reftype import RefType
# from nltk.corpus import wordnet as wn

# import Levenshtein as LE
#import logging

DEBUG=True
# DEBUG=False
DIC_LOWER_CASE=True
# DIC_LOWER_CASE=False

#logging.basicConfig(filename='/home/htran/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        if len(args) == 0:
            print('-' * 30)

def dd(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        if len(args) == 0:
            print('-' * 80)

# def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
#     if DEBUG:
#         logging.info(pformat(args))
#
# def dd(*args, **kwargs):
#     if DEBUG:
#         logging.info(args, kwargs)


class Common:
    s = "( c>5 or (p==4 and c<4) )"
    total_files = 1358
    file_count = 0
    PAGE_SIZE = 20 * 4096
    # It's pyparsing.printables without ()
    CHAR_NO_ARCHED_BRAKETS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'*+,-./:;<=>?@[\]^dd`{|}~'

    WEAK_TRANS_MARKER = "#-1#"
    debug_current_file_count = 0
    debug_max_file_count = 5
    debug_file = None
    debug_file = 'addons/3d_view'
    # debug_file = 'animation/armatures/posing/bone_constraints/introduction' # e.g.
    # debug_file = 'animation/armatures/posing/bone_constraints/inverse_kinematics/introduction' # kbd WheelDown/Up
    # debug_file = "video_editing/sequencer/strips/effects/subtract"
    # debug_file = "video_editing/introduction"
    # debug_file = "about/contribute/index"
    # debug_file="interface/window_system/topbar"
    # debug_file = "advanced/app_templates"
    # debug_file = "modeling/empties"
    # debug_file = "animation/armatures/posing/editing"
    # debug_file = "index"
    # debug_file = "animation/constraints/relationship/shrinkwrap"
    # debug_file = "getting_started/about/community"
    # debug_file = "animation/actions"
    # debug_file = "video_editing/sequencer/strips/transitions/wipe" # :ref:`easings <editors-graph-fcurves-settings-easing>`
    # debug_file = "about/contribute/editing"
    # debug_file = "about/contribute/build/windows"
    # debug_file = "about/contribute/build/macos"
    # debug_file = "about/contribute/guides/maintenance_guide"
    # debug_file = "about/contribute/guides/markup_guide" # debugging :term: :abbr:, ``:kbd:`LMB```, ``*Mirror*``, ``:menuselection:`3D View --> Add --> Mesh --> Monkey```
    # debug_file = "about"
    # debug_file = "about/contribute/install/windows"
    # debug_file = "about/license" # (online) or URL (in print) to manual
    # debug_file = "addons/3d_view/3d_navigation" # debugging :menuselection:
    # debug_file = "addons/add_curve/index"
    # debug_file = "addons/add_curve/ivy_gen"
    # debug_file = "addons/import_export/anim_nuke_chan"
    # debug_file = "addons/node/node_wrangler"
    # debug_file = "addons/object/carver"
    # debug_file = "advanced/command_line/arguments" # trouble some file
    # debug_file = "advanced/command_line/introduction"
    # debug_file = "advanced/command_line/launch/macos"
    # debug_file = "animation/armatures/bones/editing/properties"
    # debug_file = "animation/constraints/relationship/shrinkwrap"
    # debug_file = "animation/constraints/tracking/damped_track"
    # debug_file = "compositing/types/color/color_balance"
    # debug_file = "compositing/types/color/hue_saturation"
    # debug_file = "editors/dope_sheet/introduction" # Pan the view vertically (values) or horizontally (time) with click and drag (:kbd:`MMB`).
    # debug_file = "editors/graph_editor/channels" # Box Select: (:kbd:`LMB` drag) or :kbd:`B` (:kbd:`LMB` drag)
    # debug_file = "editors/preferences/system"
    # debug_file = "editors/texture_node/types/converter/rgb_to_bw"
    # debug_file = "editors/timeline"
    # debug_file = "editors/uv/introduction"
    # debug_file = "files/media/image_formats"
    # debug_file = "getting_started/about/history"
    # debug_file = "grease_pencil/modes/draw/tool_settings/line"
    # debug_file = "interface/controls/nodes/editing"
    # debug_file = "manual/modeling/meshes/primitives"
    # debug_file = "modeling/meshes/editing/vertices"
    # debug_file = "modeling/meshes/structure"
    # debug_file = "modeling/surfaces/structure"
    # debug_file = "movie_clip/tracking/clip/properties/stabilization/introduction"
    # debug_file = "render/shader_nodes/textures/white_noise"
    # debug_file = "scene_layout/object/selecting"
    # debug_file = "scene_layout/scene/properties"
    # debug_file = "sculpt_paint/sculpting/hide_mask"
    # debug_file = "sculpt_paint/weight_paint/editing"
    # debug_file = "video_editing/sequencer/properties/strip"
    # debug_file = "video_editing/sequencer/strips/movie_image"

    KBD='kbd'
    MNU='menuselection'
    DOC='doc'
    ABBREV='abbr'
    STD_REF='std-ref'
    X_REF = 'xref'
    REF_URI='refuri'
    GUI_LAB = 'guilabel'
    TAG_ABBR='abbreviation'
    TAG_NAME='tagname'
    CLASS='classes'

    COMMON_SENTENCE_BREAKS = re.compile(r'(?!\s)([^\.\,\:\!]+)\s?(?<!\s)')
    TRIMMABLE_ENDING = re.compile(r'([\s\.\,\:\!]+)$')
    TRIMMABLE_BEGINNING=re.compile(r'^([\s\.\,]+)')
    TRAILING_WITH_PUNCT = re.compile(r'[\s\.\,\:\!\'\%\$\"\\\)\}\|\]\*\?\>\`\-\+\/\#\&]$')
    HEADING_WITH_PUNCT = re.compile(r'^[\s\.\,\:\!\'\%\$\"\\\(\{\|\[\*\?\>\`\-\+\/\#\&]')

    TRAILING_WITH_PUNCT_MULTI = re.compile(r'[\s\.\,\:\!\'\%\$\"\\\*\?\-\+\/\#\&]+$')
    HEADING_WITH_PUNCT_MULTI = re.compile(r'^[\s\.\,\:\!\'\%\$\"\\\*\?\-\+\/\#\&]+')

    REMOVABLE_SYMB_FULLSET_FRONT = re.compile(r'^[\s\:\!\'$\"\\\(\{\|\[\*\?\;\<\`\-\+\/\#\&]+')
    REMOVABLE_SYMB_FULLSET_BACK = re.compile(r'[\s\:\!\'$\"\\\)\}\|\]\*\?\>\;\`\-\+\/\#\&\,\.]+$')

    RETAIN_FIRST_CHAR = re.compile(r'^[\*\'\"]+')
    RETAIN_LAST_CHAR = re.compile(r'[\*\'\"]+$')

    LEADING_WITH_SYMBOL = re.compile(r'^[\(\[]+')
    TRAILING_WITH_SYMBOL = re.compile(r'[\)\]]+$')

    ABBREV_PATTERN_PARSER = re.compile(r':abbr:[\`]+([^(]+)\s\(([^\)]+)(:[^\)]+)?\)[\`]+')
    ABBREV_CONTENT_PARSER = re.compile(r'([^(]+)\s\(([^\)]+)\)')
    ENDS_PUNCTUAL_MULTI = re.compile(r'([\.\,\:\!\?\"\*\'\`]+$)')
    ENDS_PUNCTUAL_SINGLE = re.compile(r'([\.\,\:\!\?\"\*\'\`]{1}$)')

    BEGIN_PUNCTUAL_MULTI = re.compile(r'^([\.\,\:\;\!\?\"\*\'\`]+)')
    BEGIN_PUNCTUAL_SINGLE = re.compile(r'^([\.\,\:\;\!\?\"\*\'\`]{1})')

    WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_\<\>]+)\b')
    REF_SEP = ' -- '
    NON_WORD_ONLY = re.compile(r'^([\W]+)$')
    NON_WORD = re.compile(r'([\W]+)')
    NON_WORD_ENDING = re.compile(r'([\W]+)$')
    NON_WORD_STARTING = re.compile(r'^([\W]+)')

    GA_REF_PART = re.compile(r':[\w]+:')
    GA_REF = re.compile(r'[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
    GA_REF_ONLY = re.compile(r'^[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*$')
    #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')

    # this (something ... ) can have other links inside of it as well as others
    # the greedy but more accurate is r'[\(]+(.*)?[\)]+'
    # ARCH_BRAKET_SINGLE_PARTS = re.compile(r'[\)]+([^\(]+)?[\(]+')
    ARCH_BRAKET_SINGLE_FULL = re.compile(r'[\(]+([^\)]+)[\)]+')
    #ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)?[\)]+')

    ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)[\)]+')

    AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
    DBL_QUOTE = re.compile(r'[\\\"]+(?![\s\.\,\`]+)([^\\\"]+)[\\\"]+(?<!([\s\.\,]))')
    SNG_QUOTE = re.compile(r'[\']+([^\']+)[\']+(?!([\w]))')
    DBL_QUOTE_SLASH = re.compile(r'\\[\"]+(?![\s\.\,\`]+)([^\\\"]+)\\[\"]+(?<!([\s\.\,]))')
    WORD_WITHOUT_QUOTE = re.compile(r'^[\'\"\*]*([^\'\"\*]+)[\'\"\*]*$')

    LINK_WITH_URI=re.compile(r'([^\<\>\(\)]+[\w]+)[\s]+[\<\(]+([^\<\>\(\)]+)[\>\)]+[\_]*')
    MENU_PART = re.compile(r'(?![\s]?[-]{2}[\>]?[\s]+)(?![\s\-])([^\<\>]+)(?<!([\s\-]))') # working but with no empty entries
    MENU_PART_1 = re.compile(r'(?!\s)([^\->])+(?<!\s)')
    MENU_SEP = re.compile(r'[\s]?[\-]{2}\>[\s]?')

    ABBREV_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)]+)(?<!\s)')
    REF_TEXT_REVERSE = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
    MENU_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')

    WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')

    ENDS_WITH_EXTENSION = re.compile(r'\.([\w]{2,5})$')
    MENU_KEYBOARD = re.compile(r':(kbd|menuselection):')
    MENU_TYPE = re.compile(r'^([\`]*:menuselection:[\`]+([^\`]+)[\`]+)$')

    KEYBOARD_TYPE = re.compile(r'^([\`]*:kbd:[\`]+([^\`]+)[\`]+)$')
    KEYBOARD_SEP = re.compile(r'[^\-]+')
    SPECIAL_TERM = re.compile(r'^[\`\*\"\'\(]+(.*)[\`\*\"\'\)]+$')
    ALPHA_NUMERICAL = re.compile(r'[\w]+')
    EXCLUDE_GA= re.compile(r'^[\`\'\"\*\(]+?([^\`\'\"\*\(\)]+)[\`\'\"\*\)]+?$')
    OPTION_FLAG=re.compile(r'^[\-]{2}([^\`]+)')
    FILLER_CHAR='¶'
    NEGATE_FILLER = r"[^\\" + FILLER_CHAR + r"]+"
    NEGATE_FIND_WORD=re.compile(NEGATE_FILLER)
    ABBR_TEXT = re.compile(r'[\(]([^\)]+)[\)]')

    REF_LINK = re.compile(r'[\s]?[\<]([^\<\>]+)[\>][\s]?')
    PURE_PATH = re.compile(r'^(([\/\\][\w]+)([\/\\][\w]+)*)+[\/\\]?$')
    PURE_REF = re.compile(r'^([\w]+([\-][\w]+)+)+$')
    API_REF = re.compile(r'^blender_api:.*$')

    SPACE_WORD_SEP =  re.compile(r'[^\ ]+')
    ACCEPTABLE_WORD =  re.compile(r'[\w\-]+([\'](t|ve|re|m|s))?')

    QUOTED_MSG_PATTERN = re.compile(r'((?<![\\])[\'"])((?:.)*.?)')

    BLENDER_DOCS= os.path.join(os.environ['HOME'], 'blender_docs')

    # WORD_SEP = re.compile(r'[\s\;\:\.\,\/\!\-\dd\<\>\(\)\`\*\"\|\']')
    WORD_SEP = re.compile(r'[^\W]+')
    SYMBOLS = re.compile(r'^[\W\s]+$')
    SPACE_SEP_WORD = re.compile(r'[^\s]+')
    THE_WORD = re.compile(r'\bthe\b')
    MULTI_SPACES = re.compile(r'[\s]{2,}')
    HYPHEN = re.compile(r'[\-]')

    START_WORD = '^'
    END_WORD = '$'
    BOTH_START_AND_END = '^$'

    verb_with_ending_y = [
        'aby',
        'bay',
        'buy',
        'cry',
        'dry',
        'fly',
        'fry',
        'guy',
        'hay',
        'joy',
        'key',
        'lay',
        'pay',
        'ply',
        'pry',
        'ray',
        'say',
        'shy',
        'sky',
        'spy',
        'toy',
        'try',
        'ally',
        'baby',
        'body',
        'bray',
        'buoy',
        'bury',
        'busy',
        'cloy',
        'copy',
        'defy',
        'deny',
        'eddy',
        'envy',
        'espy',
        'flay',
        'fray',
        'gray',
        'grey',
        'levy',
        'obey',
        'okay',
        'pity',
        'play',
        'pray',
        'prey',
        'rely',
        'scry',
        'slay',
        'spay',
        'stay',
        'sway',
        'tidy',
        'vary',
        'allay',
        'alloy',
        'annoy',
        'apply',
        'array',
        'assay',
        'bandy',
        'belay',
        'belly',
        'berry',
        'bogey',
        'bully',
        'caddy',
        'candy',
        'carry',
        'chevy',
        'chivy',
        'colly',
        'curry',
        'dally',
        'decay',
        'decoy',
        'decry',
        'deify',
        'delay',
        'dirty',
        'dizzy',
        'dummy',
        'edify',
        'empty',
        'enjoy',
        'ensky',
        'epoxy',
        'essay',
        'fancy',
        'ferry',
        'foray',
        'glory',
        'harry',
        'honey',
        'hurry',
        'imply',
        'inlay',
        'jelly',
        'jimmy',
        'jolly',
        'lobby',
        'marry',
        'mosey',
        'muddy',
        'palsy',
        'parry',
        'party',
        'putty',
        'query',
        'rally',
        'ready',
        'reify',
        'relay',
        'repay',
        'reply',
        'retry',
        'savvy',
        'splay',
        'spray',
        'stray',
        'study',
        'stymy',
        'sully',
        'tally',
        'tarry',
        'toady',
        'unify',
        'unsay',
        'weary',
        'worry',
        'aerify',
        'argufy',
        'basify',
        'benday',
        'betray',
        'bewray',
        'bloody',
        'canopy',
        'chivvy',
        'citify',
        'codify',
        'comply',
        'convey',
        'convoy',
        'curtsy',
        'defray',
        'deploy',
        'descry',
        'dismay',
        'embody',
        'employ',
        'flurry',
        'gasify',
        'jockey',
        'minify',
        'mislay',
        'modify',
        'monkey',
        'motley',
        'mutiny',
        'nazify',
        'notify',
        'occupy',
        'ossify',
        'outcry',
        'pacify',
        'parlay',
        'parley',
        'parody',
        'prepay',
        'purify',
        'purvey',
        'quarry',
        'ramify',
        'rarefy',
        'rarify',
        'ratify',
        'rebury',
        'recopy',
        'remedy',
        'replay',
        'sashay',
        'scurry',
        'shimmy',
        'shinny',
        'steady',
        'supply',
        'survey',
        'tumefy',
        'typify',
        'uglify',
        'verify',
        'vilify',
        'vinify',
        'vivify',
        'volley',
        'waylay',
        'whinny',
        'acetify',
        'acidify',
        'amnesty',
        'amplify',
        'atrophy',
        'autopsy',
        'beatify',
        'blarney',
        'calcify',
        'carnify',
        'certify',
        'clarify',
        'company',
        'crucify',
        'curtsey',
        'dandify',
        'destroy',
        'dignify',
        'disobey',
        'display',
        'dulcify',
        'falsify',
        'fancify',
        'fantasy',
        'fortify',
        'gainsay',
        'glorify',
        'gratify',
        'holiday',
        'horrify',
        'jellify',
        'jollify',
        'journey',
        'justify',
        'lignify',
        'liquefy',
        'liquify',
        'magnify',
        'metrify',
        'misally',
        'misplay',
        'mollify',
        'mortify',
        'mummify',
        'mystify',
        'nigrify',
        'nitrify',
        'nullify',
        'opacify',
        'outplay',
        'outstay',
        'overfly',
        'overjoy',
        'overlay',
        'overpay',
        'petrify',
        'pillory',
        'portray',
        'putrefy',
        'qualify',
        'rectify',
        'remarry',
        'reunify',
        'satisfy',
        'scarify',
        'signify',
        'specify',
        'stupefy',
        'terrify',
        'testify',
        'tourney',
        'verbify',
        'versify',
        'vitrify',
        'alkalify',
        'ammonify',
        'beautify',
        'bioassay',
        'causeway',
        'classify',
        'corduroy',
        'denazify',
        'detoxify',
        'disarray',
        'downplay',
        'emulsify',
        'esterify',
        'etherify',
        'fructify',
        'gentrify',
        'humidify',
        'identify',
        'lapidify',
        'misapply',
        'miscarry',
        'multiply',
        'overplay',
        'overstay',
        'prettify',
        'prophesy',
        'quantify',
        'redeploy',
        'revivify',
        'rigidify',
        'sanctify',
        'saponify',
        'simplify',
        'solidify',
        'stratify',
        'stultify',
        'travesty',
        'underlay',
        'underpay',
        'accompany',
        'butterfly',
        'decalcify',
        'decertify',
        'demulsify',
        'demystify',
        'denitrify',
        'devitrify',
        'disembody',
        'diversify',
        'electrify',
        'exemplify',
        'frenchify',
        'indemnify',
        'intensify',
        'inventory',
        'microcopy',
        'objectify',
        'overweary',
        'personify',
        'photocopy',
        'preachify',
        'preoccupy',
        'speechify',
        'syllabify',
        'underplay',
        'blackberry',
        'complexify',
        'declassify',
        'dehumidify',
        'dillydally',
        'disqualify',
        'dissatisfy',
        'intermarry',
        'oversupply',
        'reclassify',
        'saccharify',
        'understudy',
        'hypertrophy',
        'misidentify',
        'oversimplify',
        'transmogrify',
        'interstratify',
    ]

    verb_with_ending_s = [
        'Bus',
        'Gas',
        'Bias',
        'Boss',
        'Buss',
        'Cuss',
        'Diss',
        'Doss',
        'Fuss',
        'Hiss',
        'Kiss',
        'Mass',
        'Mess',
        'Miss',
        'Muss',
        'Pass',
        'Sass',
        'Suds',
        'Toss',
        'Amass',
        'Bless',
        'Class',
        'Cross',
        'Degas',
        'Dress',
        'Floss',
        'Focus',
        'Glass',
        'Gloss',
        'Grass',
        'Gross',
        'Guess',
        'Press',
        'Truss',
        'Access',
        'Assess',
        'Bypass',
        'Callus',
        'Canvas',
        'Caress',
        'Caucus',
        'Census',
        'Chorus',
        'Egress',
        'Emboss',
        'Harass',
        'Obsess',
        'Precis',
        'Recess',
        'Rumpus',
        'Schuss',
        'Stress',
        'Address',
        'Aggress',
        'Callous',
        'Canvass',
        'Compass',
        'Concuss',
        'Confess',
        'Degauss',
        'Depress',
        'Digress',
        'Discuss',
        'Dismiss',
        'Engross',
        'Express',
        'Harness',
        'Impress',
        'Nonplus',
        'Oppress',
        'Percuss',
        'Possess',
        'Precess',
        'Premiss',
        'Process',
        'Profess',
        'Redress',
        'Refocus',
        'Regress',
        'Repress',
        'Succuss',
        'Summons',
        'Surpass',
        'Teargas',
        'Trellis',
        'Uncross',
        'Undress',
        'Witness',
        'Bollocks',
        'Buttress',
        'Compress',
        'Distress',
        'Outclass',
        'Outguess',
        'Progress',
        'Reassess',
        'Suppress',
        'Trespass',
        'Waitress',
        'Backcross',
        'Embarrass',
        'Encompass',
        'Overdress',
        'Repossess',
        'Reprocess',
        'Unharness',
        'Verdigris',
        'Crisscross',
        'Decompress',
        'Dispossess',
        'Eyewitness',
        'Misaddress',
        'Overstress',
        'Prepossess',
        'Rendezvous',
        'Retrogress',
        'Transgress',
        'Disembarrass',
    ]

    common_removable_ending = [
        'e',
    ]

    common_prefixes = [
        'a',
        'an',
        'co',
        'de',
        'en',
        'ex',
        'il',
        'im',
        'in',
        'ir',
        'in',
        'un',
        'up',
        'com',
        'con',
        'dis',
        'non',
        'pre',
        'pro',
        'sub',
        'sym',
        'syn',
        'tri',
        'uni',
        'ante',
        'anti',
        'auto',
        'homo',
        'mono',
        'omni',
        'post',
        'tele',
        'extra',
        'homeo',
        'hyper',
        'inter',
        'intra',
        'intro',
        'macro',
        'micro',
        'trans',
        'circum',
        'contra',
        'contro',
        'hetero',
    ]
    
    common_prefix_trans = {
        'auto': (START_WORD, 'tự động'),
    }

    common_sufix_trans = {
        's': (START_WORD, 'những/các/nhiều/một số/vài'),
        'ed': (START_WORD, 'đã/bị/được'),
        'es': (START_WORD, 'mọi/những/các/nhiều/một số/vài'),
        'er': (END_WORD, 'hơn/trình/bộ/người/viên'),
        'ic': (END_WORD, 'giống/liên quan đến/hoạt động trong'),
        'or': (START_WORD, 'máy/phần/cái/trình/bộ/người/nhà/viên/vật'),
        'al': (START_WORD, 'thuộc/có tính/sự/phần'),
        'ly': (START_WORD, 'nói một cách/có tính'),
        'ty': (START_WORD, 'trạng thái/có tính'),
        '(s)': (START_WORD, '(những/các)'),
        'ers': (START_WORD, 'mọi/những/các/nhiều/một số/vài bộ/trình/người/viên'),
        'ies': (START_WORD, 'mọi/những/các/nhiều/một số/vài'),
        'ier': (END_WORD, 'hơn'),
        '\'s': (START_WORD, 'của'),
        'ors': (START_WORD, 'máy/mọi/các/những/nhiều/vài phần/cái/trình/bộ/người/nhà/viên'),
        'est': (END_WORD, 'nhất'),
        'dom': (START_WORD, 'sự/phần'),
        'ful': (START_WORD, 'rất/nhiều'),
        'nce': (START_WORD, 'sự/phần'),
        'ily': (START_WORD, 'một cách'),
        'ity': (START_WORD, 'sự/phần'),
        'ive': (START_WORD, 'có tính'),
        'ish': (START_WORD, 'hơi hơi/có xu hướng/gần giống'),
        'als': (START_WORD, 'mọi/nhiều/các/những có tính/sự/phần'),
        'ure': (START_WORD, 'sự/phần'),
        '\'ll': (START_WORD, 'sẽ'),
        'able': (START_WORD, 'có khả năng/thể'),
        'ably': (START_WORD, 'có khả năng/thể/đáng'),
        'doms': (START_WORD, 'sự/phần'),
        'ible': (START_WORD, 'có khả năng/thể/đáng'),
        'ibly': (START_WORD, 'có khả năng/thể/đáng'),
        'iest': (END_WORD, 'nhất'),
        'sion': (START_WORD, 'sự/phần'),
        'tion': (START_WORD, 'sự/phần'),
        'ness': (START_WORD, 'mức/độ/tính/sự'),
        'ency': (START_WORD, 'sự/phần'),
        'ment': (START_WORD, 'sự/phần/phép'),
        'less': (START_WORD, 'vô/không/phi'),
        '-less': (START_WORD, 'vô/không/phi'),
        'like': (START_WORD, 'Thích/Giống Như/Tương Tự'),
        '-like': (START_WORD, 'Thích/Giống Như/Tương Tự'),
        'than': (END_WORD, 'hơn'),
        'ures': (START_WORD, 'sự/phần'),
        'lable': (START_WORD, 'có khả năng/thể/đáng'),
        'ities': (START_WORD, 'mọi/nhiều/các/những sự/phần'),
        'iness': (START_WORD, 'mức/độ/tính/sự/phần'),
        'ation': (START_WORD, 'sự/phần'),
        'ively': (START_WORD, 'nói một cách/có tính'),
        'ments': (START_WORD, 'sự/phần'),
        'ption': (START_WORD, 'sự/phần'),
        'ations': (START_WORD, 'mọi/nhiều/các/những sự/phần'),
        'encies': (START_WORD, 'mọi/nhiều/các/những sự/phần'),
        'ization': (START_WORD, 'sự/phần'),
        'isation': (START_WORD, 'sự/phần'),
        'izations': (START_WORD, 'mọi/nhiều/các/những sự/phần'),
        'isations': (START_WORD, 'mọi/nhiều/các/những sự/phần'),
    }

    common_suffixes_replace_dict = {
        'e': list(sorted(
            ['able', 'ation', 'ations', 'ion', 'ions',
             'ity', 'ities', 'ing', 'ings', 'ously', 'ous', 'ive',
             'ively', 'or', 'ors', 'iness', 'ature',
             'atures', 'ition', 'itions', 'itiveness',
             'itivenesses', 'itively', 'ative', 'atives',
             'ant', 'ants', 'ator', 'ators', 'ure', 'ures',
             'al', 'als', 'iast', 'iasts', 'iastic', 'ial',
             ],
            key=lambda x: len(x), reverse=True)),
        't':['ce','cy', 'ssion', 'ssions'],
        'y':['ies', 'ied', 'ier', 'iest', 'ily', 'ic', 'ical', 'ically', 'iness', 'inesses'],
        'ion':['ively'],
        'be':['ption', 'ptions',],
        'de':['sible', 'sion', 'sions' ],
        'ate':['ant'],
        'cy':['t'],
        'ze':['s'],
        'le':['ility', 'ilities', ]
    }

    common_suffixes = [
        'd',
        'r',
        'y',
        's',
        't',
        'al',
        'an',
        'ce',
        'cy',
        'er',
        'es',
        'or',
        'th',
        'ic',
        'ly',
        'ed',
        'en',
        'er',
        'ly',
        'st',
        'ty',
        'ze',
        'ze',
        '\'s',
        '\'t',
        '\'m',
        'als',
        'dom',
        'ors',
        'ers',
        'est',
        'eer',
        'ial',
        'ied',
        'ier',
        'ion',
        'ity',
        'ics',
        'ies',
        'like',
        '-like',
        'less',
        '-less',
        'ant',
        'ent',
        'ary',
        'ful',
        'nce',
        'ous',
        'ive',
        'ing',
        'ily',
        'ity',
        'ize',
        'ise',
        'ish',
        'ite',
        'ful',
        'ual',
        'ure',
        'ous',
        '(s)',
        '\'re',
        '\'ve',
        '\'ll',
        'n\'t',
        'ator',
        'ants',
        'doms',
        'ence',
        'ency',
        'ents',
        'ings',
        'ures',
        'ions',
        'iest',
        'iast',
        'iasts',
        'iastic',
        'lier',
        'less',
        'liest',
        'ment',
        'ness',
        'ning',
        'sion',
        'ship',
        'able',
        'ably',
        'ible',
        'ical',
        'ally',
        'ious',
        'less',
        'ally',
        'ward',
        'wise',
        'ency',
        'ators',
        'sible',
        'ively',
        'ually',
        'ption',
        'ation',
        'iness',
        'ities',
        'ition',
        'itive',
        'ments',
        'sions',
        'ssion',
        'ships',
        'aries',
        'ature',
        'ingly',
        'izing',
        'ising',
        'iness',
        'lable',
        'ously',
        'ptions',
        'ility',
        'ilities',
        'itives',
        'itions',
        'atures',
        'ations',
        'aceous',
        'nesses',
        'iously',
        'ically',
        'encies',
        'ssions',
        'itively',
        'ization',
        'isation',
        'itiveness',
        'itivenesses',
    ]

    common_infix = [
        '-',
    ]

    common_sufix_translation = list(sorted( list(common_sufix_trans.items()), key=lambda x: len(x[0]), reverse=True))
    common_prefix_translation = list(sorted( list(common_prefix_trans.items()), key=lambda x: len(x[0]), reverse=True))
    common_prefix_sorted = list(sorted(common_prefixes, key=lambda x: len(x), reverse=False))
    common_suffix_sorted = list(sorted(common_suffixes, key=lambda x: len(x), reverse=False))
    common_infix_sorted = list(sorted(common_infix, key=lambda x: len(x), reverse=False))

    def replaceArchedQuote(txt):
        new_txt = str(txt)
        new_txt = re.sub('\)', ']', new_txt)
        new_txt = re.sub('\(', '[', new_txt)
        # new_txt = new_txt.replace('"', '\\\"')
        return new_txt

    def hasOriginal(msg, tran):
        orig_list = Common.ALPHA_NUMERICAL.findall(msg)
        orig_set = "".join(orig_list)

        tran_list = Common.ALPHA_NUMERICAL.findall(tran)
        tran_set = "".join(tran_list)

        has_orig = (orig_set in tran_set)
        #print("orig_set:", orig_set)
        #print("tran_set:", tran_set)
        #print("has_orig:", has_orig)
        return has_orig

    def isSpecialTerm(msg: str):
        is_special = (Common.SPECIAL_TERM.search(msg) is not None)
        return is_special

    def matchCase(from_str : str , to_str : str):
        WORD_SHOULD_BE_LOWER = [
            'trong',
            'các',
            'những',
            'và',
            'thì'
            'là',
            'hoặc',
            'mà',
            'có',
            'của',
            'với',
            'đến',
            'tới',
        ]
        def lowercase(loc_text_dict, new_str):
            for loc, text in ga_ref_dic.items():
                s, e = loc
                lcase_text = text.lower()
                left_part = new_str[:s]
                right_part = new_str[e:]
                new_str = left_part + lcase_text + right_part
            return new_str

        valid = (from_str and to_str)
        if not valid:
            return to_str

        new_str = str(to_str)

        # first_char = from_str[0]
        # remain_part = from_str[1:]
        # is_first_upper = (first_char.isupper() and remain_part.islower())
        # if is_first_upper:
        #     first_char = new_str[0].upper()
        #     remain_part = new_str[1:].lower()
        #     new_str = first_char + remain_part
        # else:
        is_lower = (from_str.islower())
        if is_lower:
            new_str = new_str.lower()
        else:
            is_title = (from_str.istitle())
            if is_title:
                new_str = new_str.title()
            else:
                is_upper = (from_str.isupper())
                if is_upper:
                    new_str = new_str.upper()

        # ensure ref keywords ':doc:' is always lowercase
        ga_ref_dic = Common.patternMatchAllToDict(Common.GA_REF_PART, new_str)
        new_str = lowercase(ga_ref_dic, new_str)
        for lcase_word in WORD_SHOULD_BE_LOWER:
            p = re.compile(r'\b%s\b' % lcase_word)
            p_list = Common.patternMatchAllToDict(p, new_str)
            new_str = lowercase(p_list, new_str)

        return new_str

    def beginAndEndPunctuation(msg, is_single=False):
        if is_single:
            begin_with_punctuations = (Common.BEGIN_PUNCTUAL_SINGLE.search(msg) is not None)
            ending_with_punctuations = (Common.ENDS_PUNCTUAL_SINGLE.search(msg) is not None)
            if begin_with_punctuations:
                msg = Common.BEGIN_PUNCTUAL_SINGLE.sub("", msg)
            if ending_with_punctuations:
                msg = Common.ENDS_PUNCTUAL_SINGLE.sub("", msg)
        else:
            begin_with_punctuations = (Common.BEGIN_PUNCTUAL_MULTI.search(msg) is not None)
            ending_with_punctuations = (Common.ENDS_PUNCTUAL_MULTI.search(msg) is not None)
            if begin_with_punctuations:
                msg = Common.BEGIN_PUNCTUAL_MULTI.sub("", msg)
            if ending_with_punctuations:
                msg = Common.ENDS_PUNCTUAL_MULTI.sub("", msg)

        return msg, begin_with_punctuations, ending_with_punctuations

    def removeOriginal(msg, trans):
        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) is not None)
        endings_list = ["", "s", "es", "ies", "ed", "ing", "lly",]
        endings = sorted(endings_list, key=lambda x: len(x), reverse=True)

        if has_original:
            for end in endings:
                p = r'{}{}:\ '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'-- {}{}'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r' ({}{})'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)


            for end in endings:
                p = r'{}{} --'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'({}{}) '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'\\b{}{}\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'\\b({}{})\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            trans = trans.strip()
            is_empty = (len(trans) == 0)
            if is_empty:
                trans = None
        return trans

    def cleanSlashesQuote(msg):
        if not msg:
            return msg

        msg = msg.replace("\\\"", "\"")
        msg = msg.replace("\\\\", "\\")
        return msg

    def patternMatchAllToDict(pat, text):
        matching_list = {}
        for m in pat.finditer(text):
            s = m.start()
            e = m.end()
            orig = m.group(0)
            k = (s, e)
            entry = {k: orig}
            matching_list.update(entry)
        return matching_list

    def patternMatchAll(pat, text):
        try:
            # itor = pat.finditer(text)
            # print("itor", type(itor))
            # print("dir", dir(itor))

            for m in pat.finditer(text):
                original = ()
                break_down = []

                s = m.start()
                e = m.end()
                orig = m.group(0)
                original = (s, e, orig)

                for g in m.groups():
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        break_down.append(v)
                yield original, break_down

        except Exception as e:
            dd("patternMatchAll")
            dd("pattern:", pat)
            dd("text:", text)
            dd(e)
        return None, None

    def patternMatchAllAsDictNoDelay(pat, text):
        try:
            return_dict = {}
            for m in pat.finditer(text):
                original = ()
                # break_down = []

                s = m.start()
                e = m.end()
                orig = m.group(0)
                original = (s, e, orig)
                entry = {(s,e): orig}
                return_dict.update(entry)

                for g in m.groups():
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        # break_down.append(v)
                        entry = {(ss, ee): g}
                        return_dict.update(entry)
        except Exception as e:
            dd("patternMatchAll")
            dd("pattern:", pat)
            dd("text:", text)
            dd(e)
        return return_dict

    def findInvert(pattern, text):
        found_list={}
        tt = str(text)
        # fill in the place of pattern with a filler (FILLER_CHAR), length of found pattern
        for orig, bkdown in Common.patternMatchAll(pattern, text):
            s, e, txt = orig
            filler = str(Common.FILLER_CHAR * len(txt))
            tt = tt[:s] + filler + tt[e:]
        # tt is not contains 'word....another word...and an another word' (... represents the filler)
        # now find with NOT '[^\FILLER_CHAR]+'
        for orig, bkdown in Common.patternMatchAll(Common.NEGATE_FIND_WORD, tt):
            s, e, txt = orig
            entry={s:orig}
            found_list.update(entry)
        return found_list


    def getListOfLocation(find_list):
        loc_list = {}
        for k, v in find_list.items():
            s = v[0][0]
            e = v[0][1]
            t = v[0][2]
            entry = {k: [s, e, t]}
            loc_list.update(entry)
        return loc_list

    def inRange(item, ref_list):
        i_s, i_e, i_t = item
        for k, v in ref_list.items():
            r_s, r_e, r_t = v
            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                return True
        else:
            return False

    def diffLocation(ref_list, keep_list):
        loc_keep_list = {}
        for k, v in keep_list.items():
            in_forbiden_range = Common.inRange(v, ref_list)
            if not in_forbiden_range:
                s, e, txt = v
                ee = (s, e, txt)
                entry = {s: [ee]}
                loc_keep_list.update(entry)

        return loc_keep_list

    def mergeTwoLists(primary, secondary):

        loc_primary_list = Common.getListOfLocation(primary)
        loc_secondary_list = Common.getListOfLocation(secondary)
        keep_list = Common.diffLocation(loc_primary_list, loc_secondary_list)

        #pp(keep_list)
        for k, v in keep_list.items():
            keep_v = secondary[k]
            entry={k:keep_v}
            primary.update(entry)

        return primary

    def filteredTextList(ref_list, norm_list):
        loc_ref_list = Common.getListOfLocation(ref_list)
        loc_norm_list = Common.getListOfLocation(norm_list)
        keep_norm_list = Common.diffLocation(loc_ref_list, loc_norm_list)
        return keep_norm_list

    def getTextListForMenu(text_entry):
        #print("getTextListForMenu", text_entry, txt_item)
        entry_list = []

        its, ite, txt = text_entry
        dd("menu_list: its, ite, txt")
        dd(its, ite, txt)

        menu_list = Common.patternMatchAll(Common.MENU_PART, txt)
        dd("menu_list")
        pp(menu_list)
        for mk, mi in menu_list.items():
            ms, me, mtxt = mi[0]
            is_empty = (ms == me)
            if (is_empty):
                continue

            ss = its + ms
            se = ss + len(mtxt)
            entry=(ss, se, mtxt)
            entry_list.append(entry)
        pp(entry_list)
        return entry_list

    def isListEmpty(list_elem):
        is_empty = (list_elem is None) or (len(list_elem) == 0)
        return is_empty

    def removeLowerCaseDic(dic_list : dict ):
        l_case = {}
        u_case = {}
        k = None
        v = None
        try:
            for i, e in enumerate(dic_list.items()):
                k, v = e
                if not k:
                    continue

                is_lower_k = (k.islower())
                if is_lower_k:
                    l_case.update({k: v})
                else:
                    u_case.update({k: v})

            u_l_case = dict((k.lower(), v) for k, v in u_case.items())

            l_case_remain = {}
            for k, v in l_case.items():
                if k in u_l_case:
                    continue
                else:
                    l_case_remain.update({k: v})
            u_case.update(l_case_remain)
        except Exception as e:
            dd("k:", k)
            dd("v:", k)
            dd(e)
            raise e
        return u_case

    def isTextuallySimilar(from_txt, to_txt):
        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        is_similar = (to_set in from_set) or (from_set in to_set)
        if not is_similar:
            from_set = set(from_set)
            to_set = set(to_set)
            intersect_set = from_set.intersection(to_set)
            is_similar = (intersect_set == from_set) or (intersect_set == to_set)
        return is_similar

    # def isTextuallyVerySimilar(from_txt, to_txt):
    #     similar_ratio = LE.ratio(from_txt, to_txt)
    #     acceptable = (similar_ratio >= 0.75)
    #     return acceptable

    def isTextuallySame(from_txt:str, to_txt:str):

        is_valid = (from_txt is not None) and (to_txt is not None)
        is_both_none = (from_txt is None) and (to_txt is None)
        if is_both_none:
            return True
        if not is_valid:
            return False

        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        # perform set intersection to find common set
        is_same = (to_set == from_set)
        return is_same

    def isTextuallySubsetOf(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())
        msg_str = "".join(msg_list)
        tran_str = "".join(tran_list)

        # perform set intersection to find common set
        is_subset = (msg_str in tran_str)
        return is_subset

    def alterValue(orig_value, alter_value=0, op=None):
        altering = (op is not None)
        if altering:
            if op == "+":
                orig_value += alter_value
            elif op == "=":
                orig_value -= alter_value
            elif op == "*":
                orig_value *= alter_value
            elif op == "/":
                orig_value /= alter_value
            elif op == "%":
                orig_value %= alter_value
            elif op == "=":
                orig_value = alter_value
        return orig_value

    def parseMessageWithDelimiterPair(open_char, close_char, msg):
        valid = (open_char is not None) and (close_char is not None) and (msg is not None) and (len(msg) > 0)
        if not valid:
            return None

        is_pair_same_char = (open_char == close_char)
        if is_pair_same_char:
            raise Exception("Open and close symbols must not be the same!")

        loc_list:list = []
        b_list=[]
        l = len(msg)
        s = e = 0
        k = -1
        for i in range(0, l):
            c = msg[i]
            is_open = (c == open_char)
            is_close = (c == close_char)
            if is_open:
                b_list.append(i)
            elif is_close:
                try:
                    last_s = b_list[-1]
                    b_list.pop()
                    txt = msg[last_s:i+1]
                    loc_list_entry=(last_s, i+1, txt)
                    loc_list.append(loc_list_entry)

                    ll = msg[:last_s]
                    rr = msg[i+1:]
                    ltxt = ll + txt + rr
                    is_same = (ltxt == msg)
                    if not is_same:
                        raise Exception("ERROR in location calculation for: [", txt, "] at start:", last_s, " end:", i+1, " in:[", msg, "]")
                except Exception as e:
                    continue
                    # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, i, msg)
                    # print(e)
                    # raise Exception(msg)

        # has_unprocessed_pair = (len(b_list) > 0)
        # if has_unprocessed_pair:
        #     # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, b_list, msg)
        #     # raise Exception(msg)

        has_loc_list = (len(loc_list) > 0)
        if not has_loc_list:
            return []
        else:
            sorted_loc_list = []
            sorted_loc_list = sorted(loc_list, key=lambda x: x[0])
            return sorted_loc_list

    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python , answered Jul 2 '17 at 17:23 - maxschlepzig (Georg Sauthoff)
    #
    # maxschlepzig
    # 23.3k99 gold badges9393 silver badges126
    def sha256sum(filename):
        h = hashlib.sha256()
        b = bytearray(Common.PAGE_SIZE) # PAGE_SIZE = 20 * 4096, original 128*1024
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def getFileModifiedTime(filename):
        return time.ctime( os.path.getmtime(filename))

    def getFileCreatedTime(filename):
        return time.ctime( os.path.getctime(filename))

    def getMsgAsDict(txt):
        result_dict={}
        if not txt:
            return result_dict

        parsed_list = Common.patternMatchAllToDict(Common.QUOTED_MSG_PATTERN, txt)
        print(f'getMsgAsDict:{parsed_list}')
        count=0
        entry=None
        msgid_part = msgstr_part = None
        for loc, v in parsed_list.items():
            msg = v[1:-1]
            msg = msg.replace('"', '\\"')
            msg = msg.replace("'", "\\'")
            is_even_line_index = (count % 2 == 0)
            if is_even_line_index:
                msgid_part = msg
            else:
                msgstr_part = msg
                entry = {msgid_part: msgstr_part}
                print(f'getMsgAsDict entry:{entry}')
                result_dict.update(entry)
            count += 1
        return result_dict

    def removeLeadingTrailingSymbs(txt):
        def cleanForward(txt, pair_dict, leading_set):
            if not leading_set:
                return txt, leading_set

            temp_txt = str(txt)
            count = 0
            for sym_on in leading_set:
                is_sym_on_in_dict = (sym_on in pair_dict)
                if not is_sym_on_in_dict:
                    continue

                sym_off = pair_dict[sym_on]
                temp = temp_txt[1:]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
            return temp_txt, leading_set

        def cleanBackward(txt, pair_dict, trailing_set):
            if not trailing_set:
                return txt, trailing_set

            temp_txt = str(txt)
            count = 0
            for sym_off in reversed(trailing_set):
                is_controlled = (sym_off in pair_dict)
                if not is_controlled:
                    temp_txt = temp_txt[:-1]
                    count += 1
                    continue

                sym_on = pair_dict[sym_off]
                temp = temp_txt[:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                trailing_set = trailing_set[:-count]
            return temp_txt, trailing_set

        def cleanBothEnds(txt, pair_dict, leading_set, trailing_set):
            count = 0
            temp_txt = str(txt)

            if leading_set and trailing_set:
                symbol_set = leading_set + trailing_set
            elif leading_set:
                symbol_set = leading_set
            elif trailing_set:
                symbol_set = trailing_set
            else:
                return temp_txt, leading_set, trailing_set

            for sym_on in symbol_set:
                is_sym_off_there = (sym_on in pair_dict)
                if not is_sym_off_there:
                    break

                sym_off = pair_dict[sym_on]
                is_both_ends = (temp_txt.startswith(sym_on) and temp_txt.endswith(sym_off))
                if not is_both_ends:
                    continue

                temp = temp_txt[1:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
                trailing_set = trailing_set[:-count]
            return temp_txt, leading_set, trailing_set

        # txt = '   ({this}....,!'
        # # txt = '(also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :ref:`bone locking <animation_armatures_bones_locking>`'
        # # txt = '(Top/Side/Front/Camera...)'
        txt = txt.strip()

        pair_list = [('{', '}'), ('[', ']'), ('(', ')'), ('<', '>'), ('$', '$'),(':', ':'), ('*', '*'), ('\'', '\''), ('"', '"'), ('`', '`'),]
        pair_dict = {}
        for p in pair_list:
            s, e = p
            entry_1 = {s:e}
            entry_2 = {e:s}
            pair_dict.update(entry_1)
            pair_dict.update(entry_2)

        leading_set = Common.REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)
        if leading_set:
            leading_set = leading_set[0]

        trailing_set = Common.REMOVABLE_SYMB_FULLSET_BACK.findall(txt)
        if trailing_set:
            trailing_set = trailing_set[0]

        temp_txt = str(txt)
        temp_txt, leading_set, trailing_set = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)

        temp_txt, leading_set = cleanForward(temp_txt, pair_dict, leading_set)
        temp_txt, trailing_set = cleanBackward(temp_txt, pair_dict, trailing_set)

        temp_txt, _, _ = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)
        return temp_txt

    def isBalancedSymbol(symb_on, symb_off, txt):
        p_str = f'\{symb_on}([^\{symb_on}\{symb_off}]+)\{symb_off}'
        p_exp = r'%s' % (p_str.replace("\\\\", "\\"))
        pattern = re.compile(p_exp)
        p_list = Common.patternMatchAllToDict(pattern, txt)
        has_p_list = (len(p_list) > 0)
        if has_p_list:
            temp_txt = str(txt)
            for loc, txt in p_list.items():
                s, e = loc
                left = temp_txt[:s]
                right = temp_txt[e:]
                temp_txt = left + right
            return not ((symb_on in temp_txt) or (symb_off in temp_txt))
        else:
            return True
        # default_last_i = 0xffffffff
        # counter = 0
        # last_i = default_last_i
        # off_happened_first = False
        # for i, c in enumerate(text):
        #     is_on = (i != last_i) and (c == symb_on)
        #     if is_on:
        #         counter += 1
        #         last_i = i
        #     else:
        #         is_off = (i != last_i) and (c == symb_off)
        #         if is_off:
        #             off_happened_first = (last_i == default_last_i)
        #             counter -= 1
        #             last_i = i
        #
        # return (counter == 0) and not (off_happened_first)

    def hasAbbr(txt):
        abbr_str = RefType.ABBR.value
        has_abbr = (abbr_str in txt)
        return has_abbr

    def extractAbbr(abbr_txt):
        if not abbr_txt:
            return None, None, None

        has_abbr = Common.hasAbbr(abbr_txt)
        if not has_abbr:
            return None, None, None

        abbr_dict = Common.patternMatchAllAsDictNoDelay(Common.ABBREV_PATTERN_PARSER, abbr_txt)
        if not abbr_dict:
            return None, None, None

        abbrev_list = list(abbr_dict.items())
        length = len(abbr_dict)
        if length > 0:
            abbrev_orig_rec = abbr_dict[0]
        else:
            abbrev_orig_rec = None

        if length > 1:
            abbrev_rec = abbr_dict[1]
        else:
            abbrev_rec = None

        if length > 2:
            abbrev_exp_rec = abbr_dict[2]
        else:
            abbrev_exp_rec = None

        return abbrev_orig_rec, abbrev_rec, abbrev_exp_rec

    def testDict(dic_to_use):
        test_txt = 'Build'
        is_test_text_in_dic = (test_txt in dic_to_use)
        if is_test_text_in_dic:
            # value_old = dic[test_txt]
            value = dic_to_use[test_txt]
            dd(f'found: {test_txt} => {value}')
        else:
            dd(f'NOT found: {test_txt} SOMETHING WRONG!!!')



