# uncompyle6 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.13 (default, Oct 21 2022, 23:50:54) 
# [GCC 11.2.0]
# Embedded file name: /home/wbb/Share/roadside-depth-estimation-toolkit/scripts/../libs/roi_extractor.py
# Compiled at: 2023-09-25 15:37:53
# Size of source mod 2**32: 4337 bytes
import numpy as np

class AutomaticROIExtractor(object):

    def __init__(self, camera_config=None, detector_2d=None, tracker_2d=None, stop_count=500):
        self.detector_2d = detector_2d
        self.tracker_2d = tracker_2d
        self.stop_count = min(stop_count, 1000)
        self.img_count = 0
        self.trk_results = []
        self.img_org_h = camera_config['image_height']
        self.img_org_w = camera_config['image_width']
        self.curr_targets = None
        self.curr_velocities = []
        self.velocity_thresh = 10
        self.prev_tracked = None

    def compute_velocity(self, curr_targets, prev_targets):
        curr_objs = {int(obj[4]): np.asarray([0.5 * (obj[0] + obj[2]), obj[3]]) for obj in curr_targets}
        prev_objs = {int(obj[4]): np.asarray([0.5 * (obj[0] + obj[2]), obj[3]]) for obj in prev_targets}
        velocities = {trk_id: np.abs(curr_objs[trk_id] - prev_objs[trk_id]).sum() for trk_id in curr_objs if trk_id in prev_objs}
        return (velocities, curr_objs, prev_objs)

    def create_region(self, trk_results, lmbd_y=0.1, lmbd_x=0.05):
        y0 = max(np.min(trk_results[:, 1]), lmbd_y * self.img_org_h)
        y1 = min(np.max(trk_results[:, 1]), (1.0 - lmbd_y) * self.img_org_h)
        x0 = max(np.min(trk_results[:, 0]), lmbd_x * self.img_org_w)
        x1 = min(np.max(trk_results[:, 0]), (1.0 - lmbd_x) * self.img_org_w)
        x_ave = np.mean(trk_results[:, 0])
        return (
         [
          [
           int(x0), int(y0)], [int(x1), int(y1)]], np.array([[int(x_ave), int(y0)], [int(x0), int(y1)], [int(x1), int(y1)]]))

    def filter_by_velocity_thresh--- This code section failed: ---

 L.  54         0  LOAD_CLOSURE             'self'
                2  LOAD_CLOSURE             'velocities'
                4  BUILD_TUPLE_2         2 
                6  LOAD_SETCOMP             '<code_object <setcomp>>'
                8  LOAD_STR                 'AutomaticROIExtractor.filter_by_velocity_thresh.<locals>.<setcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_DEREF               'velocities'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def callback(self, img):
        trk_results = self.detect_and_track_objects(img)
        print(f"length of tracked results: {len(trk_results)}")
        if len(trk_results) > self.stop_count:
            rec, tri = self.create_region(trk_results)
            return (rec, tri)

    def detect_and_track_objects(self, img_org):
        if len(self.trk_results) > self.stop_count:
            return np.asarray(self.trk_results)
        else:
            self.curr_targets = self.detector_2d.detection_2d(img_org)
            if len(self.curr_targets) < 1:
                return np.asarray(self.trk_results)
                self.curr_tracked = self.tracker_2d.tracking_2d(self.curr_targets)
                velocities = dict()
                if self.img_count < 1:
                    self.prev_tracked = self.curr_tracked
            else:
                velocities, curr_tracked, prev_tracked = self.compute_velocity(self.curr_tracked, self.prev_tracked)
            trk_ids = self.filter_by_velocity_thresh(velocities)
            for trk_id in trk_ids:
                self.trk_results.append(prev_tracked[trk_id])
            else:
                self.prev_tracked = self.curr_tracked

        self.img_count += 1
        return np.asarray(self.trk_results)


if __name__ == '__main__':
    extractor = AutomaticROIExtractor(camera_config=None, detector=None, tracker=None, stop_count=1500)