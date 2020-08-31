# flake8: noqa

import pkg_resources
import os.path as osp


__version__ = pkg_resources.get_distribution('depth-viewer').version


depth_viewer_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'depth_viewer')
