import os
import json
import time
import openai

# obj_detect_dir="./test_data/ocr_detect_files"
ocr_detect_dir="./test_data/ocr_detect_texts/"
parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 512,
            'stop': None,
        }


# prefix="""
# You are a question generation system designed to produce synthetic data in the form of questions. These questions are in local Hong Kong Cantonese and are used to test the capabilities of a question answering system. You are required to generate questions mainly in two categories, the first concerning the direction of an object (relative to the hand or the center of the field of view), and the second concerning what objects are near a specified object. Examples of questions include: "我點樣可以攞到椅子？" , "laptop喺邊？", "電視喺我手嘅邊個方向？" , "電視機附近有冇其他物體？".
#
#  Given an object detection list like this: """
#
# suffix="""what questions might you ask? Please must return 1-3 Cantonese questions for each category. The response format should be in json format, for example: [{"find_position": [q1, q2, q3], "ask_near": [q1]}]"""
prefix="""
You are a question generation system designed to produce synthetic data in the form of questions. These questions are in local Hong Kong Cantonese and are used to test the capabilities of a question answering system. You are required to generate questions mainly in three categories: the first concerning the existence of a specific product, the second concerning the price of a product, and the third about asking the total cost of this shopping. Examples of questions include: "请问有冇咖啡？" (Is there any coffee available?), "糖醋排骨要几多钱？" (How much does sweet and sour pork cost?), "我今次购物一共用几多钱？" (How much is the total cost of this shopping?).

Given an OCR result like this: """

suffix="""what questions might you ask? Please return 1-3 Cantonese questions for each category. The response format should be in JSON format, for example: [{"ask_exist": [q1, q2, q3], "ask_price":[q1, q2, q3], "ask_total_price": [q1]}]"""

gen_questions=[]
for ii in range(78):
    with open(os.path.join(ocr_detect_dir, f"{ii}.json"), "r", encoding="utf-8") as f:
        data=json.load(f)
    text=data["text"]
    keys = os.getenv("OPENAI_API_KEYS").split(',')
    current_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = keys[ii % 5]
    response = openai.ChatCompletion.create(
        model=parameters['engine'],
        messages=[
            {"role": "user", "content": prefix+str(text)+suffix}
        ],
        max_tokens=parameters['max_tokens'],
        stop=parameters['stop'],
    )
    resp = f"{response['choices'][0]['message']['content']}"
    print(resp)
    time.sleep(6)
    with open(f"./test_data/ocr_gen_questions/{ii}.json", "w", encoding="utf-8") as f:
        json.dump(resp, f, ensure_ascii=False, indent=4)


