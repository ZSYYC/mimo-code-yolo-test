import json
import os
import random
import cv2
import numpy as np
from pycocotools.coco import COCO
from pycocotools import mask as maskUtils
from tqdm import tqdm


def set_mask_to_zero(image, masks):
    # Create a combined mask for all objects
    combined_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for mask in masks:
        combined_mask = np.maximum(combined_mask, mask)
    
    # Ensure the mask is 3-channel for broadcasting
    combined_mask_3c = np.repeat(combined_mask[:, :, np.newaxis], 3, axis=2)
    
    # Set the mask area to zero in the image 这里决定mask的像素
    image[combined_mask_3c == 1] = 255
    
    return image

def process_images(coco_annotation_path, image_dir, output_dir):
    # Load COCO annotations
    coco = COCO(coco_annotation_path)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    img_ids = coco.getImgIds()
    
    for img_id in tqdm(img_ids, desc="Processing images"):
        img_info = coco.loadImgs(img_id)[0]
        img_path = os.path.join(image_dir, img_info['file_name'])
        image = cv2.imread(img_path)
        
        # Get all annotations for this image
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)
        
        # Collect all masks for this image
        masks = []
        for ann in anns:
            if ann['image_id'] != img_id:
                continue
            if 'segmentation' in ann:
                segm = ann['segmentation']
                if isinstance(segm, list):
                    # Polygon
                    mask = np.zeros((img_info['height'], img_info['width']), dtype=np.uint8)
                    for poly in segm:
                        poly = np.array(poly).reshape((len(poly) // 2, 2))
                        cv2.fillPoly(mask, [poly.astype(np.int32)], 1)
                elif isinstance(segm, dict) and 'counts' in segm:
                    # RLE
                    mask = maskUtils.decode(segm)
                elif isinstance(segm, str):
                    # Uncompressed RLE
                    mask = maskUtils.decode(maskUtils.frPyObjects([segm], img_info['height'], img_info['width']))
                else:
                    raise ValueError("Unsupported segmentation format")
                masks.append(mask)
        
        # Set the mask area to zero in the image
        image = set_mask_to_zero(image, masks)
        
        # Save the modified image
        output_path = os.path.join(output_dir, img_info['file_name'])
        cv2.imwrite(output_path, image)

# Usage
coco_annotation_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/掩膜标注.json'
image_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/images/'
output_dir = '/home/yaoteam/yaoteam/wz/20250226 去大虫后10000张图片/'
process_images(coco_annotation_path, image_dir, output_dir)
