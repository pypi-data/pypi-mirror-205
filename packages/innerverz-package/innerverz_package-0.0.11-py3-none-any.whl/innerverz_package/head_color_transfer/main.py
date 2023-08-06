import os
import sys
sys.path.append('../')
cwd = os.path.dirname(os.path.realpath(__file__))

import cv2
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F

import torchvision.transforms as transforms

from .nets import MyGenerator
from .utils.utils import to_one_hot
from ..utils import check_ckpt_exist, convert_image_type, get_url_id


class HWCT(nn.Module):
    def __init__(self, img_size : int = 512, folder_name='head_color_transfer', ckpt_name = 'G_128_512_head_60k.pt', force=False, device='cuda'):
        super(HWCT, self).__init__()
        self.img_size = img_size
        self.device = device
        self.generator = MyGenerator().to(self.device)
        
        url_id = get_url_id('~/.invz_pack/', folder_name, ckpt_name)
        root = os.path.join('~/.invz_pack/', folder_name)
        ckpt_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)
        ckpt = torch.load(ckpt_path, map_location=self.device)
       
        self.generator.load_state_dict(ckpt['model'], strict=True)
        for param in self.generator.parameters():
            param.requires_grad = False
        self.generator.eval()
        del ckpt
        self.tf_gray = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.5), (0.5))
        ])
        
        self.tf_color = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.kernel = np.ones((3, 3), np.uint8)
        
    def data_preprocess(self, image_input, label_input, unsqueeze=True):
        PIL_rgb_image = convert_image_type(image_input)
        rgb_image = self.tf_color(PIL_rgb_image).to(self.device).unsqueeze(0)
        
        PIL_gray_image = PIL_rgb_image.convert("L")
        gray_image = self.tf_gray(PIL_gray_image).to(self.device).unsqueeze(0)

        np_label = np.array(convert_image_type(label_input).convert("L").resize((self.img_size, self.img_size), Image.NEAREST))
        # skin + ears
        np_label = np.where(np_label==8,1,np_label)
        np_label = np.where(np_label==7,1,np_label)
        
        # L_brow + R_brow
        np_label = np.where(np_label==3,2,np_label)
        # L_eye + R_eye
        np_label = np.where(np_label==5,4,np_label)
        # u_lip + d_lip + mouth(11)
        np_label = np.where(np_label==13,12,np_label)
        np_label = np.where(np_label==11,12,np_label)
        
        innerface_mask = np.clip(np.clip(np.where(np_label <= 13, 1, 0) + np.where(np_label == 17, 1, 0),0,1) - np.where(np_label == 0, 1, 0), 0, 1)
        
        new_innerface_label = np_label * innerface_mask
        one_hot_label = to_one_hot(new_innerface_label, self.img_size).to(self.device)
        
        innerface_mask = torch.tensor(innerface_mask).view(1, 1, self.img_size, self.img_size).to(self.device)
        gray_image = gray_image * innerface_mask
        
        if unsqueeze:
            return rgb_image, gray_image, one_hot_label, innerface_mask
        else:
            return rgb_image.squeeze(0), gray_image.squeeze(0), one_hot_label.squeeze(0), innerface_mask.squeeze(0)
            
            
    def forward(self, source_rgb, target_rgb, source_onehot, target_onehot, target_gray, target_face_mask):
        result, _ = self.generator(source_rgb, target_rgb, source_onehot, target_onehot, target_gray, target_face_mask)
        return result, _
        
    def data_postprocess(self, tensor_image):
        tensor_image = F.interpolate(tensor_image, (self.img_size, self.img_size))
        cv2_image = ((tensor_image.clone().detach().squeeze().permute([1,2,0]).cpu().numpy()*.5+.5)*255)
        return cv2_image
