import torch
import torch.nn.functional as F

def arrange_mask(parsing, output_size=512):
    Lbrow_mask = torch.where(parsing==2, 1, 0) + torch.where(parsing==3, 1, 0)
    Lbrow_mask[:, :, :output_size//2] = 0
    parsing = Lbrow_mask * 2 + (1 - Lbrow_mask) * parsing

    Rbrow_mask = torch.where(parsing==2, 1, 0) + torch.where(parsing==3, 1, 0)
    Rbrow_mask[:, :, output_size//2:] = 0
    parsing = Rbrow_mask * 3 + (1 - Rbrow_mask) * parsing

    Leye_mask = torch.where(parsing==4, 1, 0) + torch.where(parsing==5, 1, 0)
    Leye_mask[:, :, :output_size//2] = 0
    parsing = Leye_mask * 4 + (1 - Leye_mask) * parsing
    
    Reye_mask = torch.where(parsing==4, 1, 0) + torch.where(parsing==5, 1, 0)
    Reye_mask[:, :, output_size//2:] = 0
    parsing = Reye_mask * 5 + (1 - Reye_mask) * parsing
    
    Leye_mask = torch.where(parsing==7, 1, 0) + torch.where(parsing==8, 1, 0)
    Leye_mask[:, :, :output_size//2] = 0
    parsing = Leye_mask * 7 + (1 - Leye_mask) * parsing
    
    # Reye
    Reye_mask = torch.where(parsing==7, 1, 0) + torch.where(parsing==8, 1, 0)
    Reye_mask[:, :, output_size//2:] = 0
    parsing = Reye_mask * 8 + (1 - Reye_mask) * parsing
    return parsing

def get_one_hot(mask): # 0 ~ 8 h w
    mask_ = torch.tensor(mask, dtype=torch.int64)
    c = 19
    _,_,h,w = mask_.size()

    mask_ = torch.reshape(mask_,(1,1,h,w))
    one_hot_mask = torch.zeros((1, c, h, w), device=mask.device)
    one_hot_mask_ = one_hot_mask.scatter_(1, mask_, 1.0)
    return one_hot_mask_