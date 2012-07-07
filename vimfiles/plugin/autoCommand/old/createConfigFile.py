# -*- coding:utf-8 -*-
#import os
import json

def createConfigFile():
	config = '''{
	".haml": {
		"_buildPath": "../",
		"": ""
		/* 编译路径 */
	},
	".sass": {
		"buildPath": "../css/",
		"": ""
		/* 编译路径 */
	},
	".coffee": {
		"buildPath": "../js/",
		"": ""
		/* 编译路径 */
	},
	"": ""
}'''


	cFile = open( '.config', 'w' )
	cFile.write( config )
	cFile.close()
	print "success!"
	#print config

if __name__ == '__main__':
	createConfigFile()
