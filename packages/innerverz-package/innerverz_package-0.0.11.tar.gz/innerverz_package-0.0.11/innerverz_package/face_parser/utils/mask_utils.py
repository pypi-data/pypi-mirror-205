import torch
import torch.nn.functional as F
from torchvision import transforms

def get_innerface_mask(label):
    innerface_mask  = torch.where(label<14, 1, 0)
    innerface_mask -= torch.where(label==0, 1, 0)
    
    return innerface_mask

def get_dilate_blur_mask(mask, do_dilate=True, do_blur=True, dilate_kernel_size=5, blur_kernel_size=5):
    assert len(mask.shape) == 4, "Mask must have batch-channel and tensor type."
    
    if do_dilate:
        kernel = torch.ones((1,1,dilate_kernel_size, dilate_kernel_size), device = mask.device)
        mask = torch.clamp(F.conv2d(mask.float(), kernel, padding=(dilate_kernel_size//2, dilate_kernel_size//2)), 0, 1)

    if do_blur:
        GaussianBlur = transforms.GaussianBlur(kernel_size=blur_kernel_size, sigma=(0.1, 5))
        mask = GaussianBlur(mask)
        
    return mask