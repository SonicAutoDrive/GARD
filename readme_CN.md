# 基于几何约束的路侧深度估计方法 (GARD)
## Introduction

基于几何约束的路侧单目深度估计方法（Geometry-Aware Roadside Monocular Depth Estimation, GARD）是一个目标级单目深度估计算法库，旨在提供一套基于路侧摄像头视角的低成本、高泛化纯视觉测距与3D感知的解决方案。基于2D检测结果与环境几何特征检测，本工具通过后处理的方式对目标3D坐标与速度信息进行重建，其算法核心是基于透视成像的数学原理，无需大量数据进行算法训练，并可在cpu平台进行快速计算。

GARD的应用场景是路侧单目相机，示意图如下：
<div align=center><img height="480" src="docs/单目深度估计repo-基本原理示意图.png"/></div>

```
论文投稿中
```

### Major features
example，介绍你的算法有哪些特征
- **Unified benchmark**
  
  Provide a unified benchmark toolbox for various depth estimation methods.
- **Modular design**
  
  Depth estimation frameworks are decomposed into different components. One can easily construct a customized framework by combining different modules.
- **Support of multiple methods out of box**
  
  I would like to reproduce some of the most excellent depth estimation methods based on this toolbox.
- **High efficiency**
  
  It seems that there are few depth estimation benchmarks, so I start this project and hope it is helpful for research.
  数据结果对比也可以在这里

### CPUs
fast computation on CPU platforms.介绍一下怎么CPU快速
The code can only be run on a single GPU.
You can specify which GPU to use with the `CUDA_VISIBLE_DEVICES` environment variable:
```shell
CUDA_VISIBLE_DEVICES=2 python train.py --model_name mono_model
```

All our experiments were performed on a single NVIDIA Titan Xp.

| Training modality | Approximate GPU memory  | Approximate training time   |
|-------------------|-------------------------|-----------------------------|
| Mono              | 9GB                     | 12 hours                    |
| Stereo            | 6GB                     | 8 hours                     |
| Mono + Stereo     | 11GB                    | 15 hours                    |

## Latest News
比如在哪里投了CVPR，或者什么时间提交的
The stable version will be formed on November 31, 2023.

## System Architecture
系统架构，包含了哪些内容，都有哪些功能。网络框架也可以介绍在这里

## Datasets
支持哪些数据集

### Installation
1. Clone the repository:
git clone https://github.com/SonicAutoDrive/GARD.git

2. Install dependencies:
go to the cloned repository, then run: pip install -r requirements.txt

3. Run the project with a designated mp4 file (we provide a demo file under demo/):
python3 scripts/object_detector.py path_to_the_mp4_file


## Getting Started
单独
We provide train.md and inference.md for the usage of this toolbox.
或者直接
1. Step 1...
2. Step 2...
3. Step 3...

### Prerequisites
路侧摄像头：使用该工具箱需要有安装在路侧的摄像头，以获取视角为基础的图像数据。
视觉2D检测结果：该工具箱依赖准确且强泛化的视觉2D检测结果，因此在使用之前，需要先进行视觉2D检测的处理。
数据集或标注：为了进行算法训练，可能需要有大量的数据集或者标注数据。
CPU平台：工具箱可以在CPU平台上进行快速计算，因此需要有适用的CPU设备。
- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]

## License
GraphScope is released under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Cite
```bibtex
@misc{lidepthtoolbox2022,
  title={Monocular Depth Estimation Toolbox},
  author={Zhenyu Li},
  howpublished = {\url{https://github.com/zhyever/Monocular-Depth-Estimation-Toolbox}},
  year={2022}
}
```
##Changelog

## TODO
未来要干啥
- I will complete the release of BinsFormer models on KITTI dataset (currently limited by the GPU resource). 
- I would like to include self-supervised depth estimation methods, such as MonoDepth2.

## Contact Information
- Email: wbb@iai.ustc.edu.cn
- GitHub: [username1](https://github.com/username1)
