import cv2
from ultralytics import YOLO
from icare_nlp.object_desc import ObjectDesc
from icare_nlp.utils import CvUtils
import os
from tqdm import tqdm
import time
import json
import openai
import pdb
# 加载YOLO模型
model = YOLO('yolov8n.pt')
obj_desc=ObjectDesc()


image_directory = "./test_data/object_eval/"
annotated_image_directory = "./test_data/annotated_images/"
os.makedirs(annotated_image_directory, exist_ok=True)
markdown_file_path = "./test_data/object_descriptions.md"

obj_desc_dict={}


parameters = {
            'engine': 'gpt-3.5-turbo',
            'max_tokens': 1024,
            'stop': None,
        }

system="""
The input consists of a list of object detection results and a text string in Cantonese describing the detected environment. Your task is to evaluate how correctly the text string reflects the object detection results. Additionally, assess the fluency and coherence of the language. You need to evaluate based on the following 3 aspects, each dimension with a score ranging from 0 to 1:

1. Object Correctness Score: This score assesses whether all detected objects are mentioned in the text. You can focus on the first sentence of the text string. A full score of 1 is given if all objects are mentioned. If some objects are omitted, the score should be proportionately reduced but must remain above 0. If no objects are mentioned, the score for this dimension is 0.

2. Position Correctness Score: The view includes four parts: upper left, upper right, lower left, and lower right. This score evaluates whether the descriptions of these areas for objects are generally accurate. Focus should be given to all sentences in the text string except the first one. The coordinate system starts at the top left vertex of the image, with the x-axis running horizontally from left to right, and the y-axis running vertically from top to bottom. The center of the image is located at (640, 360). The positions of objects are indicated in the format [x, y, w, h], representing the coordinates of the center of the object's detection bounding box, its width (w), and height (h). We focus on the center point of the object to determine the section it belongs to. A full score of 1 is awarded if all sections are described correctly in general. If the description of some areas is not entirely accurate, the score should be proportionally reduced but must remain above 0. A score of 0 is given if no areas are correctly described. Specifically, if an area contains no objects and there is no description of that area in the text string, such a description is considered correct.

3. Fluency and Coherence Score: This score measures the fluency and coherence of the text. If the sentence is both fluent and coherent, the score is 1. If some language is not fluent, the score should be proportionately reduced but must remain above 0. A score of 0 is given if the text is completely incoherent or not fluent.

Please must return the scores in the form: {"object correctness": obj_correct_score, "position correctness": position_correct_score, "language": fluent_and_coherent_score}.
"""

user="""
The object detect result is: {}, the text string is {}. Please return the scores in the required form without any additional words.
"""
ii=0
scores=[]
with open(markdown_file_path, 'w') as md_file:
    for filename in tqdm(sorted(os.listdir(image_directory))):
        if filename.endswith(".jpg"):
            ii+=1
            img_path = os.path.join(image_directory, filename)
            img = cv2.imread(img_path)
            cv_utils=CvUtils()
            if img is None:
                raise ValueError("Image not loaded, please check the path.")

            results = model.predict(source=img, conf=0.4, iou=0.5)
            annotated_frame = results[0].plot()

            annotated_filename = f"annotated_{filename}"
            annotated_img_path = os.path.join(annotated_image_directory, annotated_filename)
            cv2.imwrite(annotated_img_path, annotated_frame)


            obj_detect=cv_utils.form_cv_json(results)

            description=obj_desc.form_response(obj_detect)
            keys = os.getenv("OPENAI_API_KEYS").split(',')
            current_key = os.getenv("OPENAI_API_KEY")
            openai.api_key = keys[ii%6]
            response = openai.ChatCompletion.create(
                model=parameters['engine'],
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user.format(obj_detect,description)}
                ],
                max_tokens=parameters['max_tokens'],
                stop=parameters['stop'],
            )
            resp = f"{response['choices'][0]['message']['content']}"
            print(resp)
            time.sleep(6)

            md_file.write(f"\n{filename}:\n {description}\n\n")
            # obj_desc_dict[filename.replace(".jpg","")]=description
            scores.append({"obj_detect":obj_detect, "description":description, "scores": resp.strip()})


filename = 'scores.json'

# 使用with语句打开文件，确保正确关闭文件
with open(filename, 'w') as f:
    # 将字典转换为JSON格式并写入文件
    json.dump(scores, f, indent=2, ensure_ascii=False)