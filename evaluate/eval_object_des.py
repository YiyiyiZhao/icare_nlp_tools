import cv2
from ultralytics import YOLO
from icare_nlp.object_desc import ObjectDesc
from icare_nlp.utils import CvUtils
import os
from tqdm import tqdm
# 加载YOLO模型
model = YOLO('yolov8n.pt')
obj_desc=ObjectDesc()


image_directory = "./test_data/object_eval/"
markdown_file_path = "./test_data/object_descriptions.md"

with open(markdown_file_path, 'w') as md_file:
    for filename in tqdm(os.listdir(image_directory)):
        if filename.endswith(".jpg"):
            img_path = os.path.join(image_directory, filename)
            img = cv2.imread(img_path)
            cv_utils=CvUtils()
            if img is None:
                raise ValueError("Image not loaded, please check the path.")

            # 使用模型进行预测
            results = model(img)
            results = model(img)
            annotated_frame = results[0].plot()

            # cv2.imshow('Image Window', annotated_frame)
            # key=cv2.waitKey(0)
            # if key == ord('q'):
            #     cv2.destroyAllWindows()


            obj_detect=cv_utils.form_cv_json(results)
            description=obj_desc.form_response(obj_detect)
            md_file.write(f"![]({img_path})\n{description}\n\n")
