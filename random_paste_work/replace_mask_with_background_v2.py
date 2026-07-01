import json
import os
import random
import cv2
import numpy as np
from pycocotools.coco import COCO
from pycocotools import mask as maskUtils
from difflib import SequenceMatcher
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

def get_most_similar_background(target_filename, background_filenames):
    max_similarity = 0
    most_similar_bg = background_filenames[0]
    for bg_filename in background_filenames:
        similarity = SequenceMatcher(None, target_filename, bg_filename).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_bg = bg_filename
    return most_similar_bg

def replace_mask_with_background(image, masks, background_image):
    # Resize background image to match the target image dimensions
    background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
    
    # Create a combined mask for all objects
    combined_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for mask in masks:
        combined_mask = np.maximum(combined_mask, mask)
    
    # Create a mask for the inverse of the combined object mask
    inverse_mask = np.ones_like(combined_mask) - combined_mask
    
    # Ensure the masks are 3-channel for broadcasting
    combined_mask_3c = np.repeat(combined_mask[:, :, np.newaxis], 3, axis=2)
    inverse_mask_3c = np.repeat(inverse_mask[:, :, np.newaxis], 3, axis=2)
    
    # Composite the final image
    composite_image = np.where(inverse_mask_3c, image, background_image)
    
    return composite_image

def process_images(coco_annotation_path, image_dir, background_dir, output_dir):
    # Load COCO annotations
    coco = COCO(coco_annotation_path)
    
    # List all background images
    background_filenames = [f for f in os.listdir(background_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    img_ids = coco.getImgIds()
    
    for img_id in tqdm(img_ids, desc="Processing images"):
        img_info = coco.loadImgs(img_id)[0]
        img_path = os.path.join(image_dir, img_info['file_name'])
        image = cv2.imread(img_path)
        
        # Get the most similar background image
        bg_filename = get_most_similar_background(img_info['file_name'], background_filenames)
        bg_image = cv2.imread(os.path.join(background_dir, bg_filename))
        
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
        
        # Replace masks with background in the image
        image = replace_mask_with_background(image, masks, bg_image)
        
        # Save the modified image
        output_path = os.path.join(output_dir, img_info['file_name'])
        cv2.imwrite(output_path, image)
        # break

def process_one_images_debug(image_name, coco_annotation_path, image_dir, background_dir, output_dir):
    # Load COCO annotations
    coco = COCO(coco_annotation_path)
    
    # List all background images
    background_filenames = [f for f in os.listdir(background_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    img_ids = coco.getImgIds()
    for img_id in tqdm(img_ids, desc="Processing images"):
        img_info = coco.loadImgs(img_id)[0]
        if img_info['file_name'] != image_name:
            continue
        img_path = os.path.join(image_dir, img_info['file_name'])
        image = cv2.imread(img_path)
        
        # Get the most similar background image
        bg_filename = get_most_similar_background(img_info['file_name'], background_filenames)
        bg_image = cv2.imread(os.path.join(background_dir, bg_filename))
        
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
        
        # # Replace masks with background in the image
        # image = replace_mask_with_background(image, masks, bg_image)
        # Set the mask area to zero in the image
        image = set_mask_to_zero(image, masks)
        
        # Save the modified image
        output_path = os.path.join(output_dir, img_info['file_name'])
        cv2.imwrite(output_path, image)
        # break
# Usage
coco_annotation_path = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/掩膜标注.json'
image_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616'
background_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/背景图和分离出的小虫图/只含有小虫的背景图'
# background_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/背景图和分离出的小虫图/背景图'
output_dir = '/home/yaoteam/yaoteam/yyc/random_paste_work/分离出来的数据集0616/output20241001'
# process_images(coco_annotation_path, image_dir, background_dir, output_dir)
process_one_images_debug('0220715_Image_20220715100546085-3.jpg', coco_annotation_path, image_dir, background_dir, output_dir)
