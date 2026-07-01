from ultralytics import YOLO
# 流程大概是：
# 1. 第一次随机生成一组超参数（不是只改一个参数，而是所有待搜索参数一起随机采样）
#     然后训练 30 个 epoch。
# 2. 得到 fitness（通常综合 mAP 等指标）。
# 3. 第二次不是重新随机，而是：
#     * 选择目前最好的参数
#     * 对它做轻微变异（mutation）
#     * 或与其他优秀参数交叉（crossover）
#     * 得到新的一整套参数
#     * 再训练 30 个 epoch。
# 4. 重复直到 iterations 次结束。
# 所以：
# 一次 iteration = 一整套超参数训练一次，而不是一个参数训练一次。
# -----------------------------
# Configuration
# -----------------------------
MODEL = "yolo26n.pt"
DATA = "dataset.yaml"

IMGSZ = 768

SEARCH_EPOCHS = 30      # 每组参数训练30轮
ITERATIONS = 120        # 搜索120组参数

PROJECT = "runs/tune"
NAME = "yolo26n_768"

# -----------------------------
# Search Space
# -----------------------------
search_space = {
    # Optimizer
    "lr0": (3e-5, 3e-3),
    "lrf": (0.01, 0.20),
    "weight_decay": (1e-5, 1e-3),
    "warmup_epochs": (0.0, 5.0),
    # Loss
    "box": (4.0, 8.0),
    "cls": (0.2, 1.0),
    # Color Augmentation
    "hsv_h": (0.0, 0.08),
    "hsv_s": (0.2, 0.9),
    "hsv_v": (0.2, 0.9),
    # Geometry
    "translate": (0.0, 0.3),
    "scale": (0.3, 0.95),
    "degrees": (0.0, 5.0),
    # Flip
    "fliplr": (0.0, 1.0),
    # Strong Augmentation
    "mosaic": (0.5, 1.0),
    "mixup": (0.0, 0.3),
    "close_mosaic": (5, 20),
}

# -----------------------------
# Model
# -----------------------------
model = YOLO(MODEL)

results = model.tune(
    data=DATA,
    imgsz=IMGSZ,
    epochs=SEARCH_EPOCHS,
    iterations=ITERATIONS,
    optimizer="AdamW",
    batch=16,
    workers=8,
    device=0,
    cache=True,
    amp=True,
    # 是否可复现
    deterministic=False,
    cos_lr=True,
    plots=False,
    space=search_space,
    project=PROJECT,
    name=NAME,
)

print(results)


# 这两个问题问得非常专业！直接切中了模型调参（Tuning）过程中的核心机制。

# 以下是针对这两个问题的详细解答：

# ### 1. 为什么不用设置 `search_space`（搜索空间）？

# 在很多传统的机器学习框架（如 Optuna 或 Ray Tune）中，你确实需要手动定义每个参数的搜索范围（比如学习率是 $10^{-5}$ 到 $10^{-2}$）。

# 但 **Ultralytics YOLO 框架内建了一套高度优化的“默认搜索空间”**。当你调用 `model.tune()` 且没有额外指定时，框架会自动使用底层预设的超参数变异范围。

# * **默认空间包含了什么？** 它包含了近 30 个对 YOLO 目标检测影响最大的超参数，包括：初始学习率 (`lr0`)、最终学习率 (`lrf`)、动量 (`momentum`)、权重衰减 (`weight_decay`)、预热轮数 (`warmup_epochs`)，以及各种数据增强比例（如 `hsv_h`, `mosaic`, `mixup` 等）。
# * **为什么推荐用默认的？** YOLO 官方团队在 COCO 等超大数据集上测试后得出的这套默认变异范围，往往比我们手动拍脑袋设置的范围更科学。对于绝大多数自定义数据集，直接使用底层默认的 search space 就能搜索出极佳的结果。

# **如果你非要自定义搜索空间该怎么做？**
# 如果你明确知道只想调某几个参数（比如只想调学习率），Ultralytics 也支持结合 `Ray Tune` 来定义特定的 `space`，或者通过修改源码中的 `default.yaml` 来实现。但在 100 万级别的数据量面前，建议**直接相信官方的默认搜索空间**，把精力花在数据抽样（Fraction）上。

# ---

# ### 2. 为什么之前脚本里建议加上 `val=False`？

# 这是一个非常敏锐的发现！我需要向你详细解释其**初衷**以及一个**需要注意的避坑点**。

# **初衷：为了极大地节省时间**

# * 在正常的 `model.train()` 中，YOLO 默认会在**每一个 Epoch 结束时**都在验证集上跑一遍，计算一次 mAP（平均精度）。
# * 在超参数搜索（Tuning）时，遗传算法通常只需要知道这组参数在跑完 30 个 Epoch 后的最终表现（Fitness Score）即可。
# * 如果你有 300 次迭代，每次 30 个 Epoch，那就是要训练 9000 个 Epoch。如果每次 Epoch 都去做完整的验证，耗费的时间是极其恐怖的（尤其你的数据量极大，即便抽样后验证集也不小）。
# * 因此，初衷是想关闭**过程中的逐轮验证**，仅让算法评估最终结果。

# **⚠️ 修正与避坑建议（重要）：**
# 尽管关闭逐轮验证能省时间，但在 Ultralytics 较新的版本中，`model.tune()` 的底层逻辑已经非常智能。它内部会自动精简输出并优化验证流程（比如默认自动把 `plots` 和 `save` 关掉）。

# 如果你强行传入 `val=False`，在某些特定版本的 Ultralytics 中，**可能会导致整个训练过程完全不计算任何验证指标 (mAP)**。如果验证指标为 0，遗传算法就拿不到 Fitness Score（适应度分数），导致 300 次迭代搜了个寂寞。

# **👉 最终建议做法：**
# 为了保证不出 bug 且遗传算法能稳定拿到评估分数，**最安全的做法是直接去掉 `val=False**`，把这些底层控制权交还给 `tune()` 函数自己去管理。

# 你可以把脚本精简成这样，最安全且高效：

# ```python
# model.tune(
#     data='your-dataset.yaml',
#     fraction=0.02,             # 100万数据千万别忘了这个！只用 2% 搜索
#     epochs=15,                 # 搜索时每个组合跑 15 轮看个趋势即可
#     iterations=100,            # 迭代 100 次不同参数组合
#     optimizer='MuSGD',         
#     batch=32,                  
#     imgsz=640
#     # 删除了 save, plots 和 val 的强制干预，让 tune() 自动处理
# )

# ```