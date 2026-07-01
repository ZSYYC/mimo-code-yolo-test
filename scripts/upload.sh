#!/bin/bash
# Git 上传脚本 - 仅同步脚本文件，不同步模型权重和运行结果

set -e

# 检查是否在 git 仓库中
if [ ! -d .git ]; then
    echo "错误：当前目录不是 git 仓库"
    exit 1
fi

# 添加所有文件（.gitignore 会自动排除模型权重和运行结果）
git add .

# 检查是否有更改需要提交
if git diff --cached --quiet; then
    echo "没有需要提交的更改"
    exit 0
fi

# 提交更改
if [ -n "$1" ]; then
    git commit -m "$1"
else
    git commit -m "更新脚本文件"
fi

# 推送到远程仓库
git push

echo "上传完成！"
