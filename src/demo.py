from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import re
import cv2
import json
import numpy as np

from opts import opts
from detectors.detector_factory import detector_factory

image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']

output_dir = '../exp/demo_results/'
output_path = os.path.join(output_dir, 'results.json')

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def demo(opt):
  os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
  opt.debug = max(opt.debug, 1)
  Detector = detector_factory[opt.task]
  detector = Detector(opt)

  if opt.demo == 'webcam' or \
    opt.demo[opt.demo.rfind('.') + 1:].lower() in video_ext:
    cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
    detector.pause = False
    while True:
        _, img = cam.read()
        cv2.imshow('input', img)
        ret = detector.run(img)
        time_str = ''
        for stat in time_stats:
          time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
        print(time_str)
        if cv2.waitKey(1) == 27:
            return  # esc to quit
  else:
    if os.path.isdir(opt.demo):
        image_names = []
        ls = os.listdir(opt.demo)
        sorted_ls = sorted(ls, key=natural_keys)
        for file_name in sorted_ls:
            ext = file_name[file_name.rfind('.') + 1:].lower()
            if ext in image_ext:
                image_names.append(os.path.join(opt.demo, file_name))
    else:
      image_names = [opt.demo]

    results_dict = {}
    
    for (image_name) in image_names:
      ret = detector.run(image_name)

      ret['results'][1] = ret['results'][1].tolist()

      results_dict[image_name] = ret['results'][1]

      time_str = ''
      for stat in time_stats:
        time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
      print(time_str)

    with open(output_path, 'w') as f:
        json.dump(results_dict, f)


if __name__ == '__main__':
  opt = opts().init()
  print(opt)
  demo(opt)
