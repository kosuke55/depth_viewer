import argparse
import os.path as osp

import cv2
import numpy as np
from PIL import Image


def remove_nan(img):
    img = img.copy()
    nan_mask = np.isnan(img)
    img[nan_mask] = 0
    return img


def normalize_depth(depth, min_value=None, max_value=None):
    normalized_depth = depth.copy()
    min_value = np.nanmin(depth) if min_value is None else min_value
    max_value = np.nanmax(depth) if max_value is None else max_value
    normalized_depth = remove_nan(normalized_depth)
    normalized_depth = (normalized_depth - min_value) / (max_value - min_value)
    normalized_depth[normalized_depth <= 0] = 0
    normalized_depth[normalized_depth > 1] = 1

    return normalized_depth


def colorize_depth(depth, min_value=None, max_value=None, ignore_value=None):
    depth = depth.copy()
    if ignore_value is not None:
        depth[depth == ignore_value] = np.nan

    normalized_depth = normalize_depth(depth, min_value, max_value)
    nan_mask = np.isnan(normalized_depth)
    gray_depth = normalized_depth * 255
    gray_depth = gray_depth.astype(np.uint8)
    colorized = cv2.applyColorMap(gray_depth, cv2.COLORMAP_JET)
    colorized[nan_mask] = (0, 0, 0)

    return colorized


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', '-i', type=str,
                        help='Input filename', required=True)
    parser.add_argument('--min', type=float,
                        help='min_value', default=-1)
    parser.add_argument('--max', type=float,
                        help='max_value', default=-1)
    parser.add_argument('--ignore', type=float,
                        help='ignore_value', default=-1)
    args = parser.parse_args()
    input_file = args.input
    min_value = None if args.min == -1 else args.min
    max_value = None if args.max == -1 else args.max
    ignore_value = None if args.ignore == -1 else args.ignore

    root, ext = osp.splitext(input_file)

    if 'png' in ext.lower() \
            or 'jpg' in ext.lower() \
            or 'jpeg' in ext.lower():
        depth = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE).astype(np.float32)

    if 'npy' in ext:
        depth = np.load(input_file)

    print('input depth min:{} max:{}'.format(depth.min(), depth.max()))
    colorized_depth = colorize_depth(
        depth, min_value, max_value, ignore_value)
    colorized_depth = cv2.cvtColor(colorized_depth, cv2.COLOR_BGR2RGB)
    colorized_depth = Image.fromarray(colorized_depth)
    colorized_depth.show()


if __name__ == '__main__':
    main()