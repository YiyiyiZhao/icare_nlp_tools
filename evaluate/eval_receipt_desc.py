import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
from icare_nlp.receipt_desc import ReceiptDesc
from icare_nlp.receipt_qa import ReceiptQA
from tqdm import tqdm
import openai
import time
import json
# Initialize PaddleOCR with GPU support
ocr = PaddleOCR(use_gpu=True)
parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 1024,
            'stop': None,
        }
# Directories
image_directory = "./test_data/can_receipts/"
ocr_annotated_directory = "./test_data/can_receipts_ocr"
annotated_image_directory = "./test_data/annotated_receipts"

# Ensure directories exist
os.makedirs(ocr_annotated_directory, exist_ok=True)
os.makedirs(annotated_image_directory, exist_ok=True)

# Instantiate NLP tools
receipt_desc = ReceiptDesc()
receipt_qa = ReceiptQA()

# Font settings
font_path = 'zh_font.ttf'
font_size = 20
font = ImageFont.truetype(font_path, font_size)

def ocr_detect(img_path):
    # Read image
    img_cv = cv2.imread(img_path)
    if img_cv is None:
        print(f"Error loading image {img_path}")
        return None, None

    # Convert the BGR image to RGB and then to PIL Image
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img)

    # Perform OCR using PaddleOCR
    out = ocr.ocr(img_rgb, cls=True)

    text = ''
    if out:
        for line in out:
            if line:
                for entry in line:
                    vertices = entry[0]
                    entry_text = entry[1][0].strip()
                    if entry_text:
                        # Draw rectangle and text using PIL
                        draw.rectangle([tuple(vertices[0]), tuple(vertices[2])], outline=(0, 255, 0), width=2)
                        text_position = (vertices[0][0], vertices[0][1] - 10)
                        draw.text(text_position, entry_text, font=font, fill=(0, 255, 0))
                        text += entry_text + '\n'

    # Convert PIL Image back to OpenCV format
    img_anno = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return text, img_anno


receipt_desc_res_list=[]

system="""
"The input consists of an OCR detection result from a receipt and a text string in Cantonese describing the receipt summary. Your task is to evaluate how accurately the summary reflects the OCR results. Additionally, assess the fluency and coherence of the summary language. You need to evaluate based on the following two aspects, with each dimension scored from 0 to 1:

1. OCR Correctness: This score evaluates whether the summary reflects the content detected in the OCR result of the receipt. A full score of 1 is awarded if the general content corresponds to the OCR content. If none of the summary's information corresponds to the receipt, the score for this dimension is 0.

2. Fluency and Coherence Score: This score assesses the fluency and coherence of the summary. If the summary is both fluent and coherent, the score is 1. If the summary is completely incoherent or lacks fluency, the score is 0.

Please must return the scores in the format: {"ocr correctness": ocr_correct_score, "language": fluent_and_coherent_score}."

"""
user="""The ocr detect result is: {}, the text string summary is {}. Please return the scores in the required form without any additional words.
"""
ii=0
markdown_file_path = "./test_data/can_receipts/receipt_description.md"
scores=[]
with open(markdown_file_path, 'w') as md_file:
    for filename in tqdm(sorted(os.listdir(image_directory))):
        if filename.endswith(".jpg"):
            ii+=1
            print(filename)
            img_path = os.path.join(image_directory, filename)
            ocr_text, img_anno = ocr_detect(img_path)
            if img_anno is not None:
                rc_desc_res = receipt_desc.form_response(ocr_text)
                annotated_filename = f"annotated_{filename}"
                annotated_img_path = os.path.join(annotated_image_directory, annotated_filename)
                cv2.imwrite(annotated_img_path, img_anno)
                md_file.write(f"***********{filename}****************:\n {ocr_text}\n\n")

                receipt_desc_res=receipt_desc.form_response(ocr_text)
                receipt_desc_res_list.append({"filename":filename, "desc":receipt_desc_res})

                keys = os.getenv("OPENAI_API_KEYS").split(',')
                current_key = os.getenv("OPENAI_API_KEY")
                openai.api_key = keys[ii%6]
                response = openai.ChatCompletion.create(
                    model=parameters['engine'],
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user.format(ocr_text, receipt_desc_res)}
                    ],
                    max_tokens=parameters['max_tokens'],
                    stop=parameters['stop'],
                )
                resp = f"{response['choices'][0]['message']['content']}"
                print(resp)
                time.sleep(15)
                scores.append({"ocr_text": ocr_text, "description": receipt_desc_res, "scores": resp.strip()})

filename = './test_data/can_receipts/scores.json'

# 使用with语句打开文件，确保正确关闭文件
with open(filename, 'w') as f:
    # 将字典转换为JSON格式并写入文件
    json.dump(scores, f, indent=2, ensure_ascii=False)

with open("receipt_description.json", 'w', encoding="utf-8") as f:
    # 将字典转换为JSON格式并写入文件
    json.dump(receipt_desc_res_list, f, indent=2, ensure_ascii=False)

