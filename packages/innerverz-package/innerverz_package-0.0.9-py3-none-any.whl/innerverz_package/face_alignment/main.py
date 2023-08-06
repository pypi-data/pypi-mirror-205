import os
import cv2
import numpy as np
from .retina_face import RetinaFace
from .landmark import Landmark
from .graphic_utils import *
from ..utils import convert_image_type

class FaceAligner():
    def __init__(self, size = 1024, align_style = 'invz'):
        '''
        algin_style has 2 options
        "ffhq" : algorithm used in FFHQ dataset
        "invz" : algorithm costumed by Innerverz.co  
        
        '''
        
        self.backbone = RetinaFace()
        self.lmk_detector = Landmark()
        self.size = size
        self.algin_style = align_style
        if self.algin_style == 'invz':
            self.index_5 = [33,87,73,85,79]
        
        else:
            self.index_5 = [38,88,86,52,61]
    
    def get_face(self, img):
        # img is numpy array
        if img is None:
            return None, None, None, None, False, None 
        
        #get bounding box and confidence score from retina face
        temp, _ = self.backbone.detect(img)

        if len(temp):
            FaceBool = True
            bbox = temp[0][0:4]
            lms_106 = self.lmk_detector.get(img, bbox)
            lms_5 = np.array([lms_106[self.index_5[0]], lms_106[self.index_5[1]], lms_106[self.index_5[2]], lms_106[self.index_5[3]], lms_106[self.index_5[4]]])

            aligned_face, tfm, tfm_inv = self.align_face(img, lms_5)
            return aligned_face, tfm, tfm_inv, lms_5, FaceBool, lms_106
    
        else :
            return None, None, None, None, False, None, 
    
    def detect_lmk(self, img, target_face_num=0):
        FaceBool = False
        temp, _ = self.backbone.detect(img)
        
        assert target_face_num < len(temp), 'index is larger than detected face' 
        
        if len(temp):
            FaceBool = True
            bbox = temp[0][0:4]
            lms_106 = self.lmk_detector.get(img, bbox)
            lms_5 = np.array([lms_106[self.index_5[0]], lms_106[self.index_5[1]], lms_106[self.index_5[2]], lms_106[self.index_5[3]], lms_106[self.index_5[4]]])

        if FaceBool:
            return FaceBool, lms_106, lms_5

        else:
            return FaceBool, None, None
    
    def align_face(self, img, lms_5p, size = None) :
        if size == None: size = self.size 
        
        if self.algin_style == 'ffhq':
            eye_left     = lms_5p[0]
            eye_right    = lms_5p[1]
            eye_avg      = (eye_left + eye_right) * 0.5
            eye_to_eye   = eye_right - eye_left
            mouth_left   = lms_5p[3]
            mouth_right  = lms_5p[4]
            mouth_avg    = (mouth_left + mouth_right) * 0.5
            eye_to_mouth = mouth_avg - eye_avg


            x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
            x /= np.hypot(*x)
            x *= max(np.hypot(*eye_to_eye) * 2.0, np.hypot(*eye_to_mouth) * 1.8)
            y = np.flipud(x) * [-1, 1]
            c = eye_avg + eye_to_mouth * 0.1
            quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])

            src_pts = quad 
            ref_pts = np.array(((0, 0), (0, size), (size, size), (size, 0)))
            tfm, tfm_inv = get_similarity_transform_for_cv2(src_pts, ref_pts)
            face_img = cv2.warpAffine(np.array(img), tfm, (size, size), borderMode=None)

            return face_img, tfm, tfm_inv
    
        else:
            eye_left     = lms_5p[0]
            eye_right    = lms_5p[1]
            eye_avg      = (eye_left + eye_right) * 0.5
            eye_to_eye   = eye_right - eye_left
            mouth_avg = (lms_5p[3] + lms_5p[4])*0.5
            eye_to_mouth = (mouth_avg - eye_avg)*1.5
            # Choose oriented crop rectangle.

            x = eye_to_eye.copy()
            x /= np.hypot(*x) #x를 단위벡터로 만듦
            x *= max(np.hypot(*eye_to_eye) * 2.0 , np.hypot(*eye_to_mouth) * 1.8) 
            y = np.flipud(x) * [-1, 1] 
            c = lms_5p[2]
            quad = np.stack([c - x - y, c - x + y, c + x + y, c + x - y])

            src_pts = quad #+ 0.01*np.random.rand(4,2)
            ref_pts = np.array(((0, 0), (0, size), (size, size), (size, 0)))
            tfm, tfm_inv = get_similarity_transform_for_cv2(src_pts, ref_pts)
            face_img = cv2.warpAffine(np.array(img), tfm, (size, size))

            return face_img, tfm, tfm_inv
        
    def data_preprocess(self, input):
        pil_img = convert_image_type(input)
        np_arr = np.array(pil_img)
        return np_arr