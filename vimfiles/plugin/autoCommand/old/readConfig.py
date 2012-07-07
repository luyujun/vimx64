# -*- coding:utf-8 -*-
import re
import json

def readConfig( cPath ):
  fp = open( cFilePath+'/'+cFileName )
  config = fp.read()
  fp.close()
  del fp

  # 去除注释
  rex = re.compile( r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
  config = rex.sub( '', config )
  # 序列化Json
  config = json.loads( config )

  return config

if __name__ == '__main__':
  readConfig()
