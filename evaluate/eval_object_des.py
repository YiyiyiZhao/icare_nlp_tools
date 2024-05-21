import cv2
from ultralytics import YOLO
from icare_nlp.object_desc import ObjectDesc
from icare_nlp.utils import CvUtils
import os
from tqdm import tqdm
import json
import pdb
# 加载YOLO模型
model = YOLO('yolov8n.pt')
obj_desc=ObjectDesc()


image_directory = "./test_data/object_eval/"
annotated_image_directory = "./test_data/annotated_images/"
os.makedirs(annotated_image_directory, exist_ok=True)
markdown_file_path = "./test_data/object_descriptions.md"

obj_desc_dict={}

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
            annotated_frame = results[0].plot()

            annotated_filename = f"annotated_{filename}"
            annotated_img_path = os.path.join(annotated_image_directory, annotated_filename)
            cv2.imwrite(annotated_img_path, annotated_frame)

            # cv2.imshow('Image Window', annotated_frame)
            # key=cv2.waitKey(0)
            # if key == ord('q'):
            #     cv2.destroyAllWindows()


            obj_detect=cv_utils.form_cv_json(results)

            description=obj_desc.form_response(obj_detect)
            md_file.write(f"\n{filename}:\n {description}\n\n")
            obj_desc_dict[filename.replace(".jpg","")]=description


filename = 'images_descriptions.json'

# 使用with语句打开文件，确保正确关闭文件
with open(filename, 'w') as f:
    # 将字典转换为JSON格式并写入文件
    json.dump(obj_desc_dict, f, indent=2, ensure_ascii=False)