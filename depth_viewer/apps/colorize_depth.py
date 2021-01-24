import argparse
from pathlib import Path

import cv2
import numpy as np

from view import colorize_depth


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--input', '-i', type=str,
        help='input directory', required=True)
    parser.add_argument('--min', type=float,
                        help='min value', default=-1)
    parser.add_argument('--max', type=float,
                        help='max value', default=-1)
    parser.add_argument('--ignore', type=float,
                        help='ignore_value', default=-1)
    parser.add_argument('--depth-scale', '-ds', type=float,
                        help='depth scale', default=-1)
    args = parser.parse_args()

    input_dir = args.input
    min_value = None if args.min == -1 else args.min
    max_value = None if args.max == -1 else args.max
    ignore_value = None if args.ignore == -1 else args.ignore
    depth_scale = None if args.depth_scale == -1 else args.depth_scale  # noqa

    paths = Path(input_dir).glob('*.npy')
    for path in paths:
        depth = np.load(path)

        if depth_scale is not None:
            depth /= depth_scale

        colorized_depth = colorize_depth(
            depth, min_value, max_value, ignore_value)

        output_file = str(path.with_suffix('.png'))
        cv2.imwrite(output_file, colorized_depth)


if __name__ == '__main__':
    main()
