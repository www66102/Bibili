# Video_Craw

## 项目简介

**Video_Craw** 是一个专注于从视频平台（如 Bilibili、YouTube、MOOC 等）爬取病理学相关视频的模块化工具。其目标是通过视频爬取和处理，构建包含病理学切片的图文对数据集，为多模态模型的微调提供高质量数据。

## 项目目标

1. **视频识别与爬取**：
   - 在指定平台上查找并识别病理学相关视频。
   - 获取视频的唯一 ID。
2. **视频下载与处理**：
   - 使用开源工具下载视频。
   - 提取视频帧并生成图文对数据。

## 项目进度表

| 序号 | 标题                 | 更改的内容                          | 状态     |
|------|----------------------|-------------------------------------|----------|
| 1    | 项目架构设计         | 重新设计项目结构，模块化代码        | 进行中   |
| 2    | 视频爬取模块开发     | 实现 Bilibili 视频爬取功能          | 进行中   |
| 3    | 视频下载模块开发     | 集成开源工具实现视频下载            | 未开始   |
| 4    | 数据处理模块开发     | 提取视频帧并生成图文对数据          | 未开始   |
| 5    | 测试与文档完善       | 编写测试用例并完善文档              | 未开始   |

## 文件目录结构

```
Video_Craw/
├── README.md                # 项目说明文档
├── Bilibili/                # Bilibili 平台相关代码
│   ├── 1.py                 # 示例代码（已重构功能）
│   ├── downloaded_bv.txt    # 已下载视频的 ID 列表
├── docs/                    # 文档目录
│   └── Prompt.md            # 项目需求文档
├── src/                     # 源代码目录
│   ├── __init__.py          # 包初始化文件
│   ├── bilibili_scraper.py  # 项目入口，调用 Bilibili 模块功能
│   ├── config.py            # 配置文件
│   └── bilibili/            # Bilibili 模块
│       ├── __init__.py      # Bilibili 模块初始化
│       └── scraper.py       # Bilibili 爬取功能实现
├── tests/                   # 测试目录
│   └── test_bilibili_scraper.py # 测试 Bilibili 爬取模块
```

## 使用说明

1. **创建并激活 Conda 虚拟环境**：
   ```bash
   conda create -n video_craw python=3.9 -y
   conda activate video_craw
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **运行爬取脚本**：
   ```bash
   python src/bilibili_scraper.py
   ```

4. **运行测试**：
   ```bash
   pytest tests/
   ```

## 贡献指南

欢迎对本项目提出建议或贡献代码！请提交 Pull Request 或创建 Issue。
