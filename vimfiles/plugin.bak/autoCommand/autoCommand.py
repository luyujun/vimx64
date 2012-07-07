# -*- coding:utf-8 -*-
import os
import re
import sys
import vim
import json
import types
import time
import locale
import subprocess

cFileName = '_config'

def createConfigFile():
  # 初始化配置
  config = '''{
  ".haml": {
    "command": "haml --no-escape-attrs -q #{$fileName}.haml ../#{$fileName}.html"
    /* 执行命令 */
  },
  ".sass": {
    "command": "sass #{$fileName}.sass ../css/#{$fileName}.css"
    /* 执行命令 */
  },
  ".less": {
    "command": "lessc #{$fileName}.less>../css/#{$fileName}.css"
    /* 执行命令 */
  },
  ".coffee": {
    "command": "coffee -pb #{$fileName}.coffee ../js/#{$fileName}.js"
    /* 执行命令 */
  }
}'''
  # 写入配置
  fp = open(cFileName, 'w')
  fp.write(config)
  # 关闭文件
  fp.close()
  del fp

  return True;

def readConfig(cPath):
  # 读取配置
  fp = open(cPath+'/'+cFileName)
  config = fp.read()
  fp.close()
  del fp
  # 去除注释
  rex = re.compile(r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
  config = rex.sub('', config)
  # 序列化Json
  config = json.loads(config)

  return config

def getCommand(path, fname, suffix):
  config = readConfig(path)
  command = config[suffix]['command']
  if type(command) is types.ListType:
    command = '|'.join(command)
  command = re.sub(r'#{\$fileName}', fname, command.encode('UTF-8'))
  return command

#def getRelativePath(path):
  #relative = ''
  #prefix = ''
  #result = False
  #temp = ''

  #for i in range(0, 3):
    #if os.path.isdir(path):
      #if os.path.isfile(path + '/' + cFileName):
        #result = (path, relative)
        #break

      #else:
        #temp = os.path.split(path)
        #path = temp[0]
        #relative = temp[1]+'/'+relative

    #else:
      #break

  #return result

def runCommand():
  # 获取文件相关信息
  fullFileName = vim.eval('w:fullFileName')
  if os.name == 'nt':
    fullFileName = re.sub(r'\\', '/', fullFileName)
  result = re.match(r'^(.*/|)([^/]+?)(\.[^.]+|)$', fullFileName)
  result = result.groups()
  filePath = result[0]
  fileName = result[1]
  fileSuffix = result[2]
  # 检测命令缓存
  commandCache = vim.eval('w:commandCache')
  if commandCache == '':
    command=getCommand(filePath, fileName, fileSuffix)
    #print 'let w:commandCache='+command
    vim.command('let w:commandCache="'+command+'"')
  else:
    #print "use cache"
    command=commandCache

  # 将UTF-8的编码转换为系统默认文件编码
  if sys.platform == 'win32':
    localeencoding = locale.getdefaultlocale()[1]
    command = command.decode('UTF-8').encode(localeencoding or 'cp936')

  # 命令数组
  if command.find('|') > -1:
      command = command.split('|')
  else:
    command = [ command ]

  commandName = ''

  # 改变路径
  if filePath != '':
    tempPath = os.getcwd();
    os.chdir(filePath);

  for i in range(0, len(command)):
    # 获取执行命令的名称
    if not commandName:
      commandName = re.match(r'(^[^|> ]+)', command[i])
      if commandName:
        commandName = ' '+commandName.group()
      else:
        commandName = ' command'
    # 执行命令
    ret = subprocess.Popen(command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errMsg = ret.stderr.read()
    if errMsg != '': break

  # 返回初始目录
  if filePath != '':
    os.chdir(tempPath)
  # 打印执行结果或错误信息
  if errMsg:
    errMsg = re.sub(r'\r\n', '\n', errMsg)
    errMsg = re.sub(r'\\', r'\\\\', errMsg)
    errMsg = re.sub(r'\"', r'\\"', errMsg)
    #print errMsg
    vim.command('echohl ErrorMsg | echo "'+errMsg+'" | echohl None')
  else:
    print time.strftime('%H:%M:%S')+' execute'+commandName

#if __name__ == '__main__':
  #print 'autoCommand.py is load'
