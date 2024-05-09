import json
from icare_nlp.object_desc import ObjectDesc
obj_desc=ObjectDesc()
with open("./obj_detect_files/59.json", "r") as f:
    obj_detect=json.load(f)
print(obj_detect)
obj_desc_res=obj_desc.form_response(obj_detect)
print(obj_desc_res)