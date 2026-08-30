# spark2json

[English](README.md) | 简体中文

将 [spark](https://github.com/lucko/spark) 生成的 `.sparkprofile` 文件转换为可读的 JSON。

完全自包含，只依赖 Python 标准库，不需要 protoc、`*_pb2.py` 绑定或任何第三方包。

Windows、Linux、macOS 的独立可执行文件可在 [Releases](../../releases) 页面下载（使用 [Nuitka](https://nuitka.net) 打包），最终用户无需安装 Python。

## 背景

[spark](https://github.com/lucko/spark) 是一款流行的 Minecraft 服务端性能分析插件。它生成的 `.sparkprofile` 文件是 protobuf 编码的二进制数据，通常只能上传到 spark 官网查看。本工具将其在本地直接解码为 JSON，方便脚本处理、数据分析或离线归档。

## 安装

推荐使用 [uv](https://docs.astral.sh/uv/)：

```bash
# 从项目目录安装
uv tool install .
```

也可以使用 pip：

```bash
pip install .
```

或从 [Releases](../../releases) 下载独立二进制文件（Nuitka 打包，无需 Python 环境）。

## 使用

命令行：

```bash
spark2json EeMEbUmJ3R.sparkprofile                 # 输出到 EeMEbUmJ3R.json
spark2json in.sparkprofile out.json                # 指定输出文件
spark2json in.sparkprofile -                       # 打印到 stdout
```

作为库使用：

```python
from spark2json import parse_message

with open('EeMEbUmJ3R.sparkprofile', 'rb') as fh:
    data = parse_message(fh.read(), 'SamplerData')
```

## 输出结构

顶层对象为 `SamplerData`，主要字段：

| 字段 | 说明 |
|---|---|
| `metadata` | 采样元数据：创建者、起止时间、平台信息、CPU/内存/磁盘/Java 版本、TPS/MSPT/在线模式等 |
| `threads` | 采样到的线程，每个线程包含扁平的 `children` 数组和 `children_refs` 索引，构成调用树 |
| `time_window_statistics` | 每个时间窗口的统计：TPS、MSPT、CPU 占用、玩家数、实体数、区块数等 |
| `metrics` | 时间序列指标：TPS、tick 时长、CPU 占用、内存占用、世界信息、玩家延迟 |
| `class_sources` / `method_sources` / `line_sources` | 采样点归属的插件来源 |

注意：`ThreadNode` 和 `StackTraceNode` 的调用树采用扁平数组 + `children_refs` 索引表示（spark 的空间优化设计），而非嵌套结构。`times` 为 repeated double，每个采样窗口对应一个值（单位：微秒）。

## 工作原理

`.sparkprofile` 是 protobuf 编码的 `SamplerData` 消息。本工具包含：

1. 一个手写的 proto 线格式（wire format）解码器，支持 varint、64-bit、length-delimited、32-bit 四种 wire type；
2. 一份按 spark 官方 proto schema（`spark-common/src/main/proto/spark_sampler.proto` 等）硬编码的字段映射表，含枚举名称映射；
3. 一个递归的通用 message 解码器，支持嵌套 message、packed repeated、map 类型；未知字段自动跳过（前向兼容）。

## 系统要求

- Python 3.8 或更高版本
- 无任何第三方依赖

## 打包独立可执行文件

CI 工作流（`.github/workflows/build.yml`）在每次推送时使用 Nuitka 为 Windows、Linux、macOS 构建二进制文件，并以 `v` 开头的 tag 发布时自动附加到 GitHub Releases。

本地手动打包：

```bash
pip install . nuitka
python -m nuitka --onefile --assume-yes-for-downloads \
    --include-package=spark2json nuitka_main.py
```

## 与 spark 原生行为的一致性校验

仓库内附两个校验脚本（需要本地存在 `../spark` checkout）：

- `verify_schema.py`：解析 spark 官方 `.proto` 文件，逐字段比对本工具的字段映射表（消息名、字段号、字段名、类型、枚举值）。当前覆盖 43 个消息 / 195 个字段 / 8 组枚举，全部一致。
- `test_diff.py`：用官方 protoc 生成绑定，随机填充一个覆盖所有字段类型的 `SamplerData`（含嵌套消息、packed repeated、map、枚举、uint32、负数 int64/int32、bytes），序列化后用本工具解码，并与官方 protobuf 反射 API 的结果逐字段比对。多个随机种子下均完全一致。

调用树语义（`children_refs` 指向扁平 `children` 数组的索引、`times` 按窗口透传）已对照 spark 源码 `AbstractNodeExporter.java` 确认。

## 许可证

本项目基于 [GPL-3.0](LICENSE) 发布。

`.sparkprofile` 的格式源自 spark 项目（同以 GPL-3.0 授权），本工具对其 proto schema 的字段映射直接派生自该项目的官方定义。

spark 本身：Copyright (C) lucko，详见其[项目仓库](https://github.com/lucko/spark)。
