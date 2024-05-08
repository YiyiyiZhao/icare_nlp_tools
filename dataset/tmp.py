import json
import os
with open("obj_detect_question.json", "r") as f:
    data=json.load(f)
for item in data:
    idx=item["index"]
    obj_detect=item["obj_detect"]
    with open(os.path.join("obj_detect_files", f"{idx}.json"), "w") as f_i:
        json.dump(obj_detect, f_i, indent=2)


