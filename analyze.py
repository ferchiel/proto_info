#!/usr/bin/env python
# coding=utf-8

import os
# pip install murmurhash3
import mmh3

class Analyze():
	""" analyze protobuf file """

	__file = None
	__name = None
	__path = None
	__exname = None
	__proto_version = 2
	__package = None
	__data = {}

	def parse( self, file_path ):
		if not file_path:
			return
		if not os.path.isfile( file_path ):
			print('Analyze init file_path is not file' + file_path )
			os._exit(0)

		self.__file = None
		self.__name = None
		self.__path = None
		self.__exname = None
		self.__proto_version = 2
		self.__package = None
		self.__data = {}

		print( 'Open file: ', file_path )
		self.__file = open( file_path, 'r' )
		
		idx = file_path.rfind( '/' )
		if idx == -1:
			idx = file_path.rfind( '\\' )

		fullfilename = ''
		if idx == -1:
			self.__path = './'
			fullfilename = file_path
		else:
			self.__path = file_path[ : idx + 1 ]
			fullfilename = file_path[ idx + 1 : ]

		idx = fullfilename.rfind( '.' )
		if idx == -1:
			self.__name = fullfilename
			self.__exname = ''
		else:
			self.__name = fullfilename[ : idx ]
			self.__exname = fullfilename[ idx + 1 : ]

		for line in self.__file:
			line.strip()
			if line.startswith( 'syntax' ):
				key = 'proto'
				idx = line.index( key )
				self.__proto_version = line[ idx + len( key ) ]
				continue

			if line.startswith( 'package' ) == True:
				key1 = ' '
				key2 = ';'
				idx1 = line.rindex( key1 )
				idx2 = line.rindex( key2 )
				self.__package = line[ idx1 + 1 : idx2 ]
				self.__package = self.__package.strip()
				continue

			if line.startswith( 'message' ) == True:
				key_tab = ( 'request_', 'response_' )
				re_key = None
				for key in key_tab:
					if line.find( key ) != -1:
						re_key = key[: -1]
						break

				if not re_key:
					continue
				idx1 = line.index( re_key ) + len( re_key ) + 1

				idx2 = line.find( '{' )
				if idx2 == -1:
					idx2 = None

				tab_name = line[ idx1 : idx2 ].strip()
				tab_index = mmh3.hash( self.__package + '.' + tab_name )

				if tab_index in self.__data:
					if self.__data[tab_index]['action'] != tab_name:
						print('Game Over Hash Collide Action Name:', tab_name)
						os._exit(0)
					self.__data[tab_index][re_key] = re_key + '_' + tab_name
				else:
					self.__data[tab_index] = {
							'index' : tab_index,
							'module' : self.__name + 'd',
							'action' : tab_name,
							'proto' : self.__name,
							re_key : re_key + '_' + tab_name,
							}
		
		self.__file.close()




	def get_file_name( self ):
		return self.__name

	def get_ex_name( self ):
		return self.__exname

	def get_path( self ):
		return self.__path

	def get_data( self ):
		return self.__data

	def get_proto_version( self ):
		return self.__proto_version

	def get_package_name( self ):
		return self.__package



if __name__ == "__main__":
	_a = Analyze()
	_a.parse( './test/anti_addiction.proto')
	print( _a.get_file_name() )
	print( _a.get_ex_name() )
	print( _a.get_path() )
	print( _a.get_proto_version() )
	print( _a.get_package_name() )
	print('--------------------------------------')
	print( _a.get_data() )






