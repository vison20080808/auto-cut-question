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

import detectron2.utils.comm as comm

import detectron2.data.transforms as T

from detectron2.checkpoint import DetectionCheckpointer
from detectron2.config import get_cfg

from detectron2.engine import DefaultPredictor, default_argument_parser, default_setup

import numpy as np

from detectron2.utils.visualizer import Visualizer
from dyhead import add_dyhead_config
from extra import add_extra_config
from detectron2.utils.visualizer import ColorMode


def setup(args):
    """
    Create configs and perform basic setups.
    """
    cfg = get_cfg()
    add_dyhead_config(cfg)
    add_extra_config(cfg)
    cfg.merge_from_file(args.config)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    return cfg


class OkayQuesCut():
    def __init__(self):
        parser = default_argument_parser()
        parser.add_argument("--config", type=str, default="configs/dyhead_swint_atss_fpn_2x_ms.yaml")
        parser.add_argument("--threshould", type=float, default=0.3)
        self.args = parser.parse_args()
        cfg = setup(self.args)
        self.predictor = DefaultPredictor(cfg)

    def __call__(self, image: np.ndarray):
        # 输入opencv读取的图片，格式为numpy array
        # 返回 list[list[x1,y1,x2,y2]]
        boxes = []
        outputs = self.predictor(image)

        instances = outputs["instances"]
        confident_detections = instances[instances.scores > 0.3]

        for i, box in enumerate(confident_detections.pred_boxes.__iter__()):
            boxes.append(box.cpu().tolist())
        # classes = outputs["pred_classes"]

        # print("scores",scores)
        # print("classes",classes)
        # return confident_detections
        return boxes


okay_cut = OkayQuesCut()


def main():
    # image = "./test/IMG_20211022_145648.jpg"
    image = "./test/img_000049.jpg"
    image = cv2.imread(image)
    outputs = okay_cut(image)

    # v = Visualizer(image[:, :, ::-1],
    #                 metadata=None, 
    #                 scale=0.75, 
    #                 instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
    # )
    # v = v.draw_instance_predictions(outputs.to("cpu"))
    # cv2.imwrite("image.jpg",v.get_image()[:, :, ::-1])


if __name__ == "__main__":
    main()
