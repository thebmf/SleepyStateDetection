import argparse
import yaml
from pathlib import Path
from yolov5.train import train, parse_opt
from yolov5.utils.callbacks import Callbacks
import torch

def main():
    opt = parse_opt(known=True)

    opt.data = 'yolov5/custom_dataset.yml'
    opt.cfg = 'yolov5/models/yolov5s.yaml'
    opt.weights = 'yolov5s.pt'
    opt.epochs = 120
    opt.batch_size = 16
    opt.img_size = 640
    opt.device = 'cpu'
    opt.save_dir = 'yolov5/runs/train'
    opt.single_cls = False
    opt.evolve = False
    opt.noval = False
    opt.nosave = False
    opt.workers = 8
    opt.freeze = [0]

    with open('yolov5/data/hyps/hyp.scratch-med.yaml', 'r') as f:
        hyp = yaml.safe_load(f)

    device = torch.device('cpu')

    callbacks = Callbacks()

    train(hyp, opt, device, callbacks)

if __name__ == '__main__':
    main()
