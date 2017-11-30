#!/usr/bin/env python
# coding=utf-8


class lua_writer():
	"""excel writer"""
	__file = None
	__name = None
	__table = 0

	def __init__(self, output_file):
		aname = output_file
		_path = ''
		idx = aname.rfind('/')
		if idx != -1:
			_path = aname[:idx + 1]
			aname = aname[idx + 1:]
		idx = aname.find('.')
		if idx != -1:
			aname = aname[: idx]
		self.__name = aname
		self.__file = open(_path + aname + '.lua', 'w', encoding = 'utf8')
		self.description()

	def __del__(self):
		self.__file.close()

	def description(self):
		self.__file.write(
'''-- automake by excel2lua
-- auth: ferchiel	mail: ferchiel@163.com

''')

	def table_beg(self, name, _type):
		s = ''
		for x in range(self.__table):
			s += '\t'

		assert(_type == 'str' or _type == 'int')
		if _type == 'str':
			s += str(name) + ' = {\n'
		elif _type == 'int':
			if int(name) == name:
				name = int(name)
			name = str(name)
			s += '[' + name + '] = {\n'
		else:
			print('proto info! lua_writer: line : 49! _type: ' + _type)
			exit(0)
		self.__file.write(s)
		self.__table += 1

	def table_end(self):
		s = ''
		for x in range(self.__table - 1):
			s += '\t'
		s += '},\n'
		self.__file.write(s)
		self.__table -= 1

	def attribute(self, key, value, _type):
		s = ''
		for x in range(self.__table):
			s += '\t'
		if key.find('.') != -1:
			s += '[\'' + key + '\'] = '
		else:
			s += key + ' = '
		if _type == 'int':
			if int(value) == value:
				value = int(value)
			value = str(value)
			s += value
		elif _type == 'str':
			value = str(value)
			s += '\'' + value + '\''
		else:
			print('proto info! lua_writer: line : 76! _type: ' + _type)
			exit(0)
		s += ',\n'
		self.__file.write(s)

	def array(self, value, _type):
		s = ''
		for x in range(self.__table):
			s += '\t'
		if _type == 'int':
			if int(value) == value:
				value = int(value)
			value = str(value)
			s += value
		elif _type == 'str':
			value = str(value)
			s += '\'' + value + '\''
		else:
			print('proto info! lua_writer: line : 94! _type: ' + _type)
			exit(0)
		s += ',\n'
		self.__file.write(s)

	def write_beg(self):
		self.__table += 1
		s = 'return {\n'
		self.__file.write(s)

	def write_end(self):
		self.__table -= 1
		s = '}'
		self.__file.write(s)




