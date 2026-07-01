# ==============================================================================
# YOLO26 自动超参数搜索 (Hyperparameter Tuning) 脚本
# 
# 基于 Ultralytics 官方文档：
# - Hyperparameter Tuning: https://docs.ultralytics.com/guides/hyperparameter-tuning/
# - YOLO26 Training Recipe: https://docs.ultralytics.com/guides/yolo26-training-recipe/
# ==============================================================================

from ultralytics import YOLO

def main():
    # 1. 初始化 YOLO26 模型
    # YOLO26 提供了多种不同尺度的模型 (n, s, m, l, x)。
    # 这里以 yolo26n.pt (Nano 版本) 为例，建议根据自己的算力选择合适的初始权重。
    model = YOLO('yolo26n.pt')

    # 2. 配置并启动自动超参数搜索 (Tuning)
    # Ultralytics 默认使用遗传算法 (Genetic Algorithm) 来变异和评估超参数配置。
    # 推荐设置最少 300 次 iterations 以获得最佳结果。
    
    print("🚀 开始进行 YOLO26 超参数进化搜索...")
    
    # 提示：tune() 方法会在底层反复调用 train() 进行简短的训练，
    # 请确保你的机器有充足的 GPU 资源。
    # model.tune(
    #     data='your-dataset.yaml',  # TODO: 替换为你的数据集 yaml 配置文件路径
    #     epochs=30,                 # 每次演化的训练轮数（推荐设置较小值，例如 30~50 以加速搜索）
    #     iterations=300,            # 遗传算法进化代数，官方推荐最少 300
    #     optimizer='MuSGD',         # YOLO26 训练策略中推荐的优化器：MuSGD 结合了 SGD 和 Muon 风格的更新
    #     batch=16,                  # 根据显存大小调整
    #     imgsz=640,                 # 图像大小，通常为 640 或更高
    #     save=False,                # 搜索期间不保存不必要的模型权重以节省空间
    #     plots=False,               # 搜索期间不生成图表以加快速度
    #     val=False                  # 搜索期间仅在最后一轮进行验证
    # )
    model.tune(
    data='your-dataset.yaml',
    fraction=0.02,             # 🌟 关键：只随机使用 2% 的数据 (约 2 万张图) 来进行搜索
    epochs=30,                 # 针对子集，将每次评估的 epoch 降低到 10~20
    iterations=100,            # 迭代次数也可以适当降低到 100 次以节省时间
    optimizer='MuSGD',
    batch=128,                  # 尽量拉满你的显存
    imgsz=768,
    save=False,
    plots=False,
    val=False
    )
    # 3. 搜索结束提示
    # 搜索完成后，Ultralytics 会自动将表现最好的超参数保存为 best_hyperparameters.yaml
    print("✅ 超参数搜索完成！")
    print("💡 最佳超参数结果通常保存在类似路径: runs/detect/tune/best_hyperparameters.yaml")
    print("你可以使用该 yaml 文件作为新的超参数配置来完整训练你的 YOLO26 模型。")
    print("例如: model.train(data='your-dataset.yaml', epochs=300, cfg='runs/detect/tune/best_hyperparameters.yaml')")

if __name__ == '__main__':
    main()
