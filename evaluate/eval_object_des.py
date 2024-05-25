import cv2
from ultralytics import YOLO
from icare_nlp.object_desc import ObjectDesc
from icare_nlp.utils import CvUtils
import os
from tqdm import tqdm
import json
import numpy as np
import pdb
# 加载YOLO模型
model = YOLO('yolov8n.pt')
obj_desc=ObjectDesc()


image_directory = "./test_data/object_eval/"
annotated_image_directory = "./test_data/annotated_images_white/"
os.makedirs(annotated_image_directory, exist_ok=True)
markdown_file_path = "./test_data/object_descriptions_v2.md"

obj_desc_dict={}

def form_cv_json(results):
    cls_def = results[0].names  # Class definitions
    cls_ids = results[0].boxes.cls.int().tolist()  # Class IDs as integers
    clses = ['hand' if cls_def[id] == 'person' else cls_def[id] for id in cls_ids]  # Convert 'person' to 'hand'
    xywh = results[0].boxes.xywh  # Bounding box coordinates
    scores = results[0].boxes.conf # Assuming the scores are accessed this way

    json_data = []
    for box, cls, score in zip(xywh.int().tolist(), clses, scores.tolist()):
        json_entry = {
            "position": box,  # Bounding box position
            "text": cls,  # Object class text
            "score": str(round(score,2))  # Confidence score of the detection
        }
        json_data.append(json_entry)
    return json_data


with open(markdown_file_path, 'w') as md_file:
    for filename in tqdm(sorted(os.listdir(image_directory))):
        if filename.endswith(".jpg"):
            img_path = os.path.join(image_directory, filename)
            img = cv2.imread(img_path)
            cv_utils=CvUtils()
            if img is None:
                raise ValueError("Image not loaded, please check the path.")

            # 使用模型进行预测
            results = model.predict(source=img, conf=0.4, iou=0.5)
            #pdb.set_trace()
            annotated_frame = results[0].plot()
            obj_detect=form_cv_json(results)

            blank_image = np.ones((720, 1280, 3), dtype=np.uint8) * 255

            for det in obj_detect:
                cx, cy, w, h = det['position']
                x1 = int(cx - w / 2)
                y1 = int(cy - h / 2)
                x2 = int(cx + w / 2)
                y2 = int(cy + h / 2)
                cv2.rectangle(blank_image, (x1, y1), (x2, y2), 2)
                cv2.putText(blank_image, det['text']+' '+det['score'], (x1, y1+50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, 1.5)

            # # 显示图像
            # cv2.imshow('Annotated Frame', blank_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            annotated_filename = f"annotated_{filename}"
            annotated_img_path = os.path.join(annotated_image_directory, annotated_filename)
            cv2.imwrite(annotated_img_path, blank_image)



            # cv2.imshow('Image Window', annotated_frame)
            # key=cv2.waitKey(0)
            # if key == ord('q'):
            #     cv2.destroyAllWindows()



            #
            # description=obj_desc.form_response(obj_detect)
            # md_file.write(f"\n{filename}:\n {description}\n\n")
            # obj_desc_dict[filename.replace(".jpg","")]=description


# filename = 'images_descriptions.json'
#
# # 使用with语句打开文件，确保正确关闭文件
# with open(filename, 'w') as f:
#     # 将字典转换为JSON格式并写入文件
#     json.dump(obj_desc_dict, f, indent=2, ensure_ascii=False)