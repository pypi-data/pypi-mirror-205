import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms

from .model import BiSeNet
from .utils import arrange_mask, get_one_hot
from ..utils import check_ckpt_exist, convert_image_type, get_url_id

class FaceParser(nn.Module):
    def __init__(self, folder_name='face_parser', ckpt_name = 'faceparser.pth', force=False, device = 'cuda'):
        """
        Related Links
        --------
        https://github.com/zllrunning/face-parsing.PyTorch
        
        Label Number
        --------
        1 'skin', 2 'l_brow', 3 'r_brow', 4 'l_eye', 5 'r_eye', 6 'eye_g',  7 'l_ear', 8 'r_ear', 9 'ear_r', 10 'nose', 
        11 'mouth', 12 'u_lip', 13 'l_lip', 14 'neck', 15 'neck_l', 16 'cloth', 17 'hair', 18 'hat'
        
        Methods
        --------
        data_preprocess
            "설명"
            
        data_postprocess
            "설명"
            
        get label
            "설명"
            
        get_onehot
            "설명"
        """
        
        super(FaceParser, self).__init__()

        self.device = device
        self.parsing_net = BiSeNet(n_classes=19).to(self.device)
        
        url_id = get_url_id('~/.invz_pack/', folder_name, ckpt_name)
        root = os.path.join('~/.invz_pack/', folder_name)
        ckpt_path = check_ckpt_exist(root, ckpt_name = ckpt_name, url_id = url_id, force = force)
        ckpt = torch.load(ckpt_path, map_location=self.device)
        
        self.parsing_net.load_state_dict(ckpt)
        for param in self.parsing_net.parameters():
            param.requires_grad = False
        self.parsing_net.eval()
        del ckpt

        self.GaussianBlur = transforms.GaussianBlur(kernel_size=5, sigma=(0.1, 5))
        self.kernel = torch.ones((1,1,5,5), device=self.device)
        
        self.transform = transforms.Compose([
            transforms.Resize((512,512)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    

    def data_preprocess(self, input, unsqueeze = True):
        """
        설명 : 전처리
        - input
            - dtype : str or cv2 image or pillow image
            - shape : (h, w, 3)
            - min max : (0, 255)
        - output
            - shape : (1, 3, 512, 512)
            - min max : (-1, 1)
        """
        
        pil_img = convert_image_type(input)
        tensor_img = self.transform(pil_img).to(self.device)
        if unsqueeze:
            return tensor_img.unsqueeze(0)
        return tensor_img
        
    def data_postprocess(self, tensor_label):
        """
        설명 : 후처리
        - input
            - dtype : tensor
            - shape : (b, 512, 512)
            - min max : (0, 18)
        - output
            - type : numpy
            - shape : (1, 512, 512)
            - min max : (0, 18)
        """
        cv2_label = tensor_label.squeeze().cpu().numpy()
        return cv2_label
    
    def get_label(self, tensor_img, size=512):
        """
        설명 : label 얻기
        - input
            - dtype : tensor
            - shape : (b, 3, 512, 512)
            - min max : (-1, 1)
        - result
            - dtype : tensor
            - shape : (b, 512, 512)
            - min max : (0, 18)
        """
        label = self.parsing_net(tensor_img)
        _label = F.interpolate(label, (size,size), mode='bilinear').max(1)[1]
        _label = arrange_mask(_label, size)
        return _label
    
    def get_onehot(self, tensor_img, size=512):
        """
        설명 : onehot 얻기
        - input
            - dtype : tensor
            - shape : (b, 3, 512, 512)
            - min max : (-1, 1)
        - result
            - dtype : tensor
            - shape : (b, 19, size, size)
            - min max : (0 or 1)
        """
        label = self.get_label(tensor_img, size)
        onehot = get_one_hot(label.unsqueeze(0))
        return onehot
    
if __name__ == '__main__':
    FP = FaceParser()
    FP.data_preprocess
    FP.get_label
    FP.get_onehot
    FP.data_postprocess