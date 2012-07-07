# -*- coding:utf-8 -*-
import os

def findConfig():
	fileName = '.config'
	prefix = ''
	result = False;

	for i in range( 0, 3 ):
		if os.path.isdir( prefix or './' ):
			if os.path.isfile( prefix + fileName ):
				result = prefix + fileName
				break;

			prefix += '../'

		else:
			break

	return result

if __name__ == '__main__':
	findConfig()
