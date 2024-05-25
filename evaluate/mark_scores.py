import json
import cv2
import pdb
with open("obj_qa_answers.json", "r", encoding="utf-8") as f:
    data=json.load(f)

data_up = []
for item in data:
    for key, value in item.items():
        print(f"{key}: {value}")
    index=item["index"]
    score=input("\n The score is: ")
    if score==2:
        continue
    else:
        item.update({"score":score})
        data_up.append(item)

with open("./test_data/obj_qa_scores.json", "w", encoding="utf-8") as f:
    json.dump(data_up, f, ensure_ascii=False, indent=2)
