#!/usr/bin/env python
# coding=utf-8


import os
import analyze
import lua_writer
import csharp_writer

INPUT_PATH = './input/'
LUA_OUTPATH = './lua_out/'
CS_OUTPATH = './cs_out/'
__cache = {}
__files = set()

parser = analyze.Analyze()

for filename in os.listdir(INPUT_PATH):
	if not filename.endswith('.proto'):
		continue
	fullpath = INPUT_PATH + filename

	parser.parse( fullpath )
	__files.add( parser.get_file_name() + '.' + parser.get_ex_name() )
	data = parser.get_data()
	for v in data.values():
		idx = v['index']
		if idx in __cache:
			print('Game Over Hash Collide File:', 
					parser.get_path() + parser.get_file_name() + '.' + parser.get_ex_name(), 
					'Action Name:', 
					v['action'], 
					'Hash Num.:', 
					idx)
			print(__cache[idx]['module'], __cache[idx]['action'])
			os._exit(0)

	__cache.update( data )

del parser

l_writer = lua_writer.lua_writer(LUA_OUTPATH + 'proto_info.lua')
cs_writer = csharp_writer.csharp_writer(CS_OUTPATH + 'proto_info.cs')


cs_writer.write_beg()
cs_writer.using('ProtoBuf')
cs_writer.using('gprotocol')
cs_writer.using('System')
cs_writer.using('System.Collections.Generic')
cs_writer.using('System.IO')

cs_writer.namespace_beg('protoinfo')
cs_writer.class_beg('protofunc')

cs_writer.write_line('public static Dictionary<string, int> _dic = new Dictionary<string, int>();')
cs_writer.public()
cs_writer.static()
cs_writer.func_beg('void', 'init', '')

for v in __cache.values():
	if 'request' in v:
		cs_writer.write_line('_dic.Add("ProtoBuf.%s", %d);' % (v['request'], v['index']))

cs_writer.func_end()


cs_writer.public()
cs_writer.static()
cs_writer.func_beg('ProtoBuf.IExtensible', 'decode', 'int proto_id, byte[] content')
cs_writer.switch_beg('proto_id')

keys = { 'index', 'module', 'action', 'proto', 'fullname' }

l_writer.write_beg()
l_writer.table_beg( 'decode', 'str' )
for v in __cache.values():
	l_writer.table_beg( v['index'], 'int' )
	for k in keys:
		l_writer.attribute( k, v[k], 'str' )
	if 'request' in v:
		l_writer.attribute( 'request', v['request'], 'str' )
	if 'response' in v:
		l_writer.attribute('response', v['response'], 'str')
		cs_writer.case_ret( v['index'], 'SocketManager.ProtoBuf_Deserialize<%s.%s>(content)' % (v['package'], v['response']))
	l_writer.table_end()

l_writer.table_end()

cs_writer.default('throw new Exception(String.Format("Decode No find net message id! id is {0}!", proto_id))')
cs_writer.switch_end()
cs_writer.func_end()


cs_writer.public()
cs_writer.static()
cs_writer.func_beg('byte[]', 'encode', 'ProtoBuf.IExtensible data, out int proto_id')
cs_writer.write_line('Type _t = data.GetType();')
cs_writer.write_line('proto_id = _dic[_t.FullName];')
cs_writer.write_line('using (MemoryStream m = new MemoryStream())')
cs_writer.write_line('{')
cs_writer.add_tab()
cs_writer.write_line('byte[] buffer = null;')
cs_writer.write_line('Serializer.Serialize(m, data);')
cs_writer.write_line('m.Position = 0;')
cs_writer.write_line('int length = (int)m.Length;')
cs_writer.write_line('buffer = new byte[length];')
cs_writer.write_line('m.Read(buffer, 0, length);')
cs_writer.write_line('return buffer;')
cs_writer.dec_tab()
cs_writer.write_line('}')
cs_writer.func_end()

cs_writer.public()
cs_writer.static()
cs_writer.func_beg('int', 'dispatch', 'int proto_id, ProtoBuf.IExtensible data')
cs_writer.switch_beg('proto_id')

l_writer.table_beg('encode', 'str')
for v in __cache.values():
	if 'response' in v:
		l_writer.attribute(v['response'], v['index'], 'int')
		cs_writer.case_ret( v['index'], 'msg_handler.%s.%s((%s.%s)data)' % (v['proto'], v['response'], v['package'], v['response']))

l_writer.table_end()

cs_writer.default('throw new Exception(String.Format("Dispatch No find net message id! id is {0}!", proto_id))')
cs_writer.switch_end()
cs_writer.func_end()

l_writer.table_beg('files', 'str')
for v in __files:
	l_writer.array(v, 'str')

l_writer.table_end()
l_writer.write_end()


cs_writer.class_end()
cs_writer.namespace_end()
cs_writer.write_end()




