import argparse
import os.path as osp
from PIL import Image

import cv2
import numpy as np


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
                        help='min value', default=-1)
    parser.add_argument('--max', type=float,
                        help='max value', default=-1)
    parser.add_argument('--ignore', type=float,
                        help='ignore_value', default=-1)
    parser.add_argument('--depth-scale', '-ds', type=float,
                        help='depth scale', default=-1)
    parser.add_argument('--cloud', '-c', type=int,
                        help='visualize point cloud', default=0)
    args = parser.parse_args()
    input_file = args.input
    min_value = None if args.min == -1 else args.min
    max_value = None if args.max == -1 else args.max
    ignore_value = None if args.ignore == -1 else args.ignore
    depth_scale = None if args.depth_scale == -1 else args.depth_scale  # noqa

    root, ext = osp.splitext(input_file)

    if 'png' in ext.lower() \
            or 'jpg' in ext.lower() \
            or 'jpeg' in ext.lower():
        # depth = np.asarray(Image.open(input_file), np.float32)
        depth = cv2.imread(input_file, cv2.IMREAD_ANYDEPTH).astype(np.float32)

    if 'npy' in ext:
        depth = np.load(input_file)

    if depth_scale is not None:
        depth /= depth_scale

    print('input depth min:{} max:{}'.format(depth.min(), depth.max()))
    colorized_depth = colorize_depth(
        depth, min_value, max_value, ignore_value)
    colorized_depth = cv2.cvtColor(colorized_depth, cv2.COLOR_BGR2RGB)
    colorized_depth = Image.fromarray(colorized_depth)
    colorized_depth.show()

    if args.cloud:
        import open3d as o3d
        dummy_color_o3d = o3d.geometry.Image(
            np.full((depth.shape[0], depth.shape[1], 3), 100, np.uint8))
        depth_o3d = o3d.geometry.Image(depth)
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            dummy_color_o3d, depth_o3d)
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd, o3d.camera.PinholeCameraIntrinsic(
                o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
        o3d.visualization.draw_geometries([pcd])


if __name__ == '__main__':
    main()
