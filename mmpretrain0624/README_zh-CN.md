<div align="center">

<img src="resources/mmpt-logo.png" width="600"/>
  <div>&nbsp;</div>
  <div align="center">
    <b><font size="5">OpenMMLab 官网</font></b>
    <sup>
      <a href="https://openmmlab.com">
        <i><font size="4">HOT</font></i>
      </a>
    </sup>
    &nbsp;&nbsp;&nbsp;&nbsp;
    <b><font size="5">OpenMMLab 开放平台</font></b>
    <sup>
      <a href="https://platform.openmmlab.com">
        <i><font size="4">TRY IT OUT</font></i>
      </a>
    </sup>
  </div>
  <div>&nbsp;</div>

[![PyPI](https://img.shields.io/pypi/v/mmpretrain)](https://pypi.org/project/mmpretrain)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://mmpretrain.readthedocs.io/zh_CN/latest/)
[![Build Status](https://github.com/open-mmlab/mmpretrain/workflows/build/badge.svg)](https://github.com/open-mmlab/mmpretrain/actions)
[![codecov](https://codecov.io/gh/open-mmlab/mmpretrain/branch/main/graph/badge.svg)](https://codecov.io/gh/open-mmlab/mmpretrain)
[![license](https://img.shields.io/github/license/open-mmlab/mmpretrain.svg)](https://github.com/open-mmlab/mmpretrain/blob/main/LICENSE)
[![open issues](https://isitmaintained.com/badge/open/open-mmlab/mmpretrain.svg)](https://github.com/open-mmlab/mmpretrain/issues)
[![issue resolution](https://isitmaintained.com/badge/resolution/open-mmlab/mmpretrain.svg)](https://github.com/open-mmlab/mmpretrain/issues)

[📘 中文文档](https://mmpretrain.readthedocs.io/zh_CN/latest/) |
[🛠️ 安装教程](https://mmpretrain.readthedocs.io/zh_CN/latest/get_started.html) |
[👀 模型库](https://mmpretrain.readthedocs.io/zh_CN/latest/modelzoo_statistics.html) |
[🆕 更新日志](https://mmpretrain.readthedocs.io/zh_CN/latest/notes/changelog.html) |
[🤔 报告问题](https://github.com/open-mmlab/mmpretrain/issues/new/choose)

<img src="https://user-images.githubusercontent.com/36138628/230307505-4727ad0a-7d71-4069-939d-b499c7e272b7.png" width="400"/>

[English](/README.md) | 简体中文

</div>

<div align="center">
  <a href="https://openmmlab.medium.com/" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/219255827-67c1a27f-f8c5-46a9-811d-5e57448c61d1.png" width="3%" alt="" /></a>
  <img src="https://user-images.githubusercontent.com/25839884/218346358-56cc8e2f-a2b8-487f-9088-32480cceabcf.png" width="3%" alt="" />
  <a href="https://discord.gg/raweFPmdzG" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/218347213-c080267f-cbb6-443e-8532-8e1ed9a58ea9.png" width="3%" alt="" /></a>
  <img src="https://user-images.githubusercontent.com/25839884/218346358-56cc8e2f-a2b8-487f-9088-32480cceabcf.png" width="3%" alt="" />
  <a href="https://twitter.com/OpenMMLab" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/218346637-d30c8a0f-3eba-4699-8131-512fb06d46db.png" width="3%" alt="" /></a>
  <img src="https://user-images.githubusercontent.com/25839884/218346358-56cc8e2f-a2b8-487f-9088-32480cceabcf.png" width="3%" alt="" />
  <a href="https://www.youtube.com/openmmlab" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/218346691-ceb2116a-465a-40af-8424-9f30d2348ca9.png" width="3%" alt="" /></a>
  <img src="https://user-images.githubusercontent.com/25839884/218346358-56cc8e2f-a2b8-487f-9088-32480cceabcf.png" width="3%" alt="" />
  <a href="https://space.bilibili.com/1293512903" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/219026751-d7d14cce-a7c9-4e82-9942-8375fca65b99.png" width="3%" alt="" /></a>
  <img src="https://user-images.githubusercontent.com/25839884/218346358-56cc8e2f-a2b8-487f-9088-32480cceabcf.png" width="3%" alt="" />
  <a href="https://www.zhihu.com/people/openmmlab" style="text-decoration:none;">
    <img src="https://user-images.githubusercontent.com/25839884/219026120-ba71e48b-6e94-4bd4-b4e9-b7d175b5e362.png" width="3%" alt="" /></a>
</div>

## Introduction

MMPreTrain 是一款基于 PyTorch 的开源深度学习预训练工具箱，是 [OpenMMLab](https://openmmlab.com/) 项目的成员之一

`主分支`代码目前支持 PyTorch 1.8 以上的版本。

### 主要特性

- 支持多样的主干网络与预训练模型
- 支持多种训练策略（有监督学习，无监督学习，多模态学习等）
- 提供多种训练技巧
- 大量的训练配置文件
- 高效率和高可扩展性
- 功能强大的工具箱，有助于模型分析和实验
- 支持多种开箱即用的推理任务
  - 图像分类
  - 图像描述（Image Caption）
  - 视觉问答（Visual Question Answering）
  - 视觉定位（Visual Grounding）
  - 检索（图搜图，图搜文，文搜图）

https://github.com/open-mmlab/mmpretrain/assets/26739999/e4dcd3a2-f895-4d1b-a351-fbc74a04e904

## 更新日志

🌟 2024/01/04 发布了 v1.2.0 版本

- 支持了 LLaVA 1.5
- 实现了一个 RAM 模型的 gradio 推理例程

🌟 2023/10/12 发布了 v1.1.0 版本

- 支持 Mini-GPT4 训练并提供一个基于 Baichuan-7B 的中文模型
- 支持基于 CLIP 的零样本分类。

🌟 2023/7/4 发布了 v1.0.0 版本

- 支持更多**多模态**算法的推理, 例如 [**LLaVA**](./configs/llava/), [**MiniGPT-4**](./configs/minigpt4), [**Otter**](./configs/otter/) 等。
- 支持约 **10 个多模态**数据集!
- 添加自监督学习算法 [**iTPN**](./configs/itpn/), [**SparK**](./configs/spark/)。
- 提供[新配置文件](./mmpretrain/configs/)和 [DeepSpeed/FSDP](./configs/mae/benchmarks/) 的样例。这是[新配置文件](https://mmengine.readthedocs.io/en/latest/advanced_tutorials/config.html#a-pure-python-style-configuration-file-beta) 和 [DeepSpeed/FSDP with FlexibleRunner](https://mmengine.readthedocs.io/en/latest/api/generated/mmengine.runner.FlexibleRunner.html#mmengine.runner.FlexibleRunner) 的文档链接。

🌟 从 MMClassification 升级到 MMPreTrain

- 整合来自 MMSelfSup 的自监督学习算法，例如 `MAE`, `BEiT` 等
- 支持了 **RIFormer**，简单但有效的视觉主干网络，却移除了 token mixer
- 重构数据管道可视化
- 支持了 **LeViT**, **XCiT**, **ViG**, **ConvNeXt-V2**, **EVA**, **RevViT**, **EfficientnetV2**, **CLIP**, **TinyViT** 和 **MixMIM** 等骨干网络结构

这个版本引入一个全新的，可扩展性强的训练和测试引擎，但目前仍在开发中。欢迎根据 [文档](https://mmpretrain.readthedocs.io/zh_CN/latest/) 进行试用。

同时，新版本中存在一些与旧版本不兼容的修改。请查看 [迁移文档](https://mmpretrain.readthedocs.io/zh_CN/latest/migration.html) 来详细了解这些变动。

发布历史和更新细节请参考 [更新日志](https://mmpretrain.readthedocs.io/zh_CN/latest/notes/changelog.html)。

## 安装

以下是安装的简要步骤：

```shell
conda create -n open-mmlab python=3.8 pytorch==1.10.1 torchvision==0.11.2 cudatoolkit=11.3 -c pytorch -y
conda activate open-mmlab
pip3 install openmim
git clone https://github.com/open-mmlab/mmpretrain.git
cd mmpretrain
mim install -e .
```

更详细的步骤请参考 [安装指南](https://mmpretrain.readthedocs.io/zh_CN/latest/get_started.html) 进行安装。

如果需要多模态模型，请使用如下方式安装额外的依赖：

```shell
mim install -e ".[multimodal]"
```

## 基础教程

我们为新用户提供了一系列基础教程：

- [学习配置文件](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/config.html)
- [准备数据集](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/dataset_prepare.html)
- [使用现有模型推理](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/inference.html)
- [训练](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/train.html)
- [测试](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/test.html)
- [下游任务](https://mmpretrain.readthedocs.io/zh_CN/latest/user_guides/downstream.html)

关于更多的信息，请查阅我们的 [相关文档](https://mmpretrain.readthedocs.io/zh_CN/latest/)。

## 模型库

相关结果和模型可在 [模型库](https://mmpretrain.readthedocs.io/zh_CN/latest/modelzoo_statistics.html) 中获得。

<div align="center">
  <b>概览</b>
</div>
<table align="center">
  <tbody>
    <tr align="center" valign="bottom">
      <td>
        <b>支持的主干网络</b>
      </td>
      <td>
        <b>自监督学习</b>
      </td>
      <td>
        <b>多模态算法</b>
      </td>
      <td>
        <b>其它</b>
      </td>
    </tr>
    <tr valign="top">
      <td>
        <ul>
        <li><a href="configs/vgg">VGG</a></li>
        <li><a href="configs/resnet">ResNet</a></li>
        <li><a href="configs/resnext">ResNeXt</a></li>
        <li><a href="configs/seresnet">SE-ResNet</a></li>
        <li><a href="configs/seresnet">SE-ResNeXt</a></li>
        <li><a href="configs/regnet">RegNet</a></li>
        <li><a href="configs/shufflenet_v1">ShuffleNet V1</a></li>
        <li><a href="configs/shufflenet_v2">ShuffleNet V2</a></li>
        <li><a href="configs/mobilenet_v2">MobileNet V2</a></li>
        <li><a href="configs/mobilenet_v3">MobileNet V3</a></li>
        <li><a href="configs/swin_transformer">Swin-Transformer</a></li>
        <li><a href="configs/swin_transformer_v2">Swin-Transformer V2</a></li>
        <li><a href="configs/repvgg">RepVGG</a></li>
        <li><a href="configs/vision_transformer">Vision-Transformer</a></li>
        <li><a href="configs/tnt">Transformer-in-Transformer</a></li>
        <li><a href="configs/res2net">Res2Net</a></li>
        <li><a href="configs/mlp_mixer">MLP-Mixer</a></li>
        <li><a href="configs/deit">DeiT</a></li>
        <li><a href="configs/deit3">DeiT-3</a></li>
        <li><a href="configs/conformer">Conformer</a></li>
        <li><a href="configs/t2t_vit">T2T-ViT</a></li>
        <li><a href="configs/twins">Twins</a></li>
        <li><a href="configs/efficientnet">EfficientNet</a></li>
        <li><a href="configs/edgenext">EdgeNeXt</a></li>
        <li><a href="configs/convnext">ConvNeXt</a></li>
        <li><a href="configs/hrnet">HRNet</a></li>
        <li><a href="configs/van">VAN</a></li>
        <li><a href="configs/convmixer">ConvMixer</a></li>
        <li><a href="configs/cspnet">CSPNet</a></li>
        <li><a href="configs/poolformer">PoolFormer</a></li>
        <li><a href="configs/inception_v3">Inception V3</a></li>
        <li><a href="configs/mobileone">MobileOne</a></li>
        <li><a href="configs/efficientformer">EfficientFormer</a></li>
        <li><a href="configs/mvit">MViT</a></li>
        <li><a href="configs/hornet">HorNet</a></li>
        <li><a href="configs/mobilevit">MobileViT</a></li>
        <li><a href="configs/davit">DaViT</a></li>
        <li><a href="configs/replknet">RepLKNet</a></li>
        <li><a href="configs/beit">BEiT</a></li>
        <li><a href="configs/mixmim">MixMIM</a></li>
        <li><a href="configs/revvit">RevViT</a></li>
        <li><a href="configs/convnext_v2">ConvNeXt V2</a></li>
        <li><a href="configs/vig">ViG</a></li>
        <li><a href="configs/xcit">XCiT</a></li>
        <li><a href="configs/levit">LeViT</a></li>
        <li><a href="configs/riformer">RIFormer</a></li>
        <li><a href="configs/glip">GLIP</a></li>
        <li><a href="configs/sam">ViT SAM</a></li>
        <li><a href="configs/eva02">EVA02</a></li>
        <li><a href="configs/dinov2">DINO V2</a></li>
        <li><a href="configs/hivit">HiViT</a></li>
        </ul>
      </td>
      <td>
        <ul>
        <li><a href="configs/mocov2">MoCo V1 (CVPR'2020)</a></li>
        <li><a href="configs/simclr">SimCLR (ICML'2020)</a></li>
        <li><a href="configs/mocov2">MoCo V2 (arXiv'2020)</a></li>
        <li><a href="configs/byol">BYOL (NeurIPS'2020)</a></li>
        <li><a href="configs/swav">SwAV (NeurIPS'2020)</a></li>
        <li><a href="configs/densecl">DenseCL (CVPR'2021)</a></li>
        <li><a href="configs/simsiam">SimSiam (CVPR'2021)</a></li>
        <li><a href="configs/barlowtwins">Barlow Twins (ICML'2021)</a></li>
        <li><a href="configs/mocov3">MoCo V3 (ICCV'2021)</a></li>
        <li><a href="configs/beit">BEiT (ICLR'2022)</a></li>
        <li><a href="configs/mae">MAE (CVPR'2022)</a></li>
        <li><a href="configs/simmim">SimMIM (CVPR'2022)</a></li>
        <li><a href="configs/maskfeat">MaskFeat (CVPR'2022)</a></li>
        <li><a href="configs/cae">CAE (arXiv'2022)</a></li>
        <li><a href="configs/milan">MILAN (arXiv'2022)</a></li>
        <li><a href="configs/beitv2">BEiT V2 (arXiv'2022)</a></li>
        <li><a href="configs/eva">EVA (CVPR'2023)</a></li>
        <li><a href="configs/mixmim">MixMIM (arXiv'2022)</a></li>
        <li><a href="configs/itpn">iTPN (CVPR'2023)</a></li>
        <li><a href="configs/spark">SparK (ICLR'2023)</a></li>
        <li><a href="configs/mff">MFF (ICCV'2023)</a></li>
        </ul>
      </td>
      <td>
        <ul>
        <li><a href="configs/blip">BLIP (arxiv'2022)</a></li>
        <li><a href="configs/blip2">BLIP-2 (arxiv'2023)</a></li>
        <li><a href="configs/ofa">OFA (CoRR'2022)</a></li>
        <li><a href="configs/flamingo">Flamingo (NeurIPS'2022)</a></li>
        <li><a href="configs/chinese_clip">Chinese CLIP (arxiv'2022)</a></li>
        <li><a href="configs/minigpt4">MiniGPT-4 (arxiv'2023)</a></li>
        <li><a href="configs/llava">LLaVA (arxiv'2023)</a></li>
        <li><a href="configs/otter">Otter (arxiv'2023)</a></li>
        </ul>
      </td>
      <td>
      图像检索任务：
        <ul>
        <li><a href="configs/arcface">ArcFace (CVPR'2019)</a></li>
        </ul>
      训练和测试 Tips:
        <ul>
        <li><a href="https://arxiv.org/abs/1909.13719">RandAug</a></li>
        <li><a href="https://arxiv.org/abs/1805.09501">AutoAug</a></li>
        <li><a href="mmpretrain/datasets/samplers/repeat_aug.py">RepeatAugSampler</a></li>
        <li><a href="mmpretrain/models/tta/score_tta.py">TTA</a></li>
        <li>...</li>
        </ul>
      </td>
  </tbody>
</table>

## 参与贡献

我们非常欢迎任何有助于提升 MMPreTrain 的贡献，请参考 [贡献指南](https://mmpretrain.readthedocs.io/zh_CN/latest/notes/contribution_guide.html) 来了解如何参与贡献。

## 致谢

MMPreTrain 是一款由不同学校和公司共同贡献的开源项目。我们感谢所有为项目提供算法复现和新功能支持的贡献者，以及提供宝贵反馈的用户。
我们希望该工具箱和基准测试可以为社区提供灵活的代码工具，供用户复现现有算法并开发自己的新模型，从而不断为开源社区提供贡献。

## 引用

如果你在研究中使用了本项目的代码或者性能基准，请参考如下 bibtex 引用 MMPreTrain。

```BibTeX
@misc{2023mmpretrain,
    title={OpenMMLab's Pre-training Toolbox and Benchmark},
    author={MMPreTrain Contributors},
    howpublished = {\url{https://github.com/open-mmlab/mmpretrain}},
    year={2023}
}
```

## 许可证

该项目开源自 [Apache 2.0 license](LICENSE).

## OpenMMLab 的其他项目

- [MMEngine](https://github.com/open-mmlab/mmengine): OpenMMLab 深度学习模型训练基础库
- [MMCV](https://github.com/open-mmlab/mmcv): OpenMMLab 计算机视觉基础库
- [MIM](https://github.com/open-mmlab/mim): MIM 是 OpenMMlab 项目、算法、模型的统一入口
- [MMEval](https://github.com/open-mmlab/mmeval): 统一开放的跨框架算法评测库
- [MMPreTrain](https://github.com/open-mmlab/mmpretrain): OpenMMLab 深度学习预训练工具箱
- [MMDetection](https://github.com/open-mmlab/mmdetection): OpenMMLab 目标检测工具箱
- [MMDetection3D](https://github.com/open-mmlab/mmdetection3d): OpenMMLab 新一代通用 3D 目标检测平台
- [MMRotate](https://github.com/open-mmlab/mmrotate): OpenMMLab 旋转框检测工具箱与测试基准
- [MMYOLO](https://github.com/open-mmlab/mmyolo): OpenMMLab YOLO 系列工具箱与测试基准
- [MMSegmentation](https://github.com/open-mmlab/mmsegmentation): OpenMMLab 语义分割工具箱
- [MMOCR](https://github.com/open-mmlab/mmocr): OpenMMLab 全流程文字检测识别理解工具包
- [MMPose](https://github.com/open-mmlab/mmpose): OpenMMLab 姿态估计工具箱
- [MMHuman3D](https://github.com/open-mmlab/mmhuman3d): OpenMMLab 人体参数化模型工具箱与测试基准
- [MMSelfSup](https://github.com/open-mmlab/mmselfsup): OpenMMLab 自监督学习工具箱与测试基准
- [MMRazor](https://github.com/open-mmlab/mmrazor): OpenMMLab 模型压缩工具箱与测试基准
- [MMFewShot](https://github.com/open-mmlab/mmfewshot): OpenMMLab 少样本学习工具箱与测试基准
- [MMAction2](https://github.com/open-mmlab/mmaction2): OpenMMLab 新一代视频理解工具箱
- [MMTracking](https://github.com/open-mmlab/mmtracking): OpenMMLab 一体化视频目标感知平台
- [MMFlow](https://github.com/open-mmlab/mmflow): OpenMMLab 光流估计工具箱与测试基准
- [MMagic](https://github.com/open-mmlab/mmagic): OpenMMLab 新一代人工智能内容生成（AIGC）工具箱
- [MMGeneration](https://github.com/open-mmlab/mmgeneration): OpenMMLab 图片视频生成模型工具箱
- [MMDeploy](https://github.com/open-mmlab/mmdeploy): OpenMMLab 模型部署框架
- [Playground](https://github.com/open-mmlab/playground): 收集和展示 OpenMMLab 相关的前沿、有趣的社区项目

## 欢迎加入 OpenMMLab 社区

扫描下方的二维码可关注 OpenMMLab 团队的 [知乎官方账号](https://www.zhihu.com/people/openmmlab)，扫描下方微信二维码添加喵喵好友，进入 MMPretrain 微信交流社群。【加好友申请格式：研究方向+地区+学校/公司+姓名】

<div align="center">
<img src="./resources/zhihu_qrcode.jpg" height="400"/> <img src="./resources/miaomiao_qrcode.jpg" height="400"/>
</div>

我们会在 OpenMMLab 社区为大家

- 📢 分享 AI 框架的前沿核心技术
- 💻 解读 PyTorch 常用模块源码
- 📰 发布 OpenMMLab 的相关新闻
- 🚀 介绍 OpenMMLab 开发的前沿算法
- 🏃 获取更高效的问题答疑和意见反馈
- 🔥 提供与各行各业开发者充分交流的平台

干货满满 📘，等你来撩 💗，OpenMMLab 社区期待您的加入 👬
