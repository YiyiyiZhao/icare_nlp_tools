import os
import json

dir_ocr_ans="./test_data/ocr_answers"

data_up=[]
for i in range(26):
    ans_file=os.path.join(dir_ocr_ans,f"{i}.json")
    with open(ans_file, "r", encoding="utf-8") as f:
        data=json.load(f)
    for item in data:
        for k, v in item.items():
            print(f"{k}: {v}")
        index = item["index"]
        score = input("\n The score is: ")
        if score == 2:
            continue
        else:
            item.update({"score": score})
            data_up.append(item)

    with open("./test_data/ocr_qa_scores.json", "w", encoding="utf-8") as f:
        json.dump(data_up, f, ensure_ascii=False, indent=2)
