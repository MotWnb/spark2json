import json
import os

from .decoder import parse_message

__all__ = ['parse_message', 'convert']
__version__ = '1.0.0'


def convert(src: str, dst=None):
    with open(src, 'rb') as fh:
        data = fh.read()
    parsed = parse_message(data, 'SamplerData')
    text = json.dumps(parsed, ensure_ascii=False, indent=1)
    if dst == '-' or dst is None and src.endswith('.json'):
        return text
    if dst is None:
        dst = os.path.splitext(src)[0] + '.json'
    with open(dst, 'w', encoding='utf8') as fh:
        fh.write(text)
    return dst
