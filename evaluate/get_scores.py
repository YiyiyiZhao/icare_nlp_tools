import json

# with open("scores.json", "r") as f:
#     data=json.load(f)
#
# obj_sc=[]
# pos_sc=[]
# lan_sc=[]
# for item in data:
#     try:
#         sc=item["scores"]
#         aa=json.loads(sc)
#         obj_sc.append(aa["object correctness"])
#         pos_sc.append(aa["position correctness"])
#         lan_sc.append(aa["language"])
#     except:
#         pass
#
# print(sum(obj_sc)/len(obj_sc))
#
# print(sum(pos_sc)/len(pos_sc))
# print(sum(lan_sc)/len(lan_sc))

with open("./test_data/can_receipts/scores.json", "r") as f:
    data=json.load(f)

ocr_sc=[]
lan_sc=[]
for item in data:
    try:
        sc=item["scores"]
        aa=json.loads(sc)
        ocr_sc.append(aa["ocr correctness"])
        lan_sc.append(aa["language"])
    except:
        pass

print(sum(ocr_sc)/len(ocr_sc))
print(len(ocr_sc))
print(sum(lan_sc)/len(lan_sc))
