import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

cls_model = "Yiyiyiyiyi/icare_task_disp_bert"
tokenizer = AutoTokenizer.from_pretrained(cls_model)
model = AutoModelForSequenceClassification.from_pretrained(cls_model)
model.eval()

with open("test_data/task_disp/test_td.json", "r" , encoding= "utf-8") as f:
    test_data=json.load(f)

pred_list, gt_list=[], []
for test_item in test_data:
    inputs = tokenizer(test_item["text"], return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=-1)
        pred_id=prediction.item()
        gt_id = int(model.config.label2id[test_item["label"]])
    pred_list.append(pred_id)
    gt_list.append(gt_id)


print(pred_list)
print(gt_list)

import evaluate
precision_metric = evaluate.load('precision')
recall_metric = evaluate.load('recall')
f1_metric = evaluate.load('f1')

y_true=gt_list
y_pred=pred_list

# 计算指标
precision_result = precision_metric.compute(predictions=y_pred, references=y_true, average='macro')
recall_result = recall_metric.compute(predictions=y_pred, references=y_true, average='macro')
f1_result = f1_metric.compute(predictions=y_pred, references=y_true, average='macro')

print("Precision (Macro):", precision_result['precision'])
print("Recall (Macro):", recall_result['recall'])
print("F1 Score (Macro):", f1_result['f1'])

#go to "https://huggingface.co/Yiyiyiyiyi/icare_task_disp_bert"

#Precision (Macro): 1.0
#Recall (Macro): 1.0
#F1 Score (Macro): 1.0