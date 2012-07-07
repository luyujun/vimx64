# -*- coding:utf-8 -*-
import os
def getRelativePath( path ):
  configFileName = '.config'
  relative = ''
  prefix = ''
  result = False
  temp = ''

  for i in range( 0, 3 ):
    if os.path.isdir( path ):
      if os.path.isfile( path + '/' + configFileName ):
        result = ( path, relative )
        break

      else:
        temp = os.path.split( path )
        path = temp[0]
        relative = temp[1]+'/'+relative

    else:
      break

  return result

if __name__ == '__main__':
  print getRelativePath('D:/testdir/_source')
