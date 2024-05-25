import json

with open("ocr_qa_scores.json", "r", encoding="utf-8") as f:
    data=json.load(f)

cnt_ae_all=0
cnt_ae_correct=0
cnt_ap_all=0
cnt_ap_correct=0
cnt_atp_all=0
cnt_atp_correct=0

for i in range(len(data)):
    if data[i]["question_type"]=="ask_exist":
        cnt_ae_all+=1
        if data[i]['score'] == "1":
            cnt_ae_correct += 1
    if data[i]["question_type"]=="ask_price":
        cnt_ap_all+=1
        if data[i]['score'] == "1":
            cnt_ap_correct += 1
    if data[i]["question_type"]=="ask_total_price":
        cnt_atp_all+=1
        if data[i]['score'] == "1":
            cnt_atp_correct += 1

print("NUMBER ASK_EXIST: ", cnt_ae_all)
print("NUMBER AE CORRECT: ", cnt_ae_correct)
print("AE Rate: ", cnt_ae_correct/cnt_ae_all)

print("NUMBER ASK_PRICE: ", cnt_ap_all)
print("NUMBER AP CORRECT: ", cnt_ap_correct)
print("AP Rate: ", cnt_ap_correct/cnt_ap_all)

print("NUMBER ASK_Total_PRICE: ", cnt_atp_all)
print("NUMBER ATP CORRECT: ", cnt_atp_correct)
print("ATP Rate: ", cnt_atp_correct/cnt_atp_all)