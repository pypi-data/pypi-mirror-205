import os
import numpy as np
from pycocotools.coco import COCO
from tqdm import tqdm
import json 
import uuid
import pandas as pd
import math
import cv2
import re

### report ###
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

### detectron2 ###
from detectron2.data import DatasetCatalog
from detectron2.data.datasets.coco import register_coco_instances 
from detectron2.data.detection_utils import read_image
from detectron2.data import detection_utils as utils
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer_new import Visualizer
from detectron2.utils.visualizer import Visualizer as Vis_box
from detectron2.utils.visualizer_new import ColorMode
from detectron2.engine.defaults import DefaultPredictor
from detectron2.data import MetadataCatalog

#### shapely ###
import shapely
import shapely.wkt
from shapely.geometry import Polygon, MultiPoint

## PDF
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

## ZIP
import zipfile

# email
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart

### Function for target address center lat long computation ###
def image_info_to_center_lat_lon(image_info, zoom, flag = 1):
    '''
    image_info is '[topleft tile x,
                    topleft tile y,
                    bottom right tile x,
                    bottom right tile y]'
    flag = 0 : NW-corner of the square
    flag = 1 : center
    flag = 2 : Other corner
    '''
    image_info_array = image_info.split(',')
    if flag == 0:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]))//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]))//2
    
    elif flag == 1:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]) + 1)//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]) + 1)//2

    elif flag ==2:
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]) + 2)//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]) + 2)//2
    else:
        print('flag is not defined. Using NW-corner of the square')
        xtile = (int(image_info_array[0][1:]) + int(image_info_array[2]))//2
        ytile = (int(image_info_array[1]) + int(image_info_array[3][:-1]))//2

    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return [lat_deg, lon_deg]


def generate_referral_json(demoFolder, coco_json, new_cat, new_json_file_name):
    catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
    # Obtain the category names
    categories = coco_json.loadCats(catIds)
    new_categories = [x['name'] for x in categories if x['name'] in new_cat]
    new_catIds = coco_json.getCatIds(catNms=new_categories, supNms=[], catIds=[])
    # print(new_catIds)
    imgIds = coco_json.getImgIds()
    
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1

    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)

        ann_start = ann_id
        for ann in annotations:
            # print(ann)
            # class selection
            if ann['category_id'] in new_catIds:
                
                # append annotation to coco jason file list
                new_annotations.append({"id": ann_id,
                                        "image_id": new_image_id,
                                        "category_id": ann['category_id'],
                                        "iscrowd": 0,
                                        # "area": ann['area'],
                                        "bbox": ann['bbox'],
                                        "segmentation": ann['segmentation']
                                        })
                # get new annotation id
                ann_id += 1

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)

def generate_referral_damage_json(demoFolder, coco_json, roof_boundary_json, new_cat, new_json_file_name):
    catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
    # Obtain the category names
    categories = coco_json.loadCats(catIds)
    new_categories = [x['name'] for x in categories if x['name'] in new_cat]
    new_catIds = coco_json.getCatIds(catNms=new_categories, supNms=[], catIds=[])
    # print(new_catIds)
    imgIds = coco_json.getImgIds()
    
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1

    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)
        
        roof_poly = Polygon()
        # get image information
        coco_img_info = roof_boundary_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = roof_boundary_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        roof_annotations = roof_boundary_json.loadAnns(annIds)
        for ann in roof_annotations:
            for seg in ann['segmentation']:
                mask = np.array(seg).reshape(len(seg) // 2, 2)
                poly = Polygon(mask)
                roof_poly = roof_poly.union(poly)
        
        # roof_poly = roof_poly.buffer(5.0)
        
        ann_start = ann_id
        for ann in annotations:
            # print(ann)
            # class selection
            if ann['category_id'] in new_catIds:
                current_poly = Polygon()
                for seg in ann['segmentation']:
                    mask = np.array(seg).reshape(len(seg) // 2, 2)
                    new_poly = Polygon(mask)
                    current_poly = current_poly.union(new_poly)

                if not current_poly.intersects(roof_poly):
                    continue
                else:
                    intersection_poly = current_poly.intersection(roof_poly)
                    
                if intersection_poly.geom_type == 'MultiPolygon':
                    for current_mask in intersection_poly.geoms:
                        if current_mask.area < 25:
                            continue
                        current_polygon_list = current_mask.exterior.coords
                        coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_mask.exterior.coords) * 2).tolist()
                        # append annotation to coco jason file list
                        new_annotations.append({"id": ann_id,
                                                "image_id": new_image_id,
                                                "category_id": ann['category_id'],
                                                "iscrowd": 0,
                                                # "area": ann['area'],
                                                "bbox": ann['bbox'],
                                                "segmentation": coco_segmentation_format
                                                })
                        # get new annotation id
                        ann_id += 1
                elif intersection_poly.geom_type == 'Polygon':
                    if intersection_poly.area < 25:
                        continue
                    current_polygon_list = intersection_poly.exterior.coords
                    coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_polygon_list) * 2).tolist()
                    # append annotation to coco jason file list
                    new_annotations.append({"id": ann_id,
                                            "image_id": new_image_id,
                                            "category_id": ann['category_id'],
                                            "iscrowd": 0,
                                            # "area": ann['area'],
                                            "bbox": ann['bbox'],
                                            "segmentation": coco_segmentation_format
                                            })
                    # get new annotation id
                    ann_id += 1             

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)

        
def generate_multi_model_referral_roof_boundary_based_json(demoFolder, coco_jsons, roof_boundary_json, new_cats, new_json_file_name):
    # new json file name
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1
    new_catIds = []
    category_names = []
    new_categories =[]
    
    total_images = len(coco_jsons[0].getImgIds())
    for i, new_cat in enumerate(new_cats):
        new_categories.append({'id': i, 'name': f'{new_cats[i]}'})
    
    for coco_json in coco_jsons:
        catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
        # Obtain the category names
        categories = coco_json.loadCats(catIds)
        category_names.append(categories)
        new_category_names = [x['name'] for x in categories if x['name'] in new_cats]
        new_catIds.append(coco_json.getCatIds(catNms=new_category_names, supNms=[], catIds=[]))
    
    for img_id in range(total_images):
        for i, coco_json in enumerate(coco_jsons):
            imgIds = coco_json.getImgIds()
            # get image information
            coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
            # get the raw image annotations Id
            annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
            # get annotations from annotation Id
            annotations = coco_json.loadAnns(annIds)

            roof_poly = Polygon()
            # get image information
            coco_img_info = roof_boundary_json.loadImgs(imgIds[img_id])[0]
            # get the raw image annotations Id
            annIds = roof_boundary_json.getAnnIds(imgIds=coco_img_info['id'])
            # get annotations from annotation Id
            roof_annotations = roof_boundary_json.loadAnns(annIds)
            for ann in roof_annotations:
                for seg in ann['segmentation']:
                    mask = np.array(seg).reshape(len(seg) // 2, 2)
                    poly = Polygon(mask)
                    roof_poly = roof_poly.union(poly)

            roof_poly = roof_poly.buffer(5.0)

            ann_start = ann_id
            for ann in annotations:
                # print(ann)
                # class selection
                if ann['category_id'] in new_catIds[i]:
                    # get the class name
                    cat_name = coco_json.loadCats(ann['category_id'])[0]['name']
                    # get new class id
                    category_id = new_cats.index(cat_name)
                    current_poly = Polygon()
                    for seg in ann['segmentation']:
                        mask = np.array(seg).reshape(len(seg) // 2, 2)
                        new_poly = Polygon(mask)
                        current_poly = current_poly.union(new_poly)

                    if not current_poly.intersects(roof_poly):
                        continue
                    else:
                        intersection_poly = current_poly.intersection(roof_poly)

                    if intersection_poly.geom_type == 'MultiPolygon':
                        for current_mask in intersection_poly.geoms:
                            if current_mask.area < 25:
                                continue
                            current_polygon_list = current_mask.exterior.coords
                            coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_mask.exterior.coords) * 2).tolist()
                            # append annotation to coco jason file list
                            new_annotations.append({"id": ann_id,
                                                    "image_id": new_image_id,
                                                    "category_id": category_id,
                                                    "iscrowd": 0,
                                                    # "area": ann['area'],
                                                    "bbox": ann['bbox'],
                                                    "segmentation": coco_segmentation_format
                                                    })
                            # get new annotation id
                            ann_id += 1
                    elif intersection_poly.geom_type == 'Polygon':
                        if intersection_poly.area < 25:
                            continue
                        current_polygon_list = intersection_poly.exterior.coords
                        coco_segmentation_format = np.array(current_polygon_list).reshape(1, len(current_polygon_list) * 2).tolist()
                        # append annotation to coco jason file list
                        new_annotations.append({"id": ann_id,
                                                "image_id": new_image_id,
                                                "category_id": category_id,
                                                "iscrowd": 0,
                                                # "area": ann['area'],
                                                "bbox": ann['bbox'],
                                                "segmentation": coco_segmentation_format
                                                })
                        # get new annotation id
                        ann_id += 1             

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": new_categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)

        
class ReferralPoints:
    '''
    Read in referral rules and generate the csv format:
    Address    Total points    each referral elemten
      aaa          3              3  
    '''

    def __init__(self, referral_file, index):
        with open(referral_file) as f1:
            self.ref_json = json.load(f1)
        self.score = {'Address': index}
        self.score.update(dict(('number of ' + score_cat, 0) for score_cat in self.ref_json))
        self.score.update({'Total points': 0})
        self.score.update(dict((score_cat, 0) for score_cat in self.ref_json))
        self.score.update({'Roof area (pixels)': 0})

        self.score_cat = [x for x in self.ref_json]

        self.buffer = dict((score_cat,{'area_percentage': 0, 'count': 0}) for score_cat in self.ref_json)
        self.buffer.update({'Roof_boundary': 0})
        
        # print(self.score_cat)
        # print(self.buffer)

    def set_points(self, cat, points=0):
        self.score[cat] = points

    def update_total_points(self):
        for cat in self.score_cat:
            score = self.score[cat]
            self.score['Total points'] += score
            # print(f'{cat}:, {score}')

    def obtation_roof_boundary(self, predict_result,image_id):
        # get the image annotations ids
        annIds = predict_result.getAnnIds(imgIds=image_id)
        # get annotations from annotation ids
        annotations = predict_result.loadAnns(annIds)
        self.roof_poly = Polygon()
        for ann in annotations:
            for seg in ann['segmentation']:
                mask = np.array(seg).reshape(len(seg) // 2, 2)
                poly = Polygon(mask)
                self.roof_poly = self.roof_poly.union(poly)
                poly_area = poly.area
                self.buffer['Roof_boundary'] += poly_area
    
        ### compute roof area
        self.score['Roof area (pixels)'] = self.buffer['Roof_boundary']
        self.roof_poly = self.roof_poly.buffer(5.0) #add a buffer for HVAC which are located on the ground
        # aaa = self.buffer['Roof_boundary']
        # # print(poly)
        # print(f'roof {aaa*0.0002}')
        
    def update_buffer_value(self, predict_result, labels, image_id):
        # get the image annotations ids
        annIds = predict_result.getAnnIds(imgIds=image_id)
        # get annotations from annotation ids
        annotations = predict_result.loadAnns(annIds)
        # print(len(annotations))

        # update referral buffer
        for ann in annotations:
            if labels[ann['category_id']] in self.score_cat:
                                
                # if this instance is detected 'area_percentage' + current mask area
                for seg in ann['segmentation']:
                    mask = np.array(seg).reshape(len(seg) // 2, 2)
                    poly = Polygon(mask)
                    self.current_poly = poly
                    if not self.current_poly.intersects(self.roof_poly):
                        continue
                    poly_area = poly.area
                    poly_percentage = poly_area / (self.buffer['Roof_boundary'] + 1)
                    self.buffer[labels[ann['category_id']]]['area_percentage'] += poly_percentage
                    
                    # print(poly)
                    # class_label = labels[ann['category_id']]
                    # print(f'{class_label} poly_area {poly_area}')

                if not self.current_poly.intersects(self.roof_poly):
                    continue
                # if this instance is detected 'count' + 1
                self.buffer[labels[ann['category_id']]]['count'] += 1
                self.score['number of '+ labels[ann['category_id']]] +=1
                    
        # for each cat
        for referral_cat in self.score_cat:
            # for each value section
            for referral_value in self.ref_json[referral_cat]:
                # for each referral type
                for refferal_type in self.buffer[referral_cat]:
                    # print(refferal_type)
                    if refferal_type == referral_value['type']:
                        # if current value is not 0 and current value is in the value section
                        # and the new value is larger than the old value
                        # update the value
                        if self.buffer[referral_cat][refferal_type]!=0:
                            if referral_value['min'] <= self.buffer[referral_cat][refferal_type] < referral_value['max']:
                                if referral_value['point'] > self.score[referral_cat]:
                                    self.set_points(referral_cat, points=referral_value['point'])
                # print(referral_cat)
                # print(self.buffer[referral_cat])  

                
def generate_displayed_polygones(image_folder,json_file,trainingDataset):
    allColors = [(0,0,255), (255,0,0), (125,75,255), (255,255,0), (255,0,255), (0,255,255), (75,125,255), (125,75,255), (75,255,125), (125,255,75), (255,125,75), (255,75,125)]*8
    filename = str(uuid.uuid4())
    register_coco_instances(filename, {'thing_colors':allColors}, json_file, image_folder)
    metadata = MetadataCatalog.get(filename)
    dicts = DatasetCatalog.get(filename)
    model_folder = os.path.join(image_folder,'prediction_' + trainingDataset)
    print(f"Generating {trainingDataset} polygons")
    for dic in dicts:
        img = utils.read_image(dic["file_name"], "RGB")
        visualizer = Visualizer(img, metadata=metadata, instance_mode=ColorMode.SEGMENTATION)
        vis = visualizer.draw_dataset_dict(dic)
        out_filename = os.path.join(os.path.splitext(os.path.basename(dic["file_name"]))[0],trainingDataset +'_merged.jpg')
        
        out_filename2_extention = os.path.splitext(os.path.basename(dic["file_name"]))[1]
        out_filename2 = os.path.basename(dic["file_name"]).replace(out_filename2_extention,'_merged'+out_filename2_extention)
        vis.save(os.path.join(image_folder,out_filename))
        # vis.save(os.path.join(model_folder,out_filename2)) # model folder is not necessary
    print("Gereating Finished.")
    return vis


def generate_displayed_condition_polygones_and_colors(image_folder,json_file,trainingDataset):
    coco_json = COCO(json_file)
    imgIds = coco_json.getImgIds()

    print(f"Merging {trainingDataset} polygons")
    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)

        img = cv2.imread(os.path.join(image_folder,coco_img_info['file_name']))

        for i, ann in enumerate(annotations):
            bbox = ann['bbox']
            score = int(ann['scores'])

            if score < 40:
                condition_color = (0,0,255) # red
            elif score >70:
                condition_color = (0,255,0) # green
            else:
                condition_color = (0,255,255) # yellow

            img = cv2.putText(img, str(i+1), (int(bbox[0]+5),int(bbox[1]+30)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                       fontScale=1, color=condition_color, thickness=2, lineType=cv2.LINE_AA)
            img = cv2.rectangle(img, (int(bbox[0]),int(bbox[1])), (int(bbox[0] + bbox[2]),int(bbox[1] + bbox[3])), color=condition_color, thickness=3)
        
        out_filename = os.path.join(os.path.splitext(coco_img_info["file_name"])[0], trainingDataset +'_merged.jpg')
        cv2.imwrite(os.path.join(image_folder,out_filename),img)

    print("Merging Finished.")
    return img


def generate_referral_condition_json(demoFolder, coco_json, new_json_file_name):
    catIds = coco_json.getCatIds(catNms=[], supNms=[], catIds=[])
    categories = coco_json.loadCats(catIds)    
    imgIds = coco_json.getImgIds()
    new_json_file = os.path.join(demoFolder, new_json_file_name)
    new_images = []
    new_annotations = []
    ann_id = 1
    new_image_id = 1
    
    ###
    weights = np.array([0, 50, 100])
    ###
    
    for img_id in range(len(imgIds)):
        # get image information
        coco_img_info = coco_json.loadImgs(imgIds[img_id])[0]
        # get the raw image annotations Id
        annIds = coco_json.getAnnIds(imgIds=coco_img_info['id'])
        # get annotations from annotation Id
        annotations = coco_json.loadAnns(annIds)

        ann_start = ann_id
        for ann in annotations:
            if ann['area'] < 100*100:
                continue
            score = np.array(ann['scores'])
            new_score = weights.dot(score/score.sum())
            # append annotation to coco jason file list
            new_annotations.append({"id": ann_id,
                                    "image_id": new_image_id,
                                    "category_id": ann['category_id'],
                                    "iscrowd": 0,
                                    "area": ann['area'],
                                    "scores": new_score,
                                    "bbox": ann['bbox'],
                                    # "segmentation": ann['segmentation']
                                    })
            # get new annotation id
            ann_id += 1

        # get new image id
        new_image_id += 1
        # append image information to coco jason file list
        new_images.append(coco_img_info)

    info = {"year": 2022,
            "version": "1.0",
            "description": "Phase 2 data and coco json file",
            "contributor": "Ruixu Liu, Delin Shen, Aaron Lee and Qiang Wang",
            }

    json_data = {"info": info,
                 "categories": categories,
                 "images": new_images,
                 "annotations": new_annotations
                 }

    with open(new_json_file, "w") as jsonfile:
        json.dump(json_data, jsonfile, sort_keys=True, indent=4)
  
    
def generate_condition_model(file_root_path, demoFolder = 'roof_score_new_20230101'):
    pred_condition_file = os.path.join(demoFolder,'prediction_Roof_condition_three_classes/Roof_condition_three_classes_all_in_one.json')
    pred_condition = COCO(pred_condition_file)
    generate_referral_condition_json(demoFolder, pred_condition,'Referral_condition.json')
    vis_out = generate_displayed_condition_polygones_and_colors(demoFolder,os.path.join(demoFolder, 'Referral_condition.json'),'Roof_condition_three_classes')
    
    referral_condition = COCO(os.path.join(demoFolder, 'Referral_condition.json'))
    all_condition_score = []
    for referral_condition_id in referral_condition.getImgIds():
        coco_img_info = referral_condition.loadImgs(referral_condition_id)[0]
        address = os.path.splitext(coco_img_info['file_name'])[0]
        condition_dict = {'Address': address}
        condition_dict.update({'main_condition': 0})
        # get the image annotations ids
        annIds = referral_condition.getAnnIds(imgIds=referral_condition_id)
        # get annotations from annotation ids
        annotations = referral_condition.loadAnns(annIds)
        condition_text = ''
        area = []
        score = []
        max_area = 0
        for ann in annotations:
            # add new area condition score
            condition_text+=str(ann['area']) + ':' + str(int(ann['scores'])) + ','
            # update the major area condition
            if ann['area'] > max_area:
                condition_dict['main_condition'] = int(ann['scores'])
                max_area = ann['area']
            # update the weight condition
            area.append(ann['area'])
            score.append(ann['scores'])
        condition_dict.update({'Over_all_condition': np.array(area).dot(np.array(score))/sum(area)})
        condition_dict.update({'condition_details': condition_text})
        all_condition_score.append(condition_dict)
        df = pd.DataFrame.from_dict([condition_dict])
        df.to_csv(os.path.join(demoFolder,address+'/condition_referral.csv'), index=False, header=True)
    df = pd.DataFrame.from_dict(all_condition_score)
    df.to_csv(os.path.join(demoFolder,'all_condition.csv'), index=False, header=True)

def generate_merged_model_damage_equip_pdf(file_root_path, demoFolder = 'roof_score_new_20230101'):
    pred_phase3_file = os.path.join(demoFolder,'prediction_Phase3_equipment_damage/Phase3_equipment_damage_all_in_one.json')
    pred_data_all_file = os.path.join(demoFolder, 'prediction_Data_all_equipment_damage/Data_all_equipment_damage_all_in_one.json')
    pred_boundary_file =os.path.join(demoFolder, 'prediction_Roof_boundary/Roof_boundary_all_in_one.json')
    # Load prediction file as COCO formate
    pred_phase3 = COCO(pred_phase3_file)
    pred_data_all = COCO(pred_data_all_file)
    pred_boundary = COCO(pred_boundary_file)
    # read in referral rules and create corresponding functions
    referral_label_file = os.path.join(file_root_path,'referral_labels_20230315.json')
    referral_damage_label_file = os.path.join(file_root_path,'referral_labels_20230421_for_merged_damage.json')
    referral_equip_label_file = os.path.join(file_root_path,'referral_labels_20230421_for_merged_equip.json')
    
    with open(referral_damage_label_file) as f1:
        ref_json = json.load(f1)
        cat_damage = [x for x in ref_json]
    generate_multi_model_referral_roof_boundary_based_json(demoFolder, [pred_data_all, pred_phase3], pred_boundary,cat_damage,'Referral_damage_all.json')
    
    with open(referral_equip_label_file) as f1:
        ref_json = json.load(f1)
        cat_equip = [x for x in ref_json]
    generate_multi_model_referral_roof_boundary_based_json(demoFolder, [pred_data_all, pred_phase3], pred_boundary, cat_equip,'Referral_equipment_all.json')

    vis_out = generate_displayed_polygones(demoFolder,os.path.join(demoFolder, 'Referral_damage_all.json'),'Damage')
    vis_out = generate_displayed_polygones(demoFolder,os.path.join(demoFolder, 'Referral_equipment_all.json'),'Equipment')

    ################################### Referral
    referral_damage = COCO(os.path.join(demoFolder, 'Referral_damage_all.json'))
    referral_equip = COCO(os.path.join(demoFolder, 'Referral_equipment_all.json'))
    referral_output = []
    # Obtain the category ID numbers
    catIds = referral_damage.getCatIds()
    # Obtain the category names
    categories = referral_damage.loadCats(catIds)
    # Id2catname
    Damage_labels = [value['name'] for value in categories]

    # Obtain the category ID numbers
    catIds = referral_equip.getCatIds()
    # Obtain the category names
    categories = referral_equip.loadCats(catIds)
    # Id2catname
    Equipment_labels = [value['name'] for value in categories]

    for damage_img_id, equp_image_id in zip(referral_damage.getImgIds(), referral_equip.getImgIds()):
        assert referral_damage.loadImgs(damage_img_id) == referral_equip.loadImgs(equp_image_id)
        # get image information
        coco_img_info = referral_damage.loadImgs(damage_img_id)[0]
        address = os.path.splitext(coco_img_info['file_name'])[0]
        print(address)

        new_referral = ReferralPoints(referral_label_file, index=address) 

        # Roof Boundary
        new_referral.obtation_roof_boundary(pred_boundary, image_id = coco_img_info['id'])

        # Damage
        #################################################
        new_referral.update_buffer_value(referral_damage, Damage_labels, image_id = coco_img_info['id'] )

        # Equipment
        #################################################
        new_referral.update_buffer_value(referral_equip, Equipment_labels, image_id = coco_img_info['id'])

        # update total points
        new_referral.update_total_points()
        referral_output.append(new_referral.score)
        df = pd.DataFrame.from_dict([new_referral.score])
        df.to_csv(os.path.join(demoFolder,address+'/referral.csv'), index=False, header=True)

    df = pd.DataFrame.from_dict(referral_output)
    df.to_csv(os.path.join(demoFolder,'all_referral.csv'), index=False, header=True)
    image_csv = pd.read_csv(os.path.join(demoFolder,"image.csv"))
    referral_csv = pd.read_csv(os.path.join(demoFolder,"all_referral.csv"))
    condition_csv = pd.read_csv(os.path.join(demoFolder,"all_condition.csv"))

    image_csv.merge(condition_csv,how='outer',on='Address').to_csv(os.path.join(demoFolder, 'all_address.csv'), index=False, header=True)
    all_address_csv =  pd.read_csv(os.path.join(demoFolder,"all_address.csv"))
    all_address_csv.merge(referral_csv,how='outer',on='Address').to_csv(os.path.join(demoFolder, 'all_address.csv'), index=False, header=True)
    
    ################################################################# PDF
    image_csv = pd.read_csv(os.path.join(demoFolder,'image.csv'))
    referral_csv = pd.read_csv(os.path.join(demoFolder,'all_referral.csv'))
    all_address_csv = pd.read_csv(os.path.join(demoFolder, 'all_address.csv'))
    # Today_date = datetime.today().strftime('%Y-%m-%d')
    # # print(Today_date)
    full_address = all_address_csv["Address"].tolist()
    insured_name = all_address_csv["InsuredName"].tolist()
    image_date = all_address_csv["Image date"].tolist()
    image_info = all_address_csv["Image info"].tolist()
    zoom_level = all_address_csv["Image level"].tolist()
    main_roof_condition_score = all_address_csv["main_condition"].tolist()
    overall_roof_condition_score = all_address_csv["Over_all_condition"].tolist()
    all_roof_condition_score = all_address_csv["condition_details"].tolist()

    key_name = all_address_csv.columns
    HVAC_index = all_address_csv.columns.get_loc('number of HVAC/Cooling tower')
    Tarp_index = all_address_csv.columns.get_loc('number of Tarp')
    key_name_index = all_address_csv.columns.get_loc('Total points')
    gsd_key = all_address_csv.columns.get_loc('Image gsd (meters/pixels)')
    pixels_area_key = all_address_csv.columns.get_loc('Roof area (pixels)')
    
    
    # print(key_name[key_name_index])

    for address_index in range(len(full_address)):
        address = full_address[address_index]
        row = all_address_csv.iloc[address_index]
        print(f'index:{address_index}, address:{address}')
        if np.isnan(row[key_name_index]):
            continue
        # initializing variables with values
        url_zoom_level = zoom_level[address_index]
        cat_lon_coord = image_info_to_center_lat_lon(image_info[address_index], url_zoom_level)
        url_lat = cat_lon_coord[0]
        url_lon = cat_lon_coord[1]
        url_date = image_date[address_index].replace('-','')
        url = f'https://apps.nearmap.com/maps/#/@{url_lat},{url_lon},{url_zoom_level}z,0d/V/{url_date}'

        fileName = os.path.join(demoFolder,address+'.pdf')
        documentTitle = f'Refferal'
        title = f'{insured_name[address_index]}'
        subTitle = address

        Damage_image_name = os.path.join(demoFolder,address+'/Damage_merged.jpg')
        Equipment_image_name = os.path.join(demoFolder,address+'/Equipment_merged.jpg')
        # Equipment_image_name = os.path.join(demoFolder,address+'/Roof_condition_three_classes_merged.jpg')
        Roof_condition_image_name = os.path.join(demoFolder,address+'/Roof_condition_three_classes_merged.jpg')

        pdf = canvas.Canvas(fileName)
        pdf.setTitle(documentTitle)
        pdf.setFont("Times-Roman", 14)
        pdf.drawCentredString(300, 800, title)

        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Times-Roman", 12)
        pdf.drawCentredString(290, 770, subTitle)

        # drawing a line
        pdf.line(30, 760, 550, 760)

        # information
        text = pdf.beginText(40, 740)
        text.setFont("Courier", 12)
        text.setFillColor(colors.black)
        text.textLine(f'Image date: {image_date[address_index]}')

        # line = f'Roof conditon score: {roof_condition_score[address_index]}'
        line = 'Roof condition (roof number/score) : '
        roof_socres = re.findall(r'\:(.*?)\,',all_roof_condition_score[address_index])
        for i in range(len(roof_socres)):
            if i%8==0:
                text.textLine(line)
                line = ''
            line+= f'#{i+1}/{roof_socres[i]}  '
        
        text.textLine(line)
        total_point = 0

############################### SB referral 2.1
        total_score = overall_roof_condition_score[address_index]
        if key_name[i] == 'Tarp' and row[i]>0:
            if row[Tarp_index] == 1:
                total_score/= 2
            else:
                total_score/= 4
        tmp_point = 0
        for i in range(key_name_index+1, len(key_name)):
            if key_name[i] == 'HVAC/Cooling tower'and row[i]>0:
                tmp_point += row[i]*1
            elif key_name[i] == 'Pipeline'and row[i]>0:
                tmp_point += row[i]*1
            elif key_name[i] == 'Solar panel'and row[i]>0:
                tmp_point += row[i]*1
                
        total_score = total_score * (7-tmp_point)/7
        
        line= f'Overall score (condition and equipment): {int(total_score)}'
        text.textLine(line)
        text.setFillColor(colors.blue)
        #################################
        for i in range(key_name_index+1, len(key_name)):
            if i == pixels_area_key:
                gsd_area = row[gsd_key] * row[gsd_key] * row[pixels_area_key]
                # text.textLine(f'Roof area: {int(gsd_area)} m\u00b2')
                text.textLine(f'Roof area: {int(gsd_area * 10.764)} ft\u00b2')
                continue
            if int(row[i]) == 0:
                line = key_name[i] + ': ' + 'Not detected'
                # text.textLine(line)     # Hide no detected case
            elif int(row[i]) == 1:
                if key_name[i] == 'Pipeline' or key_name[i] =='Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                if key_name[i] == 'Staining' or key_name[i] =='Water pooling' or key_name[i] =='Other damage':
                    line = key_name[i] + ': ' + 'Minor'
                    text.textLine(line)
                if key_name[i] == 'Skylight':
                    line = key_name[i] + ': ' + 'Minimal'
                    text.textLine(line)
                if key_name[i] =='HVAC/Cooling tower':
                    # line = key_name[i] + ': ' + 'Minimal'
                    line = key_name[i] + ': ' + f'Minimal ({row[HVAC_index]})'
                    text.textLine(line)
            elif int(row[i]) == 2:
                if key_name[i] == 'Pipeline' or key_name[i] =='Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                if key_name[i] == 'Staining' or key_name[i] =='Water pooling' or key_name[i] =='Other damage':
                    line = key_name[i] + ': ' + 'Moderate'
                    text.textLine(line)
                if key_name[i] == 'Skylight' :
                    line = key_name[i] + ': ' + 'A few'
                    text.textLine(line)
                if key_name[i] =='HVAC/Cooling tower':
                    # line = key_name[i] + ': ' + 'A few'
                    line = key_name[i] + ': ' + f'A few ({row[HVAC_index]})'
            else:
                if key_name[i] == 'Pipeline' or key_name[i] =='Solar panel': 
                    line = key_name[i] + ': ' + 'Detected'
                    text.textLine(line)
                if key_name[i] == 'Staining' or key_name[i] =='Water pooling' or key_name[i] =='Other damage':
                    line = key_name[i] + ': ' + 'Major'
                    text.textLine(line)
                if key_name[i] == 'Skylight':
                    line = key_name[i] + ': ' + 'Many'
                    text.textLine(line)
                if key_name[i] =='HVAC/Cooling tower':
                    # line = key_name[i] + ': ' + 'Many'
                    line = key_name[i] + ': ' + f'Many ({row[HVAC_index]})'
                    text.textLine(line)
                

        pdf.drawText(text)

        textLines = ['Condition',
                    'Damage',
                    'Equipment'
        ]
        image_name = address + '.jpg'
        image_full_name = os.path.join(demoFolder,image_name)

        image = cv2.imread(image_full_name)
        height = image.shape[0]
        width = image.shape[1]
        ratio = width/height

        if height < width: # height < width horizontal
            tmp_width = 350
            tmp_height = 180
            new_width = ratio * tmp_height
            if new_width > tmp_width:
                draw_width = tmp_width
                draw_height = draw_width/ratio
            else:
                draw_width = new_width
                draw_height = tmp_height
            text = pdf.beginText(100, 500)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-3])
            pdf.drawText(text)
            # pdf.drawInlineImage(image_full_name, 230, 440, width = draw_width, height = draw_height)
            pdf.drawInlineImage(Roof_condition_image_name, 230, 440, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 440, 230+draw_width, 440+draw_height), relative=1)
    # https://apps.nearmap.com/maps/#/@30.6622190,-88.1816001,20.00z,0d/V/20220110

            text = pdf.beginText(100, 300)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-2])
            pdf.drawText(text)
            pdf.drawInlineImage(Damage_image_name, 230, 240, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 240, 230+draw_width, 240+draw_height), relative=1)


            text = pdf.beginText(100, 100)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-1])
            pdf.drawText(text)
            pdf.drawInlineImage(Equipment_image_name, 230, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (200, 40, 230+draw_width, 40+draw_height), relative=1)

        else: # vertical
            tmp_width = 250
            tmp_height = 300
            new_width = ratio * tmp_height
            if new_width > tmp_width:
                draw_width = tmp_width
                draw_height = draw_width/ratio
            else:
                draw_width = new_width
                draw_height = tmp_height
            text = pdf.beginText(310, 370)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-3])
            pdf.drawText(text)
            # pdf.drawInlineImage(image_full_name, 310, 380, width = draw_width, height = draw_height)
            pdf.drawInlineImage(Roof_condition_image_name, 310, 380, width = draw_width, height = draw_height)
            pdf.linkURL(url, (310, 380, 310+draw_width, 380+draw_height), relative=1)

            text = pdf.beginText(40, 30)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-2])
            pdf.drawText(text)
            pdf.drawInlineImage(Damage_image_name, 40, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (40, 40, 40+draw_width, 40+draw_height), relative=1)


            text = pdf.beginText(310, 30)
            text.setFont("Courier", 12)
            text.setFillColor(colors.blue)
            text.textLine(textLines[-1])
            pdf.drawText(text)
            pdf.drawInlineImage(Equipment_image_name, 310, 40, width = draw_width, height = draw_height)
            pdf.linkURL(url, (310, 40, 310+draw_width, 40+draw_height), relative=1)


        # saving the pdf
        pdf.save()    
    
    
    

def zipdir(folder, path, ziph):
    file_path = os.path.join(folder, path)
    # ziph is zipfile handle
    if not os.path.isdir(file_path):
        if path[-3:]=='jpg': # move the orignial image to image folder
            ziph.write(file_path,path.replace('.jpg','/Image.jpg'))
        else:
            ziph.write(file_path, path)
    else:
        for root, dirs, files in os.walk(file_path):           
            for file in files:
                if file[0:4] != 'Roof': # don't include the roof boundary model
                    ziph.write(os.path.join(root, file), os.path.join(path, file))

def zip_download_file(file_name, image_folder_name='roof_score_new_20230101'):
    ############################## ZIP
    # excel_file_path = "roof_score_new_20220803.csv"
    # excel_file_path = "roof_score_new_20220726.csv"
    # image_folder_name = os.path.splitext(os.path.basename(excel_file_path))[0]

    # import glob
    # jpgFilenamesList = glob.glob(image_folder_name + '/*.jpg')
    # pdfFilenamesList = glob.glob(image_folder_name + '/*.pdf')
        # for f in jpgFilenamesList:   
        #     myzip.write(f)
        # for f in pdfFilenamesList:   
        #     myzip.write(f)

    file_list = [f for f in os.listdir(image_folder_name) if f[0].isnumeric()]
    print('Zipping')
    with zipfile.ZipFile(os.path.join(image_folder_name, file_name), 'w') as myzip:
        myzip.write(os.path.join(image_folder_name, 'all_address.csv'), 'all_address_' + image_folder_name[-8:] + '.csv')
        for f in file_list:    
            zipdir(image_folder_name, f, myzip)
    print('Zipping Done')

def zip_download_file_csv(file_name, image_folder_name='roof_score_new_20230101'):
    ############################## ZIP
    # excel_file_path = "roof_score_new_20220803.csv"
    # excel_file_path = "roof_score_new_20220726.csv"
    # image_folder_name = os.path.splitext(os.path.basename(excel_file_path))[0]

    # import glob
    # jpgFilenamesList = glob.glob(image_folder_name + '/*.jpg')
    # pdfFilenamesList = glob.glob(image_folder_name + '/*.pdf')
        # for f in jpgFilenamesList:   
        #     myzip.write(f)
        # for f in pdfFilenamesList:   
        #     myzip.write(f)

    file_list = ['prediction_Phase3_equipment_damage/Phase3_equipment_damage_all_in_one.json',
                 'prediction_Data_all_equipment_damage/Data_all_equipment_damage_all_in_one.json',
                 'prediction_Roof_boundary/Roof_boundary_all_in_one.json',
                 # 'prediction_Roof_type/Roof_type_all_in_one.json',
                 # 'prediction_Roof_material/Roof_material_all_in_one.json'
                ]
    print('Zipping')
    with zipfile.ZipFile(os.path.join(image_folder_name, file_name), 'w') as myzip:
        myzip.write(os.path.join(image_folder_name, 'all_referral.csv'), 'roof_condition_predicted.csv')
        for f in file_list:    
            zipdir(image_folder_name, f, myzip)
    print('Zipping Done')

def zip_download_condition_json(file_name, image_folder_name='roof_score_new_20230101'):
    ############################## ZIP
    # excel_file_path = "roof_score_new_20220803.csv"
    # excel_file_path = "roof_score_new_20220726.csv"
    # image_folder_name = os.path.splitext(os.path.basename(excel_file_path))[0]

    # import glob
    # jpgFilenamesList = glob.glob(image_folder_name + '/*.jpg')
    # pdfFilenamesList = glob.glob(image_folder_name + '/*.pdf')
        # for f in jpgFilenamesList:   
        #     myzip.write(f)
        # for f in pdfFilenamesList:   
        #     myzip.write(f)

    file_list = ['prediction_Roof_condition/Roof_condition_all_in_one.json']
    print('Zipping')
    with zipfile.ZipFile(os.path.join(image_folder_name, file_name), 'w') as myzip:
        # myzip.write(os.path.join(image_folder_name, 'all_referral.csv'), 'roof_condition_predicted.csv')
        for f in file_list:    
            zipdir(image_folder_name, f, myzip)
    print('Zipping Done')

def send_email(receiver_email, address):
    host_server = 'smtp.qq.com'
    sender_qq = '1303242060'
    pwd = 'fhzevydopuvagfae'
    # pwd = input('Please input the password (not the login pwd)')

    sender_qq_mail = '1303242060@qq.com'
    # receiver = 'ruixu_liu@cinfin.com'

    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(0)   # 1 for debug
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)


    msg = MIMEMultipart() # .txt .jpg .xls
    mail_title = 'Roof condition file'
    mail_content = address
    msg.attach(MIMEText(mail_content,'plain','utf-8'))

    # Add attachment
    att1=MIMEText(open('roof_score_new_20230101/roof.zip','rb').read(),'base64','utf-8')  #open file
    att1['Content-Type']='application/octet-stream' 
    att1['Content-Disposition']='attachment;filename=roof.zip'  

    # att2=MIMEText(open('aaa.jpg','rb').read(),'base64','utf-8')
    # att2['Content-Type']='application/octet-stream'
    # att2['Content-Disposition']='attachment;filename=aaa.jpg' 
    msg.attach(att1)
    # msg.attach(att2)

    print('Preparing done.')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver_email

    smtp.sendmail(sender_qq_mail, receiver_email, msg.as_string())

    smtp.quit()
    print('Finish send email.')
