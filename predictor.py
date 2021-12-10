"""
Dyhead Training Script.

This script is a simplified version of the training script in detectron2/tools.
"""
import os
import sys
import itertools
import logging
import time
import cv2
# fmt: off
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# fmt: on

from typing import Any, Dict, List, Set

import torch


from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor, default_setup
import numpy as np
from dyhead import add_dyhead_config
from extra import add_extra_config


class default_argument():
    config = "configs/dyhead_swint_atss_fpn_2x_ms.yaml"
    num_gpus=1

def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    add_dyhead_config(cfg)
    add_extra_config(cfg)
    cfg.merge_from_file(args.config)
    #cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    return cfg

class OkayQuesCut():
    def __init__(self):
        args = default_argument()
        cfg = setup(args)
        self.predictor = DefaultPredictor(cfg)
    def __call__(self, image: np.ndarray):
        boxes = []
        outputs = self.predictor(image)
        instances = outputs["instances"]
        confident_detections = instances[instances.scores > 0.3]

        for box in confident_detections.pred_boxes.__iter__():
            boxes.append(box.cpu().tolist())
        return boxes
def main():
    okay_cut = OkayQuesCut()
    image = "./test/IMG_20211022_145648.jpg"
    image = cv2.imread(image)
    outputs =  okay_cut(image)
    print(outputs)

if __name__ == "__main__":
    main()

