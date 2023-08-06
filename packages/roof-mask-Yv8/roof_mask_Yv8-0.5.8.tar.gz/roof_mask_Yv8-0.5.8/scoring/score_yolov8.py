import os
#import sys
import logging
import base64
import json
#import torch
#import cv2
#import requests
#import numpy as np
#from io import BytesIO
#from PIL import Image
import zipfile

from yolo_roof.geo_functions import image_download
from yolo_roof.detect_functions import load_yolov8_model, roof_condition_predict, roof_predict_5models
from yolo_roof.report_functions import generate_condition_model, generate_merged_model_damage_equip_pdf#, zip_download_file

score_logger = logging.getLogger("score_logger")
score_logger.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
score_logger.addHandler(log_handler)

def init():
    """
    """
    global yolo_roof_model
    global yolo_roof_type_model
    global yolo_roof_material_model
    global yolo_data_all_model
    global yolo_phase3_model
    global yolo_roof_condition_model

    global file_root_path
    
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)::
    zip_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "roof_model_yolov8.zip")
    
    ## deserialize the model file back into a sklearn model
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.getenv("AZUREML_MODEL_DIR"))     
    
    file_root_path = os.getenv("AZUREML_MODEL_DIR")
    # file_root_path = '../'
    
    yolo_roof_model = load_yolov8_model(os.path.join(file_root_path, "v8_roof_1280_best_on_1280.pt"))

    yolo_roof_type_model = load_yolov8_model(os.path.join(file_root_path, "v8_roof_type_1536_best.pt"))
    yolo_roof_material_model = load_yolov8_model(os.path.join(file_root_path, "v8_roof_material_1536_best.pt"))

    yolo_data_all_model = load_yolov8_model(os.path.join(file_root_path, "data_all_best.pt"))
    yolo_phase3_model = load_yolov8_model(os.path.join(file_root_path, "phase3_all_p1p2_best.pt"))

    yolo_roof_condition_model = load_yolov8_model(os.path.join(file_root_path, "v8_roof_condition_p6_1280_best.pt"))
    
    score_logger.info("ROOF: Init complete")

def run(input_data):
    """
    """
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    interface=json.loads(input_data)
    logging.info(f"run: received {interface}")

    email=interface["Receiver email"]
    business_name=interface["Business name"]
    address=interface["Address"]

    score_logger.info("run: "+f"Model is generating roof report on the property located at {address}. This property belongs to the business {business_name}. The report is requested by {email}") 
    
    try:
        image_download(address, business_name, file_root_path)
    except Exception as inst:
        err_code, err_msg = inst.args    
        logging.error(err_msg)
        return dict(status=err_code)

    score_logger.info("RL: roof model is working")
    
    input_files = 1
    roof_condition_predict(yolo_roof_condition_model, file_root_path, input_files)
    roof_predict_5models(yolo_roof_model, yolo_roof_type_model, yolo_roof_material_model,
                         yolo_data_all_model,yolo_phase3_model,file_root_path, input_files)

    score_logger.info("RL: roof model finished working")
    generate_condition_model(file_root_path) 
    generate_merged_model_damage_equip_pdf(file_root_path) 
    
    score_logger.info("RL: roof report done")
    
    #zip_download_file(file_name='roof.zip')
    #score_logger.info("RL: download file done")
    
    pdf_path = "./roof_score_new_20230101/"+address+".pdf" # bad idea hardcoding this, deal with this later
    pdf_zip_path = "./roof_score_new_20230101/"+address+".pdf.zip"

    with zipfile.ZipFile(pdf_zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as myzip:
        myzip.write(pdf_path, os.path.basename(pdf_path)) 

    with open(pdf_zip_path, mode="rb") as pdf_zip_file:
        contents=pdf_zip_file.read()  

    contents_base64=base64.b64encode(contents)
    contents_base64_utf8=contents_base64.decode("utf-8")

    result = dict()
    #score_logger.info("run: roof report is successfully generated.")
    result["status"] = 0
    result["content"] = contents_base64_utf8
    return result 
