#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pprint import pprint as pp

def writeDocument(path, document):

    is_env_set = False
    env_var="RECORD_RST_AS_HTML"
    print("os.environ")
    sorted_env = sorted(os.environ.items())
    pp(sorted_env)

    is_env_there=(env_var in os.environ)
    if (is_env_there):
        is_env_set=bool(os.environ[env_var])

    if (not is_env_set): return

    rst_path = path.replace("manual", "build/rstdoc_0002").replace(".rst", ".html")
    doc = str(document)

    print("rst_path", rst_path)
    print("doc", doc)

    try:
        os.makedirs(os.path.dirname(rst_path), exist_ok=True)
        with open(rst_path, "w") as f:
            f.write(doc);
            f.close()
    except Exception as e:
        print("Exception writeDocument:{}".format(rst_path))
        raise e

    exit(0)
