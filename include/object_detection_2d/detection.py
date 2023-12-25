# coding=utf-8
'''
2D detection 和 tracking
'''
import time
import cv2
import os
import platform
import shutil
import time
from pathlib import Path
from easydict import EasyDict
import simplejson


import torch
import torch.backends.cudnn as cudnn
from numpy import random

# YOLOR
from object_detection_2d.YOLOR.utils.google_utils import attempt_load
# from YOLOR.utils.datasets import LoadStreams, LoadImages
from object_detection_2d.YOLOR.utils.general import (check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, box_iou)
from object_detection_2d.YOLOR.utils.plots import plot_one_box
from object_detection_2d.YOLOR.utils.torch_utils import select_device, load_classifier, time_synchronized
from object_detection_2d.YOLOR.models.models import *
from object_detection_2d.YOLOR.utils.datasets import *
from object_detection_2d.YOLOR.utils.general import *




class detection_2d:
    def __init__(self, model_name='YOLOR', config_path='config/YOLOR/default.json'):
        # 参数
        parent_dir = os.path.dirname(__file__)
        parent_dir = os.path.split(parent_dir)[0]
        self.root_dir = os.path.split(parent_dir)[0]     # 功能包的根目录
        self.model_name = model_name
        if self.model_name == 'YOLOR':
            self.opt = EasyDict(simplejson.load(open(os.path.join(self.root_dir, config_path), 'r')))        # YOLOR的
            self._init_YOLOR()


    def _init_YOLOR(self):
        '''YOLOR模型加载'''
        # webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')
        self.device = select_device(self.opt.device)
        output_path = os.path.join(self.root_dir,self.opt.output)
        if os.path.exists(output_path):
            shutil.rmtree(output_path)  # delete output folder
        os.makedirs(output_path)  # make new output folder
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        # Load model
        self.model = Darknet(os.path.join(self.root_dir,self.opt.cfg), self.opt.img_size)
        self.model.load_state_dict(torch.load(os.path.join(self.root_dir,self.opt.weights[0]), map_location=self.device)['model'])
        self.model.to(self.device).eval()
        if self.half:
            self.model.half()  # to FP16


    def detection_2d_YOLOR(self, img_data):
        '''2d目标检测, 单张图片'''
        # 图像rescale成YOLOR格式
        image_hwc = letterbox(img_data, new_shape=self.opt.img_size, auto_size=64)[0]
        image_chw = np.transpose(image_hwc, (2,0,1))
        img = torch.from_numpy(image_chw).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # detection
        with torch.no_grad():
            # Inference
            pred = self.model(img, augment=self.opt.augment)[0]
            # Apply NMS
            pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes, agnostic=self.opt.agnostic_nms)
            # from detect.py line 95
            for i, det in enumerate(pred):  # detection per image
                # Rescale boxes from opt.img_size to img_data size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img_data.shape).round()
        return det

    
    def detection_2d(self, img):
        '''img的回调'''
        time1 = time.perf_counter()
        if self.model_name == 'YOLOR':
            det = self.detection_2d_YOLOR(img)
        time2 = time.perf_counter()
        return det
