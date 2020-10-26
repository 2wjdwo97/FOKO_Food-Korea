"""  
Copyright (c) 2019-present NAVER Corp.
MIT License
"""

# -*- coding: utf-8 -*-
import sys
import os
import time
import argparse

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image

import cv2
from skimage import io
import numpy as np
from . import craft_utils
from . import imgproc
from . import file_utils
import json
import zipfile

from ocr.CRAFT.craft import CRAFT

from collections import OrderedDict

trained_model = '/home/ubuntu/proj/FOKO_FoodKorea/mysite/ocr/CRAFT/craft_mlt_25k.pth'
text_threshold = 0.7
low_text = 0.4
link_threshold = 0.1
cuda = False
canvas_size = 1280
mag_ratio = 1.5
poly = False
show_time = False
refine = False
refiner_model = 'craft_refiner_CTW1500.pth'

def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")



def test_net(net, image, text_threshold, link_threshold, low_text, cuda, refine_net=None):
    global canvas_size
    global mag_ratio
    t0 = time.time()

    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0, :, :, 0].cpu().data.numpy()
    score_link = y[0, :, :, 1].cpu().data.numpy()

    # refine link
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0, :, :, 0].cpu().data.numpy()

    t0 = time.time() - t0
    t1 = time.time()

    # Post-processing
    # boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)
    boxes = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text)  # , poly)
    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    # polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    # for k in range(len(polys)):
    #     if polys[k] is None:
    #         polys[k] = boxes[k]

    t1 = time.time() - t1

    # render results (optional)
    # render_img = score_text.copy()
    # render_img = np.hstack((render_img, score_link))
    # ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    return boxes  # , polys


def runCRAFT(img):
    global trained_model
    global text_threshold
    global low_text
    global link_threshold
    global cuda
    global canvas_size
    global mag_ratio
    global poly
    global show_time
    global refine
    global refiner_model

    """ For test images in a folder """
    # image_list, _, _ = file_utils.get_files(args.test_folder)

    # result_folder = './result/'
    # if not os.path.isdir(result_folder):
    #     os.mkdir(result_folder)

    # load net
    net = CRAFT()     # initialize

    if cuda:
        net.load_state_dict(copyStateDict(torch.load(trained_model)))
    else:
        net.load_state_dict(copyStateDict(torch.load(trained_model, map_location='cpu')))

    if cuda:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False

    net.eval()

    # LinkRefiner
    refine_net = None
    if refine:
        from refinenet import RefineNet
        refine_net = RefineNet()
        print('Loading weights of refiner from checkpoint (' + refiner_model + ')')
        if cuda:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model)))
            refine_net = refine_net.cuda()
            refine_net = torch.nn.DataParallel(refine_net)
        else:
            refine_net.load_state_dict(copyStateDict(torch.load(refiner_model, map_location='cpu')))

        refine_net.eval()
        poly = True
    t = time.time()

    # load data
    # for k, image_path in enumerate(image_list):
    #    print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path), end='\r')
    #    img = imgproc.loadImage('C:/Users/LG/Desktop/testImages/cheese.png')

    img = np.array(img)
    if img.shape[0] == 2:
        img = img[0]
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    if img.shape[2] == 4:
        img = img[:, :, :3]
    boxes = test_net(net, img, text_threshold, link_threshold, low_text, cuda, refine_net)
    # save score text
    # filename, file_ext = os.path.splitext(os.path.basename('./CRAFT_image/test6.jpg'))
    # mask_file = result_folder + "/res_" + filename + '_mask.jpg'
    # cv2.imwrite(mask_file, score_text)

    # file_utils.saveResult(image_path, image[:, :, ::-1], polys, dirname=result_folder)
    strResult = file_utils.saveResult(img[:, :, ::-1], boxes)

    return strResult
