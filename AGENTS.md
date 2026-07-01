# AGENTS.md

## 环境信息

- Python 版本: 3.12
- 虚拟环境工具: uv (v0.6.12)
- 框架: Ultralytics YOLO26
- 目标模型: yolo26n
- 测试数据集: coco128

## 快速开始

### 1. 初始化虚拟环境并安装依赖

```bash
# 使用 uv 创建虚拟环境并安装 ultralytics
uv venv
source .venv/bin/activate
uv pip install ultralytics
```

### 2. 验证安装

```bash
python -c "from ultralytics import YOLO; print('Ultralytics OK')"
yolo version
```

### 3. 训练测试 (使用 coco128)

```bash
# CLI 方式训练 (epochs=1 用于快速验证)
yolo detect train model=yolo26n.pt data=coco128.yaml epochs=1 imgsz=640

# 或 Python 方式
python -c "
from ultralytics import YOLO
model = YOLO('yolo26n.pt')
model.train(data='coco128.yaml', epochs=1, imgsz=640)
"
```

### 4. 推理测试

```bash
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
```

## 注意事项

- 模型权重 `yolo26n.pt` 首次运行时会自动下载
- coco128 数据集首次使用时会自动下载到 `datasets/coco128`
- macOS 上默认使用 CPU，训练较慢但可用于验证环境
- 如需 GPU 加速需安装对应的 PyTorch CUDA 版本

## 训练结果

训练结果保存在 `runs/detect/` 目录下：
- `runs/detect/train/` - 训练结果（包含权重、图表、混淆矩阵等）
- `runs/detect/train/weights/` - 模型权重（best.pt, last.pt）
- `runs/detect/train/results.csv` - 训练指标记录
- `runs/detect/train/results.png` - 训练曲线图

## 代码上传

当用户说"上传"时，执行以下脚本：

```bash
bash scripts/upload.sh "提交信息"
```

脚本会自动：
1. 添加所有文件（模型权重和运行结果已被 .gitignore 排除）
2. 提交更改
3. 推送到远程仓库

## 常用命令

| 任务 | 命令 |
|------|------|
| 训练 | `yolo detect train model=yolo26n.pt data=coco128.yaml epochs=100` |
| 验证 | `yolo detect val model=best.pt data=coco128.yaml` |
| 推理 | `yolo detect predict model=best.pt source=path/to/images` |
| 导出 | `yolo export model=best.pt format=onnx` |
| 上传 | `bash scripts/upload.sh "提交信息"` |
