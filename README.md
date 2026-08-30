# spark2json

English | [简体中文](README.zh-CN.md)

Convert spark `.sparkprofile` files into readable JSON.

Fully self-contained: it only depends on the Python standard library and needs neither protoc, `*_pb2.py` bindings, nor any third-party package.

Prebuilt standalone binaries for Windows, Linux and macOS are available on the [Releases](../../releases) page, so end users do not need a Python installation at all.

## Background

[spark](https://github.com/lucko/spark) is a popular performance profiler for Minecraft servers. The `.sparkprofile` files it produces are protobuf-encoded binary data that normally can only be viewed by uploading them to the spark website. This tool decodes them locally into JSON, which makes scripted processing, data analysis and offline archiving easy.

## Install

Prefer [uv](https://docs.astral.sh/uv/):

```bash
uv tool install .
```

Or use pip:

```bash
pip install .
```

Or grab a standalone binary from [Releases](../../releases) (built with [Nuitka](https://nuitka.net), no Python required).

## Usage

Command line:

```bash
spark2json EeMEbUmJ3R.sparkprofile                 # writes EeMEbUmJ3R.json
spark2json in.sparkprofile out.json                # explicit output file
spark2json in.sparkprofile -                       # print to stdout
```

As a library:

```python
from spark2json import parse_message

with open('EeMEbUmJ3R.sparkprofile', 'rb') as fh:
    data = parse_message(fh.read(), 'SamplerData')
```

## Output structure

The top-level object is `SamplerData` with these main fields:

| Field | Description |
|---|---|
| `metadata` | Sampler metadata: creator, start/end time, platform info, CPU/memory/disk/Java version, TPS/MSPT, online mode, and so on |
| `threads` | Sampled threads; each thread holds a flat `children` array plus a `children_refs` index that forms the call tree |
| `time_window_statistics` | Per-window statistics: TPS, MSPT, CPU usage, player count, entity count, chunk count, etc. |
| `metrics` | Time-series metrics: TPS, tick duration, CPU usage, memory usage, world info, player ping |
| `class_sources` / `method_sources` / `line_sources` | Plugin attribution of sampled locations |

Note: the call tree in `ThreadNode` and `StackTraceNode` is represented as a flat array with `children_refs` indexes (a space optimization used by spark itself), not as a nested structure. `times` is a repeated double with one value per sampling window (unit: microseconds).

## How it works

A `.sparkprofile` file is a protobuf-encoded `SamplerData` message. This tool contains:

1. A hand-written proto wire-format decoder supporting all four wire types (varint, 64-bit, length-delimited, 32-bit);
2. A field mapping table hardcoded from spark's official proto schemas (`spark-common/src/main/proto/spark_sampler.proto` and friends), including enum name mappings;
3. A recursive generic message decoder supporting nested messages, packed repeated fields and map types; unknown fields are skipped (forward compatible).

## Requirements

- Python 3.8 or newer
- No third-party dependencies

## Building a standalone binary

The CI workflow (`.github/workflows/build.yml`) builds binaries for Windows, Linux and macOS with Nuitka on every push, and attaches them to GitHub Releases for tags starting with `v`.

To build locally:

```bash
pip install . nuitka
python -m nuitka --onefile --assume-yes-for-downloads \
    --include-package=spark2json nuitka_main.py
```

## License

This project is released under the [GPL-3.0](LICENSE).

The `.sparkprofile` format originates from the spark project (also GPL-3.0 licensed); this tool's proto schema field mappings are directly derived from that project's official definitions.

spark itself: Copyright (C) lucko, see its [repository](https://github.com/lucko/spark).
