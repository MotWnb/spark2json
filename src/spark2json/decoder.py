import struct

SCHEMAS = {}

ENUMS = {
    'SenderType':      {0: 'OTHER', 1: 'PLAYER'},
    'PlatformType':    {0: 'SERVER', 1: 'CLIENT', 2: 'PROXY', 3: 'APPLICATION'},
    'OnlineMode':      {0: 'UNKNOWN', 1: 'OFFLINE', 2: 'ONLINE'},
    'SamplerMode':     {0: 'EXECUTION', 1: 'ALLOCATION'},
    'SamplerEngine':   {0: 'JAVA', 1: 'ASYNC'},
    'ThreadDumper':    {0: 'ALL', 1: 'SPECIFIC', 2: 'REGEX'},
    'AggregatorType':  {0: 'SIMPLE', 1: 'TICKED'},
    'ThreadGrouper':   {0: 'BY_NAME', 1: 'BY_POOL', 2: 'AS_ONE'},
}

SCHEMAS['CommandSenderMetadata'] = {
    1: ('type', ('enum', 'SenderType'), 0),
    2: ('name', 'string', 0),
    3: ('unique_id', 'string', 0),
}

SCHEMAS['PlatformMetadata'] = {
    1: ('type', ('enum', 'PlatformType'), 0),
    2: ('name', 'string', 0),
    3: ('version', 'string', 0),
    4: ('minecraft_version', 'string', 0),
    7: ('spark_version', 'int32', 0),
    8: ('brand', 'string', 0),
}

SCHEMAS['PluginOrModMetadata'] = {
    1: ('name', 'string', 0),
    2: ('version', 'string', 0),
    3: ('author', 'string', 0),
    4: ('description', 'string', 0),
    5: ('builtin', 'bool', 0),
}

SCHEMAS['RollingAverageValues'] = {
    1: ('mean', 'double', 0),
    2: ('max', 'double', 0),
    3: ('min', 'double', 0),
    4: ('median', 'double', 0),
    5: ('percentile95', 'double', 0),
}

SCHEMAS['CpuUsage'] = {1: ('last1m', 'double', 0), 2: ('last15m', 'double', 0)}
SCHEMAS['Cpu'] = {
    1: ('threads', 'int32', 0),
    2: ('process_usage', ('msg', 'CpuUsage'), 0),
    3: ('system_usage', ('msg', 'CpuUsage'), 0),
    4: ('model_name', 'string', 0),
}
SCHEMAS['MemoryPool64'] = {1: ('used', 'int64', 0), 2: ('total', 'int64', 0)}
SCHEMAS['SysMemory'] = {
    1: ('physical', ('msg', 'MemoryPool64'), 0),
    2: ('swap', ('msg', 'MemoryPool64'), 0),
}
SCHEMAS['Gc'] = {1: ('total', 'int64', 0), 2: ('avg_time', 'double', 0), 3: ('avg_frequency', 'double', 0)}
SCHEMAS['Disk'] = {1: ('used', 'int64', 0), 2: ('total', 'int64', 0)}
SCHEMAS['Os'] = {1: ('arch', 'string', 0), 2: ('name', 'string', 0), 3: ('version', 'string', 0)}
SCHEMAS['Java'] = {1: ('vendor', 'string', 0), 2: ('version', 'string', 0), 3: ('vendor_version', 'string', 0), 4: ('vm_args', 'string', 0)}
SCHEMAS['Jvm'] = {1: ('name', 'string', 0), 2: ('vendor', 'string', 0), 3: ('version', 'string', 0)}
SCHEMAS['NetInterface'] = {
    1: ('rx_bytes_per_second', ('msg', 'RollingAverageValues'), 0),
    2: ('tx_bytes_per_second', ('msg', 'RollingAverageValues'), 0),
    3: ('rx_packets_per_second', ('msg', 'RollingAverageValues'), 0),
    4: ('tx_packets_per_second', ('msg', 'RollingAverageValues'), 0),
}
SCHEMAS['SystemStatistics'] = {
    1: ('cpu', ('msg', 'Cpu'), 0),
    2: ('memory', ('msg', 'SysMemory'), 0),
    3: ('gc', ('map', 'string', 'Gc'), 0),
    4: ('disk', ('msg', 'Disk'), 0),
    5: ('os', ('msg', 'Os'), 0),
    6: ('java', ('msg', 'Java'), 0),
    7: ('uptime', 'int64', 0),
    8: ('net', ('map', 'string', 'NetInterface'), 0),
    9: ('jvm', ('msg', 'Jvm'), 0),
}

SCHEMAS['MemoryUsage'] = {1: ('used', 'int64', 0), 2: ('committed', 'int64', 0), 3: ('init', 'int64', 0), 4: ('max', 'int64', 0)}
SCHEMAS['PlatMemoryPool'] = {1: ('name', 'string', 0), 2: ('usage', ('msg', 'MemoryUsage'), 0), 3: ('collection_usage', ('msg', 'MemoryUsage'), 0)}
SCHEMAS['PlatMemory'] = {
    1: ('heap', ('msg', 'MemoryUsage'), 0),
    2: ('non_heap', ('msg', 'MemoryUsage'), 0),
    3: ('pools', ('msg', 'PlatMemoryPool'), 1),
    4: ('alloc_bps_last1m', ('msg', 'RollingAverageValues'), 0),
    5: ('alloc_bps_last5m', ('msg', 'RollingAverageValues'), 0),
    6: ('alloc_bps_last15m', ('msg', 'RollingAverageValues'), 0),
}
SCHEMAS['Tps'] = {1: ('last1m', 'double', 0), 2: ('last5m', 'double', 0), 3: ('last15m', 'double', 0), 4: ('game_target_tps', 'int32', 0)}
SCHEMAS['Mspt'] = {1: ('last1m', ('msg', 'RollingAverageValues'), 0), 2: ('last5m', ('msg', 'RollingAverageValues'), 0), 3: ('game_max_ideal_mspt', 'int32', 0)}
SCHEMAS['Ping'] = {1: ('last15m', ('msg', 'RollingAverageValues'), 0)}
SCHEMAS['GameRule'] = {1: ('name', 'string', 0), 2: ('default_value', 'string', 0), 3: ('world_values', ('map', 'string', 'string'), 0)}
SCHEMAS['DataPack'] = {1: ('name', 'string', 0), 2: ('description', 'string', 0), 3: ('source', 'string', 0), 4: ('builtin', 'bool', 0)}
SCHEMAS['Chunk'] = {1: ('x', 'int32', 0), 2: ('z', 'int32', 0), 3: ('total_entities', 'int32', 0), 4: ('entity_counts', ('map', 'string', 'int32'), 0)}
SCHEMAS['Region'] = {1: ('total_entities', 'int32', 0), 2: ('chunks', ('msg', 'Chunk'), 1)}
SCHEMAS['World'] = {1: ('name', 'string', 0), 2: ('total_entities', 'int32', 0), 3: ('regions', ('msg', 'Region'), 1)}
SCHEMAS['WorldStatistics'] = {
    1: ('total_entities', 'int32', 0),
    2: ('entity_counts', ('map', 'string', 'int32'), 0),
    3: ('worlds', ('msg', 'World'), 1),
    4: ('game_rules', ('msg', 'GameRule'), 1),
    5: ('data_packs', ('msg', 'DataPack'), 1),
}
SCHEMAS['PlatformStatistics'] = {
    1: ('memory', ('msg', 'PlatMemory'), 0),
    2: ('gc', ('map', 'string', 'Gc'), 0),
    3: ('uptime', 'int64', 0),
    4: ('tps', ('msg', 'Tps'), 0),
    5: ('mspt', ('msg', 'Mspt'), 0),
    6: ('ping', ('msg', 'Ping'), 0),
    7: ('player_count', 'int64', 0),
    8: ('world', ('msg', 'WorldStatistics'), 0),
    9: ('online_mode', ('enum', 'OnlineMode'), 0),
}

SCHEMAS['SocketChannelInfo'] = {1: ('channel_id', 'string', 0), 2: ('public_key', 'bytes', 0)}

SCHEMAS['ThreadDumper'] = {
    1: ('type', ('enum', 'ThreadDumper'), 0),
    2: ('ids', 'int64', 1),
    3: ('patterns', 'string', 1),
}
SCHEMAS['DataAggregator'] = {
    1: ('type', ('enum', 'AggregatorType'), 0),
    2: ('thread_grouper', ('enum', 'ThreadGrouper'), 0),
    3: ('tick_length_threshold', 'int64', 0),
    4: ('number_of_included_ticks', 'int32', 0),
}
SCHEMAS['SamplerMetadata'] = {
    1: ('creator', ('msg', 'CommandSenderMetadata'), 0),
    2: ('start_time', 'int64', 0),
    3: ('interval', 'int32', 0),
    4: ('thread_dumper', ('msg', 'ThreadDumper'), 0),
    5: ('data_aggregator', ('msg', 'DataAggregator'), 0),
    6: ('comment', 'string', 0),
    7: ('platform_metadata', ('msg', 'PlatformMetadata'), 0),
    8: ('platform_statistics', ('msg', 'PlatformStatistics'), 0),
    9: ('system_statistics', ('msg', 'SystemStatistics'), 0),
    10: ('server_configurations', ('map', 'string', 'string'), 0),
    11: ('end_time', 'int64', 0),
    12: ('number_of_ticks', 'int32', 0),
    13: ('sources', ('map', 'string', 'PluginOrModMetadata'), 0),
    14: ('extra_platform_metadata', ('map', 'string', 'string'), 0),
    15: ('sampler_mode', ('enum', 'SamplerMode'), 0),
    16: ('sampler_engine', ('enum', 'SamplerEngine'), 0),
    17: ('sampler_engine_version', 'string', 0),
    18: ('metrics', ('msg', 'Metrics'), 0),
}

SCHEMAS['StackTraceNode'] = {
    3: ('class_name', 'string', 0),
    4: ('method_name', 'string', 0),
    5: ('parent_line_number', 'int32', 0),
    6: ('line_number', 'int32', 0),
    7: ('method_desc', 'string', 0),
    8: ('times', 'double', 1),
    9: ('children_refs', 'int32', 1),
}

SCHEMAS['ThreadNode'] = {
    1: ('name', 'string', 0),
    3: ('children', ('msg', 'StackTraceNode'), 1),
    4: ('times', 'double', 1),
    5: ('children_refs', 'int32', 1),
}

SCHEMAS['WindowStatistics'] = {
    1: ('ticks', 'int32', 0),
    2: ('cpu_process', 'double', 0),
    3: ('cpu_system', 'double', 0),
    4: ('tps', 'double', 0),
    5: ('mspt_median', 'double', 0),
    6: ('mspt_max', 'double', 0),
    7: ('players', 'int32', 0),
    8: ('entities', 'int32', 0),
    9: ('tile_entities', 'int32', 0),
    10: ('chunks', 'int32', 0),
    11: ('start_time', 'int64', 0),
    12: ('end_time', 'int64', 0),
    13: ('duration', 'int32', 0),
}

SCHEMAS['DoubleMetricSeries'] = {
    1: ('start_timestamp_ms', 'int64', 0),
    2: ('timestamp_deltas_ms', 'uint32', 1),
    3: ('values', 'double', 1),
}

SCHEMAS['AveragesMetricSeries'] = {
    1: ('start_timestamp_ms', 'int64', 0),
    2: ('timestamp_deltas_ms', 'uint32', 1),
    3: ('values', ('msg', 'RollingAverageValues'), 1),
}

SCHEMAS['MemoryUsageMetricSeries'] = {
    1: ('start_timestamp_ms', 'int64', 0),
    2: ('timestamp_deltas_ms', 'uint32', 1),
    3: ('values', ('msg', 'MemoryUsage'), 1),
}

SCHEMAS['WorldInfoMetricSeriesValues'] = {
    1: ('players', 'int32', 0),
    2: ('entities', 'int32', 0),
    3: ('tile_entities', 'int32', 0),
    4: ('chunks', 'int32', 0),
}

SCHEMAS['WorldInfoMetricSeries'] = {
    1: ('start_timestamp_ms', 'int64', 0),
    2: ('timestamp_deltas_ms', 'uint32', 1),
    3: ('values', ('msg', 'WorldInfoMetricSeriesValues'), 1),
}

SCHEMAS['Metrics'] = {
    1: ('tps', ('msg', 'DoubleMetricSeries'), 0),
    2: ('tick_duration', ('msg', 'AveragesMetricSeries'), 0),
    3: ('cpu_usage_process', ('msg', 'DoubleMetricSeries'), 0),
    4: ('cpu_usage_system', ('msg', 'DoubleMetricSeries'), 0),
    5: ('memory_usage_heap', ('msg', 'MemoryUsageMetricSeries'), 0),
    6: ('memory_usage_non_heap', ('msg', 'MemoryUsageMetricSeries'), 0),
    7: ('memory_allocation', ('msg', 'DoubleMetricSeries'), 0),
    8: ('world_info', ('msg', 'WorldInfoMetricSeries'), 0),
    9: ('player_ping', ('msg', 'AveragesMetricSeries'), 0),
}

SCHEMAS['SamplerData'] = {
    1: ('metadata', ('msg', 'SamplerMetadata'), 0),
    2: ('threads', ('msg', 'ThreadNode'), 1),
    3: ('class_sources', ('map', 'string', 'string'), 0),
    4: ('method_sources', ('map', 'string', 'string'), 0),
    5: ('line_sources', ('map', 'string', 'string'), 0),
    6: ('time_windows', 'int32', 1),
    7: ('time_window_statistics', ('map', 'int32', 'WindowStatistics'), 0),
    8: ('channel_info', ('msg', 'SocketChannelInfo'), 0),
}


class Wire:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.pos = 0

    def eof(self):
        return self.pos >= len(self.buf)

    def read_varint(self):
        result = 0
        shift = 0
        while True:
            b = self.buf[self.pos]
            self.pos += 1
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
        return result

    def read_bytes(self, n):
        v = self.buf[self.pos:self.pos + n]
        self.pos += n
        return v

    def read_double(self):
        return struct.unpack('<d', self.read_bytes(8))[0]

    def read_float(self):
        return struct.unpack('<f', self.read_bytes(4))[0]


def to_signed(z: int) -> int:
    if z >= (1 << 63):
        z -= (1 << 64)
    return z


def to_unsigned(z: int) -> int:
    if z < 0:
        z += (1 << 64)
    return z


def read_field(w: Wire):
    key = w.read_varint()
    num = key >> 3
    wt = key & 7
    if wt == 0:
        val = to_signed(w.read_varint())
    elif wt == 1:
        val = w.read_double()
    elif wt == 2:
        val = w.read_bytes(w.read_varint())
    elif wt == 5:
        val = w.read_float()
    else:
        raise ValueError("Unsupported wire type: %d (field %d)" % (wt, num))
    return num, wt, val


def unpack_packed_doubles(buf: bytes):
    return [struct.unpack('<d', buf[i:i + 8])[0] for i in range(0, len(buf), 8)]


def unpack_packed_ints(buf: bytes):
    w = Wire(buf)
    out = []
    while not w.eof():
        out.append(to_signed(w.read_varint()))
    return out


def _decode_map_entry(buf: bytes, key_type, val_type):
    w = Wire(buf)
    key, val = None, None
    while not w.eof():
        num, wt, raw = read_field(w)
        if num == 1:
            key = _decode_scalar(raw, wt, key_type)
        elif num == 2:
            val = _decode_scalar(raw, wt, val_type)
    return key, val


def _decode_scalar(raw, wt, typ):
    if typ == 'string':
        return raw.decode('utf8', 'replace') if isinstance(raw, bytes) else raw
    if typ == 'bytes':
        return list(raw) if isinstance(raw, bytes) else raw
    if typ == 'bool':
        return bool(raw)
    if typ in ('int32', 'int64'):
        return raw
    if typ in ('uint32', 'uint64'):
        return to_unsigned(raw)
    if isinstance(typ, str) and typ in SCHEMAS:
        return parse_message(raw, typ)
    if typ == 'double':
        return raw if isinstance(raw, float) else struct.unpack('<d', raw)[0]
    if typ == 'float':
        return raw
    if isinstance(typ, tuple) and typ[0] == 'enum':
        names = ENUMS.get(typ[1], {})
        return names.get(raw, raw)
    if isinstance(typ, tuple) and typ[0] == 'msg':
        return parse_message(raw, typ[1])
    raise ValueError("Unknown type: %r" % (typ,))


def parse_message(buf: bytes, name: str):
    spec = SCHEMAS[name]
    out = {}
    w = Wire(buf)
    while not w.eof():
        num, wt, raw = read_field(w)
        f = spec.get(num)
        if f is None:
            continue
        fname, typ, rep = f
        if rep == 1:
            if isinstance(typ, tuple) and typ[0] == 'msg':
                out.setdefault(fname, []).append(parse_message(raw, typ[1]))
            elif typ == 'string' or typ == 'bytes':
                out.setdefault(fname, []).append(
                    raw.decode('utf8', 'replace') if typ == 'string' else list(raw))
            elif typ == 'double':
                vals = unpack_packed_doubles(raw) if wt == 2 else [raw]
                out.setdefault(fname, []).extend(vals)
            elif typ == 'float':
                vals = [raw]
                out.setdefault(fname, []).extend(vals)
            elif typ == 'int32' or typ == 'int64':
                if wt == 2:
                    vals = unpack_packed_ints(raw)
                else:
                    vals = [raw]
                out.setdefault(fname, []).extend(vals)
            elif typ == 'uint32' or typ == 'uint64':
                if wt == 2:
                    vals = [to_unsigned(v) for v in unpack_packed_ints(raw)]
                else:
                    vals = [to_unsigned(raw)]
                out.setdefault(fname, []).extend(vals)
            elif typ == 'bool':
                out.setdefault(fname, []).append(bool(raw))
            elif isinstance(typ, tuple) and typ[0] == 'enum':
                names = ENUMS.get(typ[1], {})
                out.setdefault(fname, []).append(names.get(raw, raw))
            else:
                raise ValueError("Unhandled repeated type: %r" % (typ,))
        else:
            if isinstance(typ, tuple) and typ[0] == 'map':
                kt, vt = typ[1], typ[2]
                k, v = _decode_map_entry(raw, kt, vt)
                out.setdefault(fname, {})[k] = v
            else:
                out[fname] = _decode_scalar(raw, wt, typ)
    return out
