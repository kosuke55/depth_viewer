# depth_viewer

### example

```
pip install -e .
depth_viewer -i data/sample.npy --ignore 0 --cloud
```

colorized depth  
<img src="https://user-images.githubusercontent.com/39142679/103687941-7173af00-4fd4-11eb-92dd-1e395e525e01.png" width="500" >

point cloud (distorted due to using open3d's default intrinsic)  
<img src="https://user-images.githubusercontent.com/39142679/103687943-733d7280-4fd4-11eb-938f-350e0a852dd9.png" width="500" >

```
usage: depth-viewer [-h] --input INPUT [--min MIN] [--max MAX]
                    [--ignore IGNORE] [--depth-scale DEPTH_SCALE] [--cloud]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input filename (default: None)
  --min MIN             min value (default: -1)
  --max MAX             max value (default: -1)
  --ignore IGNORE       ignore_value (default: -1)
  --depth-scale DEPTH_SCALE, -ds DEPTH_SCALE
                        depth scale (default: -1)
  --cloud, -c           visualize point cloud (default: False)
```