

import cv2
import sys
sys.path.append("./include/")
sys.path.append("./libs/")
sys.path.append('./config')
sys.path.append(".")

import numpy as np

from depth_estimator import DepthEstimator
from roi_extractor import AutomaticROIExtractor

from object_detection_2d.detection import detection_2d
from object_tracking_2d.tracking import tracking_2d

from bbox import plot_one_box


class ObjectDetector(object):
    def __init__(self, camera_config_path = "config/camera/camera_configs.yaml", 
                 test_video_path = "path/to/the/test/video"):
        #### 检测算法初始化
        self.detection_2d = detection_2d(config_path = "config/YOLOR/on_gpu.json")
        #### 跟踪算法初始化
        self.tracking_2d  = tracking_2d(config_path = "config/OC_SORT/default.json")
        #### 单目深度估计初始化
        self.depth_estimator = DepthEstimator(camera_config_path)
        #### 自动化ROI提取
        self.roi_extractor = AutomaticROIExtractor(camera_config = self.depth_estimator.config,
                                                   detector_2d = self.detection_2d,
                                                   tracker_2d = self.tracking_2d)
        print(dir(self.roi_extractor))
        
        self.camera_url = self.depth_estimator.config['camera_url']
        #self.cap = cv2.VideoCapture(self.camera_url)
        self.cap = cv2.VideoCapture(test_video_path)

    def callback(self):
        #img_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        #img_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #img_fourcc = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        img_fps = self.cap.get(cv2.CAP_PROP_FPS)

        ###### 读取摄像头画面
        while self.cap.isOpened():
           
            sucess, frame = self.cap.read() 
            if not sucess:
                break
                
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            ###### ROI 提取，失败则继续，直至成功 ######
            #roi = self.roi_extractor.callback(rgb)
            #if roi is None:
            #    continue

            ###### 获取目标检测结果 ######
            det = self.detection_2d.detection_2d(rgb)
            det = np.array(det.cpu())
            print(det.shape)
            #trk = self.tracking_2d.tracking_2d(det)
            #print(trk.shape)

            ####### 灭点计算 ######
            #rec, tri = roi
            #rgb_cropped = rgb[rec[1][0]:rec[1][1], rec[0][0]:rec[0][1],:]
            #self.lines = self.vpd_cv2.GetLines(rgb_cropped)
            #vp, _ = self.vpd_cv2.GetVanishingPoint(self.lines)
            #print(f"vp = {self.depth_estimator.vp}")
            #self.depth_estimator.update_pose(vp)

            ###### 在demo视频中，灭点已经被提前计算出来，因此此处固定
            self.depth_estimator.update_pose([2068, 61])
            
            depth = self.depth_estimator.get_depth(det)

            for i, obj in enumerate(det):
                x1, y1, x2, y2 = obj[:4]
                label = str(np.round(depth[i], 2))+" m"
                #### 绘制目标检测框
                plot_one_box((x1, y1, x2, y2), frame, color=(0,255,0), label=label)

            ##### 为了在1920x1080分辨率的屏幕上显示方便，改变原图尺寸    
            frame = cv2.resize(frame, (1792, 945))
            cv2.imshow('video', frame) #显示画面
            
            
            key = cv2.waitKey(int(1000/img_fps))
            if key == ord('q'):
                break

        
        self.cap.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':

    test_video_path = sys.argv[1]
    detector = ObjectDetector(camera_config_path = "./config/camera/camera_configs.yaml" ,
                              test_video_path = test_video_path)
    detector.callback()
