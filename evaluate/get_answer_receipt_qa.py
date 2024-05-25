import json
import pdb
import time
from icare_nlp.receipt_qa import ReceiptQA
receipt_qa=ReceiptQA()
AE_len=0
AP_len=0
ATP_len=0

for i in range(26):
    ans_list = []
    with open(f'./test_data/ocr_gen_questions/{i}.json', 'r', encoding="utf-8") as f:
        tmp=json.load(f)
        data=json.loads(tmp)


    ae_questions=data[0]['ask_exist']
    ap_questions=data[0]['ask_price']
    atp_questions=data[0]['ask_total_price']
    print("Image ID: ", i)

    AE_len+=len(ae_questions)
    AP_len+=len(ap_questions)
    ATP_len += len(atp_questions)

    with open(f"./test_data/ocr_detect_texts/{i}.json", "r") as f:
        ocr_detect=json.load(f)
        ocr_text=ocr_detect["text"]
    for q in ae_questions:
        ans=receipt_qa.form_response(ocr_text, q)
        time.sleep(10)
        ans_list.append({"index":i, "question_type":"ask_exist", "question": q, "answer": ans})
    for q in ap_questions:
        ans=receipt_qa.form_response(ocr_text, q)
        time.sleep(10)
        ans_list.append({"index":i, "question_type":"ask_price", "question": q, "answer": ans})
    for q in atp_questions:
        ans=receipt_qa.form_response(ocr_text, q)
        time.sleep(10)
        ans_list.append({"index":i, "question_type":"ask_total_price", "question": q, "answer": ans})
    with open(f"./test_data/ocr_answers/{i}.json", "w", encoding="utf-8") as f:
        json.dump(ans_list, f, ensure_ascii=False, indent=2)

