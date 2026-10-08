"""Point the Power BI model at this clone's data folder. Run once after cloning, before opening the .pbip.
    python set_data_folder.py
"""
import os, re
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, ".."))
tmdl = os.path.join(root, "pbip", "JordanUnemployment.SemanticModel", "definition", "expressions.tmdl")
data = os.path.join(root, "data") + os.sep
t = open(tmdl, encoding="utf8").read()
t = re.sub(r'expression DataFolder = "[^"]*"', lambda m: 'expression DataFolder = "%s"' % data, t)
open(tmdl, "w", encoding="utf8", newline="\n").write(t)
print("DataFolder ->", data)
