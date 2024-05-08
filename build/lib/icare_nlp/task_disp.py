import json

from .object_desc import ObjectDesc
from .object_qa import ObjectQA
from .receipt_desc import ReceiptDesc
from .receipt_qa import ReceiptQA

class TaskDisp(object):
    def __init__(self):
        self.intro_can="你想我幫你做咩任務？请输入对应嘅数字：1 俾我形容周围环境，2 俾我答覆关于周围环境嘅问题，3 俾我形容收据，4 俾我答覆收据嘅总费用，5 俾我形容 QR 码，同埋 6 俾我答覆关于 QR 码嘅问题。"
        self.task_id=0
        self.object_desc = ObjectDesc()
        self.object_qa=ObjectQA()
        self.receipt_desc=ReceiptDesc()
        self.receipt_qa=ReceiptQA()


    def extract_obj_detect(self, json_file):
        with open(json_file, "r") as f:
            obj_detect=json.load(f)
        return obj_detect

    def extract_ocr_text(self, json_file):
        with open(json_file, "r") as f:
            ocr_data=json.load(f)
        ocr_text=""
        for item in ocr_data:
            ocr_text+=item["text"]
        return ocr_text

    def disp_start(self):
        while True:
            print(self.intro_can)
            self.task_choice = int(input("請輸入任務編號:(1-6): "))
            if self.task_choice == 1:
                obj_detect_file=input("物件检测列表係 (json file path): ")
                obj_detect=self.extract_obj_detect(obj_detect_file)
                obj_desc_res=self.object_desc.form_response(obj_detect)
                print(obj_desc_res)
                user_task_follow=input("有冇關於嗰個場景嘅問題？如果有，輸入Yes，如果冇，輸入No.")
                if user_task_follow.lower()=="yes":
                    question = input("你嘅问题係： ")
                    obj_qa_res = self.object_qa.form_response(question, obj_detect)
                    print(obj_qa_res)
                else:
                    continue

            elif self.task_choice == 2:
                obj_detect_file = input("物件检测列表係 (json file path): ")
                obj_detect = self.extract_obj_detect(obj_detect_file)
                question = input("你嘅问题係： ")
                obj_qa_res = self.object_qa.form_response(question, obj_detect)
                print(obj_qa_res)

            elif self.task_choice == 3:
                ocr_text_file = input("OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_desc_res = self.receipt_desc.form_response(ocr_text)
                print(rc_desc_res)
                user_task_follow=input("有冇關於收據總價嘅問題？如果有，輸入Yes，如果冇，輸入No.")
                if user_task_follow.lower()=="yes":
                    rc_qa_res = self.receipt_qa.form_response(ocr_text)
                    print(rc_qa_res)
                else:
                    continue

            elif self.task_choice == 4:
                ocr_text_file = input("OCR 检测文本係 (json file path)： ")
                ocr_text = self.extract_ocr_text(ocr_text_file)
                rc_qa_res = self.receipt_qa.form_response(ocr_text)
                print(rc_qa_res)

            else:
                print("唔係有效嘅輸入，請重新輸入。")
