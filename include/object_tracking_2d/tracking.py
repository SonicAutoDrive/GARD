import os
import time
from easydict import EasyDict
import simplejson

# OC_SORT
from object_tracking_2d.OC_SORT.ocsort_tracker.ocsort import OCSort




class tracking_2d:
    def __init__(self, model_name='OC_SORT', config_path='config/OC_SORT/default.json'):
        # 参数
        parent_dir = os.path.dirname(__file__)
        parent_dir = os.path.split(parent_dir)[0]
        self.root_dir = os.path.split(parent_dir)[0]     # 功能包的根目录
        self.model_name = model_name
        if self.model_name == 'OC_SORT':
            self.args = EasyDict(simplejson.load(open(os.path.join(self.root_dir, config_path), 'r')))     # OC_SORT的
            self._init_OCSORT()


    def _init_OCSORT(self):
        '''OC_SORT初始化'''
        self.tracker = OCSort(self.args.track_thresh, iou_threshold=self.args.iou_thresh, delta_t=self.args.deltat, asso_func=self.args.asso, inertia=self.args.inertia)


    def tracking_2d_OCSORT(self, det):
        '''2d目标跟踪, 输入的det为tensor'''
        # Tracking: (xyxy, track_id, category, prev)
        # Note: prev是对轨迹初始化丢失的帧的补偿 Head Padding (HP)
        tracked = self.tracker.update_public(det[..., :4].cpu(), det[..., 5].cpu(),det[..., 4].cpu())
        return tracked


    def tracking_2d(self, det):
        '''2d目标跟踪'''
        #time1 = time.perf_counter()
        if self.model_name == 'OC_SORT':
            tracked = self.tracking_2d_OCSORT(det)
        #time2 = time.perf_counter()
        return tracked
