import requests
import json

class ReceiptQA(object):
    def __init__(self,server_url="http://10.21.4.51:5050/"):
        self.server_url = server_url

    def ocr_total(self, ocr_text):
        response = requests.post(self.server_url, json={"in_text": ocr_text})
        if response.content:
            cont = json.loads(response.content)
            return cont['prediction']
        else:
            return "未識別到總花費，請再試多次。"
