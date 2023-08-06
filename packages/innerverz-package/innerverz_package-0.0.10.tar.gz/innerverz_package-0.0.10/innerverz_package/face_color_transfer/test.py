import os, sys, glob
from tqdm import tqdm
import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from face_color_transfer.utils.utils import modulate
from main import HWCT
hwct = HWCT()

k = torch.ones((1,1,13,13), device='cuda', dtype=torch.float32)

transform = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize((0.5), (0.5))
        ])


tf_gray = transforms.Compose([
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize((0.5), (0.5))
])

def run_CT(args):
    target_rgb_image, target_gray_image, target_onehot, target_innerface_mask = hwct.data_preprocess(args.target_image_path, args.target_label_path)
    source_rgb_image, source_gray_image, source_onehot, source_innerface_mask = hwct.data_preprocess(args.source_image_path, args.source_label_path)

    # new_target_gray = target_gray_image
    new_target_gray = modulate(target_gray_image.cpu(), source_gray_image.cpu(), target_onehot.cpu(), source_onehot.cpu()).cuda()
    target_gray_innerface = new_target_gray * target_innerface_mask

    source_rgb_image = source_innerface_mask * source_rgb_image # + (1 - source_innerface_mask) * -1 # tmp

    result, color_ref = hwct(source_rgb_image, target_rgb_image, source_onehot, target_onehot, target_gray_innerface, target_innerface_mask)
        
    color_ref_pp = hwct.data_postprocess(color_ref)
    # result = result * target_head_mask + target_bg * (1 - target_head_mask)
    result_pp = hwct.data_postprocess(result)
    source_rgb_image_pp = hwct.data_postprocess(source_rgb_image)
    target_gray_image_pp = hwct.data_postprocess(target_gray_image.repeat(1,3,1,1))
    target_innerface_mask_pp = hwct.data_postprocess(target_innerface_mask.repeat(1,3,1,1))
    
    target_image = cv2.imread(args.target_image_path)
    source_image = cv2.imread(args.source_image_path)
    
    grid = np.concatenate((source_rgb_image_pp, target_image, target_gray_image_pp, target_innerface_mask_pp, color_ref_pp, result_pp), axis=1)
    cv2.imwrite(args.save_path, grid)

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='')
    parser.add_argument('--list', nargs='+', default=(10,12), type=int, help='the indices of transparent classes')
    parser.add_argument('--bool', action='store_true', help='whether to detach between depth layers and texture layers')
    args = parser.parse_args()
    
    # args.target_image_path = './assets/images/0001.png'
    # args.target_label_path = './assets/labels/0001.png'
    # args.source_image_path = './assets/images/0002.png'
    # args.source_label_path = './assets/labels/0002.png'
    
    count = 0
    os.makedirs('./test/', exist_ok=True)
    
    # pbar = tqdm(zip(sorted(glob.glob('./assets/sh/face/*.*')), sorted(glob.glob('./assets/sh/label/*.*')), sorted(glob.glob('./assets/jjy/face/*.*')), sorted(glob.glob('./assets/jjy/label/*.*'))))
    # for source_image_path, source_label_path, target_image_path, target_label_path in pbar:
    #     args.source_image_path = source_image_path
    #     args.source_label_path = source_label_path
    #     args.target_image_path = target_image_path
    #     args.target_label_path = target_label_path
    #     args.save_path = f'./jjy_test_wIM/{str(count).zfill(4)}.png'
    #     run_CT(args)
    #     count += 1
            
    for source_image_path, source_label_path in zip(sorted(glob.glob('./assets/images/*.*')), sorted(glob.glob('./assets/labels/*.*'))):
        args.source_image_path = source_image_path
        args.source_label_path = source_label_path
        for target_image_path, target_label_path in zip(sorted(glob.glob('./assets/images/*.*')), sorted(glob.glob('./assets/labels/*.*'))):
            args.target_image_path = target_image_path
            args.target_label_path = target_label_path
            args.save_path = f'./test/{str(count).zfill(4)}.png'
            run_CT(args)
            count += 1