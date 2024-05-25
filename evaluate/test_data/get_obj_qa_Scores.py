import json

with open("obj_qa_scores.json", "r", encoding="utf-8") as f:
    data=json.load(f)

cnt_an_all=0
cnt_an_correct=0
cnt_fp_all=0
cnt_fp_correct=0

for i in range(len(data)):
    if data[i]["question_type"]=="ask_near":
        cnt_an_all+=1
        if data[i]['score'] == "1":
            cnt_an_correct += 1
    if data[i]["question_type"]=="find_position":
        cnt_fp_all+=1
        if data[i]['score'] == "1":
            cnt_fp_correct += 1

print("NUMBER ASK_NEAR: ", cnt_an_all)
print("NUMBER AN CORRECT: ", cnt_an_correct)
print("AN Rate: ", cnt_an_correct/cnt_an_all)

print("NUMBER FIND_POS: ", cnt_fp_all)
print("NUMBER FP CORRECT: ", cnt_fp_correct)
print("FP Rate: ", cnt_fp_correct/cnt_fp_all)