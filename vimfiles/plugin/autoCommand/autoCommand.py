# -*- coding:utf-8 -*-
# --------------------------------------------------
#   FileName: autocommand.py
#       Desc: ���python����
#     Author: lcc
#      Email: leftcold@gmail.com
#    Version: 0.1
# LastChange: 06/01/2012 01:21
#    History: 
# --------------------------------------------------
import os, re, sys, vim, json, time, types, locale, subprocess

cFileName = '_config'

def createConfigFile():
  # ��ʼ������
  config = '''{
  ".haml": {
    "command": "haml -nq #{$fileName}.haml>../#{$fileName}.htm"
  },
  ".jade": {
    "command": "jade #{$fileName}.jade -PO>../#{$fileName}.htm"
  },
  ".sass": {
    "command": [
      "sass --style compact --sourcemap #{$fileName}.sass ../css/#{$fileName}.full.css",
      "sass --style compressed #{$fileName}.sass ../css/#{$fileName}.css"
    ]
  },
  ".scss": {
    "command": [
      "sass --scss --style compact --sourcemap #{$fileName}.scss ../css/#{$fileName}.full.css",
      "sass --scss --style compressed #{$fileName}.scss ../css/#{$fileName}.css"
    ]
  },
  ".less": {
    "command": "lessc #{$fileName}.less>../css/#{$fileName}.css"
  },
  ".coffee": {
    "command": "coffee -bp #{$fileName}.coffee>#{$fileName}.js"
  }
}'''
  # д������
  fp = open(cFileName, 'w')
  fp.write(config)
  # �ر��ļ�
  fp.close()
  del fp

  return True;

def readConfig(cPath):
  if os.path.isfile(cPath+'/'+cFileName):
    # ��ȡ����
    fp = open(cPath+'/'+cFileName)
    config = fp.read()
    fp.close()
    del fp
    # ȥ��ע��
    rex = re.compile(r'^(?:\s+|)/\*.*?\*/(?:\s+|)$', re.M+re.S)
    config = rex.sub('', config)
    # ���л�Json
    config = json.loads(config)
  else:
    config = False

  return config

def getCommand(path, fname, suffix):
  config = readConfig(path)
  #�����ȡ��ʧ���򷵻�False
  if not config:
    #���δ�������ļ�ȡ���������vim�ж�ȡ����
    command = vim.eval('autocommand#getCommand("'+suffix+'")')
  else:
    #��ȡ���óɹ�
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
  # ��ȡ�ļ������Ϣ
  fullFileName = vim.eval('w:fullFileName')
  if os.name == 'nt':
    fullFileName = re.sub(r'\\', '/', fullFileName)
  result = re.match(r'^(.*/|)([^/]+?)(\.[^.]+|)$', fullFileName)
  result = result.groups()
  filePath = result[0]
  fileName = result[1]
  fileSuffix = result[2]
  # ��������
  commandCache = vim.eval('w:commandCache')
  if not commandCache:
    command=getCommand(filePath, fileName, fileSuffix)
    #print 'let w:commandCache='+command
    vim.command('let w:commandCache="'+command+'"')
  else:
    #print "use cache"
    command=commandCache

  # ��UTF-8�ı���ת��ΪϵͳĬ���ļ�����
  if sys.platform == 'win32':
    localeencoding = locale.getdefaultlocale()[1]
    command = command.decode('UTF-8').encode(localeencoding or 'cp936')

  # ��������
  if command.find('|') > -1:
      command = command.split('|')
  else:
    command = [ command ]

  commandName = ''

  # �ı�·��
  if filePath != '':
    tempPath = os.getcwd();
    os.chdir(filePath);

  for i in range(0, len(command)):
    # ��ȡִ�����������
    if not commandName:
      commandName = re.match(r'(^[^|> ]+)', command[i])
      if commandName:
        commandName = ' '+commandName.group()
      else:
        commandName = ' command'
    # ִ������
    ret = subprocess.Popen(command[i], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errMsg = ret.stderr.read()
    if errMsg != '': break

  # ���س�ʼĿ¼
  if filePath != '':
    os.chdir(tempPath)
  # ��ӡ������Ϣ
  if errMsg:
    #ת�廻�з�
    errMsg = re.sub(r'\r(?:\n|)', r'\n', errMsg)
    #ת��б��
    errMsg = re.sub(r'\\', r'\\\\', errMsg)
    #ת������
    errMsg = re.sub(r'\"', r'\\"', errMsg)
    #��ӡ��������
    vim.command('echohl ErrorMsg | echo "'+errMsg+'" | echohl None')
  #��ӡִ�н��
  else:
    #��ӡִ�гɹ�����
    print time.strftime('%H:%M:%S')+' execute'+commandName

#if __name__ == '__main__':
  #print 'autoCommand.py is load'
# vim:sw=2:ts=2:sts=2:et:fdm=marker:fdc=1
