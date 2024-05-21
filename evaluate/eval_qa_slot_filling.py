import json
from icare_nlp.object_qa import ObjectQA

obj_qa=ObjectQA()

with open("./test_data/qa_slot_filling/split_test.json") as f:
    test_data = json.load(f)
cnt=0
for item in test_data:
    question = item["text"]
    slot_gt=item["slots"]
    if "object" in slot_gt:
        gt=slot_gt["object"]
    elif "item" in slot_gt:
        gt=slot_gt["item"]
    else:
        gt=slot_gt
    pred, _=obj_qa.get_short_expression_bert(question)
    print("PRED: ", pred, "\n GT: ", gt, "\n")
    if pred==gt:
        cnt+=1

print("ACCURACY: ", round(cnt/len(test_data),2))
print(len(test_data))