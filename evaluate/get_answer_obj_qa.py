import json
import pdb
from icare_nlp.object_qa import ObjectQA

obj_qa = ObjectQA()
FP_len=0
AN_len=0
ans_list=[]
for i in range(78):
    try:
        with open(f'./test_data/obj_gen_questions/{i}.json', 'r', encoding="utf-8") as f:
            tmp=json.load(f)
            data=json.loads(tmp)

        with open(f"./test_data/obj_detect_files/{i}.json", "r") as f:
            obj_detect=json.load(f)

        if 'find_position' in data[0]:
            fp_questions=data[0]['find_position']
            for q in fp_questions:
                ans = obj_qa.form_response(q, obj_detect)
                ans_list.append({"index": i, "question_type": "find_position", "question": q, "answer": ans})

        if 'ask_near' in data[0]:
            an_questions=data[0]['ask_near']
            for q in an_questions:
                print(q)
                ans=obj_qa.form_response(q, obj_detect)
                ans_list.append({"index":i, "question_type":"ask_near", "question": q, "answer": ans})
    except:
        print("ERROR: ", i)
with open("obj_qa_answers.json", "w", encoding="utf-8") as f:
    json.dump(ans_list, f, ensure_ascii=False, indent=2)

