#!/usr/bin/env python
# coding=utf-8


import os
import analyze
import lua_writer

INPUT_PATH = './input/'
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

writer = lua_writer.lua_writer(INPUT_PATH + 'proto_info.lua')

keys = { 'module', 'action', 'proto' }

writer.write_beg()
writer.table_beg( 'info', 'str' )
for v in __cache.values():
	writer.table_beg( v['index'], 'int' )
	for k in keys:
		writer.attribute( k, v[k], 'str' )
	if 'request' in v:
		writer.attribute( 'request', v['request'], 'str' )
	if 'response' in v:
		writer.attribute( 'response', v['response'], 'str' )
	if 'push' in v:
		writer.attribute( 'push', v['push'], 'str' )
	writer.table_end()

writer.table_end()


writer.table_beg( 'files', 'str' )
for v in __files:
	writer.array( v, 'str' )

writer.table_end()
writer.write_end()




