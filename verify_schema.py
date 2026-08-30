import re
import sys

sys.path.insert(0, 'src')
from spark2json.decoder import SCHEMAS, ENUMS

PROTO_DIR = '../spark/spark-common/src/main/proto/spark'

NESTED_FLAT = {
    'SystemStatistics.Cpu': 'Cpu',
    'SystemStatistics.Cpu.Usage': 'CpuUsage',
    'SystemStatistics.Memory': 'SysMemory',
    'SystemStatistics.Memory.MemoryPool': 'MemoryPool64',
    'SystemStatistics.Gc': 'Gc',
    'SystemStatistics.Disk': 'Disk',
    'SystemStatistics.Os': 'Os',
    'SystemStatistics.Java': 'Java',
    'SystemStatistics.Jvm': 'Jvm',
    'SystemStatistics.NetInterface': 'NetInterface',
    'PlatformStatistics.Memory': 'PlatMemory',
    'PlatformStatistics.Memory.MemoryPool': 'PlatMemoryPool',
    'PlatformStatistics.Gc': 'Gc',
    'PlatformStatistics.Tps': 'Tps',
    'PlatformStatistics.Mspt': 'Mspt',
    'PlatformStatistics.Ping': 'Ping',
    'PlatformStatistics.OnlineMode': 'ENUM:OnlineMode',
    'WorldStatistics.World': 'World',
    'WorldStatistics.Region': 'Region',
    'WorldStatistics.Chunk': 'Chunk',
    'WorldStatistics.GameRule': 'GameRule',
    'WorldStatistics.DataPack': 'DataPack',
    'SamplerMetadata.ThreadDumper': 'ThreadDumper',
    'SamplerMetadata.ThreadDumper.Type': 'ENUM:ThreadDumper',
    'SamplerMetadata.DataAggregator': 'DataAggregator',
    'SamplerMetadata.DataAggregator.Type': 'ENUM:AggregatorType',
    'SamplerMetadata.DataAggregator.ThreadGrouper': 'ENUM:ThreadGrouper',
    'SamplerMetadata.SamplerMode': 'ENUM:SamplerMode',
    'SamplerMetadata.SamplerEngine': 'ENUM:SamplerEngine',
    'PlatformMetadata.Type': 'ENUM:PlatformType',
    'CommandSenderMetadata.Type': 'ENUM:SenderType',
    'WorldInfoMetricSeries.Values': 'WorldInfoMetricSeriesValues',
}

SCALAR_TYPES = {'string', 'bytes', 'bool', 'int32', 'int64', 'uint32', 'uint64', 'double', 'float'}

IRRELEVANT = {'HealthData', 'HealthMetadata'}

problems = []

def load_messages():
    all_msgs, all_enums = {}, {}
    for pf in ('spark.proto', 'spark_sampler.proto'):
        text = open(f'{PROTO_DIR}/{pf}', encoding='utf8').read()
        text = re.sub(r'//[^\n]*', '', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
        text = re.sub(r'\bsyntax\s*=\s*"[^"]*"\s*;', '', text)
        text = re.sub(r'\bpackage\s+[\w.]+\s*;', '', text)
        text = re.sub(r'\boption\s+[^;]+;', '', text)
        text = re.sub(r'\bimport\s+[^;]+;', '', text)
        text = re.sub(r'\breserved\s+[^;]+;', '', text)
        _parse_block(text, '', all_msgs, all_enums)
    return all_msgs, all_enums

def _parse_block(text, prefix, msgs, enums):
    i, n = 0, len(text)
    while True:
        brace = text.find('{', i)
        if brace == -1:
            break
        kind = name = None
        for m in re.finditer(r'(message|enum)\s+(\w+)\s*$', text[i:brace]):
            kind, name = m.group(1), m.group(2)
        depth, j = 1, brace + 1
        while depth and j < n:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
            j += 1
        body = text[brace + 1:j - 1]
        full = (prefix + '.' + name) if prefix else name
        if kind == 'message':
            fields = []
            own = _strip_nested(body)
            for m in re.finditer(r'(map\s*<[^>]+>|[\w.]+)\s+(\w+)\s*=\s*(\d+)\s*;', own):
                fields.append((int(m.group(3)), m.group(2), re.sub(r'\s+', '', m.group(1))))
            msgs[full] = fields
            _parse_block(body, full, msgs, enums)
        elif kind == 'enum':
            vals = {int(m.group(2)): m.group(1) for m in re.finditer(r'(\w+)\s*=\s*(-?\d+)\s*;', body)}
            enums[full] = vals
        i = j

def _strip_nested(body):
    out, i, n = [], 0, len(body)
    while i < n:
        brace = body.find('{', i)
        if brace == -1:
            out.append(body[i:])
            break
        if not re.search(r'(message|enum)\s+\w+\s*$', body[i:brace]):
            out.append(body[i:brace + 1])
            i = brace + 1
            continue
        out.append(body[i:brace])
        depth, j = 1, brace + 1
        while depth and j < n:
            if body[j] == '{':
                depth += 1
            elif body[j] == '}':
                depth -= 1
            j += 1
        i = j
    return ''.join(out)

def resolve_typename(raw, owner_full, msgs, enums):
    if raw.startswith('map<'):
        inner = re.sub(r'\s+', '', raw[4:-1])
        k, v = inner.split(',', 1)
        return ('map', resolve_typename(k, owner_full, msgs, enums),
                resolve_typename(v, owner_full, msgs, enums))
    if raw in SCALAR_TYPES:
        return raw
    scope = owner_full
    while True:
        cand = (scope + '.' + raw) if scope else raw
        if cand in msgs or cand in enums:
            flat = NESTED_FLAT.get(cand, cand)
            if flat is None:
                problems.append(f'NO FLAT MAPPING for proto type "{cand}" (referenced by {owner_full})')
                return None
            if flat.startswith('ENUM:'):
                return ('enum', flat[5:])
            return ('msg', flat)
        if not scope:
            break
        scope = scope.rsplit('.', 1)[0] if '.' in scope else ''
    problems.append(f'UNRESOLVED proto type "{raw}" (referenced by {owner_full})')
    return None

def main():
    msgs, enums = load_messages()

    flat_enums = {}
    for full, vals in enums.items():
        flat = NESTED_FLAT.get(full)
        if flat and flat.startswith('ENUM:'):
            flat_enums[flat[5:]] = vals

    checked_msgs = checked_fields = checked_enums = 0
    for full, fields in sorted(msgs.items()):
        target = NESTED_FLAT.get(full, full)
        if target.startswith('ENUM:'):
            target = target[5:]
        if full in IRRELEVANT:
            if target in SCHEMAS:
                problems.append(f'{full}: irrelevant message unexpectedly in SCHEMAS')
            continue
        ours = SCHEMAS.get(target)
        if ours is None:
            problems.append(f'MISSING message: {full} (schema "{target}" not in SCHEMAS)')
            continue
        checked_msgs += 1
        for num, fname, ftyp in fields:
            expected = resolve_typename(ftyp, full, msgs, enums)
            if num not in ours:
                problems.append(f'{full}.{fname} (field {num}, type {ftyp}): MISSING in SCHEMAS["{target}"]')
                continue
            checked_fields += 1
            oname, otyp, _ = ours[num]
            if oname != fname:
                problems.append(f'{full} field {num}: name mismatch proto="{fname}" ours="{oname}"')
            def norm(t):
                if isinstance(t, tuple) and t[0] == 'msg':
                    return t
                if isinstance(t, tuple) and t[0] == 'map':
                    return ('map', t[1], norm(t[2]))
                if isinstance(t, str) and t in SCHEMAS:
                    return ('msg', t)
                return t
            if expected is not None and norm(otyp) != expected:
                problems.append(f'{full}.{fname} (field {num}): type mismatch proto={expected} ours={otyp}')

    for ename, evals in sorted(flat_enums.items()):
        checked_enums += 1
        ours = ENUMS.get(ename)
        if ours is None:
            problems.append(f'MISSING enum: {ename}')
        elif ours != evals:
            problems.append(f'enum {ename} mismatch: proto={evals} ours={ours}')

    extra_enums = set(ENUMS) - set(flat_enums)
    if extra_enums:
        problems.append(f'extra enums in ours not present in protos: {sorted(extra_enums)}')

    print(f'checked {checked_msgs} messages ({checked_fields} fields) / {checked_enums} enums '
          f'against {len(msgs)} proto messages / {len(enums)} proto enums')
    if problems:
        print(f'\n{len(problems)} problem(s):')
        for p in problems:
            print(' -', p)
        sys.exit(1)
    print('ALL MATCH')

if __name__ == '__main__':
    main()
