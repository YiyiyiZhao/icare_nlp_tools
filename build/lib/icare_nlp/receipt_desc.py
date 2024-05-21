import os
import random
import openai
class ReceiptDesc(object):
    def __init__(self):
        self.receipt_desc = "呢张收据主要嘅信息包括"
        self.system = """
        Task Overview: You will be given a text string resulting from the OCR scan of a receipt, primarily in traditional Chinese characters. This receipt is typical of transactions in Hong Kong, involving Cantonese language elements, numerals, and symbols. Your job is to provide a brief summary of this receipt. The summary should include four parts: time, location, some main shopping items, and the total cost. If some information cannot be found on the receipt, simply report the information you can obtain. If you can provide additional information, ensure your output consists of fluent, concise, and coherent sentences.
        
        Additional Guidelines:
        1. If a specific product is mentioned in the receipt, consider minor inconsistencies due to scanning errors.
        2. Total Cost Calculation: Identify the total cost of the purchase. Look for keywords like "總計", "總数", or "合計" near the end of the receipt, often near the symbols 'HKD' or '$'. Extract the numerical value associated with these keywords, ensuring to report the amount as a floating-point number with two decimal places, excluding any symbols.
        
        Here is a demonstration:
        input ocr_text: "鴻星中菜旺角店\n107\n九龍旺角太子道西193號新世紀廣場6婁\n601\n-601A號鋪\n電話:2628\n0890\n賬單號碼:42414\n人數:3\n日期:2022-04-24\n時間\n12:38:42\n日\n開檔員工:霞(早市)\n2×\n黃金餃皇(位)\n38.00\n1×\n原雙明蝦燒賣皇(位)\n19.00\n1x\n四寶滑街北(精)\n53.00\n1×\n費樹牛?葉\n43.00\n1×\n鮮新竹生肉球\n43.00\n1×\n蜜汁文又燒腸粉\n(頂)\n49.00\n1×\n胡叔咸菜豬肚\n(例)\n78.00\n3×\n送\n京志燒嬰交\n(推廣)\n0.00\n1×\n糯米反\n58.00\n3X\n茗茶位\n51.00\n1×小食(碟)\n15.00\n小計:\n447.00\n服務費\n44.70\n總計:\n491.00\n"
        output summary: 您于2022年4月24日中午12点38分，在旺角新世纪广场的鸿星中菜旺角店用餐。您点了多样的菜品，包括黄金饺皇、原双明虾烧卖皇、四宝滑街北、鲜新竹生肉球等。总消费为491港币。
        """
        self.user = """小票的ocr是:{}.请输出summary."""

        self.parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 400,
            'stop': None,
        }
    def form_response(self, ocr_text):
        keys = os.getenv("OPENAI_API_KEYS").split(',')
        current_key = os.getenv("OPENAI_API_KEY")
        if current_key in keys:
            keys.remove(current_key)
        if keys:
            new_key = random.choice(keys)
            openai.api_key = new_key
        else:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model=self.parameters['engine'],
            messages=[
                {"role": "user", "content": self.system},
                {"role": "user", "content": self.user.format(ocr_text)}
            ],
            max_tokens=self.parameters['max_tokens'],
            stop=self.parameters['stop'],
        )
        resp = f"{response['choices'][0]['message']['content']}"
        if resp:
            return resp
        else:
            return "請再試一次。"

    # def ocr_process(self, ocr_text):
    #     lines = ocr_text.split('\n')
    #     chinese_per_line = []
    #     for line in lines:
    #         chinese_characters = ''.join(re.findall(r'[\u4e00-\u9fff]+', line))
    #         chinese_per_line.append(chinese_characters)
    #     chinese_text_by_line = [chinese for chinese in chinese_per_line if chinese]
    #     return chinese_text_by_line
    #
    # def form_response(self, ocr_text):
    #     zh_lines=self.ocr_process(ocr_text)
    #     return self.receipt_desc+", ".join(zh_lines)