#!/usr/bin/env python
# coding=utf-8

class csharp_writer():
	"""C# writer"""
	__file = None
	__name = None
	__table = 0
	__unfinished = False
	__s = ''

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
		self.__file = open(_path + aname + '.cs', 'w', encoding = 'utf8')
		self.description()

	def __del__(self):
		self.__file.close()

	def write_beg(self):
		self.__s = ''

	def write_end(self):
		self.__file.write(self.__s)

	def description(self):
		self.__file.write(
'''// automake by protoinfo
// auth: ferchiel	mail: ferchiel@163.com

''')

	def _tab(self):
		if self.__unfinished:
			self.__unfinished = False
			return
		for x in range(self.__table):
			self.__s += '\t'

	def using(self, content):
		self.__s += 'using %s;\n' % content

	def namespace_beg(self, content):
		self._tab()
		self.__s += 'namespace %s\n' % content
		self._tab()
		self.__s += '{\n'
		self.__table += 1

	def namespace_end(self):
		self.__table -= 1
		self._tab()
		self.__s += '}\n'

	def class_beg(self, content):
		self._tab()
		self.__s += 'class %s\n' % content
		self._tab()
		self.__s += '{\n'
		self.__table += 1

	def class_end(self):
		self.__table -= 1
		self._tab()
		self.__s += '}\n'

	def public(self):
		self._tab()
		self.__s += 'public '
		self.__unfinished = True

	def static(self):
		self._tab()
		self.__s += 'static '
		self.__unfinished = True
		
	def func_beg(self, ret, name, args):
		self._tab()
		self.__s += '%s %s(%s)\n' % (ret, name, args)
		self._tab()
		self.__s += '{\n'
		self.__table += 1

	def func_end(self):
		self.__table -= 1
		self._tab()
		self.__s += '}\n'

	def switch_beg(self, content):
		self._tab()
		self.__s += 'switch( %s )\n' % content
		self._tab()
		self.__s += '{\n'
		self.__table += 1

	def switch_end(self):
		self.__table -= 1
		self._tab()
		self.__s += '}\n'

	def case(self, comp, content):
		self._tab()
		self.__s += 'case %s:\n' % comp
		self._tab()
		self.__s += '\t%s;\n' % content
		self._tab()
		self.__s += 'break;\n'

	def default(self, content):
		self._tab()
		self.__s += 'default:\n'
		self._tab()
		self.__s += '\t%s;\n' % content

	def case_ret(self, sid, content):
		self._tab()
		self.__s += 'case %s:\n' % sid
		self._tab()
		self.__s += '\treturn %s;\n' % content

	def ret(self, content):
		self._tab()
		self.__s += 'return %s;\n' % content

	def write_line(self, content):
		self._tab()
		self.__s += content + '\n'

	def add_tab(self, count = 1):
		self.__table += count

	def dec_tab(self, count = 1):
		self.__table -= count
